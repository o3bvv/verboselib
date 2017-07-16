# -*- coding: utf-8 -*-
"""
Show current version of verboselib.
"""
from verboselib.management.utils import print_out
from verboselib.version import VERSION


def execute(prog_name, args=None):
    print_out(VERSION)
