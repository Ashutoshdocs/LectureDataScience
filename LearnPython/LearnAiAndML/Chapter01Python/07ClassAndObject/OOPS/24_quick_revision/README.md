# Lecture 24: Quick revision: the whole OOP course on one page

Run: `python lecture.py` for a 25-question self-test. Every answer is produced by running real code.

## 1. Classes & objects (01–04)

```python
class Student:
    school = "ABC"                    # class attribute: shared
    count = 0

    def __init__(self, name, marks=0):   # constructor: runs on Student(...)
        self.name = name              # instance attribute: per object
        self.marks = marks
        Student.count += 1            # update shared data through the CLASS

    def is_pass(self):                # instance method; self = the object
        return self.marks >= 40

s = Student("Asha", 92)               # create an object
s.is_pass()                           # == Student.is_pass(s)
```

- Lookup order for `obj.x`: object → class → parents → `AttributeError`.
- `self.x = ...` on a class attribute **shadows** it for that object only.
- Never use a mutable default (`[]`). Use `None`, or a dataclass `field(default_factory=list)`.

## 2. Encapsulation (06–08)

| Name | Meaning |
|------|---------|
| `x` | public |
| `_x` | internal (convention) |
| `__x` | name-mangled to `_Class__x` (avoids subclass clashes) |

```python
@property
def balance(self): return self._balance          # getter (read-only if there's no setter)

@balance.setter
def balance(self, v):                            # setter with validation
    if v < 0: raise ValueError("negative")
    self._balance = v
```

| Method type | Decorator | Gets | Use for |
|-------------|-----------|------|---------|
| instance | none | `self` | most methods |
| class | `@classmethod` | `cls` | alternative constructors (`from_string`), class-wide data |
| static | `@staticmethod` | nothing | helpers that belong with the class |

## 3. Inheritance (09–12)

```python
class Manager(Employee):                  # Manager IS AN Employee
    def __init__(self, name, salary, team):
        super().__init__(name, salary)    # let the parent set up its part
        self.team = team

    def describe(self):                   # override; extend with super()
        return super().describe() + f" (team {self.team})"
```

- Types: single, multilevel, hierarchical, multiple, diamond.
- **MRO** (`Class.__mro__`): child before parents, left to right, each class once.
- With multiple inheritance, **always use `super()`** so every class runs once.
- **Mixins** are small single-ability classes: `class Order(JsonMixin, LoggingMixin, Base)`.

## 4. Polymorphism (13–16)

- Same call, different behaviour: `for s in shapes: s.area()`. It replaces `if type == ...` chains.
- **Magic methods** plug into Python's syntax:

| You write | Python calls |
|-----------|--------------|
| `print(x)` / console | `__str__` / `__repr__` |
| `len(x)`, `x[i]`, `v in x`, `for v in x` | `__len__`, `__getitem__`, `__contains__`, `__iter__` |
| `x + y`, `3 * x`, `x == y`, `x < y` | `__add__`, `__rmul__`, `__eq__`, `__lt__` |
| `x()` | `__call__` |
| `with x:` | `__enter__` / `__exit__` |

- Return `NotImplemented` for unsupported types. If you define `__eq__`, also define `__hash__` (or the objects become unhashable).
- **Duck typing**: what matters is what an object can do, not its class. `typing.Protocol` lets tools check it.

## 5. Abstraction & design (17–19)

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): ...     # children MUST implement it, or creating them raises TypeError

    def receipt(self, amount):     # shared code built on the contract (template method)
        return f"Receipt: {self.pay(amount)}"
```

- **Composition** ("has-a"): `self.engine = Engine()`. Delegate to it, swap it, pass it in (dependency injection). Prefer it to deep inheritance.
- **Dataclasses**: `@dataclass` generates `__init__`, `__repr__` and `__eq__`. Options: `frozen`, `order`, `slots`; `field(default_factory=...)`, `__post_init__` for validation.

## The four pillars

| Pillar | Idea | Python tools |
|--------|------|--------------|
| Encapsulation | bundle and hide | methods, `_x`, `__x`, `@property` |
| Inheritance | reuse | `class C(P)`, `super()`, MRO, mixins |
| Polymorphism | one interface, many forms | overriding, dunders, duck typing |
| Abstraction | what, not how | `ABC`, `@abstractmethod`, Protocols |

## When to use what

| Need | Use |
|------|-----|
| group data + rules | a class |
| mainly data, little behaviour | `@dataclass` |
| validate or compute an attribute | `@property` |
| another way to create objects | `@classmethod` |
| helper related to the class | `@staticmethod` |
| a true "is-a" family | inheritance |
| a "has-a" part, or swappable behaviour | composition |
| a small reusable ability | a mixin |
| children MUST implement methods | `ABC` + `@abstractmethod` |
| make objects work with `len`, `for`, `+`, `print` | magic methods |

## SOLID in one line each

**S**: one job per class · **O**: extend by adding classes · **L**: children work wherever the parent works · **I**: small interfaces · **D**: depend on abstractions; pass parts in.

← [Back to course map](../README.md)
