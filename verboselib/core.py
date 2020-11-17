import threading

from typing import Optional

from ._utils import export


_bypass_value  = "__bypass__"
_local_storage = threading.local()


@export
def get_default_language() -> Optional[str]:
  return getattr(_local_storage, "default_value", None)


@export
def set_default_language(value: Optional[str]) -> None:
  setattr(_local_storage, "default_value", value)


@export
def drop_default_language() -> None:
  set_default_language(None)


@export
def set_language(value: Optional[str]) -> None:
  setattr(_local_storage, "current_value", value)


@export
def set_language_bypass() -> None:
  set_language(_bypass_value)


@export
def drop_language() -> None:
  set_language(None)


@export
def get_language() -> Optional[str]:
  language = getattr(_local_storage, "current_value", None)

  if language is _bypass_value:
    return None

  return language or getattr(_local_storage, "default_value", None)
