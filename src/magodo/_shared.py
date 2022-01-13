"""Shared utility functions / constants / classes."""

from __future__ import annotations

import datetime as dt
from typing import Final

from .types import Priority


CONTEXT_PREFIX: Final = "@"
DATE_FMT: Final = "%Y-%m-%d"
DEFAULT_PRIORITY: Final[Priority] = "O"
PROJECT_PREFIX: Final = "+"
PUNCTUATION: Final = ",.?!;"
RE_DATE: Final = r"[1-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]"


def to_date(yyyymmdd: str) -> dt.date:
    """Helper function for constructing a date object."""
    return dt.datetime.strptime(yyyymmdd, DATE_FMT).date()


def from_date(date: dt.date) -> str:
    """Helper function for converting a date object to a string."""
    return date.strftime(DATE_FMT)


def is_meta_data(word: str) -> bool:
    """Predicate that tells us if `word` is a metadata tag or not."""
    kv = word.split(":", maxsplit=1)
    return bool(len(kv) == 2 and kv[1] and not kv[1].startswith(":"))


def is_prefix_word(prefix: str, word: str) -> bool:
    """Predicate that tells us if a word is prefixed by `prefix`."""
    return (
        word.startswith(prefix)
        and not word.startswith(prefix + prefix)
        and len(prefix) < len(word)
    )
