"""Test that we can create custom MagicTodo classes."""

from __future__ import annotations

from typing import List, Type

from pytest import mark

from magodo import MagicTodoMixin, Todo
from magodo.types import AbstractMagicTodo, TodoSpell

from .shared import MOCK_TODO_KWARGS, MagicTodo, assert_todos_equal


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


@params(
    "line,magic_todo_type,pre_inner_todo,expected_inner_todo",
    [
        (
            "x:1030 2022-01-12 Some done todo.",
            MagicTodo,
            Todo(
                desc="x:1030 Some done todo.",
                metadata={"x": "1030"},
                done=True,
            ),
            Todo(
                desc="Some done todo. | ctime:HHMM dtime:HHMM",
                done=True,
            ),
        ),
        (
            "x:1030 2022-01-12 Some done todo with a @ctx.",
            MagicTodo,
            Todo(
                desc="x:1030 Some done todo with a @ctx.",
                contexts=("ctx",),
                metadata={"x": "1030"},
                done=True,
            ),
            Todo(
                desc="Some done todo with a ctx. | @ctx ctime:HHMM dtime:HHMM",
                contexts=("ctx",),
                done=True,
            ),
        ),
    ],
)
def test_magic_todo(
    line: str,
    magic_todo_type: Type[AbstractMagicTodo[Todo]],
    pre_inner_todo: Todo,
    expected_inner_todo: Todo,
) -> None:
    """Test the MagicTodo.from_line() function."""
    from_line_mtodo = magic_todo_type.from_line(line).unwrap()
    from_line_mtodo = from_line_mtodo.new(**MOCK_TODO_KWARGS)

    pre_inner_todo = pre_inner_todo.new(**MOCK_TODO_KWARGS)
    from_todo_mtodo = magic_todo_type(pre_inner_todo).new(**MOCK_TODO_KWARGS)
    post_inner_todo = from_todo_mtodo.todo.new(**MOCK_TODO_KWARGS)
    expected_inner_todo = expected_inner_todo.new(**MOCK_TODO_KWARGS)

    assert_todos_equal(post_inner_todo, expected_inner_todo)

    assert repr(from_line_mtodo) == repr(from_todo_mtodo)


@params("line", ["foo bar baz", "test | foo bar baz"])
def test_line_todo(line: str) -> None:
    """Test that to_line and from_line spells work."""
    todo = LineTodo.from_line(line).unwrap()
    assert todo.desc == "foo bar baz"
    assert todo.to_line() == "test | foo bar baz"
