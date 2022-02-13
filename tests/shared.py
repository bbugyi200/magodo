"""Shared test utilities."""

import datetime as dt
from typing import List

from magodo import MagicTodoMixin
from magodo.spells import (
    DEFAULT_POST_TODO_SPELLS,
    DEFAULT_PRE_TODO_SPELLS,
    DEFAULT_TODO_SPELLS,
    add_o_prefix,
    remove_o_prefix,
)
from magodo.types import AbstractTodo, LineSpell, TodoSpell


CREATE_DATE = dt.datetime.strptime("1900-01-01", "%Y-%m-%d").date()
DONE_DATE = dt.datetime.strptime("2022-02-07", "%Y-%m-%d").date()
METADATA = {"ctime": "HHMM", "dtime": "HHMM"}

MOCK_TODO_KWARGS = {
    "metadata": METADATA,
    "create_date": CREATE_DATE,
    "done_date": DONE_DATE,
}


class MagicTodo(MagicTodoMixin):
    """The default MagicTodo class."""

    pre_todo_spells: List[TodoSpell] = DEFAULT_PRE_TODO_SPELLS
    todo_spells: List[TodoSpell] = DEFAULT_TODO_SPELLS
    post_todo_spells: List[TodoSpell] = DEFAULT_POST_TODO_SPELLS

    to_line_spells: List[LineSpell] = [add_o_prefix]
    from_line_spells: List[LineSpell] = [remove_o_prefix]


def assert_todos_equal(actual: AbstractTodo, expected: AbstractTodo) -> None:
    """Helper function for asserting that one Todo is equal to another."""
    assert (
        actual.desc == expected.desc
    ), f"{actual.desc!r} != {expected.desc!r}"
    assert (
        actual.priority == expected.priority
    ), f"{actual.priority!r} != {expected.priority!r}"
    assert (
        actual.create_date == expected.create_date
    ), f"{actual.create_date!r} != {expected.create_date!r}"
    assert (
        actual.done_date == expected.done_date
    ), f"{actual.done_date!r} != {expected.done_date!r}"
    assert (
        actual.projects == expected.projects
    ), f"{actual.projects!r} != {expected.projects!r}"
    assert (
        actual.contexts == expected.contexts
    ), f"{actual.contexts!r} != {expected.contexts!r}"
    assert (
        actual.done == expected.done
    ), f"{actual.done!r} != {expected.done!r}"
    assert (
        actual.metadata == expected.metadata
    ), f"{actual.metadata!r} != {expected.metadata!r}"
