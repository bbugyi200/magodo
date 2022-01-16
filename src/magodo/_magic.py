"""Contains the MagicTodoMixin class definition."""

from __future__ import annotations

import abc
import datetime as dt
from functools import total_ordering
from typing import Any, Dict, Generic, List, Tuple, Type

from eris import ErisError, Err, Ok, Result

from . import types as mtypes
from ._todo import Todo, TodoMixin
from .spells import POST_BUILTIN_SPELLS, PRE_BUILTIN_SPELLS


@total_ordering
class MagicTodoMixin(TodoMixin, Generic[mtypes.MagicTodo_T], abc.ABC):
    """Mixin class that implements the Todo protocol."""

    pre_spells: List[mtypes.TodoSpell] = []
    post_spells: List[mtypes.TodoSpell] = []

    def __init__(self: mtypes.MagicTodo_T, todo: Todo):
        self._todo = todo
        self.todo = self.cast_spells(todo).unwrap()

    @classmethod
    def from_line(
        cls: Type[mtypes.MagicTodo_T], line: str
    ) -> Result[mtypes.MagicTodo_T, ErisError]:
        """Converts a string into a MagicTodo object."""
        todo_result = Todo.from_line(line)

        err: Err[Any, ErisError]
        if isinstance(todo_result, Err):
            err = Err(
                "Failed to construct basic Todo object inside of MagicTodo."
            )
            return err.chain(todo_result)

        todo = todo_result.ok()
        if error := cls.cast_spells(todo).err():
            err = Err(f"Failed spell validation for this todo: todo={todo!r}")
            return err.chain(error)

        return Ok(cls(todo))

    def to_line(self) -> str:
        """Converts this MagicTodo back to a string."""
        return self.todo.to_line()

    def to_dict(self: mtypes.MagicTodo_T) -> dict[str, Any]:
        """Converts this MagicTodo into a dictionary."""
        result: Dict[str, Any] = {}
        result["_todo"] = self.todo.to_dict()
        result["todo"] = self.todo.to_dict()
        result["pre_spells"] = [spell.__name__ for spell in self.pre_spells]
        result["spells"] = [spell.__name__ for spell in self.spells]
        result["post_spells"] = [spell.__name__ for spell in self.post_spells]
        return result

    @classmethod
    def cast_spells(
        cls: Type[mtypes.MagicTodo_T], todo: Todo
    ) -> Result[Todo, ErisError]:
        """Casts all spells associated with this MagicTodo on `todo`."""
        new_todo = todo.new()
        for spell_list in [cls.pre_spells, cls.spells, cls.post_spells]:
            for spell in spell_list:
                new_todo_result = spell(new_todo)
                if isinstance(new_todo_result, Err):
                    err: Err[Any, ErisError] = Err(
                        f"The {spell.__name__!r} spell failed while processing"
                        " this todo."
                    )
                    return err.chain(new_todo_result)

                new_todo = new_todo_result.ok()

        return Ok(new_todo)

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
    def metadata(self) -> mtypes.Metadata:  # noqa: D102
        return self.todo.metadata

    @property
    def priority(self) -> mtypes.Priority:  # noqa: D102
        return self.todo.priority

    @property
    def projects(self) -> Tuple[str, ...]:  # noqa: D102
        return self.todo.projects


class MagicTodo(MagicTodoMixin):
    """The default MagicTodo class."""

    pre_spells: List[mtypes.TodoSpell] = PRE_BUILTIN_SPELLS
    spells: List[mtypes.TodoSpell] = []
    post_spells: List[mtypes.TodoSpell] = POST_BUILTIN_SPELLS
