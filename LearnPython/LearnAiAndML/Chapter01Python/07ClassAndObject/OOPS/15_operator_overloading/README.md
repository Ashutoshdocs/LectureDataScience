# Lecture 15: Operator overloading

Run: `python lecture.py`

## The idea

**Operator overloading** means teaching Python's operators what to do with **your** objects. It's polymorphism again: `+` already means addition for ints, joining for strings and concatenation for lists.

```python
a + b      →  a.__add__(b)
a == b     →  a.__eq__(b)
a < b      →  a.__lt__(b)
```

**When to use it:** only when the operator's meaning is **obvious** for your type: vectors, money, fractions, matrices, dates, versions. `employee + employee` is confusing, so use a method instead.

## Operator table

| Operator | Method | Reflected (right side) | In-place |
|----------|--------|------------------------|----------|
| `a + b` | `__add__` | `__radd__` | `__iadd__` (`+=`) |
| `a - b` | `__sub__` | `__rsub__` | `__isub__` |
| `a * b` | `__mul__` | `__rmul__` | `__imul__` |
| `a / b` | `__truediv__` | `__rtruediv__` | `__itruediv__` |
| `a // b`, `a % b`, `a ** b` | `__floordiv__`, `__mod__`, `__pow__` | `__r...__` | `__i...__` |
| `-a`, `abs(a)` | `__neg__`, `__abs__` | | |
| `a == b`, `a != b` | `__eq__`, `__ne__` (auto from `__eq__`) | | |
| `a < b`, `<=`, `>`, `>=` | `__lt__`, `__le__`, `__gt__`, `__ge__` | | |

## Return a new object

`a + b` should **not change `a`**, just as `2 + 3` doesn't change the 2:

```python
def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)     # new object
```

## `NotImplemented`: say "I don't know this type"

```python
def __add__(self, other):
    if not isinstance(other, Vector):
        return NotImplemented        # NOT raise, and NOT NotImplementedError
    ...
```

Returning `NotImplemented` lets Python **try the other operand's** reflected method (`other.__radd__(self)`). If neither side knows how, Python raises a clear `TypeError: unsupported operand type(s)`.

## Reflected methods: `3 * v`

`v * 3` calls `v.__mul__(3)`. But `3 * v` first calls `int.__mul__(3, v)`, which returns `NotImplemented`, and then Python tries **`v.__rmul__(3)`**. Define `__rmul__` to support numbers on the left. This also makes `sum(list_of_money)` work: `sum` starts with `0 + first`, which needs `__radd__`.

## Comparisons & `@total_ordering`

Define `__eq__` and **one** of `__lt__`/`__le__`/`__gt__`/`__ge__`, then decorate the class with `@functools.total_ordering` to get the rest. Defining `__lt__` alone is enough for `sorted()`, `min()` and `max()`.

## `__eq__` and `__hash__` go together

- Defining `__eq__` **sets `__hash__` to `None`**, so your objects can no longer be put in a set or used as dict keys.
- If equal objects should work in sets or dicts, define `__hash__` from the **same fields** as `__eq__`: `return hash((self.x, self.y))`.
- Only hash **immutable** data. If a field changes after the object is in a set, the set breaks.

## Exercises

1. Add `__sub__`, `__neg__` and `__abs__` (length) to `Vector`.
2. Make `Money` refuse to add different currencies (raise `ValueError`).
3. Write `Version("1.10.2")` with comparison operators so that `Version("1.10") > Version("1.9")`.
4. Put two equal `Point`s in a set. With `__hash__`, how many items does the set have? Without it?

**Next →** [Lecture 16: Duck typing & protocols](../16_duck_typing_and_protocols/)
