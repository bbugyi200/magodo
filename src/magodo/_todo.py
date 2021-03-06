"""Contains the basic / standard Todo class definition."""

# pylint: disable=format-string-without-interpolation

from __future__ import annotations

import abc
import datetime as dt
from functools import total_ordering
import re
from typing import Any, Dict, Final, Generic, List, Optional, Tuple, cast
import uuid

from eris import ErisError, Err, Ok, Result
from metaman import cname

from ._common import DEFAULT_PRIORITY, PUNCTUATION
from .dates import from_date, to_date
from .tags import (
    CONTEXT_PREFIX,
    EPIC_PREFIX,
    PROJECT_PREFIX,
    is_metadata_tag,
    is_prefix_tag,
)
from .types import Metadata, Priority, T


RE_DATE: Final = r"[1-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]"
RE_TODO: Final = r"""
(?P<x>x[ ]+)?                        # optional 'x'
(?:\((?P<priority>[A-Z])\)[ ]+)?     # priority
(?:
    (?:(?P<done_date>{0})[ ]+)?      # optional date of completion
    (?:(?P<create_date>{0})[ ]+)     # optional date of creation
)?
(?P<desc>[A-Za-z0-9+@].*)            # description
""".format(
    RE_DATE
)


class TodoMixin(Generic[T], abc.ABC):
    """Implements standard Todo-like behaviors.."""

    @property
    def ident(self) -> str:
        """Unique identifier."""
        key = "_uuid_ident"
        if not hasattr(self, key):
            setattr(self, key, uuid.uuid4())

        result: str = getattr(self, key)
        return result

    def __repr__(self: T) -> str:  # noqa: D105
        kwargs: Dict[str, Any] = {}

        if self.contexts:
            kwargs["contexts"] = self.contexts

        if self.create_date is not None:
            kwargs["create_date"] = self.create_date

        if self.done_date is not None:
            kwargs["done_date"] = self.done_date

        if self.done:
            kwargs["done"] = self.done

        if self.epics:
            kwargs["epics"] = self.epics

        if self.metadata:
            kwargs["metadata"] = self.metadata

        if self.priority != DEFAULT_PRIORITY:
            kwargs["priority"] = repr(self.priority)

        if self.projects:
            kwargs["projects"] = self.projects

        if kwargs:
            pretty_kwargs = ", " + ", ".join(
                f"{k}={v}" for (k, v) in kwargs.items()
            )
        else:
            pretty_kwargs = ""

        return f"{cname(self)}(desc={self.desc!r}{pretty_kwargs})"

    def __eq__(self: T, other: object) -> bool:  # noqa: D105
        if not isinstance(other, type(self)):  # pragma: no cover
            return False

        return all(
            [
                self.contexts == other.contexts,
                self.create_date == other.create_date,
                self.desc == other.desc,
                self.done == other.done,
                self.done_date == other.done_date,
                self.epics == other.epics,
                self.metadata == other.metadata,
                self.priority == other.priority,
                self.projects == other.projects,
            ]
        )

    def __lt__(self: T, other: object) -> bool:  # noqa: D105
        if not isinstance(other, type(self)):
            raise ValueError(
                f"Unable to compare '{type(other)}' object with 'Todo' object."
            )

        if self.done != other.done:
            return not self.done and other.done

        if self.priority != other.priority:
            return self.priority < other.priority

        if self.done_date is None and other.done_date is not None:
            return True

        if other.done_date is None and self.done_date is not None:
            return False

        if self.done_date is not None and other.done_date is not None:
            if self.done_date != other.done_date:
                return self.done_date < other.done_date
            elif (
                (self_dtime := self.metadata.get("dtime", None))
                and (other_dtime := other.metadata.get("dtime", None))
                and self_dtime != other_dtime
            ):
                return self_dtime < other_dtime

        if self.create_date and other.create_date:
            if self.create_date == other.create_date:
                if (
                    (self_ctime := self.metadata.get("ctime", None))
                    and (other_ctime := other.metadata.get("ctime", None))
                    and self_ctime != other_ctime
                ):
                    return self_ctime < other_ctime
            else:
                return self.create_date < other.create_date

        if (self_id := self.metadata.get("id", None)) and (
            other_id := other.metadata.get("id", None)
        ):
            return self_id < other_id

        return self.desc < other.desc


