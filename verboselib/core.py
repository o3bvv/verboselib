# -*- coding: utf-8 -*-
import gettext
import six

from copy import copy
from threading import local


__all__ = (
    'set_default_language', 'to_locale', 'to_language',
    'use_language', 'use_language_bypass', 'drop_language',
    'TranslationsFactory',
)

BYPASS_VALUE = None

_default_language = None
_current_language = local()


def set_default_language(language=None):
    global _default_language
    _default_language = language


def to_locale(language, to_lower=False):
    """
    Turns a language name (en-us) into a locale name (en_US). If 'to_lower' is
    True, the last component is lower-cased (en_us).

    Credits: https://github.com/django/django/blob/9618d68b345fe69c787f8426b07e920e647e05f3/django/utils/translation/trans_real.py#L75-L90
    """
    p = language.find('-')
    if p >= 0:
        if to_lower:
            return language[:p].lower() + '_' + language[p + 1:].lower()
        else:
            # Get correct locale for sr-latn
            if len(language[p + 1:]) > 2:
                locale = language[:p].lower() + '_' + language[p + 1].upper()
                return locale + language[p + 2:].lower()
            return language[:p].lower() + '_' + language[p + 1:].upper()
    else:
        return language.lower()


def to_language(locale):
    """
    Turns a locale name (en_US) into a language name (en-us).

    Credits: https://github.com/django/django/blob/9618d68b345fe69c787f8426b07e920e647e05f3/django/utils/translation/trans_real.py#L93-L99
    """
    p = locale.find('_')
    if p >= 0:
        return locale[:p].lower() + '-' + locale[p + 1:].lower()
    else:
        return locale.lower()


def use_language(language):
    _current_language.value = language


def use_language_bypass():
    use_language(BYPASS_VALUE)


def drop_language():
    """
    Deinstalls the currently active translation object so that further _ calls
    will resolve against the default translation object, again.
    """
    if hasattr(_current_language, "value"):
        del _current_language.value


class VerboselibTranslation(gettext.GNUTranslations):
    """
    This class sets up the GNUTranslations context with regard to output
    charset.

    Credits: https://github.com/django/django/blob/cb9704fc4ff0d0091814c59bc3bed90e9728cb16/django/utils/translation/trans_real.py#L100-L124
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
            BYPASS_VALUE: gettext.NullTranslations(),
        }

    def _get_translation(self):
        language = getattr(_current_language, 'value', copy(_default_language))

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
        self._translations[language] = t
        return t

    def gettext(self, message):
        return self._get_translation().gettext(message)

    def ugettext(self, message):
        if six.PY3:
            return self.gettext(message)
        else:
            return self._get_translation().ugettext(message)
