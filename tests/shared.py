"""Shared test utilities."""

from typing import List

from magodo import MagicTodoMixin
from magodo.spells import DEFAULT_TODO_SPELLS
from magodo.types import TodoSpell


class MagicTodo(MagicTodoMixin):
    """The default MagicTodo class."""

    todo_spells: List[TodoSpell] = DEFAULT_TODO_SPELLS
