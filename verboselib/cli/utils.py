import functools
import os
import subprocess
import sys

if sys.version_info >= (3, 9):
  from collections.abc import Callable

  List  = list
  Tuple = tuple

else:
  from typing import Callable
  from typing import List
  from typing import Tuple

from typing import Optional


ERROR_CODE = -1


def find_executable(
  name:    str,
  path:    Optional[str]=None,
  pathext: Optional[str]=None,
) -> Optional[str]:

  if path is None:
    path = os.environ.get("PATH", "").split(os.pathsep)

  if isinstance(path, str):
    path = [path, ]

  # check if there are path extensions for Windows executables
  if pathext is None:
    pathext = os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD")
    pathext = pathext.split(os.pathsep)

  # don't use extensions if the command ends with one of them
  for ext in pathext:
    if name.endswith(ext):
      pathext = ["", ]
      break

  # check if we find the command on PATH
  for p in path:
    f = os.path.join(p, name)
    if os.path.isfile(f):
      return f

    for ext in pathext:
      fext = f + ext
      if os.path.isfile(fext):
        return fext

  return None


def popen_wrapper(args: List[str]) -> Tuple[str, str, int]:
  """
  Friendly wrapper for Popen.

  Returns stdout output, stderr output and OS status code.

  """
  is_windows = (os.name == "nt")
  try:
    p = subprocess.Popen(
      args,
      shell=False,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      close_fds=(not is_windows),
    )
  except OSError as e:
    raise OSError(f"failed to execute '{args[0]}'") from e
  else:
    output, errors = p.communicate()
    return (
      output.decode("utf-8"),
      errors.decode("utf-8"),
      p.returncode
    )


def halt() -> None:
  sys.exit(ERROR_CODE)


def show_usage_error_and_halt() -> None:
  print_err("run the command with -h/--help flag for usage information")
  halt()


def _wrap_writer(writer: Callable[[str], None]) -> Callable[[str], None]:

  @functools.wraps(writer)
  def wrapped(s: str) -> None:
    writer(f"{s}\n")

  return wrapped


print_out = _wrap_writer(sys.stdout.write)
print_err = _wrap_writer(sys.stderr.write)
