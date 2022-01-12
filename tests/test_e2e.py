"""End-to-End (E2E) tests for this library."""

from __future__ import annotations

from pathlib import Path

from pytest import mark
from syrupy.assertion import SnapshotAssertion as Snapshot

import magodo

from .data import get_all_todo_paths


params = mark.parametrize


@params("todo_file", get_all_todo_paths())
def test_group_From_file(snapshot: Snapshot, todo_file: Path) -> None:
    """Test the TodoGroup.from_file() function."""
    todo_group = magodo.TodoGroup.from_path(todo_file)
    assert [todo.__dict__ for todo in todo_group] == snapshot
