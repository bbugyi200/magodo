"""Shared test utilities."""

import datetime as dt

from magodo import MagicTodoMixin
from magodo.types import TodoProto


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


def assert_todos_equal(actual: TodoProto, expected: TodoProto) -> None:
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
