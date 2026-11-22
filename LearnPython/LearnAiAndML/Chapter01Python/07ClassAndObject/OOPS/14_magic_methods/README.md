# Lecture 14: Magic (dunder) methods

Run: `python lecture.py`

## What are they?

Methods named `__like_this__` (double underscore = "dunder") are **hooks**. You don't usually call them yourself. **Python calls them** when you use built-in syntax and functions on your objects.

```python
print(book)     →  book.__str__()
len(book)       →  book.__len__()
book[0]         →  book.__getitem__(0)
for x in book   →  book.__iter__()
"x" in book     →  book.__contains__("x")
book()          →  book.__call__()
```

**Why use them?** They make your classes feel like built-in types. Users write `len(playlist)` instead of `playlist.get_length()`, and your objects work with `for`, `in`, `sorted()`, `print()`, `with` and so on. That's polymorphism with Python's own syntax.

## The most useful dunders

### Text representation

| Method | Called by | Audience | Rule of thumb |
|--------|-----------|----------|---------------|
| `__str__` | `print(x)`, `str(x)`, f-strings | **users** | friendly, readable |
| `__repr__` | the console, `repr(x)`, inside lists, `!r` | **developers** | unambiguous; ideally looks like the code to recreate it: `Book('Python', 320)` |

If you write only one, write `__repr__`: `str()` falls back to it.

### Size, truth & containers

| Method | Enables |
|--------|---------|
| `__len__(self)` | `len(x)`; also truthiness if there's no `__bool__` (length 0 → `False`) |
| `__bool__(self)` | `if x:` |
| `__getitem__(self, key)` | `x[key]`, slicing, and (as a fallback) iteration and `in` |
| `__setitem__(self, key, value)` / `__delitem__` | `x[key] = v` / `del x[key]` |
| `__contains__(self, item)` | `item in x` |
| `__iter__(self)` | `for item in x` (return an iterator, or write it as a generator with `yield`) |

### Callable objects

`__call__(self, ...)` lets an object be called like a function, **while keeping state**: a counter, a configured validator, a cache.

### Context managers

`__enter__` / `__exit__` make `with obj:` work: setup and **guaranteed cleanup**, even when an error happens (files, locks, timers, database transactions).

### Object lifecycle

| Method | When |
|--------|------|
| `__new__` | creates the object (rarely overridden; used for immutables and singletons) |
| `__init__` | initialises it |
| `__del__` | just before garbage collection (avoid relying on it; use `with` instead) |

### Attribute access (advanced)

`__getattr__(self, name)` runs **only when normal lookup fails**. It's useful for defaults and delegation (Lecture 18).

Comparison and arithmetic dunders (`__eq__`, `__lt__`, `__add__`…) get their own lecture: **15**.

## Common mistakes

| Mistake | Effect |
|---------|--------|
| `__str__` returns a non-string | `TypeError: __str__ returned non-string` |
| `__len__` returns a negative number or a float | `ValueError` / `TypeError` |
| `__iter__` returns a list instead of an iterator | `TypeError: iter() returned non-iterator`. Return `iter(self._items)` or use `yield` |
| calling `obj.__len__()` directly | works, but write `len(obj)` |

## Exercises

1. Give `Playlist` a `__repr__`, then compare `print(playlist)` with `print([playlist])` with and without `__str__`.
2. Add `__setitem__` and `__delitem__` to `Playlist`.
3. Write `Multiplier(n)` with `__call__`, so `triple = Multiplier(3); triple(5) == 15`.
4. Write a `Timer` context manager that prints the elapsed time on exit.

**Next →** [Lecture 15: Operator overloading](../15_operator_overloading/)
