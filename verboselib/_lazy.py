# -*- coding: utf-8 -*-


def text_type(*args, **kwargs):
    import six
    return six.text_type(*args, **kwargs)


class StringProxy(object):
    """
    Class to mimic the behavior of a regular string. Classes that inherit
    (or mixin) this class must implement the `__str__` magic method. Whatever
    that method returns is used by the various string-like methods.
    """

    def __getattr__(self, attr):
        """
        Forwards any non-magic methods to the resulting string's class. This
        allows support for string methods like `upper()`, `lower()`, etc.
        """
        string = text_type(self)
        if hasattr(string, attr):
            return getattr(string, attr)
        raise AttributeError(attr)

    def __len__(self):
        return len(text_type(self))

    def __getitem__(self, key):
        return text_type(self)[key]

    def __iter__(self):
        return iter(text_type(self))

    def __contains__(self, item):
        return item in text_type(self)

    def __add__(self, other):
        return text_type(self) + other

    def __radd__(self, other):
        return other + text_type(self)

    def __mul__(self, other):
        return text_type(self) * other

    def __rmul__(self, other):
        return other * text_type(self)

    def __lt__(self, other):
        return text_type(self) < other

    def __le__(self, other):
        return text_type(self) <= other

    def __eq__(self, other):
        return text_type(self) == other

    def __ne__(self, other):
        return text_type(self) != other

    def __gt__(self, other):
        return text_type(self) > other

    def __ge__(self, other):
        return text_type(self) >= other


class LazyString(StringProxy):
    """
    A lazy string *without* caching. The resulting string is regenerated for
    every request.
    """
    def __init__(self, func):
        """
        Creates a `LazyString` object using `func` as the delayed closure.
        `func` must return a string.
        """
        self._func = func

    def __str__(self):
        """
        Returns the actual string.
        """
        return text_type(self._func())
