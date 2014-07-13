# -*- coding: utf-8 -*-
import sys

from stringlike.utils import text_type  # pylint: disable=unused-import


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    string_types = (basestring, )
else:
    string_types = (str, )
