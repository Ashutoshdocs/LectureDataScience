# Lecture 01: Classes & objects

Run: `python lecture.py`

## Before you start

You should know what a **type** is (`type(5)` → `int`). A class is how you create a **new type**.

## Class vs object

| | Class | Object (instance) |
|--|-------|-------------------|
| What | a **blueprint** / template | one **real thing** built from it |
| How many | one definition | as many as you like |
| Created by | `class Dog:` | `Dog()` |
| Example | `Dog` | Bruno, Tommy, Sheru |

```python
class Dog:          # define the blueprint (CapitalWords by convention)
    pass            # "empty for now"

a = Dog()           # call the class like a function → a NEW object
b = Dog()           # another, separate object
```

### What `Dog()` does

```
Dog()  →  1. Python creates a new, empty Dog object in memory
          2. runs __init__ on it (Lecture 02), if there is one
          3. hands back the object → you store it in a variable
```

## Checking objects

| Expression | Result | Meaning |
|------------|--------|---------|
| `type(a)` | `<class '__main__.Dog'>` | the object's class (`__main__` is the file it was defined in) |
| `isinstance(a, Dog)` | `True` | is `a` a Dog (or a child of Dog, Lecture 09)? |
| `a is b` | `False` | are they the **same object**? |
| `a == b` | `False` | equal? By default, only if they're the same object (Lecture 15 changes this) |
| `id(a)` | a number | the object's identity (its memory address in CPython) |

## Attributes can be attached to objects

```python
a.name = "Bruno"      # works, but this is NOT the proper way
print(a.name)
print(b.name)         # AttributeError: b was never given a name
```

Attaching attributes from outside means each object may have different attributes, and nothing guarantees `name` exists. **Lecture 02** fixes this with `__init__`.

## Classes are objects too

`Dog` itself is an object of type `type`. You can pass it around, store it in a list, and call it later:

```python
kinds = [Dog, list, str]
things = [k() for k in kinds]     # [<Dog object>, [], '']
```

## Naming conventions (PEP 8)

| Thing | Style | Example |
|-------|-------|---------|
| class | `CapWords` | `BankAccount`, `HttpRequest` |
| object / variable | `snake_case` | `my_account` |
| method / attribute | `snake_case` | `get_balance`, `first_name` |

## Common mistakes

| Mistake | Effect |
|---------|--------|
| `a = Dog` (no brackets) | `a` is the class itself, not a new object |
| Expecting `Dog() == Dog()` to be `True` | each call makes a different object |
| Lower-case class names `class dog:` | works, but confuses readers |

## Exercises

1. Create a class `Cat`, make two cats, give each a `name`, print both.
2. Print `type(Cat)`. What is the type of a class?
3. Put three new `Cat()` objects in a list and print their `id()`s.
4. What's the difference between `x = Cat` and `x = Cat()`? Print both.

<details><summary>Solutions</summary>

`type(Cat)` is `<class 'type'>`: classes are objects made by `type`. `x = Cat` stores the class; `x = Cat()` stores a new instance.
</details>

**Next →** [Lecture 02: `__init__` & attributes](../02_init_and_attributes/)
