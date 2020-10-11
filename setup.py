import itertools
import os
import shlex

from pathlib import Path
from setuptools import setup
from subprocess import check_output

from typing import List
from typing import Optional
from typing import Text
from typing import Tuple


__here__ = Path(__file__).absolute().parent


version_file_path = __here__ / "verboselib" / "version.py"
exec(compile(version_file_path.read_text(), version_file_path, "exec"))


def maybe_get_shell_output(command: Text) -> Text:
  try:
    args = shlex.split(command)
    with open(os.devnull, "w") as devnull:
      return check_output(args, stderr=devnull).strip().decode()
  except Exception:
    pass


def maybe_get_current_branch_name() -> Optional[Text]:
  return maybe_get_shell_output("git rev-parse --abbrev-ref HEAD")


def maybe_get_current_commit_hash() -> Optional[Text]:
  return maybe_get_shell_output("git rev-parse --short HEAD")


def parse_requirements(file_path: Path) -> Tuple[List[Text], List[Text]]:
  requirements, dependencies = list(), list()

  with file_path.open("rt") as f:
    for line in f:
      line = line.strip()

      if not line or line.startswith("#"):
        continue

      if line.startswith("-e"):
        line = line.split(" ", 1)[1]
        dependencies.append(line)
        line = line.split("#egg=", 1)[1]
        requirements.append(line)
      elif line.startswith("-r"):
        name = Path(line.split(" ", 1)[1])
        path = file_path.parent / name
        subrequirements, subdependencies = parse_requirements(path)
        requirements.extend(subrequirements)
        dependencies.extend(subdependencies)
      else:
        requirements.append(line)

  return requirements, dependencies


README = (__here__ / "README.rst").read_text()

STABLE_BRANCH_NAME  = "master"
CURRENT_COMMIT_HASH = maybe_get_current_commit_hash()
CURRENT_BRANCH_NAME = maybe_get_current_branch_name()
IS_CURRENT_BRANCH_STABLE = (CURRENT_BRANCH_NAME == STABLE_BRANCH_NAME)
BUILD_TAG = (
  f".{CURRENT_BRANCH_NAME}.{CURRENT_COMMIT_HASH}"
  if not IS_CURRENT_BRANCH_STABLE and CURRENT_COMMIT_HASH
  else ""
)

REQUIREMENTS_DIR_PATH = __here__ / "requirements"

TEST_REQUIREMENTS, TEST_DEPENDENCIES = parse_requirements(
  file_path=(REQUIREMENTS_DIR_PATH / "test.txt"),
)


setup(
  name="verboselib",
  version=VERSION,
  description="A little I18N framework for libraries and applications",
  long_description=README,
  long_description_content_type="text/x-rst",
  keywords=[
      "library", "l18n", "localization", "lazy", "string", "framework", "gettext",
  ],
  license="MIT",
  url=f"https://github.com/oblalex/verboselib/tree/v{VERSION}",

  author="Oleksandr Oblovatnyi",
  author_email="oblovatniy@gmail.com",

  packages=[
    "verboselib",
    "verboselib.cli",
  ],
  entry_points={
    "console_scripts": [
      "verboselib = verboselib.cli.main:main",
    ],
  },

  python_requires=">=3.7",
  dependency_links=list(set(itertools.chain(
    TEST_DEPENDENCIES,
  ))),
  tests_require=TEST_REQUIREMENTS,
  test_suite="tests",

  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Libraries",
  ],

  options={
    'egg_info': {
      'tag_build': BUILD_TAG,
      'tag_date':  False,
    },
  },

  zip_safe=True,
)
