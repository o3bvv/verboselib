import gettext as _gettext
import threading

from pathlib import Path

from typing import Callable
from typing import Text
from typing import Union

from verboselib.core import get_language
from verboselib.helpers import to_locale
from verboselib.lazy import LazyString
from verboselib.utils import export


StringOrPath = Union[Text, Path]
MaybeLazyInteger = Union[int, Callable[[], int]]


@export
class NotThreadSafeTranslations:

  def __init__(self, domain: Text, locale_dir_path: StringOrPath):
    self._domain = domain
    self._locale_dir_path = str(locale_dir_path)
    self._translations = {
      None: _gettext.NullTranslations(),
    }

  def gettext(self, message: Text) -> Text:
    return self._get_translation().gettext(message)

  def gettext_lazy(self, message: Text) -> LazyString:
    return LazyString(
      func=self.gettext,
      message=message,
    )

  def ngettext(self, singular: Text, plural: Text, n: MaybeLazyInteger) -> Text:
    if callable(n):
      n = n()
    return self._get_translation().ngettext(singular, plural, n)

  def ngettext_lazy(self, singular: Text, plural: Text, n: MaybeLazyInteger) -> LazyString:
    return LazyString(
      func=self.ngettext,
      singular=singular,
      plural=plural,
      n=n,
    )

  def pgettext(self, context: Text, message: Text) -> Text:
    return self._get_translation().pgettext(context, message)

  def pgettext_lazy(self, context: Text, message: Text) -> LazyString:
    return LazyString(
      func=self.pgettext,
      context=context,
      message=message,
    )

  def npgettext(self, context: Text, singular: Text, plural: Text, n: MaybeLazyInteger) -> Text:
    if callable(n):
      n = n()
    return self._get_translation().npgettext(context, singular, plural, n)

  def npgettext_lazy(self, context: Text, singular: Text, plural: Text, n: MaybeLazyInteger) -> LazyString:
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

  def __init__(self, domain: Text, locale_dir_path: StringOrPath):
    super().__init__(domain=domain, locale_dir_path=locale_dir_path)
    self._lock = threading.RLock()

  def gettext(self, message: Text) -> Text:
    with self._lock:
      return super().gettext(message=message)

  def ngettext(self, singular: Text, plural: Text, n: MaybeLazyInteger) -> Text:
    with self._lock:
      return super().ngettext(singular=singular, plural=plural, n=n)

  def pgettext(self, context: Text, message: Text) -> Text:
    with self._lock:
      return super().pgettext(context=context, message=message)

  def npgettext(self, context: Text, singular: Text, plural: Text, n: MaybeLazyInteger) -> Text:
    with self._lock:
      return super().npgettext(context=context, singular=singular, plural=plural, n=n)
