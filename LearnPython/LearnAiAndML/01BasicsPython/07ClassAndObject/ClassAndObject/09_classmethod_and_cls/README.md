# Lecture 09: `@classmethod` & `cls`

Run: `python lecture.py`

## The three kinds of methods at a glance

```python
class Demo:
    def instance_method(self):      # receives the OBJECT
        ...

    @classmethod
    def class_method(cls):          # receives the CLASS
        ...

    @staticmethod
    def static_method():            # receives NOTHING automatically
        ...
```

| Kind | Decorator | First parameter | Can use | Call on |
|------|-----------|-----------------|---------|---------|
| Instance method | none | `self` = the object | object data **and** class data | an object |
| **Class method** | `@classmethod` | **`cls` = the class** | **class data only** | the class (or an object) |
| Static method | `@staticmethod` | none | only its arguments | the class (or an object) |

A **decorator** is the `@name` line just above a `def`. It changes how the function behaves. `@classmethod` tells Python: "pass the **class** as the first argument instead of the object".

## What `cls` is

`cls` is the class itself, the same thing as writing `Shop` inside the method. It holds the class **even when you call the method through an object**:

```python
Shop.how_many()      # cls is Shop
pen.how_many()       # cls is STILL Shop (not pen!)
```

Like `self`, `cls` is a convention, not a keyword.

## Use case 1: reading/changing class-wide data

```python
class Shop:
    discount = 0                       # class attribute shared by all items

    def __init__(self, item, price):
        self.item, self.price = item, price

    def final_price(self):             # instance method: needs THIS item's price
        return self.price * (100 - self.discount) / 100

    @classmethod
    def set_discount(cls, percent):    # class method: changes the shared setting
        cls.discount = percent

Shop.set_discount(10)                  # every item now gets 10% off
```

> Why `cls.discount` instead of `Shop.discount`? Same result here, but `cls` doesn't hard-code the class name, so renaming the class won't break the method.

> ⚠️ A class method has **no `self`**, so it can't read `self.price`. Writing it would give `NameError: name 'self' is not defined`.

## Use case 2: counting & tracking objects

```python
class Student:
    count = 0
    all_students = []

    def __init__(self, name):
        self.name = name
        Student.count += 1
        Student.all_students.append(self)

    @classmethod
    def total(cls):
        return cls.count

    @classmethod
    def names(cls):
        return [s.name for s in cls.all_students]
```

## Use case 3 (the most important): alternative constructors (factories)

Python has only **one** `__init__`. How do you create objects from different kinds of input? Write a **class method that returns a new object**:

```python
class Date:
    def __init__(self, day, month, year):
        self.day, self.month, self.year = day, month, year

    @classmethod
    def from_string(cls, text):            # "10-11-2026"
        d, m, y = text.split("-")
        return cls(int(d), int(m), int(y)) # cls(...) runs the normal __init__

    @classmethod
    def from_dict(cls, data):
        return cls(data["day"], data["month"], data["year"])

    @classmethod
    def today(cls):
        import datetime
        t = datetime.date.today()
        return cls(t.day, t.month, t.year)

a = Date(5, 11, 2026)                      # the main constructor
b = Date.from_string("10-11-2026")         # alternative constructors
c = Date.from_dict({"day": 1, "month": 1, "year": 2027})
```

Step by step for `Date.from_string("10-11-2026")`:

| Step | What happens |
|------|--------------|
| 1 | `from_string` runs with `cls = Date`, `text = "10-11-2026"` |
| 2 | `split` gives `"10"`, `"11"`, `"2026"` |
| 3 | `cls(10, 11, 2026)` is `Date(10, 11, 2026)`, so `__init__` runs |
| 4 | the new object is returned and stored in `b` |

Python's own library is full of these: `dict.fromkeys(...)`, `datetime.fromisoformat(...)`, `int.from_bytes(...)`.

## Use case 4: class-level configuration / registries

Settings shared by all objects (tax rate, currency, units, a registry of valid codes) and the methods that change them.

## Exercises

1. Add `@classmethod reset_discount(cls)`.
2. Add `Date.from_tuple(cls, t)` for `(day, month, year)`.
3. Make `Student.names()` return names sorted alphabetically.
4. Try to read `self.price` inside a class method. Read the error.

<details><summary>Solutions</summary>

```python
@classmethod
def reset_discount(cls):
    cls.discount = 0

@classmethod
def from_tuple(cls, t):
    return cls(*t)
```
</details>

**Next →** [Lecture 10: `@staticmethod`](../10_staticmethod/)
