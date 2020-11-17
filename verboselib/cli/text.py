import itertools
import sys

if sys.version_info >= (3, 9):
  List = list
else:
  from typing import List

from pathlib import Path
from typing import Optional


def normalize_eols(contents: str) -> str:
  lines = contents.splitlines()

  # Ensure last line has its EOL
  if lines and lines[-1]:
    lines.append("")

  return "\n".join(lines)


def flatten_comma_separated_values(values: Optional[List[str]]) -> List[str]:
  if not values:
    return []

  return list(itertools.chain(*[
    filter(
      len,
      map(
        str.strip,
        x.split(","),
      ),
    )
    for x in values
  ]))


def stringify_path(path: Path) -> str:
  return str(path.as_posix())
