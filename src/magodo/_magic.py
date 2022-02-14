"""Contains the MagicTodoMixin class definition."""

from __future__ import annotations

import abc
import datetime as dt
from functools import total_ordering
import itertools as it
from typing import Any, List, Tuple, Type, TypeVar

from eris import ErisError, Err, Ok, Result

from ._todo import Todo, TodoMixin
from .types import LineSpell, Metadata, Priority, TodoSpell, ValidateSpell


M = TypeVar("M", bound="MagicTodoMixin")


@total_ordering
class MagicTodoMixin(TodoMixin, abc.ABC):
    """Mixin class that implements the Todo protocol."""

    pre_todo_spells: List[TodoSpell] = []
    todo_spells: List[TodoSpell] = []
    post_todo_spells: List[TodoSpell] = []

    to_line_spells: List[LineSpell] = []
    from_line_spells: List[LineSpell] = []

    validate_spells: List[ValidateSpell] = []

    def __init__(self: M, todo: Todo):
        self._todo = todo
        self.todo = self.cast_todo_spells(todo)

    @classmethod
    def from_line(cls: Type[M], line: str) -> Result[M, ErisError]:
        """Converts a string into a MagicTodo object."""
        err: Err[Any, ErisError]
        if error := cls.cast_validate_spells(line).err():
            err = Err(f"Failed spell validation for this todo: line={line!r}")
            return err.chain(error)

        line = cls.cast_from_line_spells(line)
        todo_result = Todo.from_line(line)

        if isinstance(todo_result, Err):
            err = Err(
                "Failed to construct basic Todo object inside of MagicTodo."
            )
            return err.chain(todo_result)

        todo = todo_result.ok()

        return Ok(cls(todo))

    def to_line(self: M) -> str:
        """Converts this MagicTodo back to a string."""
        line = self.todo.to_line()
        line = self.cast_to_line_spells(line)
        return line

    @classmethod
    def cast_todo_spells(cls: Type[M], todo: Todo) -> Todo:
        """Casts all spells associated with this MagicTodo on `todo`."""
        new_todo = todo.new()
        for todo_spell in it.chain(
            cls.pre_todo_spells, cls.todo_spells, cls.post_todo_spells
        ):
            new_todo = todo_spell(new_todo)

        return new_todo

    @classmethod
    def cast_from_line_spells(cls: Type[M], line: str) -> str:
        """Casts all from_line spells on `line`."""
        for line_spell in cls.from_line_spells:
            line = line_spell(line)
        return line

    def cast_to_line_spells(self: M, line: str) -> str:
        """Casts all to_line spells on `line`."""
        for line_spell in self.to_line_spells:
            line = line_spell(line)
        return line

    @classmethod
    def cast_validate_spells(
        cls: Type[M], line: str
    ) -> Result[None, ErisError]:
        """Casts all spells associated with this MagicTodo on `todo`."""
        for validate_spell in cls.validate_spells:
            new_todo_result = validate_spell(line)
            if isinstance(new_todo_result, Err):
                err: Err[Any, ErisError] = Err(
                    f"The {validate_spell.__name__!r} validation spell failed"
                    " while attempting to validate this line."
                )
                return err.chain(new_todo_result)

        return Ok(None)

    def new(self: M, **kwargs: Any) -> M:
        """Creates a new Todo using the current Todo's attrs as defaults."""
        return type(self)(self.todo.new(**kwargs))

    @property
    def contexts(self: M) -> Tuple[str, ...]:  # noqa: D102
        return self.todo.contexts

    @property
    def create_date(self: M) -> dt.date | None:  # noqa: D102
        return self.todo.create_date

    @property
    def desc(self: M) -> str:  # noqa: D102
        return self.todo.desc

    @property
    def done_date(self: M) -> dt.date | None:  # noqa: D102
        return self.todo.done_date

    @property
    def done(self: M) -> bool:  # noqa: D102
        return self.todo.done

    @property
    def metadata(self: M) -> Metadata:  # noqa: D102
        return self.todo.metadata

    @property
    def priority(self: M) -> Priority:  # noqa: D102
        return self.todo.priority

    @property
    def projects(self: M) -> Tuple[str, ...]:  # noqa: D102
        return self.todo.projects
