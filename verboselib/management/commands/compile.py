# -*- coding: utf-8 -*-
"""
Compile '*.po' files into '*.mo' binaries.
"""
import argparse
import codecs
import os

from verboselib._compatibility import native_path
from verboselib._lazy import LazyUnicode
from verboselib.management.utils import (
    ensure_programs, popen_wrapper, print_out,
)


__help__ = LazyUnicode(lambda: _get_parser().format_help().strip())
_parser = None


def execute(prog_name, args=None):
    """
    Adapted `compilemessages <http://bit.ly/1r3glSu>`_ command from Django.
    """
    args = _get_parser().parse_args(args or [])
    locale, locale_dir = args.locale, args.locale_dir

    program = 'msgfmt'
    ensure_programs(program)

    def has_bom(fn):
        with open(fn, 'rb') as f:
            sample = f.read(4)
        return (sample[:3] == b'\xef\xbb\xbf'
                or sample.startswith(codecs.BOM_UTF16_LE)
                or sample.startswith(codecs.BOM_UTF16_BE))

    if locale:
        dirs = [os.path.join(locale_dir, l, 'LC_MESSAGES') for l in locale]
    else:
        dirs = [locale_dir, ]
    for ldir in dirs:
        for dir_path, dir_names, file_names in os.walk(ldir):
            for file_name in file_names:
                if not file_name.endswith('.po'):
                    continue
                print_out("Processing file '{:}' in {:}".format(file_name,
                                                                dir_path))
                file_path = os.path.join(dir_path, file_name)
                if has_bom(file_path):
                    raise RuntimeError(
                        "The '{:}' file has a BOM (Byte Order Mark). "
                        "Verboselib supports only .po files encoded in UTF-8 "
                        "and without any BOM.".format(file_path))
                prefix = os.path.splitext(file_path)[0]
                args = [
                    program,
                    '--check-format',
                    '-o',
                    native_path(prefix + '.mo'),
                    native_path(prefix + '.po'),
                ]
                output, errors, status = popen_wrapper(args)
                if status:
                    if errors:
                        msg = "Execution of %s failed: %s" % (program, errors)
                    else:
                        msg = "Execution of %s failed" % program
                    raise RuntimeError(msg)


def _get_parser():
    global _parser

    if _parser is None:
        _parser = argparse.ArgumentParser(prog='compile',
                                          description=__doc__,
                                          add_help=False)
        _parser.add_argument(
            '-l', '--locale',
            dest='locale',
            action='append',
            help="Locale(s) to process (e.g. en_US). Default is to process "
                 "all. Can be used multiple times."
        )
        _parser.add_argument(
            '-d', '--locale-dir',
            default='locale',
            dest='locale_dir',
            help="Path to the directory where locales are stored "
                 "(default: \"locale\").",
        )
    return _parser
