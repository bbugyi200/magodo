"""Contains all of magodo's default MagicTodo spell functions."""

from __future__ import annotations

from typing import Callable, Iterable, List, MutableSequence

from eris import ErisError, Err, Ok, Result

from ._shared import (
    CONTEXT_PREFIX,
    DEFAULT_PRIORITY,
    PROJECT_PREFIX,
    PUNCTUATION,
    TODO_PREFIXES,
    is_any_prefix_tag,
    is_any_tag,
    is_metadata_tag,
)
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
def handle_prefix(todo: Todo) -> Result[Todo, ErisError]:
    """Handles / validatees a magic todo's prefix.."""
    if todo.priority == DEFAULT_PRIORITY and not todo.desc.startswith(
        TODO_PREFIXES
    ):
        return Err(
            "Magic todos must satisfy one of; (1) Have a non-default"
            " (i.e. not 'O') priority set (2) Have been marked complete"
            " with an 'x' prefix (3) Have been marked open with an 'o'"
            f" prefix. todo={todo!r}"
        )

    if todo.desc.startswith("o "):
        return Ok(todo.new(desc=todo.desc[2:]))

    return Ok(todo)


@pre_spell
def x_tag(todo: Todo) -> Result[Todo, ErisError]:
    """Handles tags of the form x:1234 where 1234 is the current time."""
    if todo.metadata is None or "x" not in todo.metadata:
        return Ok(todo)

    dtime = todo.metadata["x"]
    desc = " ".join(todo.desc.split(" ")[1:]) + f" dtime:{dtime}"

    new_todo = todo.new(desc=desc, marked_done=True)
    line = new_todo.to_line()
    return Todo.from_line(line)


@post_spell
def group_tags(todo: Todo) -> Result[Todo, ErisError]:
    """Groups all @ctxs, +projs, and meta:data at the end of the line."""
    if not (todo.contexts or todo.projects or todo.metadata):
        return Ok(todo)

    all_words = [w for w in todo.desc.split(" ") if w != "|"]
    new_words = []
    regular_words_found = False
    for i, word in enumerate(all_words[:]):
        all_prev_words_are_tags = _all_words_are_tags(all_words[:i])
        all_next_words_are_tags = _all_words_are_tags(all_words[i + 1 :])

        if is_metadata_tag(word) and not (
            all_prev_words_are_tags or all_next_words_are_tags
        ):
            return Ok(todo)

        if is_metadata_tag(word) and word[-1] in PUNCTUATION:
            return Ok(todo)

        if is_any_prefix_tag(word) and (
            word[-1] in PUNCTUATION or not all_next_words_are_tags
        ):
            if regular_words_found:
                new_words.append(word[1:])
            continue

        if is_any_tag(word) and all_next_words_are_tags:
            continue

        regular_words_found = True
        new_words.append(word)

    if not regular_words_found:
        return Ok(todo)

    desc = " ".join(new_words).strip()
    desc += " |"

    if todo.contexts:
        desc += " " + " ".join(
            CONTEXT_PREFIX + ctx for ctx in sorted(todo.contexts)
        )

    if todo.projects:
        desc += " " + " ".join(
            PROJECT_PREFIX + ctx for ctx in sorted(todo.projects)
        )

    if todo.metadata:
        desc += " " + " ".join(
            f"{k}:{v}" for (k, v) in sorted(todo.metadata.items())
        )

    return Ok(todo.new(desc=desc))


def _all_words_are_tags(words: Iterable[str]) -> bool:
    """Returns True if all `words` are special words."""
    return all(is_any_tag(w) for w in words)
