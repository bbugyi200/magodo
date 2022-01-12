"""Tests for the magodo package."""

from __future__ import annotations

from pytest import mark

from magodo import Todo
from magodo._dates import to_date


params = mark.parametrize


@params(
    "line,strict,expected",
    [
        ("no priority todo", False, Todo(desc="no priority todo")),
        ("(N) basic todo", False, Todo(desc="basic todo")),
        (
            "(N) 2022-01-10 todo with create date",
            True,
            Todo(
                desc="todo with create date",
                create_date=to_date("2022-01-10"),
            ),
        ),
        (
            "(N) 2022-03-04 2022-01-10 todo with done date",
            True,
            Todo(
                desc="todo with done date",
                create_date=to_date("2022-01-10"),
                done_date=to_date("2022-03-04"),
            ),
        ),
        (
            "x (N) 2022-01-10 done todo",
            True,
            Todo(
                desc="done todo",
                create_date=to_date("2022-01-10"),
                marked_done=True,
            ),
        ),
        (
            "x (A) todo with priority",
            True,
            Todo(
                desc="todo with priority",
                marked_done=True,
                priority="A",
            ),
        ),
        (
            "(N) todo for +some +project",
            True,
            Todo(
                desc="todo for +some +project",
                projects=("some", "project"),
            ),
        ),
        (
            "(N) todo for +some +project and a @context.",
            True,
            Todo(
                desc="todo for +some +project and a @context.",
                projects=("some", "project"),
                contexts=("context",),
            ),
        ),
        (
            "(N) todo with +some meta:data and a @context due:2022-12-31",
            True,
            Todo(
                desc="todo with +some meta:data and a @context due:2022-12-31",
                projects=("some",),
                contexts=("context",),
                metadata={"meta": "data", "due": "2022-12-31"},
            ),
        ),
        (
            "(N) todo with some dep:123, another dep:456, and a 3rd dep:789..."
            " foo:bar @crazy",
            True,
            Todo(
                desc=(
                    "todo with some dep:123, another dep:456, and a 3rd"
                    " dep:789... foo:bar @crazy"
                ),
                contexts=("crazy",),
                metadata={"dep": ["123", "456", "789"], "foo": "bar"},
            ),
        ),
        (
            "x:1030 Shorthand 'dtime' syntax.",
            True,
            Todo(
                desc="Shorthand 'dtime' syntax. dtime:1030",
                metadata={"dtime": "1030"},
                marked_done=True,
            ),
        ),
        (
            "x:1030 2022-01-01 Bug with shorthand 'dtime' syntax.",
            True,
            Todo(
                desc="Bug with shorthand 'dtime' syntax. dtime:1030",
                metadata={"dtime": "1030"},
                marked_done=True,
                create_date=to_date("2022-01-01"),
            ),
        ),
    ],
)
def test_todo(line: str, strict: bool, expected: Todo) -> None:
    """Test the Todo type."""
    actual = Todo.from_line(line, strict=strict)
    assert actual.unwrap() == expected
