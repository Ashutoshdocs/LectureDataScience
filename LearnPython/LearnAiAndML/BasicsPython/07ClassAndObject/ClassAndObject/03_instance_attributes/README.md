# Lecture 03: Instance attributes

Run: `python lecture.py`

## What is an instance attribute?

A variable stored on **one particular object**. Create it by assigning with a dot:

```python
class Car:
    pass

a = Car()
b = Car()
a.color = "red"
a.speed = 120
b.color = "blue"
```

Every object has its own storage, a dictionary you can see with `obj.__dict__`:

```
a.__dict__  →  {'color': 'red', 'speed': 120}
b.__dict__  →  {'color': 'blue'}
```

Giving `a` a `speed` does **not** give `b` one, so `b.speed` raises `AttributeError: 'Car' object has no attribute 'speed'`.

> ⚠️ Adding attributes from outside works, but it's fragile: different objects end up with different attributes. In Lecture 07 the **constructor** sets up every object the same way. Normally you create attributes inside methods with `self.x = …`.

## Read, update, check & delete

| Task | Dot syntax | Built-in function |
|------|-----------|-------------------|
| Read | `b.title` | `getattr(b, "title")` |
| Read with fallback | n/a | `getattr(b, "author", "Unknown")` |
| Create / update | `b.pages = 300` | `setattr(b, "pages", 300)` |
| Check | n/a | `hasattr(b, "pages")` |
| Delete | `del b.pages` | `delattr(b, "pages")` |
| See all | `b.__dict__` | `vars(b)` |

The function versions take the attribute name as a **string**, so the name can come from a variable, a file or user input:

```python
for field in ["title", "author", "price"]:
    print(field, "=", getattr(b, field, "-"))
```

## Rules for attribute names

- Same as variable names: letters, digits, `_`, not starting with a digit.
- `_name` (one underscore) is a convention meaning "internal, please don't touch" (Lecture 12).
- `__name__`-style names with double underscores on both sides are reserved for Python's special names.

## Exercises

1. Give `b` a speed and print both `__dict__`s.
2. Loop over `["title", "author", "price"]` and print each attribute with `getattr(..., "-")`.
3. Delete an attribute, then try to read it. What error do you get?
4. Build an object from a dict: `for k, v in data.items(): setattr(obj, k, v)`.

<details><summary>Solutions</summary>

3. `AttributeError: 'Book' object has no attribute 'pages'`.
4. See section 4 of `lecture.py`.
</details>

**Next →** [Lecture 04: Class attributes & shadowing](../04_class_attributes_and_shadowing/)
