"""A Python library for working with the todo.txt format."""

import logging as _logging

from . import spells, types
from ._common import DEFAULT_PRIORITY, from_date, to_date
from ._group import DateRange, DescFilter, MetadataFilter, TodoGroup
from ._magic import MagicTodoMixin
from ._todo import Todo


__all__ = [
    "DEFAULT_PRIORITY",
    "DateRange",
    "DescFilter",
    "MagicTodoMixin",
    "MetadataFilter",
    "Todo",
    "TodoGroup",
    "from_date",
    "spells",
    "to_date",
    "types",
]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.10.1"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
