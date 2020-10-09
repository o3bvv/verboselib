import itertools

from pathlib import Path

from typing import List
from typing import Optional
from typing import Text


def normalize_eols(contents: Text) -> Text:
  lines = contents.splitlines()

  # Ensure last line has its EOL
  if lines and lines[-1]:
    lines.append("")

  return "\n".join(lines)


def flatten_comma_separated_values(values: Optional[List[Text]]) -> List[Text]:
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


def stringify_path(path: Path) -> Text:
  return str(path.as_posix())
