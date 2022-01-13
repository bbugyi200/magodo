"""Test that we can create custom MagicTodo classes."""

from __future__ import annotations

from pytest import mark

from magodo import MagicTodo, Todo
from magodo._dates import to_date


params = mark.parametrize

PARAMS = [
    (
        "x:1030 2022-01-12 Some done todo.",
        Todo(
            desc="Some done todo. dtime:1030",
            marked_done=True,
            create_date=to_date("2022-01-12"),
            metadata={"dtime": "1030"},
        ),
    )
]


@params(
    "line,expected",
    PARAMS,
)
def test_magic_todo(line: str, expected: Todo) -> None:
    """Test the MagicTodo.from_line() function."""
    magic_todo = MagicTodo.from_line(line).unwrap()
    actual = magic_todo.todo
    assert actual == expected
