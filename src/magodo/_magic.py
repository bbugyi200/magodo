"""Contains the MagicTodoMixin class definition."""

from __future__ import annotations

import abc
import datetime as dt
from functools import total_ordering
import itertools as it
from typing import Any, Iterable, List, Tuple, Type, TypeVar

from eris import ErisError, Err, Ok, Result

from magodo.types import T

from ._todo import Todo, TodoMixin
from .types import EnchantedTodo, LineSpell, Metadata, Priority, TodoSpell


M = TypeVar("M", bound="MagicTodoMixin")


@total_ordering
class MagicTodoMixin(TodoMixin, abc.ABC):
    """Mixin class that implements the Todo protocol."""

    pre_todo_spells: List[TodoSpell] = []
    todo_spells: List[TodoSpell] = []
    post_todo_spells: List[TodoSpell] = []

    to_line_spells: List[LineSpell] = []
    from_line_spells: List[LineSpell] = []

    def __init__(self: M, todo: Todo):
        self._todo = todo
        self.etodo = self.cast_todo_spells(todo)

    @classmethod
    def from_line(cls: Type[M], line: str) -> Result[M, ErisError]:
        """Converts a string into a MagicTodo object."""
        line = cls.cast_from_line_spells(line)
        todo_result = Todo.from_line(line)
        if isinstance(todo_result, Err):
            err: Err[Any, ErisError] = Err(
                "Failed to construct basic Todo object inside of MagicTodo."
            )
            return err.chain(todo_result)

        todo = todo_result.ok()

        return Ok(cls(todo))

    def to_line(self: M) -> str:
        """Converts this MagicTodo back to a string."""
        line = self.etodo.todo.to_line()
        line = self.cast_to_line_spells(line)
        return line

    @classmethod
    def cast_todo_spells(cls: Type[M], todo: T) -> EnchantedTodo[T]:
        """Casts all spells associated with this MagicTodo on `todo`."""
        new_todo = EnchantedTodo(todo.new())
        todo_spell_chain: Iterable[TodoSpell] = it.chain(
            cls.pre_todo_spells, cls.todo_spells, cls.post_todo_spells
        )
        for todo_spell in todo_spell_chain:
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

    def new(self: M, **kwargs: Any) -> M:
        """Creates a new Todo using the current Todo's attrs as defaults."""
        return type(self)(self.etodo.todo.new(**kwargs))

    @property
    def contexts(self: M) -> Tuple[str, ...]:  # noqa: D102
        return self.etodo.todo.contexts

    @property
    def create_date(self: M) -> dt.date:  # noqa: D102
        return self.etodo.todo.create_date

    @property
    def desc(self: M) -> str:  # noqa: D102
        return self.etodo.todo.desc

    @property
    def done_date(self: M) -> dt.date | None:  # noqa: D102
        return self.etodo.todo.done_date

    @property
    def done(self: M) -> bool:  # noqa: D102
        return self.etodo.todo.done

    @property
    def epics(self: M) -> Tuple[str, ...]:  # noqa: D102
        return self.etodo.todo.epics

    @property
    def metadata(self: M) -> Metadata:  # noqa: D102
        return self.etodo.todo.metadata

    @property
    def priority(self: M) -> Priority:  # noqa: D102
        return self.etodo.todo.priority

    @property
    def projects(self: M) -> Tuple[str, ...]:  # noqa: D102
        return self.etodo.todo.projects
