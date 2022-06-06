"""Test that we can create custom MagicTodo classes."""

from __future__ import annotations

from typing import List

from pytest import mark

from magodo import MagicTodoMixin
from magodo.types import TodoSpell


params = mark.parametrize


def to_test_line(line: str) -> str:
    """Prepends 'test |' to `line`."""
    return "test | " + line


def from_test_line(line: str) -> str:
    """Removes 'test | ' from `line`."""
    return line.replace("test | ", "")


class LineTodo(MagicTodoMixin):
    """MagicTodo that adds 'test | ' to the beginning of each line."""

    from_line_spells = [from_test_line]
    to_line_spells = [to_test_line]
    todo_spells: List[TodoSpell] = []

    ident: str = "LINE TODO"


@params("line", ["1900-01-01 foo bar baz", "test | 1900-01-01 foo bar baz"])
def test_line_todo(line: str) -> None:
    """Test that to_line and from_line spells work."""
    todo = LineTodo.from_line(line).unwrap()
    assert todo.desc == "foo bar baz"
    assert todo.to_line() == "test | 1900-01-01 foo bar baz"
