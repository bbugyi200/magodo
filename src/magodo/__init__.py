"""magodo package

A Python library for working with the todo.txt format, with some magic thrown
in.
"""

import logging as _logging

from ._core import dummy


__all__ = ["dummy"]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.4.0"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
