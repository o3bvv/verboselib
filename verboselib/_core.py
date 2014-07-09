# -*- coding: utf-8 -*-
from threading import local


__all__ = (
    'set_default_language',
    'use_language', 'use_language_bypass', 'drop_language',
)

BYPASS_VALUE = None

_default_language = None
_current_language = local()


def set_default_language(language=None):
    global _default_language
    _default_language = language


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
