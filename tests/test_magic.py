"""Test that we can create custom MagicTodo classes."""

from __future__ import annotations

from typing import Type

from pytest import mark

from magodo import MagicTodo, Todo
from magodo._dates import to_date
from magodo.types import AbstractMagicTodo


params = mark.parametrize


@params(
    "line,magic_todo_type,todo,etodo",
    [
        (
            "x:1030 2022-01-12 Some done todo.",
            MagicTodo,
            Todo(
                desc="x:1030 2022-01-12 Some done todo.",
                metadata={"x": "1030"},
            ),
            Todo(
                desc="Some done todo. dtime:1030",
                marked_done=True,
                create_date=to_date("2022-01-12"),
                metadata={"dtime": "1030"},
            ),
        )
    ],
)
def test_magic_todo(
    line: str,
    magic_todo_type: Type[AbstractMagicTodo],
    todo: Todo,
    etodo: Todo,
) -> None:
    """Test the MagicTodo.from_line() function."""
    actual = magic_todo_type.from_line(line).unwrap()
    expected = magic_todo_type(todo)
    assert expected.enchanted_todo == etodo
    assert actual == expected
