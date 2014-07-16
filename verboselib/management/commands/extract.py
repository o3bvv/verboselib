# -*- coding: utf-8 -*-
"""
Extract 'gettext' strings from sources.
"""
import argparse
import fnmatch
import glob
import os
import sys

from itertools import dropwhile

from verboselib._lazy import LazyUnicode
from verboselib.management.utils import (
    ensure_programs, handle_extensions, popen_wrapper, print_err, print_out,
)


__help__ = LazyUnicode(lambda: _get_parser().format_help().strip())


COMMAND_NAME = 'extract'
DEFAULT_IGNORE_PATTERNS = [
    'CVS', '.*', '*~', '*.pyc',
]
DEFAULT_KEYWORDS = [
    'gettext', 'gettext_lazy', 'ugettext', 'ugettext_lazy', '_',
]
STATUS_OK = 0

_parser = None


def execute(prog_name, args=None):
    Command(prog_name, args)()


def _get_parser():
    global _parser

    if _parser is None:
        _parser = argparse.ArgumentParser(prog=COMMAND_NAME,
                                          description=__doc__,
                                          add_help=False)
        _parser.add_argument(
            '-d', '--domain',
            default='messages',
            dest='domain',
            help="The domain of the message files (default: \"messages\").",
        )
        _parser.add_argument(
            '-l', '--locale',
            default=None,
            dest='locale',
            action='append',
            help="Create or update the message files for the given locale(s) "
                 "(e.g. en_US). Can be used multiple times.",
        )
        _parser.add_argument(
            '-a', '--all',
            action='store_true',
            dest='all',
            default=False,
            help="Update the message files for all existing locales "
                 "(default: false).",
        )
        _parser.add_argument(
            '-o', '--output-dir',
            default='locale',
            dest='output_dir',
            help="Path to the directory where locales will be stored, a.k.a. "
                 "'locale dir' (default: \"locale\").",
        )
        _parser.add_argument(
            '-k', '--keyword',
            default=None,
            dest='keyword',
            action='append',
            help="Look for KEYWORD as an additional keyword (e.g., L_). Can be "
                 "used multiple times.",
        )
        _parser.add_argument(
            '-e', '--extension',
            dest='extensions',
            action='append',
            help="The file extension(s) to examine. Separate multiple "
                 "extensions with commas, or use multiple times.",
        )
        _parser.add_argument(
            '-s', '--symlinks',
            action='store_true',
            dest='follow_symlinks',
            default=False,
            help="Follows symlinks to directories when examining sources for "
                 "translation strings (default: false).",
        ),
        _parser.add_argument(
            '-i', '--ignore',
            action='append',
            dest='ignore_patterns',
            default=[],
            metavar='PATTERN',
            help="Ignore files or directories matching this glob-style pattern."
                 " Use multiple times to ignore more.",
        )
        _parser.add_argument(
            '--no-default-ignore',
            action='store_true',
            dest='no_default_ignore_patterns',
            default=False,
            help="Don't ignore the common glob-style patterns {:} "
                 "(default: false).".format(
                     ', '.join("\'%s\'" % x for x in DEFAULT_IGNORE_PATTERNS)
                 ),
        )
        _parser.add_argument(
            '--no-wrap',
            action='store_true',
            dest='no_wrap',
            default=False,
            help="Don't break long message lines into several lines. "
                 "(default: false).",
        )
        _parser.add_argument(
            '--no-location',
            action='store_true',
            dest='no_location',
            default=False,
            help="Don't write '#: filename:line' lines (default: false).",
        )
        _parser.add_argument(
            '--no-obsolete',
            action='store_true',
            dest='no_obsolete',
            default=False,
            help="Remove obsolete message strings (default: false).",
        )
        _parser.add_argument(
            '--keep-pot',
            action='store_true',
            dest='keep_pot',
            default=False,
            help="Keep .pot file after making messages. Useful when debugging "
                 "(default: false).",
        )
        _parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help="Use verbose output (default: false).",
        )
    return _parser


