# Lecture 02: `__init__` & attributes

Run: `python lecture.py`

## Why do we need `__init__`?

In Lecture 01 we attached attributes from outside (`a.name = "Bruno"`). Nothing guaranteed that every object got a name. `__init__` **guarantees every new object starts complete and valid**.

```python
class Student:
    def __init__(self, name, marks):   # runs automatically on Student(...)
        self.name = name                # store data ON this object
        self.marks = marks

s1 = Student("Asha", 92)
```

### What happens on `Student("Asha", 92)`

```
1. Python creates an empty Student object
2. calls Student.__init__(that_object, "Asha", 92)
                          ↑ becomes self
3. __init__ stores self.name and self.marks
4. the finished object is returned → s1
```

`__init__` must **return `None`**. It sets up the object and doesn't produce it. (The object is created just before by `__new__`, which you almost never need.)

## What is `self`?

`self` is **the object being set up** (or, in methods, the object being used). It's an ordinary parameter. `self` is only a strong convention, but always use it.

| Code | Meaning |
|------|---------|
| `self.name = name` | create/update the attribute `name` **on this object**, using the parameter `name` |
| `name = name` | does nothing useful: a local variable, lost when `__init__` ends |

## Attributes

An **instance attribute** is a variable stored on one object. Each object has its own copy:

```python
s1.name   # 'Asha'
s2.name   # 'Ravi'
s1.__dict__   # {'name': 'Asha', 'marks': 92}  ← all of s1's attributes
```

| Tool | Use |
|------|-----|
| `obj.attr` | read (`AttributeError` if missing) |
| `obj.attr = v` | create / change |
| `getattr(obj, "attr", default)` | read by name (a string), with a fallback |
| `setattr(obj, "attr", v)` / `hasattr(obj, "attr")` | write / check by name |
| `del obj.attr` | remove |
| `vars(obj)` / `obj.__dict__` | all instance attributes as a dict |

## Default values & validation

```python
class Student:
    def __init__(self, name, marks=0, subjects=None):
        if not name:
            raise ValueError("name is required")
        if not 0 <= marks <= 100:
            raise ValueError(f"marks must be 0-100, got {marks}")
        self.name = name.title()
        self.marks = marks
        self.subjects = subjects if subjects is not None else []   # never a mutable default!
        self.grade = "PASS" if marks >= 40 else "FAIL"            # derived attribute
```

- **Validate in `__init__`** so an invalid object can never exist.
- `subjects=None`, then create a new list. A default `[]` would be **shared by every student** (the same trap as with functions).
- You can store **derived** values. Lecture 07 shows that a `@property` is often better, because it stays in sync.

## Good practice

- Create **all** attributes in `__init__`, even if only as `None`, so readers see the object's full shape in one place.
- Keep `__init__` simple: store and validate. Don't do slow work like network calls there.

## Common mistakes

| Mistake | Error / effect |
|---------|----------------|
| `def __init__(name, marks)` (no `self`) | `TypeError: takes 2 positional arguments but 3 were given` |
| `def _init_` or `def __int__` (typo) | no error, but `__init__` never runs, so the object has no attributes |
| `Student("Asha")` when marks has no default | `TypeError: missing 1 required positional argument: 'marks'` |
| `return self` in `__init__` | `TypeError: __init__() should return None` |

## Exercises

1. Write `Book(title, author, pages=100)` and print `__dict__` of two books.
2. Make `Book` raise `ValueError` if `pages <= 0`.
3. Add a `tags` attribute with a safe default list. Prove two books don't share it.
4. Use `getattr(book, "isbn", "unknown")`.

**Next →** [Lecture 03: Methods & `self`](../03_methods_and_self/)
