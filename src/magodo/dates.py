"""Utilities for working with dates in magodo."""

from __future__ import annotations

import datetime as dt
from typing import Final


DATE_FMT: Final = "%Y-%m-%d"


def to_date(yyyymmdd: str) -> dt.date:
    """Helper function for constructing a date object."""
    return dt.datetime.strptime(yyyymmdd, DATE_FMT).date()


def from_date(date: dt.date) -> str:
    """Helper function for converting a date object to a string."""
    return date.strftime(DATE_FMT)
