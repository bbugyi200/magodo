"""Datetime utilities used throughout this library."""

from __future__ import annotations

import datetime as dt
from typing import Final


DATE_FMT: Final = "%Y-%m-%d"
RE_DATE: Final = r"[1-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]"


def to_date(yyyymmdd: str) -> dt.date:
    """Helper function for constructing a date object."""
    return dt.datetime.strptime(yyyymmdd, DATE_FMT).date()
