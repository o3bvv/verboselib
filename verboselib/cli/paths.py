import fnmatch
import os

from pathlib import Path

from typing import List
from typing import Set
from typing import Text

from .text import stringify_path
from .utils import print_out


MESSAGES_DIR_NAME = "LC_MESSAGES"


def make_messages_dir_path(locales_dir_path: Path, locale: Text) -> Path:
  return locales_dir_path / locale / MESSAGES_DIR_NAME


def make_pot_file_path(locales_dir_path: Path, domain: Text) -> Path:
  return locales_dir_path / f"{domain}.pot"


def make_po_file_path(
  locales_dir_path: Path,
  locale: Text,
  domain: Text,
) -> Path:

  messages_dir_path = make_messages_dir_path(locales_dir_path, locale)
  messages_file_name = f"{domain}.po"

  return messages_dir_path / messages_file_name


def make_mo_file_path(po_file_path: Path) -> Path:
  return po_file_path.parent / f"{po_file_path.stem}.mo"


def get_names_of_immediate_subdirectories(root: Path) -> List[Text]:
  return [
    node.name
    for node in root.iterdir()
    if node.is_dir()
  ]


def ensure_dir_exists(path: Path) -> None:
  path.mkdir(parents=True, exist_ok=True)


def is_path_ignored(path: Path, ignore_patterns: List[Text]) -> bool:
  for pattern in ignore_patterns:
    if fnmatch.fnmatchcase(path.name, pattern):
      return True
  else:
    return False


def normalize_dir_patterns(patterns: List[Text]) -> List[Text]:
  dir_suffix = "{os.sep}*"
  return [
    (
       p[:-len(dir_suffix)]
      if p.endswith(dir_suffix)
      else p
    )
    for p in patterns
  ]


def find_source_files_paths(
  root_dir_path: Path,
  ignore_patterns: List[Text],
  extensions: Set[Text],
  follow_links: bool,
  verbose: bool,
) -> List[Path]:

  result = []

  walker = os.walk(
    top=stringify_path(root_dir_path),
    topdown=True,
    followlinks=follow_links,
  )

  normalized_ignore_patterns = normalize_dir_patterns(ignore_patterns)

  for dir_path, dir_names, file_names in walker:

    for dir_name in dir_names[:]:
      path = Path(os.path.normpath(os.path.join(dir_path, dir_name)))
      if is_path_ignored(path, normalized_ignore_patterns):
        dir_names.remove(dir_name)
        if verbose:
          print_out(f"ignoring dir '{stringify_path(path.absolute())}'")

    for file_name in file_names:
      path = Path(os.path.normpath(os.path.join(dir_path, file_name)))
      if is_path_ignored(path, ignore_patterns):
        if verbose:
          print_out(f"ignoring file '{stringify_path(path.absolute())}'")
      elif path.suffix in extensions:
        result.append(path)

  return list(sorted(result))
