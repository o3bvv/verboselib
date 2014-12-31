# -*- coding: utf-8 -*-

from stringlike import lazy


class LazyString(lazy.LazyString):

    @property
    def text_type(self):
        return str


class LazyUnicode(lazy.LazyString):
    pass