@total_ordering
class Todo(TodoMixin):
    """Represents a single task in a todo list."""

    def __init__(
        self,
        desc: str,
        *,
        contexts: Tuple[str, ...] = (),
        create_date: dt.date = None,
        done_date: dt.date = None,
        done: bool = False,
        epics: Tuple[str, ...] = (),
        metadata: Metadata = None,
        priority: Priority = DEFAULT_PRIORITY,
        projects: Tuple[str, ...] = (),
    ):
        if create_date is None:
            create_date = dt.date.today()

        if metadata is None:
            metadata = {}

        if done and done_date is None:
            done_date = dt.date.today()

        time_keys = ["ctime"]
        if done:
            time_keys.append("dtime")

        for key in time_keys:
            if key not in metadata:
                now = dt.datetime.now()
                hhmm = f"{now.hour:0>2}{now.minute:0>2}"
                metadata[key] = hhmm

        self.contexts = tuple(sorted(contexts))
        self.create_date = create_date
        self.desc = desc
        self.done_date = done_date
        self.done = done
        self.epics = tuple(sorted(epics))
        self.metadata = metadata
        self.priority = priority
        self.projects = tuple(sorted(projects))

    @classmethod
    def from_line(cls, line: str) -> Result[Todo, ErisError]:
        """Contructs a Todo object from a string (usually a line in a file).

        Args:
            line: The line to use to construct our new Todo object.
        """
        line = line.strip()

        re_todo_match = re.match(RE_TODO, line, re.VERBOSE)
        if re_todo_match is None:
            return Err(
                f"The provided string ({line!r}) does not appear to properly"
                " adhere to the todo.txt format. See"
                " https://github.com/todotxt/todo.txt for the specification."
            )

        done: bool = False
        if re_todo_match.group("x"):
            done = True

        priority: Priority = DEFAULT_PRIORITY
        if grp := re_todo_match.group("priority"):
            priority = cast(Priority, grp)

        create_date: Optional[dt.date] = None
        if grp := re_todo_match.group("create_date"):
            create_date = to_date(grp)

        done_date: Optional[dt.date] = None
        if grp := re_todo_match.group("done_date"):
            done_date = to_date(grp)

        desc = re_todo_match.group("desc")
        all_words = desc.split(" ")

        project_list: List[str] = []
        context_list: List[str] = []
        epics_list: List[str] = []
        for some_list, prefix in [
            (project_list, PROJECT_PREFIX),
            (context_list, CONTEXT_PREFIX),
            (epics_list, EPIC_PREFIX),
        ]:
            for word in all_words:
                if is_prefix_tag(prefix, word):
                    value = word[len(prefix) :]
                    value = _clean_value(value)
                    if value not in some_list:
                        some_list.append(value)

        projects = tuple(project_list)
        contexts = tuple(context_list)
        epics = tuple(epics_list)

        metadata: Metadata = {}
        for word in all_words:
            if is_metadata_tag(word):
                kv = word.split(":", maxsplit=1)
                key, value = kv
                value = _clean_value(value)

                if key in metadata:
                    continue

                metadata[key] = value

        todo = cls(
            contexts=contexts,
            create_date=create_date,
            desc=desc,
            done_date=done_date,
            done=done,
            epics=epics,
            metadata=metadata,
            priority=priority,
            projects=projects,
        )
        return Ok(todo)

    def to_line(self) -> str:
        """Converts this Todo object back to a line."""
        result = ""
        if self.done:
            result += "x "

        if self.priority != DEFAULT_PRIORITY:
            result += f"({self.priority}) "

        if self.done_date is not None:
            result += from_date(self.done_date) + " "

        if self.create_date is not None:
            result += from_date(self.create_date) + " "

        result += self.desc

        return result

    def new(self, **kwargs: Any) -> Todo:
        """Creates a new Todo using the current Todo's attrs as defaults."""
        contexts = kwargs.get("contexts", self.contexts)
        create_date = kwargs.get("create_date", self.create_date)
        desc = kwargs.get("desc", self.desc)
        done_date = kwargs.get("done_date", self.done_date)
        done = kwargs.get("done", self.done)
        epics = kwargs.get("epics", self.epics)
        metadata = kwargs.get("metadata", self.metadata)
        priority: Priority = kwargs.get("priority", self.priority)
        projects = kwargs.get("projects", self.projects)
        return Todo(
            contexts=contexts,
            create_date=create_date,
            desc=desc,
            done_date=done_date,
            done=done,
            epics=epics,
            metadata=metadata,
            priority=priority,
            projects=projects,
        )


def _clean_value(word: str) -> str:
    """Cleanup context, metadata, or project value.

    Makes the following changes to `word`:

      - Strips any punctuation from the right-side of `word`.
      - Removes any possesive apostrophe at the end of `word`.

    NOTE: Will not strip punctuation if `word` is composed ONLY of punctuation
      characters.
    """
    result = word.rstrip(PUNCTUATION)
    if not result:
        result = word

    result = result.split("'", maxsplit=1)[0]
    return result
