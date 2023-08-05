import contextlib
import functools
import inspect
import re
from functools import partial as bind

import jax
import jax.numpy as jnp


###############################################################################
# Context
###############################################################################


# When running an impure function that accesses state, it will find the state
# in this global variable. The pure() wrapper populates this global variable
# with the provided state, calles the inner function, and the takes the
# resulting state out of the global variable and returns it back to the user.
CONTEXT = [None]


class Context:

  def __init__(self, state, rng, create, modify, freeze, reserve):
    self.state = state
    self.rng = rng
    self.create = create  # Allow creating new state entries.
    self.modify = modify  # Apply modifications to existing state entries.
    self.freeze = freeze  # Disllow modifying existing state entries.
    self.reserve = reserve


def context():
  """Access and modify the global context from within an impure function. For
  advanced users only. Prefer to use state() to access and modify the global
  state and rng() to get the next RNG key."""
  global CONTEXT
  if CONTEXT[0] is None:
    raise RuntimeError('Wrap impure functions in pure() before running them.')
  return CONTEXT[0]


def pure(fun, nested=False):
  """Wrap an impure function that uses global state to explicitly pass the
  state in and out. The result is a pure function that is composable with JAX
  transformation. The pure function can be used as follows:
  `out, state = fun(state, rng, *args, **kwargs)`."""
  def purified(
      state, rng, *args, create=True, modify=True, freeze=False, **kwargs):
    global CONTEXT
    if not isinstance(state, dict):
      raise ValueError('Must provide a dict as state.')
    if CONTEXT[0] and (not nested):
      raise RuntimeError('If you want to nest run() calls, use nested=True.')
    before = CONTEXT[0]
    try:
      CONTEXT[0] = Context(state.copy(), rng, create, modify, freeze, [])
      out = fun(*args, **kwargs)
      state = CONTEXT[0].state
      return out, state
    finally:
      CONTEXT[0] = before
  purified.pure = True
  return purified


def state():
  """Access or modify the global state dictionary."""
  # TODO: Wrap state dictionary with guards for context().create and
  # context().modify.
  return context().state


def rng(amount=None, reserve=16):
  """Split the global RNG key and return a new local key."""
  ctx = context()
  if amount:
    keys = jax.random.split(ctx.rng, amount + 1)
    ctx.rng = keys[0]
    return keys[1:]
  else:
    if not ctx.reserve:
      keys = jax.random.split(ctx.rng, reserve)
      ctx.rng = keys[0]
      ctx.reserve = list(keys[1:])
    return ctx.reserve.pop(0)


def creating():
  """Boolean indicating whether the program is currently allowed to create
  state entries. Can use used for initialization logic that should be excluded
  from compiled functions."""
  return context().create


###############################################################################
# Transformations
###############################################################################


def grad(fun, keys, has_aux=False):
  """Compute the gradient of an impure function with respect to the specified
  state entries or modules. The transformed function returns a tuple containing
  the computed value, selected state entries, their gradients, and if
  applicable auxiliary outputs of the function."""
  keys = keys if hasattr(keys, '__len__') else (keys,)
  if getattr(fun, 'pure', False):
    raise ValueError('Use plain jax.grad() for pure functions.')
  if not has_aux:
    fun = lambda *args, _fun=fun, **kwargs: (_fun(*args, *kwargs), {})
  fun = pure(fun, nested=True)
  def forward(x1, x2, rng, *args, **kwargs):
    (y, aux), state = fun(
        {**x1, **x2}, rng, *args, create=False, modify=True, **kwargs)
    return y, (aux, state)
  backward = jax.value_and_grad(forward, has_aux=True)
  @functools.wraps(backward)
  def wrapper(*args, **kwargs):
    ctx = context()
    if ctx.create:
      _, state = fun(
          ctx.state, rng(), *args, create=True, modify=False, **kwargs)
      ctx.state.update(state)
    assert all(isinstance(x, (str, Module)) for x in keys)
    strs = [x for x in keys if isinstance(x, str)]
    mods = [x for x in keys if isinstance(x, Module)]
    for mod in mods:
      strs += mod.getm()
    x1 = {k: v for k, v in ctx.state.items() if k in strs}
    x2 = {k: v for k, v in ctx.state.items() if k not in strs}
    (y, (aux, state)), dx = backward(x1, x2, rng(), *args, **kwargs)
    ctx.state.update(state)
    return (y, x1, dx, aux) if has_aux else (y, x1, dx)
  return wrapper


def jit(fun, static=None, **kwargs):
  """Compiles a pure function for fast execution. Only the first call of the
  function is allowed to create state entries."""
  if not getattr(fun, 'pure', False):
    raise ValueError('Use pure() before applying jit().')
  static = static or ()
  compiled = jax.jit(
      lambda sta, *a, **kw: fun(*a, **kw, **dict(sta), create=False),
      static_argnums=[0], **kwargs)
  @functools.wraps(compiled)
  def wrapper(*args, **kwargs):
    for name in static:
      if name not in kwargs:
        raise ValueError('Please pass all static arguments by keyword.')
    if not wrapper.created:
      wrapper.created = True
      return fun(*args, create=True, **kwargs)
    nosta = {k: v for k, v in kwargs.items() if k not in static}
    sta = {k: v for k, v in kwargs.items() if k in static}
    sta = tuple(sorted(sta.items()))
    return compiled(sta, *args, **nosta)
  wrapper.created = False
  return wrapper


