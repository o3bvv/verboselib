# -*- coding: utf-8 -*-
VERSION = (0, 1, 0)


def get_version():  # pragma: no cover
    return '.'.join(str(x) for x in VERSION)


from ._core import *
from ._factory import *
from ._helpers import *
