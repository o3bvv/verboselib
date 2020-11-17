import gettext as _gettext
import sys
import threading

if sys.version_info >= (3, 9):
  from collections.abc import Callable
else:
  from typing import Callable

from pathlib import Path
from typing import Union

from lazy_string import LazyString

from .core import get_language
from .helpers import to_locale

from ._utils import export


StringOrPath = Union[str, Path]
MaybeLazyInteger = Union[int, Callable[..., int]]


@export
class NotThreadSafeTranslations:

  def __init__(self, domain: str, locale_dir_path: StringOrPath):
    self._domain = domain
    self._locale_dir_path = str(locale_dir_path)
    self._translations = {
      None: _gettext.NullTranslations(),
    }

  def gettext(self, message: str) -> str:
    return self._get_translation().gettext(message)

  def gettext_lazy(self, message: str) -> LazyString:
    return LazyString(
      func=self.gettext,
      message=message,
    )

  def ngettext(self, singular: str, plural: str, n: MaybeLazyInteger) -> str:
    if callable(n):
      n = n()
    return self._get_translation().ngettext(singular, plural, n)

  def ngettext_lazy(self, singular: str, plural: str, n: MaybeLazyInteger) -> LazyString:
    return LazyString(
      func=self.ngettext,
      singular=singular,
      plural=plural,
      n=n,
    )

  def pgettext(self, context: str, message: str) -> str:
    return self._get_translation().pgettext(context, message)

  def pgettext_lazy(self, context: str, message: str) -> LazyString:
    return LazyString(
      func=self.pgettext,
      context=context,
      message=message,
    )

  def npgettext(self, context: str, singular: str, plural: str, n: MaybeLazyInteger) -> str:
    if callable(n):
      n = n()
    return self._get_translation().npgettext(context, singular, plural, n)

  def npgettext_lazy(self, context: str, singular: str, plural: str, n: MaybeLazyInteger) -> LazyString:
    return LazyString(
      func=self.npgettext,
      context=context,
      singular=singular,
      plural=plural,
      n=n,
    )

  def _get_translation(self) -> _gettext.NullTranslations:
    language = get_language()

    translation = self._translations.get(language)
    if not translation:
      locale = to_locale(language)
      translation = _gettext.translation(
        domain=self._domain,
        localedir=self._locale_dir_path,
        languages=[locale, ],
        fallback=True,
      )
      self._translations[language] = translation

    return translation


@export
class Translations(NotThreadSafeTranslations):

  def __init__(self, domain: str, locale_dir_path: StringOrPath):
    super().__init__(domain=domain, locale_dir_path=locale_dir_path)
    self._lock = threading.RLock()

  def gettext(self, message: str) -> str:
    with self._lock:
      return super().gettext(message=message)

  def ngettext(self, singular: str, plural: str, n: MaybeLazyInteger) -> str:
    with self._lock:
      return super().ngettext(singular=singular, plural=plural, n=n)

  def pgettext(self, context: str, message: str) -> str:
    with self._lock:
      return super().pgettext(context=context, message=message)

  def npgettext(self, context: str, singular: str, plural: str, n: MaybeLazyInteger) -> str:
    with self._lock:
      return super().npgettext(context=context, singular=singular, plural=plural, n=n)