def pmap(fun, axis_name=None, static=None, in_axes=0, out_axes=0, **kwargs):
  """Compiles n pure function for fast execution across multiple devices. Only
  the first call of the function is allowed to create state entries."""
  static = static or ()
  if not getattr(fun, 'pure', False):
    raise ValueError('Use pure() before applying pmap().')
  inner = lambda sta, *a, **kw: fun(*a, **kw, **dict(sta))
  compiled = jax.pmap(
      functools.partial(inner, create=False),
      axis_name, in_axes=in_axes, out_axes=out_axes,
      static_broadcasted_argnums=[0], **kwargs)
  @functools.wraps(compiled)
  def wrapper(*args, **kwargs):
    for name in static:
      if name not in kwargs:
        raise ValueError('Please pass all static arguments by keyword.')
    nosta = {k: v for k, v in kwargs.items() if k not in static}
    sta = {k: v for k, v in kwargs.items() if k in static}
    sta = tuple(sorted(sta.items()))
    if not wrapper.created:
      wrapper.created = True
      return jax.vmap(
          functools.partial(inner, sta, create=True),
          in_axes, out_axes, axis_name)(*args, **nosta)
    return compiled(sta, *args, **nosta)
  wrapper.created = False
  return wrapper


def cond(pred, true_fun, false_fun, *operands):
  ctx = context()
  true_fun = pure(true_fun, nested=True)
  false_fun = pure(false_fun, nested=True)
  if ctx.create:
    _, state = true_fun(ctx.state, rng(), *operands, create=True, modify=False)
    ctx.state.update(state)
    _, state = false_fun(ctx.state, rng(), *operands, create=True, modify=False)
    ctx.state.update(state)
  out, state = jax.lax.cond(
      pred,
      lambda state, rng1, rng2, *args: true_fun(state, rng1, *args),
      lambda state, rng1, rng2, *args: false_fun(state, rng2, *args),
      ctx.state, *rng(2), *operands)
  ctx.state.update(state)
  return out


def scan(fun, carry, xs, reverse=False, unroll=1, modify=False):
  ctx = context()
  fun = pure(fun, nested=True)
  if ctx.create:
    first = jax.tree_util.tree_map(lambda x: x[0], xs)
    _, state = fun(ctx.state, rng(), carry, first, create=True, modify=False)
    ctx.state.update(state)
  length = len(jax.tree_util.tree_leaves(xs)[0])
  rngs = rng(length)
  if modify:
    def inner(carry, x):
      carry, state = carry
      x, rng = x
      (carry, y), state = fun(state, rng, carry, x, create=False)
      return (carry, state), y
    (carry, state), ys = jax.lax.scan(
        inner, (carry, ctx.state), (xs, rngs), length, reverse, unroll)
    ctx.state.update(state)
  else:
    def inner(carry, x):
      x, rng = x
      (carry, y), state = fun(
          ctx.state, rng, carry, x, create=False, freeze=True)
      return carry, y
    carry, ys = jax.lax.scan(inner, carry, (xs, rngs), length, reverse, unroll)
  return carry, ys


###############################################################################
# Modules
###############################################################################


SCOPE = ['']


def reset():
  """Clean up previously used scope names to provide a clean starting point for
  unit tests."""
  ModuleMeta.COUNTERS.clear()


@contextlib.contextmanager
def scope(scope, absolute=False):
  """Enter a relative or absolute name scope. Name scopes are used to make
  variable names unique."""
  global SCOPE
  if SCOPE[0] is None:
    raise RuntimeError('Run stateful functions with run().')
  previous = SCOPE[0]
  if absolute:
    SCOPE[0] = scope
  else:
    SCOPE[0] += '/' + scope
  yield SCOPE[0]
  SCOPE[0] = previous


