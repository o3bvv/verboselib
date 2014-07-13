# -*- coding: utf-8 -*-
import importlib
import os

from verboselib.management.utils import print_err
from verboselib._compatibility import text_type


_cache = None


def _list_modules():
    path = os.path.join(__path__[0], 'commands')
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
    module_name = 'verboselib.management.commands.%s' % name
    try:
        module = importlib.import_module(module_name)
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
