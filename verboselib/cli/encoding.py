import codecs

from pathlib import Path


def has_bom(file_path: Path) -> bool:
  with file_path.open("rb") as f:
    sample = f.read(4)

  return (
       sample[:3] == b"\xef\xbb\xbf"
    or sample.startswith(codecs.BOM_UTF16_LE)
    or sample.startswith(codecs.BOM_UTF16_BE)
  )
