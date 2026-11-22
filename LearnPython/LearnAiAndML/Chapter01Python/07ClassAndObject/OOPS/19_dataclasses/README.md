# Lecture 19: Dataclasses: less boilerplate for data-holding classes

Run: `python lecture.py`

## The problem

Classes that mainly **hold data** need the same boilerplate every time:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
```

## `@dataclass` writes it for you

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int          # type hints define the fields (they are not enforced at runtime)
    y: int = 0      # defaults allowed
```

You get `__init__`, `__repr__` and `__eq__` automatically. You can still add **normal methods and properties**: it's a regular class.

## Options

| Option | Effect |
|--------|--------|
| `@dataclass(frozen=True)` | **immutable**: assigning raises `FrozenInstanceError`; also gives a `__hash__`, so objects can go in sets and dict keys |
| `@dataclass(order=True)` | adds `< <= > >=`, comparing fields **in order** as a tuple |
| `@dataclass(slots=True)` (3.10+) | uses `__slots__`: less memory, faster attribute access, no new attributes by accident |
| `@dataclass(kw_only=True)` (3.10+) | all fields must be passed by keyword |

## `field()` for special cases

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    owner: str
    items: list = field(default_factory=list)       # ✅ a new list per object
    # items: list = []                              # ❌ ValueError: mutable default
    _id: int = field(default=0, repr=False, compare=False)   # hidden from repr and ==
```

## `__post_init__`: validation and derived fields

```python
@dataclass
class Student:
    name: str
    marks: int
    grade: str = field(init=False)      # not an __init__ parameter

    def __post_init__(self):            # runs after the generated __init__
        if not 0 <= self.marks <= 100:
            raise ValueError("marks must be 0-100")
        self.grade = "PASS" if self.marks >= 40 else "FAIL"
```

## Helpers

`dataclasses.asdict(obj)` converts to a dict (handy for JSON). `dataclasses.replace(obj, x=5)` makes a modified **copy** (useful with frozen objects). `dataclasses.fields(cls)` lists the fields.

## Inheritance works too

A child dataclass adds fields after the parent's. Fields without defaults can't follow fields with defaults, so use `kw_only=True` if you need that.

## When to use a dataclass

| ✅ Use `@dataclass` | Use a normal class instead |
|---------------------|----------------------------|
| the class is mainly **data**: records, DTOs, config, coordinates, API payloads | the class is mainly **behaviour** with complex setup |
| you want readable `repr` and value equality for free | you need full control of `__init__` |
| | |
| **Alternatives:** `NamedTuple` (immutable, tuple-like), `TypedDict` (typed dicts), `pydantic` (runtime validation, third-party) | |

## Exercises

1. Write `@dataclass Product(name, price, qty=1)` with a `total` property.
2. Make `Money` frozen and put two equal amounts in a set.
3. Write `Task(priority, title)` with `order=True` and sort a list of tasks.
4. Add `__post_init__` to `Product` that rejects negative prices.

**Next →** [Lecture 20: The four pillars together](../20_four_pillars_together/)
