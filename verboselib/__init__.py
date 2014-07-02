# -*- coding: utf-8 -*-
VERSION = (1, 0, 0)


def get_version():
    return '.'.join(str(x) for x in VERSION)


from verboselib.core import *
