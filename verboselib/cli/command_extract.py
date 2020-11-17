import argparse
import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable

  List = list
  Set  = set

else:
  from typing import Iterable
  from typing import List
  from typing import Set

if sys.version_info >= (3, 8):
  from typing import Literal
  MODE = Literal["w", "a"]
else:
  MODE = str

from pathlib import Path
from typing import Optional

from .command_base import BaseCommand
from .command_base import BaseCommandExecutor

from .gettext_tools import extract_translations
from .gettext_tools import extract_unique_messages
from .gettext_tools import merge_new_and_existing_translations
from .gettext_tools import remove_obsolete_translations
from .gettext_tools import strip_translations_header
from .gettext_tools import validate_gettext_tools_exist

from .paths import ensure_dir_exists
from .paths import find_source_files_paths
from .paths import get_names_of_immediate_subdirectories
from .paths import make_po_file_path
from .paths import make_pot_file_path

from .text import flatten_comma_separated_values
from .text import stringify_path

from .utils import print_err
from .utils import print_out
from .utils import show_usage_error_and_halt

from . import defaults


class ExtractCommandExecutor(BaseCommandExecutor):

  def __init__(self, args=argparse.Namespace) -> None:
    self._domain = args.domain
    self._validate_domain(self._domain)

    self._process_all_locales = args.all

    self._locales_dir_path = self._handle_locales_dir_path(args.output_dir)
    self._validate_locales_dir_path(self._locales_dir_path)

    self._pot_file_path = make_pot_file_path(self._locales_dir_path, self._domain)

    self._locales = self._handle_locales(
      locales=args.locale,
      process_all=self._process_all_locales,
      locales_dir_path=self._locales_dir_path,
    )
    self._validate_locales(self._locales)

    self._keywords = self._handle_keywords(
      keywords=args.keyword,
      no_defaults=args.no_default_keywords,
    )
    self._extensions = self._handle_extensions(args.extensions)
    self._follow_links = args.follow_links
    self._ignore_patterns = self._handle_ignore_patterns(
      ignore_patterns=args.ignore_patterns,
      no_defaults=args.no_default_ignore_patterns,
    )
    self._no_wrap = args.no_wrap
    self._no_location = args.no_location
    self._no_obsolete = args.no_obsolete
    self._keep_pot = args.keep_pot
    self._xgettext_extra_args = flatten_comma_separated_values(args.xgettext_extra_args)
    self._msguniq_extra_args = flatten_comma_separated_values(args.msguniq_extra_args)
    self._msgmerge_extra_args = flatten_comma_separated_values(args.msgmerge_extra_args)
    self._msgattrib_extra_args = flatten_comma_separated_values(args.msgattrib_extra_args)
    self._verbose = args.verbose

  @staticmethod
  def _handle_keywords(
    keywords: Optional[Iterable[str]]=None,
    no_defaults: bool=False,
  ) -> List[str]:

    keywords = (
      list(keywords)
      if keywords is not None
      else []
    )

    if not no_defaults:
      keywords.extend(defaults.DEFAULT_KEYWORDS)

    return list(sorted(set(keywords)))

  @staticmethod
  def _handle_extensions(
    extensions: Optional[Iterable[str]]=None,
    ignored: Optional[Iterable[str]]=None,
  ) -> Set[str]:

    extensions = (
      list(extensions)
      if extensions is not None
      else []
    )

    ignored = (
      set(ignored)
      if ignored is not None
      else set()
    )

    ext_list = []

    for ext in extensions:
      ext_list.extend(ext.replace(" ", "").split(","))

    for i, ext in enumerate(ext_list):
      if not ext.startswith("."):
        ext_list[i] = ".%s" % ext_list[i]

    ext_list.append(".py")

    return {
      x
      for x in ext_list
      if x.strip(".") not in ignored
    }

  @staticmethod
  def _handle_ignore_patterns(
    ignore_patterns: Optional[Iterable[str]]=None,
    no_defaults: bool=False,
  ) -> List[str]:

    ignore_patterns = (
      list(ignore_patterns)
      if ignore_patterns is not None
      else []
    )

    if not no_defaults:
      ignore_patterns.extend(defaults.DEFAULT_IGNORE_PATTERNS)

    return list(sorted(set(ignore_patterns)))

  @staticmethod
  def _validate_domain(domain: Optional[str]) -> None:
    if not domain:
      print_err(f"invalid domain value: '{domain}'")
      show_usage_error_and_halt()

  @staticmethod
  def _handle_locales_dir_path(path: str) -> Path:
    return Path(path).absolute()

  @staticmethod
  def _validate_locales_dir_path(path: Path) -> None:
    if path.exists() and not path.is_dir():
      print_err(
        f"locales dir already exists but it is not a directory "
        f"(path={stringify_path(path)})"
      )
      show_usage_error_and_halt()

  @staticmethod
  def _handle_locales(
    locales: Optional[List[str]],
    process_all: bool,
    locales_dir_path: Path,
  ) -> List[str]:

    if locales:
      return flatten_comma_separated_values(locales)
    elif process_all:
      return get_names_of_immediate_subdirectories(locales_dir_path)
    else:
      return []

  @staticmethod
  def _validate_locales(locales: List[str]) -> None:
    if not locales:
      print_err(
        "specify at least 1 locale or specify processing of all existing locales"
      )
      show_usage_error_and_halt()

  def __call__(self) -> None:
    validate_gettext_tools_exist()

    if self._verbose:
      self._print_input_args(
        domain=self._domain,
        locales_dir_path=stringify_path(self._locales_dir_path),
        process_all_locales=self._process_all_locales,
        locales=self._locales,
        keywords=self._keywords,
        extensions=self._extensions,
        follow_links=self._follow_links,
        ignore_patterns=self._ignore_patterns,
        no_wrap=self._no_wrap,
        no_location=self._no_location,
        no_obsolete=self._no_obsolete,
        keep_pot=self._keep_pot,
        xgettext_extra_args=self._xgettext_extra_args,
        msguniq_extra_args=self._msguniq_extra_args,
        msgmerge_extra_args=self._msgmerge_extra_args,
        msgattrib_extra_args=self._msgattrib_extra_args,
        verbose=self._verbose,
      )

    ensure_dir_exists(self._locales_dir_path)

    try:
      self._make_pot_file()
      self._ensure_no_duplicates_in_pot_file()
      self._make_all_po_files()
    finally:
      if not self._keep_pot:
        self._maybe_remove_pot_file()

  def _make_pot_file(self) -> None:
    if self._verbose:
      print_out("making '.pot' file")

    self._maybe_remove_pot_file()

    sources_root_dir_path = Path(".")  # explicitly use relative path

    for file_path in find_source_files_paths(
      root_dir_path=sources_root_dir_path,
      ignore_patterns=self._ignore_patterns,
      extensions=self._extensions,
      follow_links=self._follow_links,
      verbose=self._verbose,
    ):
      self._process_source_file(file_path)

  def _process_source_file(self, source_file_path: Path) -> None:
    if self._verbose:
      print_out(f"processing source '{stringify_path(source_file_path.absolute())}'")

    content = extract_translations(
      source_file_path=source_file_path,
      domain=self._domain,
      keywords=self._keywords,
      no_wrap=self._no_wrap,
      no_location=self._no_location,
      xgettext_extra_args=self._xgettext_extra_args,
    )

    if content:
      if self._pot_file_path.exists():
        content = strip_translations_header(content)
      else:
        content = content.replace("charset=CHARSET", "charset=UTF-8")

      self._write_translations_file(
        file_path=self._pot_file_path,
        content=content,
        mode="a",
      )

  def _ensure_no_duplicates_in_pot_file(self) -> None:
    unique_messages = self._extract_unique_messages()

    self._write_translations_file(
      file_path=self._pot_file_path,
      content=unique_messages,
      mode="w",
    )

  def _extract_unique_messages(self) -> str:
    if self._verbose:
      print_out("extracting unique messages from '.pot' file")

    return extract_unique_messages(
      pot_file_path=self._pot_file_path,
      no_wrap=self._no_wrap,
      no_location=self._no_location,
      msguniq_extra_args=self._msguniq_extra_args,
    )

  def _make_all_po_files(self) -> None:
    if self._verbose:
      print_out("making '.po' files")

    for locale in self._locales:
      self._make_po_file_for_locale(locale=locale)

  def _make_po_file_for_locale(self, locale: str) -> None:
    if self._verbose:
      print_out(f"processing locale '{locale}'")

    po_file_path = make_po_file_path(
      locales_dir_path=self._locales_dir_path,
      locale=locale,
      domain=self._domain,
    )

    ensure_dir_exists(po_file_path.parent)

    if po_file_path.exists():
      content = self._merge_new_and_existing_translations(po_file_path)
    else:
      content = self._pot_file_path.read_text(encoding="utf-8")

    self._write_translations_file(
      file_path=po_file_path,
      content=content,
      mode="w",
    )

    if self._no_obsolete:
      self._remove_obsolete_translations(po_file_path)

  def _merge_new_and_existing_translations(self, po_file_path: Path) -> str:
    if self._verbose:
      print_out("merging existing and new messages")

    return merge_new_and_existing_translations(
      po_file_path=po_file_path,
      pot_file_path=self._pot_file_path,
      no_wrap=self._no_wrap,
      no_location=self._no_location,
      msgmerge_extra_args=self._msgmerge_extra_args,
    )

  def _remove_obsolete_translations(self, file_path: Path) -> None:
    if self._verbose:
      print_out("removing obsolete translations")

    remove_obsolete_translations(
      po_file_path=file_path,
      no_wrap=self._no_wrap,
      no_location=self._no_location,
      msgattrib_extra_args=self._msgattrib_extra_args,
    )

  def _write_translations_file(
    self,
    file_path: Path,
    content=str,
    mode=MODE,
  ) -> None:

    if self._verbose:
      print_out(f"writing to '{stringify_path(file_path)}' file")

    # Force newlines to '\n' to work around
    # https://savannah.gnu.org/bugs/index.php?52395
    with file_path.open(mode, encoding="utf-8", newline="\n") as f:
      f.write(content)

  def _maybe_remove_pot_file(self) -> None:
    if self._pot_file_path.exists():
      if self._verbose:
        print_out("removing '.pot' file")

      self._pot_file_path.unlink()


