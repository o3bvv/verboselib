from typing import Any
from typing import Callable
from typing import Text

from .utils import export


@export
class LazyString:

  def __init__(self, func: Callable[..., Text], *args, **kwargs):
    self._func = func
    self._args = args
    self._kwargs = kwargs

  def __str__(self) -> Text:
    return self._func(*self._args, **self._kwargs)

  def __getattr__(self, attr: Text) -> Any:
    """
    Forwards any non-magic methods to the resulting string.

    This allows support for string methods like ``upper()``, ``lower()``, etc.
    """
    s = str(self)

    if hasattr(s, attr):
      return getattr(s, attr)

    raise AttributeError(attr)

  def __len__(self):
    return len(str(self))

  def __getitem__(self, key):
    return str(self)[key]

  def __iter__(self):
    return iter(str(self))

  def __contains__(self, item):
    return item in str(self)

  def __add__(self, other):
    return str(self) + other

  def __radd__(self, other):
    return other + str(self)

  def __mul__(self, other):
    return str(self) * other

  def __rmul__(self, other):
    return other * str(self)

  def __eq__(self, other):
    return str(self) == other

  def __ne__(self, other):
    return str(self) != other

  def __lt__(self, other):
    return str(self) < other

  def __le__(self, other):
    return str(self) <= other

  def __gt__(self, other):
    return str(self) > other

  def __ge__(self, other):
    return str(self) >= other
