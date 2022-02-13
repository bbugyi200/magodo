"""Contains all of magodo's default MagicTodo spell functions."""

from __future__ import annotations

import datetime as dt
from typing import Callable, Final, Iterable, List, MutableSequence

from eris import ErisResult, Err, Ok

from ._common import (
    CONTEXT_PREFIX,
    PROJECT_PREFIX,
    PUNCTUATION,
    is_any_prefix_tag,
    is_any_tag,
    is_metadata_tag,
    todo_prefixes,
)
from .types import LineSpell, T, TodoSpell, ValidateSpell


def register_todo_spell_factory(
    mut_spell_registry: MutableSequence[TodoSpell],
) -> Callable[[TodoSpell], TodoSpell]:
    """Factory for decorators used to register spell functions."""

    def register_spell(spell: TodoSpell) -> TodoSpell:
        mut_spell_registry.append(spell)
        return spell

    return register_spell


def register_line_spell_factory(
    mut_spell_registry: MutableSequence[LineSpell],
) -> Callable[[LineSpell], LineSpell]:
    """Factory for decorators used to register spell functions."""

    def register_spell(spell: LineSpell) -> LineSpell:
        mut_spell_registry.append(spell)
        return spell

    return register_spell


def register_validate_spell_factory(
    mut_spell_registry: MutableSequence[ValidateSpell],
) -> Callable[[ValidateSpell], ValidateSpell]:
    """Factory for decorators used to register spell functions."""

    def register_spell(spell: ValidateSpell) -> ValidateSpell:
        mut_spell_registry.append(spell)
        return spell

    return register_spell


DEFAULT_TODO_SPELLS: List[TodoSpell] = []
todo_spell = register_todo_spell_factory(DEFAULT_TODO_SPELLS)

DEFAULT_PRE_TODO_SPELLS: List[TodoSpell] = []
pre_todo_spell = register_todo_spell_factory(DEFAULT_PRE_TODO_SPELLS)

DEFAULT_POST_TODO_SPELLS: List[TodoSpell] = []
post_todo_spell = register_todo_spell_factory(DEFAULT_POST_TODO_SPELLS)

DEFAULT_TO_LINE_SPELLS: List[LineSpell] = []
to_line_spell = register_line_spell_factory(DEFAULT_TO_LINE_SPELLS)

DEFAULT_FROM_LINE_SPELLS: List[LineSpell] = []
from_line_spell = register_line_spell_factory(DEFAULT_FROM_LINE_SPELLS)

DEFAULT_VALIDATE_SPELLS: List[ValidateSpell] = []
validate_spell = register_validate_spell_factory(DEFAULT_VALIDATE_SPELLS)

O_PREFIX: Final = "o "


@validate_spell
def validate_prefix(line: str) -> ErisResult[None]:
    """Handles / validatees a magic todo's prefix.."""
    if not line.startswith(tuple(todo_prefixes())):
        return Err(
            "Magic todos must satisfy one of; (1) Have a non-default"
            " (i.e. not 'O') priority set (2) Have been marked complete"
            " with an 'x' prefix (3) Have been marked open with an 'o'"
            f" prefix. line={line!r}"
        )

    return Ok(None)


@todo_spell
def x_tag(todo: T) -> T:
    """Handles tags of the form x:1234 where 1234 is the current time."""
    if todo.metadata is None or "x" not in todo.metadata:
        return todo

    if not todo.desc.startswith("x:"):
        return todo

    dtime = todo.metadata["x"]
    if len(dtime) != 4:
        return todo

    desc = " ".join(todo.desc.split(" ")[1:]) + f" dtime:{dtime}"

    new_todo = todo.new(desc=desc, done=True)
    line = new_todo.to_line()
    return type(todo).from_line(line).unwrap()


@post_todo_spell
def group_tags(todo: T) -> T:
    """Groups all @ctxs, +projs, and meta:data at the end of the line."""
    if not (todo.contexts or todo.projects or todo.metadata):
        return todo

    def all_words_are_tags(words: Iterable[str]) -> bool:
        """Returns True if all `words` are special words."""
        return all(is_any_tag(w) for w in words)

    all_words = [w for w in todo.desc.split(" ") if w != "|"]
    regular_words: list[str] = []
    for i, word in enumerate(all_words[:]):
        if not word:
            continue

        all_prev_words_are_tags = all_words_are_tags(all_words[:i])
        all_next_words_are_tags = all_words_are_tags(all_words[i + 1 :])
        is_edge_tag = all_next_words_are_tags or all_prev_words_are_tags

        if is_metadata_tag(word) and word[-1] in PUNCTUATION:
            return todo

        if is_any_prefix_tag(word) and (
            word[-1] in PUNCTUATION or not all_next_words_are_tags
        ):
            if regular_words:
                regular_words.append(word[1:])
            continue

        if is_any_prefix_tag(word) and is_edge_tag:
            continue

        if is_metadata_tag(word):
            continue

        regular_words.append(word)

    desc = " ".join(regular_words).strip()
    first_space = ""
    if regular_words:
        first_space = " "
        desc += " |"

    if todo.contexts:
        desc += first_space + " ".join(
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

    return todo.new(desc=desc)


@todo_spell
def add_create_date(todo: T) -> T:
    """Adds today's date as the create date for this Todo."""
    if todo.create_date is not None:
        return todo

    today = dt.date.today()
    return todo.new(create_date=today)


@todo_spell
def add_done_date(todo: T) -> T:
    """Adds today's date as the done date for this Todo (if done)."""
    if todo.done_date is not None:
        return todo

    if not todo.done:
        return todo

    today = dt.date.today()
    return todo.new(done_date=today)


@todo_spell
def add_ctime(todo: T) -> T:
    """Adds creation time to T via the 'ctime' metadata tag."""
    if "ctime" in todo.metadata:
        return todo

    now = dt.datetime.now()

    metadata = dict(todo.metadata)
    metadata["ctime"] = f"{now.hour:0>2}{now.minute:0>2}"

    return todo.new(metadata=metadata)


@to_line_spell
def add_o_prefix(line: str) -> str:
    """Adds the 'o ' prefix to the Todo line."""
    if line.startswith(todo_prefixes()):
        return line

    return O_PREFIX + line


@from_line_spell
def remove_o_prefix(line: str) -> str:
    """Removes the 'o ' prefix from the Todo line."""
    if not line.startswith(O_PREFIX):
        return line

    return line[len(O_PREFIX) :]


@to_line_spell
def add_x_prefix(line: str) -> str:
    """Adds the 'x:HHMM ' prefix to the Todo line (when done)."""
    if not line.startswith("x "):
        return line

    words = line.split(" ")[1:]
    for i, word in enumerate(words[:]):
        if word.startswith("dtime:"):
            del words[i]
            dtime = word.split(":")[1]
            break
    else:
        now = dt.datetime.now()
        dtime = f"{now.hour:0>2}{now.minute:0>2}"

    rest = " ".join(words)
    return f"x:{dtime} {rest}"


@from_line_spell
def remove_x_prefix(line: str) -> str:
    """Removes the 'x:HHMM ' prefix from the Todo line."""
    if not line.startswith("x:"):
        return line

    xhhmm, *words = line.split(" ")
    dtime = xhhmm.split(":")[1]
    if len(dtime) != 4:
        return line

    rest = " ".join(words)
    return f"x {rest} dtime:{dtime}"
