# Lecture 04: Class vs instance attributes

Run: `python lecture.py`

## Two places data can live

```python
class Car:
    wheels = 4              # CLASS attribute: one copy, shared by all cars
    count = 0

    def __init__(self, brand):
        self.brand = brand  # INSTANCE attribute: each car has its own
        Car.count += 1
```

| | Instance attribute | Class attribute |
|--|-------------------|-----------------|
| Created | in methods: `self.x = ...` | in the class body: `x = ...` |
| Belongs to | one object | the class, so it's **shared** by all objects |
| Stored in | `obj.__dict__` | `Class.__dict__` |
| Use for | data that differs per object (name, balance) | constants, defaults, counters, registries |

## How Python looks up `obj.attr`

```
obj.wheels  →  1. in obj.__dict__?    → use it
               2. in Car.__dict__?    → use it
               3. in parent classes?  (Lecture 09)
               4. nowhere?            → AttributeError
```

Reading through the object finds the class value. **Writing** through the object is different.

## The shadowing gotcha

```python
b.wheels = 3        # creates a NEW instance attribute on b only
a.wheels            # 4  (still reads the class)
b.wheels            # 3  (its own attribute hides the class one)
Car.wheels          # 4
del b.wheels        # remove it, and b sees the class value again
```

Same with counters:

| Code | Effect |
|------|--------|
| `Car.count += 1` | ✅ updates the shared counter |
| `self.count += 1` | ❌ reads the class value, then **creates an instance attribute** on this object; the class counter never changes |

> Rule: **change shared data through the class name** (`Car.count`), or with `type(self).count` / `cls.count` (Lecture 08).

## The mutable class attribute trap

```python
class Team:
    members = []            # ONE list shared by every Team!

    def add(self, name):
        self.members.append(name)   # mutates the shared list (no shadowing: append doesn't assign)
```

Two teams end up with the same members. Fix: create the list in `__init__` (`self.members = []`).

Mutating (`.append`, `[k] = v`) changes the shared object. Assigning (`self.x = ...`) shadows it.

## Good uses of class attributes

| Use | Example |
|-----|---------|
| Constants | `Circle.PI = 3.14159`, `Account.MIN_BALANCE = 500` |
| Defaults that instances may override | `Report.format = "pdf"` |
| Counting objects | `Car.count += 1` in `__init__` |
| Registries / caches | `User.by_email = {}` (careful: shared and mutable, on purpose) |
| Configuration for a whole kind | `Employee.raise_rate = 0.05` |

## Exercises

1. Add `Car.MAX_SPEED = 180`, change it for one car only, and print all three values (two cars + the class).
2. Write `Employee` with a class attribute `raise_rate = 0.05` and a method `apply_raise()`. Then give one employee a special rate.
3. Fix the `Team` class so each team has its own members.
4. Print `Car.__dict__.keys()` and `a.__dict__`. Where does `wheels` live?

**Next →** [Lecture 05: Project: bank account](../05_project_bank_account/)
