"""Contains the MagicTodoMixin class definition."""

from __future__ import annotations

import abc
import datetime as dt
from functools import total_ordering
from typing import Any, List, Tuple, Type

from eris import ErisError, Err, Ok, Result

from ._todo import Todo, TodoMixin
from .spells import POST_BUILTIN_SPELLS, PRE_BUILTIN_SPELLS
from .types import AbstractMagicTodo, LineSpell, Metadata, Priority, TodoSpell


@total_ordering
class MagicTodoMixin(TodoMixin, abc.ABC):
    """Mixin class that implements the Todo protocol."""

    to_line_spells: List[LineSpell] = []
    todo_spells: List[TodoSpell] = []
    from_line_spells: List[LineSpell] = []

    def __init__(self: AbstractMagicTodo, todo: Todo):
        self._todo = todo
        self.todo = self.cast_todo_spells(todo).unwrap()

    @classmethod
    def from_line(
        cls: Type[AbstractMagicTodo], line: str
    ) -> Result[AbstractMagicTodo, ErisError]:
        """Converts a string into a MagicTodo object."""
        for line_spell in cls.from_line_spells:
            line = line_spell(line)

        todo_result = Todo.from_line(line)

        err: Err[Any, ErisError]
        if isinstance(todo_result, Err):
            err = Err(
                "Failed to construct basic Todo object inside of MagicTodo."
            )
            return err.chain(todo_result)

        todo = todo_result.ok()
        if error := cls.cast_todo_spells(todo).err():
            err = Err(f"Failed spell validation for this todo: todo={todo!r}")
            return err.chain(error)

        return Ok(cls(todo))

    def to_line(self) -> str:
        """Converts this MagicTodo back to a string."""
        line = self.todo.to_line()

        for line_spell in self.to_line_spells:
            line = line_spell(line)

        return line

    @classmethod
    def cast_todo_spells(
        cls: Type[AbstractMagicTodo], todo: Todo
    ) -> Result[Todo, ErisError]:
        """Casts all spells associated with this MagicTodo on `todo`."""
        new_todo = todo.new()
        for todo_spell in cls.todo_spells:
            new_todo_result = todo_spell(new_todo)
            if isinstance(new_todo_result, Err):
                err: Err[Any, ErisError] = Err(
                    f"The {todo_spell.__name__!r} spell failed while"
                    " processing this todo."
                )
                return err.chain(new_todo_result)

            new_todo = new_todo_result.ok()

        return Ok(new_todo)

    def new(self, **kwargs: Any) -> Todo:
        """Creates a new Todo using the current Todo's attrs as defaults."""

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
    def done(self) -> bool:  # noqa: D102
        return self.todo.done

    @property
    def metadata(self) -> Metadata:  # noqa: D102
        return self.todo.metadata

    @property
    def priority(self) -> Priority:  # noqa: D102
        return self.todo.priority

    @property
    def projects(self) -> Tuple[str, ...]:  # noqa: D102
        return self.todo.projects


class MagicTodo(MagicTodoMixin):
    """The default MagicTodo class."""

    todo_spells: List[TodoSpell] = (
        PRE_BUILTIN_SPELLS + [] + POST_BUILTIN_SPELLS
    )
