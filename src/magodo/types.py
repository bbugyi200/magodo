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


if TYPE_CHECKING:
    from ._todo import Todo


# Type Variables (i.e. `TypeVar`s)
Todo_T = TypeVar("Todo_T", bound="AbstractTodo")
MagicTodo_T = TypeVar("MagicTodo_T", bound="AbstractMagicTodo")

TodoSpell = Callable[["Todo"], "Todo"]
TodoValidator = Callable[["Todo"], Result[None, ErisError]]

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


@runtime_checkable
class AbstractTodo(Protocol):
    """Describes how any valid Todo object should look."""

    @classmethod
    def from_line(cls: Type[Todo_T], line: str) -> Result[Todo_T, ErisError]:
        """Constructs a new Todo object from a string."""

    def to_line(self) -> str:
        """Converts a Todo object back to a string."""

    @property
    def contexts(self) -> Tuple[str, ...]:
        pass

    @property
    def create_date(self) -> dt.date | None:
        pass

    @property
    def desc(self) -> str:
        pass

    @property
    def done_date(self) -> dt.date | None:
        pass

    @property
    def marked_done(self) -> bool:
        pass

    @property
    def metadata(self) -> Optional[Metadata]:
        pass

    @property
    def priority(self) -> Priority:
        pass

    @property
    def projects(self) -> Tuple[str, ...]:
        pass


class AbstractMagicTodo(AbstractTodo, Protocol):
    """Describes how subclasses of MagicTodoMixin should look."""

    pre_spells: List[TodoSpell]
    spells: List[TodoSpell]
    post_spells: List[TodoSpell]

    def __init__(self, todo: "Todo") -> None:
        pass

    @property
    def todo(self) -> "Todo":
        pass
