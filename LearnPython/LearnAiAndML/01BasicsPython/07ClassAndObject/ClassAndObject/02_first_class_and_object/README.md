# Lecture 02: Your first class & object

Run: `python lecture.py`

## The smallest class

```python
class Dog:
    pass
```

- `class` is the keyword, `Dog` is the name, and `:` starts the body.
- The body needs at least one statement. `pass` means "nothing here yet".
- **Naming convention:** classes use `CapitalizedWords` (`BankAccount`); functions and variables use `snake_case` (`bank_account`).
- A docstring right under the `class` line documents it: `"""A dog in our shelter."""`. Read it with `Dog.__doc__` or `help(Dog)`.

## Creating objects (instantiation)

Calling the class like a function creates a **new object** (an **instance**):

```python
d1 = Dog()
d2 = Dog()
```

Each call makes a brand-new, separate object.

| Check | Result | Meaning |
|-------|--------|---------|
| `type(d1)` | `<class '__main__.Dog'>` | d1 was made from Dog (`__main__` = the file being run) |
| `isinstance(d1, Dog)` | `True` | "is d1 a Dog?" |
| `d1 is d2` | `False` | two different objects |
| `id(d1)`, `id(d2)` | two different numbers | each object's identity |
| `type(Dog)` | `<class 'type'>` | a class is itself an object, of type `type` |
| `print(d1)` | `<__main__.Dog object at 0x…>` | default text (Lecture 15 makes it nicer) |

## Vocabulary for the rest of the course

| Term | Meaning | Example |
|------|---------|---------|
| **Class** | blueprint / template | `Phone` |
| **Object / instance** | a thing built from the class | `my_phone` |
| **Instantiation** | creating an object | `Phone()` |
| **Attribute** | a variable belonging to a class or object | `brand` |
| **Method** | a function defined inside a class | `ring` |
| **`self`** | the object the method was called on | first parameter of `ring` |
| **`cls`** | the class a class method was called on | Lecture 09 |
| **Constructor** | `__init__`, runs when an object is created | Lecture 07 |
| **Destructor** | `__del__`, runs when an object is destroyed | Lecture 08 |

You reach attributes and methods with the **dot operator**: `obj.attribute`, `obj.method()`.

## Exercises

1. Remove `pass` from an empty class. What error appears?
2. Make a class `Cat` and check `isinstance(d1, Cat)`.
3. Add a docstring to `Dog` and print `Dog.__doc__`.

<details><summary>Solutions</summary>

1. `IndentationError: expected an indented block`.
2. `False`.
</details>

**Next →** [Lecture 03: Instance attributes](../03_instance_attributes/)
