"""Contains the MagicTodoMixin class definition."""

from __future__ import annotations

import abc
import datetime as dt
from typing import Any, Generic, List, Optional, Tuple, Type

from eris import ErisError, Err, Ok, Result

from . import types as mtypes
from ._todo import DEFAULT_PRIORITY, Todo
from .spells import POST_BUILTIN_SPELLS, PRE_BUILTIN_SPELLS


TODO_PREFIXES = ("x", "o")


class MagicTodoMixin(Generic[mtypes.MagicTodo_T], abc.ABC):
    """Mixin class that implements the Todo protocol."""

    pre_spells: List[mtypes.TodoSpell] = PRE_BUILTIN_SPELLS
    post_spells: List[mtypes.TodoSpell] = POST_BUILTIN_SPELLS

    def __init__(self, todo: Todo):
        self.todo = todo

    def __repr__(self) -> str:
        return repr(self.todo)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.todo == other.todo
        else:
            return False

    @classmethod
    def from_line(
        cls: Type[mtypes.MagicTodo_T], line: str
    ) -> Result[mtypes.MagicTodo_T, ErisError]:
        """Converts a string into a MagicTodo object."""
        todo_result = Todo.from_line(line)
        if isinstance(todo_result, Err):
            err: Err[Any, ErisError] = Err(
                "Failed to construct basic Todo object inside of MagicTodo."
            )
            return err.chain(todo_result)

        todo = todo_result.ok()
        if todo.priority == DEFAULT_PRIORITY and not todo.desc.startswith(
            TODO_PREFIXES
        ):
            return Err(
                "Magic todos must satisfy one of; (1) Have a non-default"
                " (i.e. not 'O') priority set (2) Have been marked complete"
                " with an 'x' prefix (3) Have been marked open with an 'o'"
                f" prefix. todo={todo!r}"
            )

        for spell in cls.spells:
            todo = spell(todo)

        return Ok(cls(todo))

    def to_line(self) -> str:
        """Converts this MagicTodo back to a string."""
        return self.todo.to_line()

    @property
    def contexts(self) -> Tuple[str, ...]:
        return self.todo.contexts

    @property
    def create_date(self) -> dt.date | None:
        return self.todo.create_date

    @property
    def desc(self) -> str:
        return self.todo.desc

    @property
    def done_date(self) -> dt.date | None:
        return self.todo.done_date

    @property
    def marked_done(self) -> bool:
        return self.todo.marked_done

    @property
    def metadata(self) -> Optional[mtypes.Metadata]:
        return self.todo.metadata

    @property
    def priority(self) -> mtypes.Priority:
        return self.todo.priority

    @property
    def projects(self) -> Tuple[str, ...]:
        return self.todo.projects


class MagicTodo(MagicTodoMixin):
    """The default MagicTodo class."""

    spells: List[mtypes.TodoSpell] = []