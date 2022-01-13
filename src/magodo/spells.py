"""Contains all of magodo's default Todo spell functions."""

from __future__ import annotations

from typing import Callable, List, MutableSequence

from ._todo import Todo
from .types import TodoSpell


def register_spell_factory(
    mut_spell_registry: MutableSequence[TodoSpell],
) -> Callable[[TodoSpell], TodoSpell]:
    """Factory for decorators used to register spell functions."""

    def register_spell(spell: TodoSpell) -> TodoSpell:
        mut_spell_registry.append(spell)
        return spell

    return register_spell


PRE_BUILTIN_SPELLS: List[TodoSpell] = []
pre_spell = register_spell_factory(PRE_BUILTIN_SPELLS)

POST_BUILTIN_SPELLS: List[TodoSpell] = []
post_spell = register_spell_factory(POST_BUILTIN_SPELLS)


@pre_spell
def x_tag(todo: Todo) -> Todo:
    """Handles tags of the form x:1234 where 1234 is the current time."""
    if todo.metadata is None or "x" not in todo.metadata:
        return todo

    dtime = todo.metadata["x"]
    desc = " ".join(todo.desc.split(" ")[1:]) + f" dtime:{dtime}"

    new_todo = todo.new(desc=desc, marked_done=True)
    line = new_todo.to_line()
    return Todo.from_line(line).unwrap()
