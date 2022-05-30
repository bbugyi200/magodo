"""Test that TodoGroup objects work as they should."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest import mark, param
from syrupy.assertion import SnapshotAssertion as Snapshot

from magodo import DescFilter, TodoGroup

from .data import get_all_todo_paths
from .shared import MOCK_TODO_KWARGS, MagicTodo


params = mark.parametrize


@params("todo_file", get_all_todo_paths())
@params(
    "filter_kwargs",
    [
        param({}, id="no-filter-kwargs"),
        param(
            {"desc_filters": [DescFilter("Double colons")]},
            id="filter-kwarg-desc",
        ),
        param({"contexts": ["high"]}, id="ctx"),
        param(
            {"desc_filters": [DescFilter("item")], "projects": ["-test"]},
            id="negative project match",
        ),
        param(
            {"desc_filters": [DescFilter("Item")], "projects": ["-test"]},
            id="case-sensitive desc filter",
        ),
    ],
)
def test_group_from_path(
    snapshot: Snapshot, todo_file: Path, filter_kwargs: dict[str, Any]
) -> None:
    """Test the TodoGroup.from_path() function."""
    todo_group = TodoGroup.from_path(MagicTodo, todo_file)
    todo_group = todo_group.filter_by(**filter_kwargs)
    assert (
        sorted(repr(todo.new(**MOCK_TODO_KWARGS)) for todo in todo_group)
        == snapshot
    )
