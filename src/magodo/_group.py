"""Contains the TodoGroup class definition."""

from __future__ import annotations

from logging import Logger
from pathlib import Path
from typing import Iterable, Iterator, List

from eris import Err
from typist import PathLike

from ._todo import Todo


logger = Logger(__name__)


class TodoGroup:
    """Manages a group of Todo objects."""

    def __init__(self, todos: Iterable[Todo]) -> None:
        self._todos = list(todos)

    def __repr__(self) -> str:  # noqa: D105
        return f"{self.__class__.__name__}(todos={self._todos})"

    def __iter__(self) -> Iterator[Todo]:
        """Yields the Todo objects that belong to this group."""
        yield from self._todos

    @classmethod
    def from_path(cls, path_like: PathLike) -> TodoGroup:
        """Reads all todo lines from a given file or directory (recursively).

        Pre-conditions:
            * `path_like` exists and is either a file or directory.
        """
        path = Path(path_like)

        assert path.exists(), f"The provided path does not exist: {path}"

        todos: List[Todo] = []
        if path.is_file():
            logger.debug(
                "Attempting to load todos from text file: file=%r", str(path)
            )

            for line in path.read_text().split("\n"):
                line = line.strip()
                todo_result = Todo.from_line(line, strict=True)
                if isinstance(todo_result, Err):
                    continue

                todo = todo_result.ok()
                todos.append(todo)
                logger.debug("New todo loaded: todo=%r", todo)
        else:
            assert path.is_dir(), (
                "The provided path exists but is neither a file nor a"
                f" directory: {path}"
            )

            logger.debug("Loading from directory: dir=%r", str(path))
            for other_path in path.glob("*"):
                if other_path.is_file() and other_path.suffix != ".txt":
                    continue

                other_todo_group = TodoGroup.from_path(other_path)
                todos.extend(other_todo_group)

        return cls(todos)
