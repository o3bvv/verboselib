# -*- coding: utf-8 -*-

from threading import local


__all__ = (
    'set_default_language', 'to_locale', 'to_language',
    'use_language', 'use_language_bypass', 'drop_language',
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
