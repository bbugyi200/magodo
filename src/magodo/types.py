"""Custom types used by this library."""

from __future__ import annotations

import datetime as dt
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

from eris import ErisError, Result
from typist import Comparable, ToDictable


if TYPE_CHECKING:
    from ._todo import Todo  # pragma: no cover


# Type Variables (i.e. `TypeVar`s)
Todo_T = TypeVar("Todo_T", bound="AbstractTodo")
MagicTodo_T = TypeVar("MagicTodo_T", bound="AbstractMagicTodo")

# Type of the Todo.metadata attribute.
Metadata = Dict[str, Union[str, List[str]]]
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
# Type of spell functions used by MagicTodo objects.
TodoSpell = Callable[["Todo"], Result["Todo", ErisError]]


@runtime_checkable
class AbstractTodo(Comparable, ToDictable, Protocol):
    """Describes how any valid Todo object should look."""

    @classmethod
    def from_line(cls: Type[Todo_T], line: str) -> Result[Todo_T, ErisError]:
        """Constructs a new Todo object from a string."""

    def to_line(self) -> str:
        """Converts a Todo object back to a string."""

    @property
    def contexts(self) -> Tuple[str, ...]:  # noqa: D102
        """A todo's contexts.

        A word is normally marked as a context by prefixing it with '@'.
        """

    @property
    def create_date(self) -> Optional[dt.date]:  # noqa: D102
        """The date this todo was created."""

    @property
    def desc(self) -> str:  # noqa: D102
        """A description of this todo."""

    @property
    def done_date(self) -> Optional[dt.date]:  # noqa: D102
        """The date this todo was completed."""

    @property
    def marked_done(self) -> bool:  # noqa: D102
        """Is this todo marked done with an 'x'?"""

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


@runtime_checkable
class AbstractMagicTodo(AbstractTodo, Protocol):
    """Describes how subclasses of MagicTodoMixin should look."""

    pre_spells: List[TodoSpell]
    spells: List[TodoSpell]
    post_spells: List[TodoSpell]

    def __init__(self, todo: "Todo") -> None:
        pass

    @classmethod
    def cast_spells(cls, todo: "Todo") -> Result["Todo", ErisError]:
        """Casts all spells associated with this MagicTodo on `todo`."""

    @property
    def todo(self) -> "Todo":
        """The raw Todo object used by this MagicTodo."""
