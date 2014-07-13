# -*- coding: utf-8 -*-
import sys

from stringlike.utils import text_type  # pylint: disable=unused-import


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    string_types = (basestring, )

    def reraise(tp, value, tb=None):
        raise tp, value, tb

else:
    string_types = (str, )

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
