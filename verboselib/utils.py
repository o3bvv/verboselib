import inspect

from typing import Any


def export(target: Any) -> Any:
  """
  Mark a module-level object as exported.

  Simplifies tracking of objects available via wildcard imports.

  """
  frm = inspect.stack()[1]
  mod = inspect.getmodule(frm[0])

  __all__ = getattr(mod, '__all__', None)

  if __all__ is None:
    __all__ = []
    setattr(mod, '__all__', __all__)

  elif not isinstance(__all__, list):
    __all__ = list(__all__)
    setattr(mod, '__all__', __all__)

  target_name = target.__name__
  if target_name not in __all__:
    __all__.append(target_name)

  return target
