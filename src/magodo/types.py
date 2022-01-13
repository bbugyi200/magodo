"""Custom types used by this library."""

from __future__ import annotations

import datetime as dt
from typing import (
    TYPE_CHECKING,
    Any,
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


if TYPE_CHECKING:
    from ._todo import Todo


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
TodoSpell = Callable[["Todo"], "Todo"]


@runtime_checkable
class AbstractTodo(Protocol):
    """Describes how any valid Todo object should look."""

    @classmethod
    def from_line(cls: Type[Todo_T], line: str) -> Result[Todo_T, ErisError]:
        """Constructs a new Todo object from a string."""

    def to_line(self) -> str:
        """Converts a Todo object back to a string."""

    def to_dict(self) -> dict[str, Any]:
        """Converts a Todo object into a dictionary."""

    @property
    def contexts(self) -> Tuple[str, ...]:  # noqa: D102
        pass

    @property
    def create_date(self) -> Optional[dt.date]:  # noqa: D102
        pass

    @property
    def desc(self) -> str:  # noqa: D102
        pass

    @property
    def done_date(self) -> Optional[dt.date]:  # noqa: D102
        pass

    @property
    def marked_done(self) -> bool:  # noqa: D102
        pass

    @property
    def metadata(self) -> Optional[Metadata]:  # noqa: D102
        pass

    @property
    def priority(self) -> Priority:  # noqa: D102
        pass

    @property
    def projects(self) -> Tuple[str, ...]:  # noqa: D102
        pass


@runtime_checkable
class AbstractMagicTodo(AbstractTodo, Protocol):
    """Describes how subclasses of MagicTodoMixin should look."""

    pre_spells: List[TodoSpell]
    spells: List[TodoSpell]
    post_spells: List[TodoSpell]

    def __init__(self, todo: "Todo") -> None:
        pass

    @property
    def todo(self) -> "Todo":
        """The raw Todo object used by this MagicTodo."""

    @property
    def enchanted_todo(self) -> "Todo":
        """The todo created by casting spells on self.todo."""
