"""Utilities related to tags (i.e. projects, epics, contexts, or metatags)."""

from __future__ import annotations

from typing import Final


CONTEXT_PREFIX: Final = "@"
EPIC_PREFIX: Final = "#"
PROJECT_PREFIX: Final = "+"


def is_metadata_tag(word: str) -> bool:
    """Predicate that tells us if `word` is a metadata tag or not."""
    kv = word.split(":", maxsplit=1)
    return bool(len(kv) == 2 and kv[1] and not kv[1].startswith(":"))


def is_prefix_tag(ch: str, word: str) -> bool:
    """Predicate that tells us if a word is prefixed by `ch`.

    Pre-Conditions:
        * `ch` is only a single character.
    """
    return len(word) > 1 and word[0] == ch and word[1] != ch


def is_context_tag(word: str) -> bool:
    """Returns True if `word` is a context tag."""
    return is_prefix_tag(CONTEXT_PREFIX, word)


def is_project_tag(word: str) -> bool:
    """Returns True if `word` is a project tag."""
    return is_prefix_tag(PROJECT_PREFIX, word)


def is_epic_tag(word: str) -> bool:
    """Returns True if `word` is an epic tag."""
    return is_prefix_tag(EPIC_PREFIX, word)


def is_any_prefix_tag(word: str) -> bool:
    """Returns True if `word` is either an epic, context, or project tag."""
    return is_epic_tag(word) or is_context_tag(word) or is_project_tag(word)


def is_any_tag(word: str) -> bool:
    """Returns True if `word` is a project, context, or metadata."""
    return is_any_prefix_tag(word) or is_metadata_tag(word)
