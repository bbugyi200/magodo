"""Contains the MagicTodoMixin class definition."""

from __future__ import annotations

import abc
import datetime as dt
from typing import Any, Generic, List, Optional, Tuple, Type

from eris import ErisError, Err, Ok, Result
from metaman import cname

from . import types as mtypes
from ._todo import DEFAULT_PRIORITY, Todo
from .spells import POST_BUILTIN_SPELLS, PRE_BUILTIN_SPELLS


TODO_PREFIXES = ("x ", "x:", "o ")


class MagicTodoMixin(Generic[mtypes.MagicTodo_T], abc.ABC):
    """Mixin class that implements the Todo protocol."""

    pre_spells: List[mtypes.TodoSpell] = PRE_BUILTIN_SPELLS
    post_spells: List[mtypes.TodoSpell] = POST_BUILTIN_SPELLS

    def __init__(self: mtypes.MagicTodo_T, todo: Todo):
        self.todo = todo

        etodo = todo.new()
        for spell_list in [self.pre_spells, self.spells, self.post_spells]:
            for spell in spell_list:
                etodo = spell(etodo)

        self.enchanted_todo = etodo

    def __repr__(self) -> str:  # noqa: D105
        result = ""
        result += cname(self)
        result += "(\n    TODO:           "
        result += repr(self.todo) + "\n"
        result += "    ENCHANTED TODO: "
        result += repr(self.enchanted_todo) + "\n"
        result += ")"
        return result

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, type(self)):
            return False

        if self.todo != other.todo:
            return False

        if self.enchanted_todo != other.enchanted_todo:
            return False

        return True

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

        return Ok(cls(todo))

    def to_line(self) -> str:
        """Converts this MagicTodo back to a string."""
        return self.enchanted_todo.to_line()

    def to_dict(self) -> dict[str, Any]:
        """Converts this MagicTodo into a dictionary."""
        result = {}
        result["todo"] = self.todo.to_dict()
        result["enchanted_todo"] = self.enchanted_todo.to_dict()
        return result

    @property
    def contexts(self) -> Tuple[str, ...]:  # noqa: D102
        return self.todo.contexts

    @property
    def create_date(self) -> dt.date | None:  # noqa: D102
        return self.todo.create_date

    @property
    def desc(self) -> str:  # noqa: D102
        return self.todo.desc

    @property
    def done_date(self) -> dt.date | None:  # noqa: D102
        return self.todo.done_date

    @property
    def marked_done(self) -> bool:  # noqa: D102
        return self.todo.marked_done

    @property
    def metadata(self) -> Optional[mtypes.Metadata]:  # noqa: D102
        return self.todo.metadata

    @property
    def priority(self) -> mtypes.Priority:  # noqa: D102
        return self.todo.priority

    @property
    def projects(self) -> Tuple[str, ...]:  # noqa: D102
        return self.todo.projects


class MagicTodo(MagicTodoMixin):
    """The default MagicTodo class."""

    spells: List[mtypes.TodoSpell] = []
