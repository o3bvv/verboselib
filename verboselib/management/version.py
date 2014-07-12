# -*- coding: utf-8 -*-
"""
Show current version of verboselib.
"""
from verboselib.management import print_out
from verboselib.version import __version__


def execute(args=None):
    print_out(__version__)
