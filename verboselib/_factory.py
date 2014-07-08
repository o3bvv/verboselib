# -*- coding: utf-8 -*-
import gettext

from copy import copy
from stringlike.lazy import LazyString

from verboselib import _core, to_language, to_locale
from verboselib._compatibility import PY3


__all__ = (
    'TranslationsFactory',
)


class VerboselibTranslation(gettext.GNUTranslations):
    """
    This class sets up the GNUTranslations context with regard to output
    charset.

    Credits: http://bit.ly/1xME37A
    """
    def __init__(self, *args, **kwargs):
        gettext.GNUTranslations.__init__(self, *args, **kwargs)
        self.set_output_charset('utf-8')
        self.__language = '??'

    def merge(self, other):
        self._catalog.update(other._catalog)

    def set_language(self, language):
        self.__language = language
        self.__to_language = to_language(language)

    def language(self):
        return self.__language

    def to_language(self):
        return self.__to_language

    def __repr__(self):
        return "<VerboselibTranslation lang:%s>" % self.__language


class TranslationsFactory(object):

    __slots__ = [
        '_translations', 'domain', 'locale_dir',
    ]

    def __init__(self, domain, locale_dir):
        self.domain = domain
        self.locale_dir = locale_dir
        self._translations = {
            _core.BYPASS_VALUE: gettext.NullTranslations(),
        }

    def _get_translation(self):
        language = getattr(_core._current_language,
                           'value',
                           copy(_core._default_language))

        t = self._translations.get(language, None)
        if t is not None:
            return t

        locale = to_locale(language)
        t = gettext.translation(
            domain=self.domain,
            localedir=self.locale_dir,
            languages=[locale, ],
            class_=VerboselibTranslation,
            fallback=True)
        t.set_language(language)
        self._translations[language] = t
        return t

    def gettext(self, message):
        return self._get_translation().gettext(message)

    def ugettext(self, message):
        if PY3:
            return self.gettext(message)
        else:
            return self._get_translation().ugettext(message)

    def gettext_lazy(self, message):
        return LazyString(lambda: self.gettext(message))

    def ugettext_lazy(self, message):
        return LazyString(lambda: self.ugettext(message))
