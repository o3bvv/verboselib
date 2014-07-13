#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Execute management commands for verboselib.
"""
import os
import sys

from verboselib.management import get_commands
from verboselib.management.utils import print_out, print_err


def main(prog_name, args=None):
    args = args[:] if args else []
    commands = get_commands()

    try:
        command = args.pop(0)
    except IndexError:
        command = 'help'
        print_out(__doc__.strip())

    if command in commands.keys():
        commands[command].execute(prog_name, args)
    else:
        print_err("Unknown command '{:}'.".format(command))
        commands['help'].execute(prog_name)

    print_out("")


if __name__ == "__main__":
    prog_name = os.path.basename(sys.argv[0])
    main(prog_name, args=sys.argv[1:])
