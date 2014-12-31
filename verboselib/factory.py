# -*- coding: utf-8 -*-

import gettext

from . import _core
from ._compatibility import PY3
from ._lazy import LazyString, LazyUnicode
from .helpers import to_locale


__all__ = ('TranslationsFactory', )


class TranslationsFactory(object):

    __slots__ = ['_translations', 'domain', 'locale_dir', ]

    def __init__(self, domain, locale_dir):
        self.domain = domain
        self.locale_dir = locale_dir
        self._translations = {
            _core.BYPASS_VALUE: gettext.NullTranslations(),
        }

    def _get_translation(self):
        language = _core.get_language()

        t = self._translations.get(language, None)
        if t is not None:
            return t

        locale = to_locale(language)
        t = gettext.translation(domain=self.domain,
                                localedir=self.locale_dir,
                                languages=[locale, ],
                                codeset='utf-8',
                                fallback=True)
        self._translations[language] = t
        return t

    def gettext(self, message):
        return self._get_translation().gettext(message)

    def ugettext(self, message):
        method = self.gettext if PY3 else self._get_translation().ugettext
        return method(message)

    def gettext_lazy(self, message):
        return LazyString(lambda: self.gettext(message))

    def ugettext_lazy(self, message):
        return LazyUnicode(lambda: self.ugettext(message))
