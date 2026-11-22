# Lecture 06: Encapsulation: public, `_protected`, `__private`

Run: `python lecture.py`

## What is encapsulation?

**Encapsulation** = (1) **bundling** data with the methods that use it, and (2) **hiding** the internal details so outside code uses the object only through a small, deliberate **public interface**.

Think of a car. You use the **interface** (steering wheel, pedals, dashboard). The engine internals are hidden. You can't accidentally stick your hand in the gearbox, and the manufacturer can redesign the engine without changing how you drive.

## Why bother?

| Without encapsulation | With encapsulation |
|-----------------------|--------------------|
| any code can set `acc.balance = -5000` | balance changes only through `deposit()`/`withdraw()`, which check the rules |
| changing an internal detail breaks code everywhere | internals can change freely; the public methods stay the same |
| readers can't tell what's safe to use | the names tell you what's public and what's internal |

## Python's three levels (by naming convention)

| Name | Level | Meaning | Enforced? |
|------|-------|---------|-----------|
| `owner` | **public** | use freely from anywhere | n/a |
| `_branch` | **protected** | "internal: for this class and its subclasses; please don't touch from outside" | ❌ just a convention (linters and IDEs warn) |
| `__pin` | **private** | "strictly internal to this class" | ⚠️ partly: Python renames it (name mangling) |

```python
class Account:
    def __init__(self, owner, pin):
        self.owner = owner        # public
        self._branch = "Pune"     # protected
        self.__pin = pin          # private → stored as _Account__pin

    def check_pin(self, guess):   # public method = the approved way in
        return guess == self.__pin
```

## Name mangling, explained

Inside a class body, any name like `__pin` (two leading underscores, **at most one** trailing underscore) is rewritten to `_ClassName__pin`:

```python
acc.__pin            # AttributeError: there's no attribute called "__pin"
acc._Account__pin    # 4321: the real (mangled) name; possible, but don't
acc.__dict__         # {'owner': ..., '_branch': ..., '_Account__pin': 4321}
```

Its real purpose is **avoiding accidental name clashes in subclasses**: a child class's `__pin` becomes `_Child__pin`, so it can't overwrite the parent's `_Account__pin`.

> Dunder names like `__init__` (two underscores on **both** sides) are **not** mangled. They're special methods, not private ones.

## "We're all consenting adults"

Python has no truly private data. Underscores are **signals of intent**, not locks. The community rule:

- Use **`_single`** for internal attributes and helper methods. This is the normal choice.
- Use **`__double`** only when you specifically need to avoid clashes with subclasses.
- Expose what users need through **public methods or properties** (Lecture 07).

## Designing a public interface

Ask "what does the *user* of this class need to do?" and make only that public:

| Public (stable) | Internal (may change) |
|-----------------|-----------------------|
| `deposit()`, `withdraw()`, `balance` (read-only) | `_transactions`, `_validate()`, `_apply_fees()` |

## Exercises

1. Add `change_pin(old, new)` that changes the PIN only if `old` is correct and `new` has 4 digits.
2. Print `acc.__dict__` and find the mangled name.
3. Create `class Child(Account)` that sets its own `self.__pin`. Print the child's `__dict__`. Do the two PINs clash?
4. Turn `_transactions` into a read-only copy returned by `history()`. Why return a copy?

**Next →** [Lecture 07: Properties: getters & setters](../07_properties_getters_setters/)