class Command(object):
    """
    Adapted `makemessages <http://bit.ly/1r7Et7O>`_ command from Django.
    """
    def __init__(self, prog_name, args=None):
        self.prog_name = prog_name
        args = _get_parser().parse_args(args or [])

        self.domain = args.domain
        self.locale = args.locale
        self.process_all = args.all
        self.locale_dir = args.output_dir

        self.keyword = args.keyword
        self.extensions = handle_extensions(args.extensions)
        self.follow_symlinks = args.follow_symlinks

        ignore_patterns = args.ignore_patterns
        if not args.no_default_ignore_patterns:
            ignore_patterns.extend(DEFAULT_IGNORE_PATTERNS)
        self.ignore_patterns = list(set(ignore_patterns))

        self.wrap = '--no-wrap' if args.no_wrap else ''
        self.no_location = '--no-location' if args.no_location else ''
        self.no_obsolete = args.no_obsolete
        self.keep_pot = args.keep_pot
        self.verbose = args.verbose

    def __call__(self):
        self.ensure_domain()
        self.ensure_target_locale()

        locales = self.get_locales()
        if not locales:
            print_out("No target locales")
            sys.exit()

        ensure_programs('xgettext', 'msguniq', 'msgmerge', 'msgattrib')
        self.ensure_locale_dir()

        potfile = self.make_pot_file()
        try:
            for locale in sorted(locales):
                print_out("Processing locale '{:}'".format(locale))
                self.make_po_file(potfile, locale)
        finally:
            if not self.keep_pot and os.path.exists(potfile):
                os.unlink(potfile)

    def ensure_domain(self):
        if not self.domain:
            self.usage_error()

    def ensure_target_locale(self):
        if self.locale is None and not self.process_all:
            self.usage_error()

    def ensure_locale_dir(self):
        if os.path.exists(self.locale_dir):
            if not os.path.isdir(self.locale_dir):
                raise OSError("\"%s\" is not a directory." % self.locale_dir)
        else:
            # This may throw an OSError
            os.makedirs(self.locale_dir)

    def usage_error(self):
        print_err("Type '{:} help {:}' for usage information.".format(
                  self.prog_name, COMMAND_NAME))
        sys.exit()

    def get_locales(self):
        if self.locale is not None:
            return self.locale
        elif self.process_all:
            return [
                os.path.basename(x) for x in
                filter(os.path.isdir, glob.glob('%s/*' % self.locale_dir))
            ]
        return []

    def make_pot_file(self):
        potfile = os.path.join(self.locale_dir, "%s.pot" % str(self.domain))
        if os.path.exists(potfile):
            # Remove a previous undeleted potfile, if any
            os.unlink(potfile)

        for dir_path, file_name in self.find_files("."):
            try:
                self.process_source_file(dir_path, file_name, potfile)
            except UnicodeDecodeError:
                print_err("Skipped file '{:}' in '{:}': UnicodeDecodeError."
                          .format(file_name, dir_path))
        return potfile

    def find_files(self, root):
        """
        Helper method to get all files in the given root.
        """

        def is_ignored(path, ignore_patterns):
            """
            Check if the given path should be ignored or not.
            """
            filename = os.path.basename(path)
            ignore = lambda pattern: fnmatch.fnmatchcase(filename, pattern)
            return any(ignore(pattern) for pattern in ignore_patterns)

        dir_suffix = '%s*' % os.sep
        normalized_patterns = [
            p[:-len(dir_suffix)] if p.endswith(dir_suffix) else p
            for p in self.ignore_patterns
        ]

        all_files = []
        walker = os.walk(root, topdown=True, followlinks=self.follow_symlinks)
        for dir_path, dir_names, file_names in walker:
            for dir_name in dir_names[:]:
                path = os.path.normpath(os.path.join(dir_path, dir_name))
                if is_ignored(path, normalized_patterns):
                    dir_names.remove(dir_name)
                    if self.verbose:
                        print_out("Ignoring directory '{:}'".format(dir_name))
            for file_name in file_names:
                path = os.path.normpath(os.path.join(dir_path, file_name))
                if is_ignored(path, self.ignore_patterns):
                    if self.verbose:
                        print_out("Ignoring file '{:}' in '{:}'".format(
                                  file_name, dir_path))
                else:
                    all_files.append((dir_path, file_name))
        return sorted(all_files)

    def process_source_file(self, dir_path, file_name, potfile):
        file_ext = os.path.splitext(file_name)[1]
        if not (file_ext == '.py' or file_ext in self.extensions):
            return
        if self.verbose:
            print_out("Processing file '{:}' in '{:}'".format(
                      file_name, dir_path))
        file_path = os.path.join(dir_path, file_name)

        args = [
            'xgettext',
            '-d', self.domain,
            '--language=Python',
            '--from-code=UTF-8',
            '--add-comments=Translators',
            '--output=-',
        ]

        keywords = DEFAULT_KEYWORDS
        if self.keyword:
            keywords.extend(self.keyword)
        args.extend([
            '--keyword=%s' % x for x in list(set(keywords))
        ])

        if self.wrap:
            args.append(self.wrap)
        if self.no_location:
            args.append(self.no_location)
        args.append(file_path)

        msgs, errors, status = popen_wrapper(args)
        if errors:
            if status != STATUS_OK:
                if not self.keep_pot and os.path.exists(potfile):
                    os.unlink(potfile)
                print_err("Errors happened while running xgettext on {:}:\n{:}"
                          .format(file_name, errors))
                sys.exit(status)
            else:  # Print warnings
                print_out(errors)
        if msgs:
            if os.path.exists(potfile):
                # Strip the header
                msgs = '\n'.join(dropwhile(len, msgs.split('\n')))
            else:
                msgs = msgs.replace('charset=CHARSET', 'charset=UTF-8')
            with open(potfile, 'a') as fp:
                fp.write(msgs)

    def make_po_file(self, potfile, locale):
        """
        Creates or updates the PO file for self.domain and :param locale:.
        Uses contents of the existing :param potfile:.

        Uses mguniq, msgmerge, and msgattrib GNU gettext utilities.
        """
        pofile = self._get_po_path(potfile, locale)

        msgs = self._get_unique_messages(potfile)
        msgs = self._merge_messages(potfile, pofile, msgs)
        msgs = self._strip_package_version(msgs)

        with open(pofile, 'w') as fp:
            fp.write(msgs)

        self._remove_obsolete_messages(pofile)

    def _get_unique_messages(self, potfile):
        args = ['msguniq', '--to-code=utf-8']
        self._ensure_messages_extra_args(args)
        args.append(potfile)
        return self._get_messages_from_command(args)

    def _get_po_path(self, potfile, locale):
        basedir = os.path.join(os.path.dirname(potfile), locale, 'LC_MESSAGES')
        if not os.path.isdir(basedir):
            os.makedirs(basedir)
        return os.path.join(basedir, '%s.po' % str(self.domain))

    def _merge_messages(self, potfile, pofile, msgs):
        if not os.path.exists(pofile):
            return msgs

        with open(potfile, 'w') as fp:
            fp.write(msgs)

        args = ['msgmerge', '-q']
        self._ensure_messages_extra_args(args)
        args.extend([pofile, potfile])

        return self._get_messages_from_command(args)

    def _strip_package_version(self, msgs):
        return msgs.replace(
            "#. #-#-#-#-#  %s.pot (PACKAGE VERSION)  #-#-#-#-#\n" % self.domain,
            "")

    def _remove_obsolete_messages(self, pofile):
        if not self.no_obsolete:
            return
        args = ['msgattrib', '-o', pofile, '--no-obsolete']
        self._ensure_messages_extra_args(args)
        args.append(pofile)
        self._get_messages_from_command(args)

    def _ensure_messages_extra_args(self, args):
        if self.wrap:
            args.append(self.wrap)
        if self.no_location:
            args.append(self.no_location)

    def _get_messages_from_command(self, args):
        msgs, errors, status = popen_wrapper(args)
        if errors:
            if status != STATUS_OK:
                raise RuntimeError(
                    "Errors happened while running {:}\n:{:}"
                    .format(args[0], errors))
            else:  # Print warnings
                print_out(errors)
        return msgs
