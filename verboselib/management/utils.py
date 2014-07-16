# -*- coding: utf-8 -*-
import os
import sys

from subprocess import PIPE, Popen

from verboselib._compatibility import string_types, text_type


def find_command(cmd, path=None, pathext=None):
    """
    Taken `from Django http://bit.ly/1njB3Y9>`_.
    """
    if path is None:
        path = os.environ.get('PATH', '').split(os.pathsep)
    if isinstance(path, string_types):
        path = [path]

    # check if there are path extensions for Windows executables
    if pathext is None:
        pathext = os.environ.get('PATHEXT', '.COM;.EXE;.BAT;.CMD')
        pathext = pathext.split(os.pathsep)

    # don't use extensions if the command ends with one of them
    for ext in pathext:
        if cmd.endswith(ext):
            pathext = ['']
            break

    # check if we find the command on PATH
    for p in path:
        f = os.path.join(p, cmd)
        if os.path.isfile(f):
            return f
        for ext in pathext:
            fext = f + ext
            if os.path.isfile(fext):
                return fext
    return None


def ensure_programs(*programs):
        for program in programs:
            if find_command(program) is None:
                raise RuntimeError(
                    "Can't find %s. Make sure you have GNU gettext tools 0.15 "
                    "or newer installed." % program)


def handle_extensions(extensions=None, ignored=None):
    """
    Organizes multiple extensions that are separated with commas or passed by
    using --extension/-e multiple times. Note that the .py extension is ignored
    here because of the way non-*.py files are handled in ``extract`` messages
    (they are copied to file.ext.py files to trick xgettext to parse them as
     Python files).

    For example: running::

        $ verboselib-manage extract -e js,txt -e xhtml -a

    would result in an extension list ``['.js', '.txt', '.xhtml']``

    .. code-block:: python

        >>> handle_extensions(['.html', 'html,js,py,py,py,.py', 'py,.py'])
        set(['.html', '.js'])
        >>> handle_extensions(['.html, txt,.tpl'])
        set(['.html', '.tpl', '.txt'])

    Taken `from Django <http://bit.ly/1r7Eokw>`_ and changed a bit.
    """
    extensions = extensions or ()
    ignored = ignored or ('py', )

    ext_list = []
    for ext in extensions:
        ext_list.extend(ext.replace(' ', '').split(','))
    for i, ext in enumerate(ext_list):
        if not ext.startswith('.'):
            ext_list[i] = '.%s' % ext_list[i]
    return set([x for x in ext_list if x.strip('.') not in ignored])


def popen_wrapper(args):
    """
    Friendly wrapper around Popen.

    Returns stdout output, stderr output and OS status code.
    """
    try:
        p = Popen(args,
                  shell=False,
                  stdout=PIPE,
                  stderr=PIPE,
                  close_fds=os.name != 'nt',
                  universal_newlines=True)
    except OSError as e:
        raise OSError(
            "Error executing '{:}': '{:}'".format(args[0], e.strerror))
    output, errors = p.communicate()
    return (
        output,
        text_type(errors),
        p.returncode
    )


def _wrap_writer(writer):
    return lambda x: writer("%s\n" % x)


print_out = _wrap_writer(sys.stdout.write)
print_err = _wrap_writer(sys.stderr.write)