class ModuleMeta(type):

  """Meta class that creates a unique path for each module instance and wraps
  the methods and properties of the module to enter the name scope."""

  COUNTERS = {}

  def __new__(mcs, name, bases, clsdict):
    """This runs once per user module class definition. It wraps the methods of
    the module class to automatically enter the name scope of the module."""
    method_names = []
    for key, value in clsdict.items():
      if key.startswith('__') and key != '__call__':
        continue
      elif isinstance(value, property):
        clsdict[key] = property(
            value.fget if not value.fget else _scope_method(value.fget),
            value.fset if not value.fset else _scope_method(value.fset),
            value.fdel if not value.fdel else _scope_method(value.fdel),
            doc=value.__doc__)
      elif inspect.isfunction(value):
        method_names.append(key)
    cls = super(ModuleMeta, mcs).__new__(mcs, name, bases, clsdict)
    for method_name in method_names:
      method = getattr(cls, method_name)
      method = _scope_method(method)
      setattr(cls, method_name, method)
    return cls

  def __call__(cls, *args, name=None, **kwargs):
    """This runs once per use module instance creation. It derives a unique
    name and path for the module instance."""
    obj = cls.__new__(cls)
    name = name or cls.__name__
    global SCOPE
    path = SCOPE[0] + '/' + name
    if path in cls.COUNTERS:
      cls.COUNTERS[path] += 1
      path += str(cls.COUNTERS[path])
    else:
      cls.COUNTERS[path] = 1
    obj._path = path
    obj._submodules = {}
    init = _scope_method(cls.__init__)
    init(obj, *args, **kwargs)
    return obj


def _scope_method(method):
  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    with scope(self._path, absolute=True):
      return method(self, *args, **kwargs)
  return wrapper


class Module(object, metaclass=ModuleMeta):

  """Base class for users to inherit their modules from. Provides automatic
  name scoping via the meta class and helper functions for accessing state."""

  def __repr__(self):
    return f'{self.__class__.__name__}({self.path})'

  @property
  def path(self):
    """The unique name scope of this module instance as a string."""
    return self._path

  def get(self, name, *args, **kwargs):
    """Retrieve or create a state entry that belongs to this module."""
    state_ = state()
    path = self.path + '/' + name
    if name in self._submodules:
      return self._submodules[name]
    if path in state_:
      return state_[path]
    ctor, *args = args
    if 'name' in inspect.signature(ctor).parameters:
      kwargs['name'] = name
    value = ctor(*args, **kwargs)
    flat, _ = jax.tree_util.tree_flatten(value)
    if all(isinstance(x, jnp.ndarray) for x in flat):
      state_[path] = value
    else:
      self._submodules[name] = value
    return value

  def put(self, name, value):
    """Update or create a single state entry that belongs to this module."""
    self.putm({self.path + '/' + name: value})
    return value

  def getm(self, pattern=r'.*', allow_empty=False):
    """Read the state entries of this module, optionally filtered by regex."""
    state_ = state()
    pattern = re.compile(pattern)
    prefix = self.path + '/'
    results = {}
    for key, value in state_.items():
      if not key.startswith(prefix):
        continue
      if pattern.match(key[len(prefix):]):
        results[key] = value
    if not allow_empty and not results:
      raise KeyError(f'Pattern {pattern} matched no state keys.')
    return results

  def putm(self, mapping):
    """Update or create multiple state entries that belong to this module."""
    prefix = self.path + '/'
    for key in mapping:
      if not key.startswith(prefix):
        raise KeyError(f'Key {key} does not belong to module {self.path}.')
    ctx = context()
    if ctx.freeze:
      raise RuntimeError(
          'Cannot modify state entries here. If you want to modify '
          'state inside of scan() set modify=True.')
    if not ctx.modify:
      mapping = {k: v for k, v in mapping.items() if k not in ctx.state}
    if not ctx.create:
      for key, value in mapping.items():
        if key not in ctx.state:
          raise RuntimeError(
              f'Can only create state entries during first call ({key}).')
    ctx.state.update(mapping)


class Variable(Module):

  def __init__(self, ctor, *args, **kwargs):
    self.ctor = ctor
    self.args = args
    self.kwargs = kwargs

  def read(self):
    return self.get('value', self.ctor, *self.args, **self.kwargs)

  def write(self, value):
    return self.put('value', value)


###############################################################################
# Integrations
###############################################################################


class HaikuModule(Module):

  def __init__(self, ctor, *args, **kwargs):
    import haiku as hk
    def net(*args_, **kwargs_):
      return ctor(*args, **kwargs)(*args_, **kwargs_)
    self.transformed = hk.transform(net)

  def __call__(self, *args, **kwargs):
    state = self.get('state', self.transformed.init, rng(), *args, **kwargs)
    return self.transformed.apply(state, rng(), *args, **kwargs)


class FlaxModule(Module):

  def __init__(self, ctor, *args, **kwargs):
    self.module = ctor(*args, **kwargs)

  def __call__(self, *args, **kwargs):
    state = self.get('state', self.module.init, rng(), *args, **kwargs)
    return self.module.apply(state, *args, **kwargs)


class OptaxModule(Module):

  def __init__(self, ctor, *args, **kwargs):
    self.opt = ctor(*args, **kwargs)

  def __call__(self, loss, keys, *args, **kwargs):
    import optax
    loss, params, grads = grad(loss, keys)(*args, **kwargs)
    optstate = self.get('state', self.opt.init, params)
    updates, optstate = self.opt.update(grads, optstate)
    self.put('state', optstate)
    state().update(optax.apply_updates(params, updates))
    return {'loss': loss.mean(), 'grad_norm': optax.global_norm(grads)}
