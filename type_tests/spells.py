from magodo.types import TodoSpell, T


def print_todo_spell(todo_spell: TodoSpell) -> None:
    print(todo_spell.__name__)


def dummy_spell(todo: T) -> T:
    """Dummy spell."""
    return todo


print_todo_spell(dummy_spell)
