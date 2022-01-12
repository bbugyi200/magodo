"""A Python library for working with the todo.txt format."""

import logging as _logging

from . import types
from ._group import TodoGroup
from ._todo import DEFAULT_PRIORITY, Todo


__all__ = ["DEFAULT_PRIORITY", "Todo", "TodoGroup", "types"]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.4.1"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
