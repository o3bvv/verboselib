import abc
import argparse
import sys

if sys.version_info >= (3, 9):
  List = list
  Type = type
else:
  from typing import List
  from typing import Type

from .lang import classproperty_readonly
from .utils import print_out


class BaseCommandExecutor(abc.ABC):

  @abc.abstractmethod
  def __init__(self, args: argparse.Namespace) -> None:
    ...

  @abc.abstractmethod
  def __call__(self) -> None:
    ...

  @staticmethod
  def _print_input_args(**kwargs) -> None:
    print_out(f"input args: {kwargs}")


class BaseCommand(abc.ABC):

  @classproperty_readonly
  def name(self) -> str:
    raise NotImplementedError

  @classproperty_readonly
  def aliases(self) -> List[str]:
    return []

  @classproperty_readonly
  def executor_class(self) -> Type[BaseCommandExecutor]:
    raise NotImplementedError

  @classmethod
  def make_executor(cls, args=argparse.Namespace) -> BaseCommandExecutor:
    return cls.executor_class(args)

  @classmethod
  @abc.abstractmethod
  def make_parser(cls, factory=argparse.ArgumentParser) -> argparse.ArgumentParser:
    ...
