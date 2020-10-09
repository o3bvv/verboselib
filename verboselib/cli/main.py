import argparse
import functools

from verboselib.version import VERSION

from .utils import print_out

from .command_compile import CompileCommand
from .command_extract import ExtractCommand


def show_version() -> None:
  print_out(f"verboselib {VERSION}")


def make_parser() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description="run a verboselib command",
    add_help=True,
  )
  parser.add_argument(
    "-V", "--version",
    dest="show_version",
    action="store_true",
    help="show version of verboselib and exit"
  )

  subparsers = parser.add_subparsers(
    title="subcommands",
    dest="command_name",
  )

  extract_cmd_parser = ExtractCommand.make_parser(
    factory=functools.partial(
      subparsers.add_parser,
      name=ExtractCommand.name,
      aliases=ExtractCommand.aliases,
    ),
  )
  extract_cmd_parser.set_defaults(executor_factory=ExtractCommand.make_executor)

  compile_cmd_parser = CompileCommand.make_parser(
    factory=functools.partial(
      subparsers.add_parser,
      name=CompileCommand.name,
      aliases=CompileCommand.aliases,
    ),
  )
  compile_cmd_parser.set_defaults(executor_factory=CompileCommand.make_executor)

  return parser


def main():
  parser = make_parser()
  args = parser.parse_args()

  if args.show_version:
    show_version()
    return

  if hasattr(args, "executor_factory"):
    executor = args.executor_factory(args)
    executor()
  else:
    parser.print_help()