class ExtractCommand(BaseCommand):
  name = "extract"
  aliases = ["x", ]
  executor_class = ExtractCommandExecutor

  @classmethod
  def make_parser(cls, factory=argparse.ArgumentParser) -> argparse.ArgumentParser:
    description = "extract translatable strings from sources into '.po' files"
    parser = factory(
      prog=cls.name,
      description=description,
      add_help=True,
      help=description,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
      "-d", "--domain",
      dest="domain",
      default=defaults.DEFAULT_DOMAIN,
      help="domain of message files",
    )
    parser.add_argument(
      "-l", "--locale",
      dest="locale",
      action="append",
      help=(
        "create or update '.po' message files for the given locale(s), "
        "ex: 'en_US'; can be specified multiple times"
      ),
    )
    parser.add_argument(
      "-a", "--all",
      dest="all",
      action="store_true",
      default=False,
      help="update all '.po' message files for all existing locales",
    )
    parser.add_argument(
      "-o", "--output-dir",
      dest="output_dir",
      default=defaults.DEFAULT_LOCALE_DIR_NAME,
      help="path to the directory where locales will be stored, a.k.a. 'locale dir'",
    )
    parser.add_argument(
      "-k", "--keyword",
      action="append",
      dest="keyword",
      help="extra keyword to look for, ex: 'L_'; can be specified multiple times",
    )
    parser.add_argument(
      "--no-default-keywords",
      action="store_true",
      dest="no_default_keywords",
      default=False,
      help=(
        "do not use default keywords as {{{:}}}".format(
          ", ".join(map(repr, defaults.DEFAULT_KEYWORDS))
        )
      ),
    )
    parser.add_argument(
      "-e", "--extension",
      dest="extensions",
      action="append",
      help=(
        "extra file extension(s) to scan in addition to '.py'; separate multiple "
        "values with commas or specify the parameter multiple times"
      ),
    )
    parser.add_argument(
      "-s", "--links",
      action="store_true",
      dest="follow_links",
      default=False,
      help=(
        "follow links to files and directories when scanning sources for "
        "translation strings"
      ),
    )
    parser.add_argument(
      "-i", "--ignore",
      action="append",
      dest="ignore_patterns",
      metavar="PATTERN",
      help=(
        "extra glob-style patterns for ignoring files or directories; "
        "can be specified multiple times"
      ),
    )
    parser.add_argument(
      "--no-default-ignore",
      action="store_true",
      dest="no_default_ignore_patterns",
      default=False,
      help=(
        "do not ignore the common glob-style patterns as {{{:}}}".format(
          ", ".join(map(repr, defaults.DEFAULT_IGNORE_PATTERNS))
        )
      ),
    )
    parser.add_argument(
      "--no-wrap",
      action="store_true",
      dest="no_wrap",
      default=False,
      help="do not break long message lines into several lines",
    )
    parser.add_argument(
      "--no-location",
      action="store_true",
      dest="no_location",
      default=False,
      help="do not write location lines, ex: '#: filename:lineno'",
    )
    parser.add_argument(
      "--no-obsolete",
      action="store_true",
      dest="no_obsolete",
      default=False,
      help="remove obsolete message strings",
    )
    parser.add_argument(
      "--keep-pot",
      action="store_true",
      dest="keep_pot",
      default=False,
      help="keep '.pot' file after creating '.po' files (useful for debugging)",
    )
    parser.add_argument(
      "--xgettext-extra-args",
      action="append",
      dest="xgettext_extra_args",
      help=(
        "extra arguments for 'xgettext' utility; "
        "can be comma-separated or specified multiple times"
      ),
    )
    parser.add_argument(
      "--msguniq-extra-args",
      action="append",
      dest="msguniq_extra_args",
      help=(
        "extra arguments for 'msguniq' utility; "
        "can be comma-separated or specified multiple times"
      ),
    )
    parser.add_argument(
      "--msgmerge-extra-args",
      action="append",
      dest="msgmerge_extra_args",
      help=(
        "extra arguments for 'msgmerge' utility; "
        "can be comma-separated or specified multiple times"
      ),
    )
    parser.add_argument(
      "--msgattrib-extra-args",
      action="append",
      dest="msgattrib_extra_args",
      help=(
        "extra arguments for 'msgattrib' utility; "
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
