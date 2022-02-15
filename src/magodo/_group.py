"""Contains the TodoGroup class definition."""

from __future__ import annotations

import datetime as dt
from logging import Logger
from pathlib import Path
from typing import Generic, Iterable, Iterator, Mapping, Type

from eris import Err
from metaman import cname
from typist import PathLike

from .types import MetadataChecker, Priority, T


logger = Logger(__name__)


class TodoGroup(Generic[T]):
    """Manages a group of Todo objects."""

    def __init__(
        self,
        todos: Iterable[T],
        todo_map: dict[str, T],
        path_map: dict[str, Path],
    ) -> None:
        self.todos = list(todos)
        self.todo_map = todo_map
        self.path_map = path_map

    def __repr__(self) -> str:  # noqa: D105
        return f"{cname(self)}({self.todos})"

    def __iter__(self) -> Iterator[T]:
        """Yields the Todo objects that belong to this group."""
        yield from self.todos

    def __len__(self) -> int:  # noqa: D105
        return len(self.todos)

    @classmethod
    def from_path(
        cls,
        todo_type: Type[T],
        path_like: PathLike,
        *,
        path_map: dict[str, Path] = None,
        todo_map: dict[str, T] = None,
    ) -> TodoGroup:
        """Reads all todo lines from a given file or directory (recursively).

        Pre-conditions:
            * `path_like` exists and is either a file or directory.
        """
        path = Path(path_like)
        if path_map is None:
            path_map = {}

        if todo_map is None:
            todo_map = {}

        assert path.exists(), f"The provided path does not exist: {path}"

        todos = []
        if path.is_file():
            logger.debug(
                "Attempting to load todos from text file: file=%r", str(path)
            )

            for line in path.read_text().split("\n"):
                line = line.strip()
                todo_result = todo_type.from_line(line)
                if isinstance(todo_result, Err):
                    continue

                todo = todo_result.ok()
                logger.debug("New todo loaded: todo=%r", todo)
                todos.append(todo)

                key = todo.ident
                path_map[key] = path
                todo_map[key] = todo

        else:
            assert path.is_dir(), (
                "The provided path exists but is neither a file nor a"
                f" directory: {path}"
            )

            logger.debug("Loading from directory: dir=%r", str(path))
            for other_path in path.glob("*"):
                if other_path.is_file() and other_path.suffix != ".txt":
                    continue

                todos.extend(
                    TodoGroup.from_path(
                        todo_type,
                        other_path,
                        path_map=path_map,
                        todo_map=todo_map,
                    )
                )

        return cls(todos, todo_map, path_map)

    def filter_by(
        self,
        *,
        contexts: Iterable[str] = (),
        create_date: dt.date = None,
        desc: str = None,
        done_date: dt.date = None,
        done: bool = None,
        metadata_checks: Mapping[str, MetadataChecker] = None,
        priorities: Iterable[Priority] = (),
        projects: Iterable[str] = (),
    ) -> TodoGroup:
        """Filter this group using one or more Todo properties."""
        todos = []
        path_map = {}
        todo_map = {}

        for key, todo in self.todo_map.items():
            skip_this_todo = False
            for ctx in contexts:
                if ctx.startswith("-") and ctx[1:] in todo.contexts:
                    skip_this_todo = True
                    break

                if ctx not in todo.contexts:
                    skip_this_todo = True
                    break

            for proj in projects:
                if proj.startswith("-") and proj[1:] in todo.projects:
                    skip_this_todo = True
                    break

                if proj not in todo.projects:
                    skip_this_todo = True
                    break

            if priorities and todo.priority not in priorities:
                continue

            if create_date is not None and todo.create_date != create_date:
                continue

            if desc is not None and desc.lower() not in todo.desc.lower():
                continue

            if done_date is not None and todo.done_date != done_date:
                continue

            if done is not None and todo.done != done:
                continue

            if metadata_checks is not None:
                for mkey, check in metadata_checks.items():
                    if mkey not in todo.metadata:
                        skip_this_todo = True
                        break

                    mvalue = todo.metadata[mkey]
                    assert isinstance(mvalue, str)
                    if not check(mvalue):
                        skip_this_todo = True
                        break

            if skip_this_todo:
                continue

            todos.append(todo)
            path_map[key] = self.path_map[key]
            todo_map[key] = todo

        return TodoGroup(todos, todo_map, path_map)
