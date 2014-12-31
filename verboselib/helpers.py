# -*- coding: utf-8 -*-

__all__ = ('to_locale', 'to_language', )


def to_locale(language, to_lower=False):
    """
    Turns a language name (en-us) into a locale name (en_US). If 'to_lower' is
    True, the last component is lower-cased (en_us).

    Taken `from Django <http://bit.ly/1ssrxqE>`_.
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

    Taken `from Django <http://bit.ly/1vWACbE>`_.
    """
    p = locale.find('_')
    if p >= 0:
        return locale[:p].lower() + '-' + locale[p + 1:].lower()
    else:
        return locale.lower()
