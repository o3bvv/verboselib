# -*- coding: utf-8 -*-
import importlib
import os
import sys

from stringlike.utils import text_type

_cache = None


def _list_modules():
    path = __path__[0]
    try:
        return [
            file_name[:-3] for file_name in os.listdir(path)
            if not file_name.startswith('_') and file_name.endswith('.py')
        ]
    except OSError as e:
        print_err("Failed to list modules at '{:}': {:}"
                  .format(path, text_type(e)))
        return []


def _load_module(name):
    try:
        module = importlib.import_module('verboselib.management.%s' % name)
    except Exception as e:
        print_err("Failed to load module for command '{:}': {:}"
                  .format(name, text_type(e)))
    else:
        if hasattr(module, 'execute'):
            return module


def get_commands():
    global _cache
    if _cache is None:
        command_names = _list_modules()
        _cache = {
            name: module for name, module in
            zip(command_names, map(_load_module, command_names))
            if module if not None
        }
    return _cache


def _wrap_writer(writer):
    return lambda x: writer("%s\n" % x)


print_out = _wrap_writer(sys.stdout.write)
print_err = _wrap_writer(sys.stderr.write)
