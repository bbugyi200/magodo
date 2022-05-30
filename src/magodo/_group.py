"""Contains the TodoGroup class definition."""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from logging import Logger
from pathlib import Path
from typing import Generic, Iterable, Iterator, Type

from eris import Err
from metaman import cname
from typist import PathLike

from ._common import to_date
from .types import DoublePredicate, Priority, SinglePredicate, T


logger = Logger(__name__)


@dataclass(frozen=True)
class MetadataFilter:
    """A specification for filtering on metadata."""

    key: str
    check: SinglePredicate = lambda _: True
    required: bool = True


@dataclass(frozen=True)
class DescFilter:
    """A description filter specification."""

    value: str
    check: DoublePredicate = lambda x, y: x in y
    case_sensitive: bool | None = None


@dataclass(frozen=True)
class DateRange:
    """Represents a range of dates."""

    start: dt.date
    end: dt.date | None = None

    @classmethod
    def from_strings(cls, start_str: str, end_str: str = None) -> DateRange:
        """Constructs a DateRange from two strings."""
        start = to_date(start_str)
        end = to_date(end_str) if end_str else None
        return cls(start, end)


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

    def filter_by(  # noqa: C901
        self,
        *,
        contexts: Iterable[str] = (),
        create_date_ranges: Iterable[DateRange] = (),
        desc_filters: Iterable[DescFilter] = (),
        done_date_ranges: Iterable[DateRange] = (),
        done: bool = None,
        epics: Iterable[str] = (),
        metadata_filters: Iterable[MetadataFilter] = (),
        priorities: Iterable[Priority] = (),
        projects: Iterable[str] = (),
    ) -> TodoGroup:
        """Filter this group using one or more Todo properties."""
        todos = []
        path_map = {}
        todo_map = {}

        for key, todo in self.todo_map.items():
            skip_this_todo = False

            for desired_props, attr in [
                (contexts, "contexts"),
                (epics, "epics"),
                (projects, "projects"),
            ]:
                todo_props = getattr(todo, attr)
                for prop in desired_props:
                    if prop.startswith("-") and _has_property(
                        todo_props, prop[1:]
                    ):
                        skip_this_todo = True
                        break

                    if not prop.startswith("-") and not _has_property(
                        todo_props, prop
                    ):
                        skip_this_todo = True
                        break

            if priorities and todo.priority not in priorities:
                continue

            for date_ranges, date in [
                (create_date_ranges, todo.create_date),
                (done_date_ranges, todo.done_date),
            ]:
                if not date_ranges:
                    continue

                if not any(
                    date is not None
                    and date_range.start
                    <= date
                    <= (date_range.end or date_range.start)
                    for date_range in date_ranges
                ):
                    skip_this_todo = True
                    break

            for dfilter in desc_filters:
                case_sensitive = dfilter.case_sensitive
                if case_sensitive is None:
                    case_sensitive = not bool(dfilter.value.islower())

                desc = dfilter.value
                todo_desc = todo.desc
                if not case_sensitive:
                    desc = desc.lower()
                    todo_desc = todo_desc.lower()

                if not dfilter.check(desc, todo_desc):
                    skip_this_todo = True
                    break

            if done is not None and todo.done != done:
                continue

            for mfilter in metadata_filters:
                key_not_found = mfilter.key not in todo.metadata
                if mfilter.required and key_not_found:
                    skip_this_todo = True
                    break

                if key_not_found:
                    continue

                mvalue = todo.metadata[mfilter.key]
                assert isinstance(mvalue, str)
                if not mfilter.check(mvalue):
                    skip_this_todo = True
                    break

            if skip_this_todo:
                continue

            todos.append(todo)
            path_map[key] = self.path_map[key]
            todo_map[key] = todo

        return TodoGroup(todos, todo_map, path_map)


def _has_property(all_props: tuple[str], prop: str) -> bool:
    if prop.endswith(".*"):
        parent_prop = prop[:-2]
        return any(
            p == parent_prop or p.startswith(parent_prop + ".")
            for p in all_props
        )
    else:
        return prop in all_props
