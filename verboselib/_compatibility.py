# -*- coding: utf-8 -*-

import sys

from stringlike.utils import text_type  # pylint: disable=unused-import


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:  # pragma: no cover
    string_types = (basestring, )
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
else:  # pragma: no cover
    string_types = (str, )


def native_path(path):  # pragma: no cover
    """
    Always return a native path, that is unicode on Python 3 and bytestring on
    Python 2.

    Taken `from Django <http://bit.ly/1r3gogZ>`_.
    """
    if PY2 and not isinstance(path, bytes):
        return path.encode(fs_encoding)
    return path
