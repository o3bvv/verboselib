# -*- coding: utf-8 -*-
"""
List available commands or show help for a particular command.
"""
from verboselib.management import get_commands
from verboselib.management.utils import print_out, print_err


__usage__ = 'help [COMMAND]'


def execute(prog_name, args=None):
    if args:
        command = args[0]
        commands = get_commands()
        if command in commands:
            _print_module_help(commands[command])
        else:
            print_err("Unknown command '{:}'.".format(command))
            _list_commands()
    else:
        _list_commands()


def _print_module_help(module):
    message = getattr(module, '__help__', None)
    if message:
        print_out(message)
    else:
        messages = []
        usage = getattr(module, '__usage__', None)
        if usage:
            messages.append("usage: %s" % usage.strip())
            messages.append("")

        description = _description(module)
        if description:
            messages.append(_description(module))
        else:
            messages.append("No description.")

        print_out('\n'.join(messages))


def _list_commands():
    messages = [
        "Available commands:",
        "",
    ]
    commands = get_commands()
    for name in sorted(commands.keys()):
        module = commands[name]
        description = _description(module)
        if description:
            description = description.split('\n')[0].rstrip('.')
            description = description[0].lower() + description[1:]
            message = "{:} ({:}).".format(name, description)
        else:
            message = name
        messages.append("    - " + message)

    print_out('\n'.join(messages))


_description = lambda module: module.__doc__.strip() if module.__doc__ else None
