"""Tests for the magodo package."""

from __future__ import annotations

from pytest import mark

from magodo import DEFAULT_PRIORITY, Todo
from magodo._dates import to_date


params = mark.parametrize


@params(
    "line,expected",
    [
        ("no priority todo", Todo(desc="no priority todo")),
        (f"({DEFAULT_PRIORITY}) basic todo", Todo(desc="basic todo")),
        (
            f"({DEFAULT_PRIORITY}) 2022-01-10 todo with create date",
            Todo(
                desc="todo with create date",
                create_date=to_date("2022-01-10"),
            ),
        ),
        (
            f"({DEFAULT_PRIORITY}) 2022-03-04 2022-01-10 todo with done date",
            Todo(
                desc="todo with done date",
                create_date=to_date("2022-01-10"),
                done_date=to_date("2022-03-04"),
            ),
        ),
        (
            f"x ({DEFAULT_PRIORITY}) 2022-01-10 done todo",
            Todo(
                desc="done todo",
                create_date=to_date("2022-01-10"),
                marked_done=True,
            ),
        ),
        (
            "x (A) todo with priority",
            Todo(
                desc="todo with priority",
                marked_done=True,
                priority="A",
            ),
        ),
        (
            f"({DEFAULT_PRIORITY}) todo for +some +project",
            Todo(
                desc="todo for +some +project",
                projects=("some", "project"),
            ),
        ),
        (
            f"({DEFAULT_PRIORITY}) todo for +some +project and a @context.",
            Todo(
                desc="todo for +some +project and a @context.",
                projects=("some", "project"),
                contexts=("context",),
            ),
        ),
        (
            f"({DEFAULT_PRIORITY}) todo with +some meta:data and a @context"
            " due:2022-12-31",
            Todo(
                desc="todo with +some meta:data and a @context due:2022-12-31",
                projects=("some",),
                contexts=("context",),
                metadata={"meta": "data", "due": "2022-12-31"},
            ),
        ),
        (
            f"({DEFAULT_PRIORITY}) todo with some dep:123, another dep:456,"
            " and a 3rd dep:789... foo:bar @crazy",
            Todo(
                desc=(
                    "todo with some dep:123, another dep:456, and a 3rd"
                    " dep:789... foo:bar @crazy"
                ),
                contexts=("crazy",),
                metadata={"dep": ["123", "456", "789"], "foo": "bar"},
            ),
        ),
    ],
)
def test_todo(line: str, expected: Todo) -> None:
    """Test the Todo type."""
    actual = Todo.from_line(line)
    assert actual.unwrap() == expected
