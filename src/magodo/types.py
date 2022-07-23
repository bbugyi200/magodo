"""Custom types used by this library."""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Literal,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    runtime_checkable,
)

from eris import ErisError, Result
from typist import Comparable


# Type of the Todo.metadata attribute.
Metadata = Dict[str, str]
# A todo item's priority is always a capital letter.
Priority = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

# Type of a spell function which transforms a line (i.e. a str).
LineSpell = Callable[[str], str]

# Type Variables (i.e. `TypeVar`s)
T = TypeVar("T", bound="TodoProto")


@runtime_checkable
class TodoProto(Comparable, Protocol, Generic[T]):
    """Describes how any valid Todo object should look."""

    def __init__(self, **kwargs: Any) -> None:
        """DOCSTRING."""

    @property
    def ident(self) -> str:
        """A unique identifier for this Todo."""

    @classmethod
    def from_line(cls: Type[T], line: str) -> Result[T, ErisError]:
        """Constructs a new Todo object from a string."""

    def to_line(self) -> str:
        """Converts a Todo object back to a string."""

    def new(self: T, **kwargs: Any) -> T:
        """Creates a new Todo using the current Todo's attrs as defaults."""

    @property
    def contexts(self) -> Tuple[str, ...]:
        """A todo's contexts.

        A word is normally marked as a context by prefixing it with '@'.
        """

    @property
    def create_date(self) -> dt.date:  # noqa: D102
        """The date this todo was created."""

    @property
    def desc(self) -> str:  # noqa: D102
        """A description of this todo."""

    @property
    def done_date(self) -> dt.date | None:  # noqa: D102
        """The date this todo was completed."""

    @property
    def done(self) -> bool:  # noqa: D102
        """Is this todo marked done with an 'x'?"""

    @property
    def epics(self) -> Tuple[str, ...]:  # noqa: D102
        """A todo's epics.

        A word is normally marked as an epic by prefixing it with '#'.
        """

    @property
    def metadata(self) -> Metadata:  # noqa: D102
        """A todo's corresponding metadata dictionary.

        A word is metadata if it is of the form KEY:VALUE.
        """

    @property
    def priority(self) -> Priority:  # noqa: D102
        """A todo's priority."""

    @property
    def projects(self) -> Tuple[str, ...]:  # noqa: D102
        """A todo's projects.

        A word is normally marked as a project by prefixing it with '+'.
        """


@dataclass
class EnchantedTodo(Generic[T]):
    """Return type for Todo spells.

    Attributes:
        changed: Has any spell changed this todo?
        todo: The possibly modified todo after casting spells on it.
    """

    todo: T
    changed: bool = False


# Type of spell functions used by MagicTodo objects.
TodoSpell = Callable[[T], EnchantedTodo[T]]
