"""Contains the Todo class definition."""

# pylint: disable=format-string-without-interpolation

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import re
from typing import Final, List, Optional, Tuple, cast

from eris import ErisError, Err, Ok, Result

from ._dates import RE_DATE, to_date
from .types import Metadata, Priority


re_todo_fmt = r"""
(?P<x>x[ ]+)?                        # optional 'x'
{{0}}                                # priority
(?:
    (?:(?P<done_date>{0})[ ]+)?      # optional date of completion
    (?:(?P<create_date>{0})[ ]+)     # optional date of creation
)?
(?P<desc>[A-Za-z0-9+@].*)            # description
""".format(
    RE_DATE
).format
re_opt_fmt = r"(?:{})?".format

CONTEXT_PREFIX: Final = "@"
DEFAULT_PRIORITY: Final[Priority] = "N"
PROJECT_PREFIX: Final = "+"
PUNCTUATION: Final = ",.?!;"
RE_PRIORITY: Final = r"\((?P<priority>[A-Z])\)[ ]+"
RE_OPTIONAL_PRIORITY: Final = re_opt_fmt(RE_PRIORITY)


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
    def from_line(
        cls, line: str, *, strict: bool = False
    ) -> Result[Todo, ErisError]:
        """Contructs a Todo object from a string (usually a line in a file).

        Args:
            line: The line to use to construct our new Todo object.
            strict: If this option is set, require that valid todo lines
              either explicitly specify a priority OR have been marked done /
              not done with an "x " or "o " at the start of the line,
              respectively. NOTE: The special "o " prefix is treated as
              short-hand for the next letter after the default priority letter
              and is ONLY allowed when this option is set.
        """
        line = line.strip()

        if (
            strict
            and line
            and line.startswith("x:")
            and line[2:6].isnumeric()
            and line[6].isspace()
        ):
            xword, *rest = line.split(" ")
            dtime = xword[2:]
            new_line_words = ["x"] + rest + ["dtime:" + dtime]
            line = " ".join(new_line_words)

        if strict and line.startswith("o "):
            o_priority = (
                DEFAULT_PRIORITY
                if DEFAULT_PRIORITY == "Z"
                else chr(ord(DEFAULT_PRIORITY) + 1)
            )
            line = f"({o_priority})" + line[1:]

        if strict and not line.startswith("x "):
            RE_TODO = re_todo_fmt(RE_PRIORITY)
        else:
            RE_TODO = re_todo_fmt(RE_OPTIONAL_PRIORITY)

        re_todo_match = re.match(RE_TODO, line, re.VERBOSE)
        if re_todo_match is None:
            return Err(
                f"The provided string ({line!r}) does not appear to properly"
                " adhere to the todo.txt format. See"
                " https://github.com/todotxt/todo.txt for the specification. "
                f" |  require_priority={strict}"
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
