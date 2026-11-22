# Lecture 07: The constructor `__init__`

Run: `python lecture.py`

## Why do we need a constructor?

Without one, every object starts **empty** and you attach attributes by hand:

```python
a = Student(); a.name = "Asha"; a.marks = 88; a.show()   # works
b = Student(); b.name = "Ravi";                b.show()   # forgot marks → AttributeError
```

- **Repetitive:** several lines of setup for every object.
- **Easy to forget** something, and the crash happens later, somewhere else.
- **No single place** that defines what a Student *must* have.

A **constructor** is a special method that Python runs **automatically** each time an object is created. You use it to give every new object its starting attributes, the same way every time.

## `__init__`: Python's constructor

```python
class Student:
    def __init__(self, name, marks):
        self.name = name          # copy the PARAMETER onto the OBJECT
        self.marks = marks

    def show(self):
        print(self.name, "scored", self.marks)

a = Student("Asha", 88)
```

### What happens on `Student("Asha", 88)`

```
 1. Python creates an empty object          (done by __new__, behind the scenes)
 2. calls  __init__(obj, "Asha", 88)        ← your constructor fills it in
 3. hands the finished object back          → stored in a
```

| Line | Effect | Object afterwards |
|------|--------|-------------------|
| `Student("Asha", 88)` | empty object made, `__init__` called | `{}` |
| `self.name = name` | attribute stored | `{'name': 'Asha'}` |
| `self.marks = marks` | attribute stored | `{'name': 'Asha', 'marks': 88}` |
| back on the creation line | object assigned to `a` | ready to use |

Key points:
- The arguments in `Student(...)` go to `__init__` **after `self`**.
- `name` (parameter) is a **local** variable that vanishes when `__init__` ends. `self.name` (attribute) **lives on the object**.
- You never call `__init__` yourself. Python calls it once per object.
- "dunder init" = **d**ouble **under**score init.

## Default & keyword arguments

```python
class Pizza:
    def __init__(self, size="medium", toppings=None, cheese=True):
        self.size = size
        self.toppings = toppings if toppings is not None else []
        self.cheese = cheese

Pizza()                              # all defaults
Pizza("large", ["olive"])            # positional
Pizza(cheese=False, size="small")    # keyword, any order
```

> ⚠️ **Never use a mutable default** like `toppings=[]`. That single list is created **once** when the `def` runs and is **shared by every object** that uses the default. Use `None` and create a new list inside `__init__`. `lecture.py` demonstrates the bug.

## Validation & computed attributes

The constructor is the ideal place to **refuse bad data** and to **derive** attributes:

```python
class Temperature:
    def __init__(self, celsius):
        if celsius < -273.15:
            raise ValueError("below absolute zero")    # no object is created
        self.celsius = celsius
        self.fahrenheit = celsius * 9 / 5 + 32          # computed
        self.label = "hot" if celsius > 30 else "pleasant"
```

If `__init__` raises, **no object exists**. So every `Temperature` that exists is valid.

## Kinds of constructors

| Kind | Looks like | Example |
|------|-----------|---------|
| **Default constructor** | none written; Python supplies an empty one | `class Dog: pass` → `Dog()` |
| **Non-parameterised** | `def __init__(self):` | `Box()` always starts with `size = 1` |
| **Parameterised** | `def __init__(self, a, b, …):` | `Item("pen", 3)` |

## ❌ No constructor overloading

Some languages (Java, C++) allow several constructors with different parameters. **Python doesn't.** A second `def __init__` simply **replaces** the first, like reassigning a variable.

To support several ways of creating objects, Python uses:
1. **default arguments**: `def __init__(self, x=0, y=0)`
2. **class methods as alternative constructors**: `Date.from_string("10-11-2026")` (Lecture 09)

## Constructor gotchas

| Gotcha | Symptom | Fix |
|--------|---------|-----|
| Mutable default `def __init__(self, items=[])` | objects share one list | `items=None` → `self.items = items or []`, or better the explicit `if … is None` |
| List/dict in the **class body** | shared by every object | create it in `__init__`: `self.members = []` |
| `return` a value from `__init__` | `TypeError: __init__() should return None, not 'int'` | don't return anything |
| Forgetting `self.` | `name = name` just sets a local; the attribute never exists | always `self.name = name` |
| Typo `__int__` / `_init_` | constructor never runs → missing attributes | exactly two underscores each side: `__init__` |
| Counting objects with `self.count += 1` | the class counter stays 0 | `ClassName.count += 1` |

## A constructor that counts objects

```python
class Ticket:
    count = 0                       # class attribute

    def __init__(self, passenger):
        Ticket.count += 1           # bump the SHARED counter
        self.number = Ticket.count  # this ticket's own serial number
        self.passenger = passenger
```

## Exercises

1. Add an `age` parameter (default `None`) to `Student`, and print it in `show`.
2. Add `kelvin` to `Temperature`.
3. Fix `Point` so `Point()` and `Point(5)` both work, using one `__init__`.
4. Reproduce the mutable-default bug, then fix it.

<details><summary>Solutions</summary>

```python
class Point:
    def __init__(self, x=0):
        self.x = x
```
`self.kelvin = celsius + 273.15`.
</details>

**Next →** [Lecture 08: The destructor `__del__`](../08_destructor_del/)
