# Lecture 08: Class methods & static methods

Run: `python lecture.py`

## Three kinds of methods

| Kind | Decorator | First parameter | Can access | Called as |
|------|-----------|-----------------|------------|-----------|
| **Instance method** | none | `self` (the object) | the object **and** the class | `obj.m()` |
| **Class method** | `@classmethod` | `cls` (the class) | the class (not a specific object) | `Class.m()` or `obj.m()` |
| **Static method** | `@staticmethod` | none | only its own arguments | `Class.m()` or `obj.m()` |

```python
class Date:
    def __init__(self, day, month, year):           # instance-level setup
        self.day, self.month, self.year = day, month, year

    def show(self):                                 # instance method: needs THIS date
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

    @classmethod
    def from_string(cls, text):                     # class method: builds a new object
        d, m, y = map(int, text.split("-"))
        return cls(d, m, y)

    @staticmethod
    def is_leap(year):                              # static: plain helper, no self or cls
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

## `@classmethod`: when you need the class, not an object

### Use 1: alternative constructors (the main use)

`__init__` gives you one way to create objects. Class methods add more, with clear names:

```python
Date(13, 11, 2026)               # normal
Date.from_string("13-11-2026")   # from text
Date.today()                     # from the system clock
Employee.from_csv_row(row)       # from a file row
User.from_dict(json_data)        # from an API response
```

Python itself does this: `dict.fromkeys(...)`, `datetime.fromisoformat(...)`, `int.from_bytes(...)`.

### Why `cls(...)` instead of `Date(...)`?

`cls` is **whatever class the method was called on**. If `IndianDate(Date)` calls `IndianDate.from_string(...)`, then `cls` is `IndianDate`, so you get the right type automatically. Hard-coding `Date(...)` would always build the parent.

### Use 2: working with class-level data

```python
@classmethod
def set_raise_rate(cls, rate):
    cls.raise_rate = rate      # change for the whole class
```

## `@staticmethod`: a function that lives in the class

It gets no `self` and no `cls`. Use it for a helper that **logically belongs** with the class but doesn't need its data: validators, converters, formulas.

```python
Date.is_leap(2024)        # True
Employee.is_valid_email("a@b.com")
```

> If a static method doesn't really belong with the class, make it a normal module-level function instead. Both are fine Python.

## How to choose

```
Does the method need data from a particular object (self.x)?
   ├─ yes → instance method
   └─ no → Does it need the class (to create objects, or read/change class data)?
             ├─ yes → @classmethod
             └─ no  → @staticmethod (or a plain function outside the class)
```

## Common mistakes

| Mistake | Effect |
|---------|--------|
| forgetting `@classmethod` but naming the parameter `cls` | `cls` receives the **object**, not the class |
| using `self.x` inside a `@staticmethod` | `NameError`: there is no `self` |
| `return Date(...)` in a class method | subclasses get parent objects |
| `@staticmethod` that changes class data via `ClassName.x` | works, but `@classmethod` is the correct tool |

## Exercises

1. Add `Date.today()` using `datetime.date.today()`.
2. Add `Employee.from_csv("Asha,IT,50000")` and `Employee.is_valid_salary(x)`.
3. Create `class IndianDate(Date)` with a `show()` that prints `13-Nov-2026`, and check that `IndianDate.from_string(...)` returns an `IndianDate`.
4. Write a class method that counts how many objects were created.

**Next →** [Lecture 09: Inheritance basics](../09_inheritance_basics/)
