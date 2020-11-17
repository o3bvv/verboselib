import argparse
import sys

if sys.version_info >= (3, 9):
  List = list
else:
  from typing import List

from pathlib import Path
from typing import Optional

from .command_base import BaseCommand
from .command_base import BaseCommandExecutor

from .encoding import has_bom

from .gettext_tools import compile_translations
from .gettext_tools import validate_gettext_tools_exist

from .paths import get_names_of_immediate_subdirectories
from .paths import make_messages_dir_path
from .paths import make_mo_file_path

from .text import flatten_comma_separated_values
from .text import stringify_path

from .utils import halt
from .utils import print_err
from .utils import print_out
from .utils import show_usage_error_and_halt

from . import defaults


class CompileCommandExecutor(BaseCommandExecutor):

  def __init__(self, args=argparse.Namespace) -> None:
    self._locales_dir_path = self._handle_locales_dir_path(args.locales_dir)
    self._validate_locales_dir_path(self._locales_dir_path)

    self._locales = self._handle_locales(
      locales=args.locale,
      locales_dir_path=self._locales_dir_path,
    )
    self._validate_locales(
      locales=self._locales,
      locales_dir_path=self._locales_dir_path,
    )

    self._exclude = set(flatten_comma_separated_values(args.exclude))

    self._fuzzy = args.fuzzy

    self._msgfmt_extra_args = flatten_comma_separated_values(args.msgfmt_extra_args)
    self._verbose = args.verbose

  @staticmethod
  def _handle_locales_dir_path(path: str) -> Path:
    return Path(path).absolute()

  @staticmethod
  def _validate_locales_dir_path(path: Path) -> None:
    if not path.exists():
      print_err(f"locales dir does not exist (path={stringify_path(path)}")
      show_usage_error_and_halt()

    if not path.is_dir():
      print_err(f"locales dir is not a directory (path={stringify_path(path)})")
      show_usage_error_and_halt()

  @staticmethod
  def _handle_locales(
    locales: Optional[List[str]],
    locales_dir_path: Path,
  ) -> List[str]:

    if locales:
      return flatten_comma_separated_values(locales)

    return get_names_of_immediate_subdirectories(locales_dir_path)

  @staticmethod
  def _validate_locales(
    locales: List[str],
    locales_dir_path: Path,
  ) -> None:
    if not locales:
      print_err(
        "specify at least 1 locale or specify processing of all existing locales"
      )
      show_usage_error_and_halt()

    for locale in locales:
      path = make_messages_dir_path(locales_dir_path, locale)
      if not (path.exists() and path.is_dir()):
        print_err(
          f"invalid locale '{locale}': "
          f"directory '{stringify_path(path)}' expected to exist"
        )
        show_usage_error_and_halt()

  def __call__(self) -> None:
    validate_gettext_tools_exist()

    if self._verbose:
      self._print_input_args(
        locales_dir_path=stringify_path(self._locales_dir_path),
        locales=self._locales,
        fuzzy=self._fuzzy,
        msgfmt_extra_args=self._msgfmt_extra_args,
        verbose=self._verbose,
      )

    final_locales = sorted(set(self._locales) - self._exclude)

    for locale in final_locales:
      self._process_locale(locale=locale)

  def _process_locale(self, locale: str) -> None:
    if self._verbose:
      print_out(f"processing locale '{locale}'")

    messages_dir_path = make_messages_dir_path(self._locales_dir_path, locale)

    for path in messages_dir_path.iterdir():
      if path.is_file() and path.suffix == ".po":
        self._process_translations_file(file_path=path)

  def _process_translations_file(self, file_path: Path) -> None:
    if self._verbose:
      print_out(f"processing file '{stringify_path(file_path)}'")

    if has_bom(file_path):
      print_err(
        f"the file '{stringify_path(file_path)}' file has a BOM (Byte Order Mark). "
        f"Verboselib supports only '.po' files encoded in UTF-8 and without any BOM."
      )
      halt()

    mo_file_path = make_mo_file_path(file_path)

    compile_translations(
      mo_file_path=mo_file_path,
      po_file_path=file_path,
      fuzzy=self._fuzzy,
      msgfmt_extra_args=self._msgfmt_extra_args,
    )


class CompileCommand(BaseCommand):
  name = "compile"
  aliases = ["c", ]
  executor_class = CompileCommandExecutor

  @classmethod
  def make_parser(cls, factory=argparse.ArgumentParser) -> argparse.ArgumentParser:
    description = "compile '.po' text files into '.mo' binaries"
    parser = factory(
      prog=cls.name,
      description=description,
      add_help=True,
      help=description,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
      "-d", "--locale-dir",
      dest="locales_dir",
      default=defaults.DEFAULT_LOCALE_DIR_NAME,
      help="path to the directory where locales are stored",
    )
    parser.add_argument(
      "-l", "--locale",
      dest="locale",
      action="append",
      help=(
        "locale(s) to process, ex: 'en_US'; "
        "can be specified multiple times; "
        "all locales are processed if not specified"
      ),
    )
    parser.add_argument(
      "-e", "--exclude",
      dest="exclude",
      action="append",
      help="locale(s) to exclude, ex: 'en_US'; can be specified multiple times",
    )
    parser.add_argument(
      "-f", "--use-fuzzy",
      action="store_true",
      dest="fuzzy",
      default=False,
      help="use fuzzy translations",
    )
    parser.add_argument(
      "--msgfmt-extra-args",
      action="append",
      dest="msgfmt_extra_args",
      help=(
        "extra arguments for 'msgfmt' utility; "
        "can be comma-separated or specified multiple times"
      ),
    )
    parser.add_argument(
      "-v", "--verbose",
      action="store_true",
      dest="verbose",
      default=False,
      help="use verbose output",
    )
    return parser
