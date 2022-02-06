"""A Python library for working with the todo.txt format."""

import logging as _logging

from . import spells, types
from ._reader import TodoReader
from ._magic import MagicTodoMixin
from ._shared import DEFAULT_PRIORITY
from ._todo import Todo


__all__ = [
    "DEFAULT_PRIORITY",
    "MagicTodoMixin",
    "Todo",
    "TodoReader",
    "spells",
    "types",
]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.7.1"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
