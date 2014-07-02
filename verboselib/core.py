# -*- coding: utf-8 -*-
__all__ = (
    'register', 'register_many',
)


def _register(components):
    pass


def register(domain, locale_dir):
    return _register([(domain, locale_dir), ])


def register_many(*args, **kwargs):

    def _from_dict(value):

        def _by_key(key):
            try:
                return value[key]
            except KeyError:
                raise ValueError("Argument \"{:}\" does not have keyword '{:}'."
                                 .format(value, key))

        return (_by_key('domain'), _by_key('locale_dir'))

    def _from_iterable(value):
        try:
            return tuple(arg[:2])
        except ValueError:
            raise ValueError("Argument \"{:}\" has not enough components. Use "
                             "'(domain, locale_dir)' format.".format(arg))

    components = []

    for arg in args:
        if isinstance(arg, dict):
            components.append(_from_dict(arg))
        elif isinstance(arg, (list, tuple)):
            components.append(_from_iterable(arg))
        else:
            raise TypeError("Argument  \"{:}\" is not a dictionary nor an "
                            "iterable.".format(arg))

    return _register(components)
