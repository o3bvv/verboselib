# -*- coding: utf-8 -*-

from copy import copy
from threading import local


__all__ = (
    'set_default_language', 'get_default_language', 'get_language',
    'use_language', 'use_language_bypass', 'drop_language',
)

BYPASS_VALUE = None

_default_language = BYPASS_VALUE
_current_language = local()


def set_default_language(language=None):
    global _default_language
    _default_language = copy(language)


def get_default_language():
    return copy(_default_language)


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


def get_language():
    """
    Returns the currently selected language.
    """
    return copy(getattr(_current_language, 'value', _default_language))
