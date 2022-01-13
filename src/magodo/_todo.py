"""Contains the basic / standard Todo class definition."""

# pylint: disable=format-string-without-interpolation

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import re
from typing import Any, Final, List, Optional, Tuple, cast

from eris import ErisError, Err, Ok, Result

from ._dates import RE_DATE, from_date, to_date
from .types import Metadata, Priority


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

CONTEXT_PREFIX: Final = "@"
DEFAULT_PRIORITY: Final[Priority] = "O"
PROJECT_PREFIX: Final = "+"
PUNCTUATION: Final = ",.?!;"


@dataclass(frozen=True)
class Todo:
    """Represents a single task in a todo list."""

    desc: str

    contexts: Tuple[str, ...] = ()
    create_date: Optional[dt.date] = None
    done_date: Optional[dt.date] = None
    marked_done: bool = False
    metadata: Optional[Metadata] = None
    priority: Priority = DEFAULT_PRIORITY
    projects: Tuple[str, ...] = ()

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

        marked_done: bool = False
        if re_todo_match.group("x"):
            marked_done = True

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
        for some_list, prefix in [
            (project_list, PROJECT_PREFIX),
            (context_list, CONTEXT_PREFIX),
        ]:
            for word in all_words:
                if (
                    word.startswith(prefix)
                    and not word.startswith(prefix + prefix)
                    and len(prefix) < len(word)
                ):
                    value = word[len(prefix) :]
                    value = _clean_value(value)
                    some_list.append(value)

        projects = tuple(project_list)
        contexts = tuple(context_list)

        metadata: Optional[Metadata] = None
        mdata: Metadata = {}
        for word in all_words:
            kv = word.split(":", maxsplit=1)
            if len(kv) == 2 and kv[1] and not kv[1].startswith(":"):
                key, value = kv
                value = _clean_value(value)

                if key in mdata:
                    value_list = mdata[key]
                    if not isinstance(value_list, list):
                        value_list = [value_list]
                        mdata[key] = value_list

                    value_list.append(value)
                else:
                    mdata[key] = value

        if mdata:
            metadata = mdata

        todo = cls(
            contexts=contexts,
            create_date=create_date,
            desc=desc,
            done_date=done_date,
            marked_done=marked_done,
            metadata=metadata,
            priority=priority,
            projects=projects,
        )
        return Ok(todo)

    def to_line(self) -> str:
        """Converts this Todo object back to a line."""
        result = ""
        if self.marked_done:
            result += "x "

        if self.priority != DEFAULT_PRIORITY:
            result += f"({self.priority})"

        if self.done_date is not None:
            result += from_date(self.done_date) + " "

        if self.create_date is not None:
            result += from_date(self.create_date) + " "

        result += self.desc

        return result

    def to_dict(self) -> dict[str, Any]:
        """Converts this Todo into a dictionary."""
        return self.__dict__

    def new(self, **kwargs: Any) -> Todo:
        """Creates a new Todo using the current Todo's attrs as defaults."""
        contexts = kwargs.get("contexts", self.contexts)
        create_date = kwargs.get("create_date", self.create_date)
        desc = kwargs.get("desc", self.desc)
        done_date = kwargs.get("done_date", self.done_date)
        marked_done = kwargs.get("marked_done", self.marked_done)
        metadata = kwargs.get("metadata", self.metadata)
        priority: Priority = kwargs.get("priority", self.priority)
        projects = kwargs.get("projects", self.projects)
        return Todo(
            contexts=contexts,
            create_date=create_date,
            desc=desc,
            done_date=done_date,
            marked_done=marked_done,
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
