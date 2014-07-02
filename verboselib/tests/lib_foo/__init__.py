# -*- coding: utf-8 -*-
import verboselib

from os import path


here = path.abspath(path.dirname(__file__))
translator = verboselib.register(
    domain='foo',
    locale_dir=path.join(here, 'locale'))
