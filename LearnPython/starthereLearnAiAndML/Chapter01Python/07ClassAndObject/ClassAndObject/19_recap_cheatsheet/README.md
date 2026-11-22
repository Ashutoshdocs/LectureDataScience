# Lecture 19: Recap & cheat sheet

Run: `python lecture.py` (a self-test: predict each answer before reading it)

## A complete class template

```python
TAX = 0.18                                   # global constant

def with_tax(x):                             # GLOBAL FUNCTION: general utility
    return x * (1 + TAX)

class Product:
    """One product in the shop."""           # docstring

    count = 0                                # CLASS ATTRIBUTE: shared

    def __init__(self, name, price=0):       # CONSTRUCTOR
        self.name = name                     # INSTANCE ATTRIBUTE
        self.price = price                   # goes through the property setter
        self._history = []                   # per-object list: always in __init__
        Product.count += 1
        self._counted = True                 # see the __del__ gotcha (Lecture 11)

    @property
    def price(self):                         # GETTER
        return self._price

    @price.setter
    def price(self, value):                  # SETTER with validation
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value

    @property
    def price_with_tax(self):                # COMPUTED, read-only property
        return with_tax(self.price)

    def discount(self, percent):             # INSTANCE METHOD: uses self
        self.price *= (100 - percent) / 100
        return self                          # allows chaining

    @classmethod
    def from_csv(cls, line):                 # CLASS METHOD: alternative constructor
        name, price = line.split(",")
        return cls(name, float(price))

    @classmethod
    def how_many(cls):                       # CLASS METHOD: class-wide data
        return cls.count

    @staticmethod
    def rupees(x):                           # STATIC METHOD: helper, no self/cls
        return f"Rs {x:,.2f}"

    def __str__(self):                       # SPECIAL METHOD: print(p)
        return f"{self.name}: {self.rupees(self.price)}"

    def __repr__(self):                      # SPECIAL METHOD: debugging / lists
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):                 # SPECIAL METHOD: ==
        return isinstance(other, Product) and (self.name, self.price) == (other.name, other.price)

    def __del__(self):                       # DESTRUCTOR (runs even if __init__ failed!)
        if getattr(self, "_counted", False):
            Product.count -= 1
```

## Which function type?

| Needs… | Use | Signature | Call |
|--------|-----|-----------|------|
| this object's data | **instance method** | `def f(self, …)` | `obj.f(…)` |
| class-wide data / create objects | **class method** | `@classmethod def f(cls, …)` | `Class.f(…)` |
| neither, but belongs to the class | **static method** | `@staticmethod def f(…)` | `Class.f(…)` |
| nothing class-related | **global function** | `def f(…)` outside the class | `f(…)` |
| attribute-style access with checks | **property** | `@property` / `@x.setter` / `@x.deleter` | `obj.x`, `obj.x = v` |
| run at creation | **constructor** | `def __init__(self, …)` | `Class(…)` |
| run at destruction | **destructor** | `def __del__(self)` | automatic |
| built-in syntax (`print`, `==`, `+`, `len`) | **special method** | `__str__`, `__eq__`, `__add__`, `__len__`… | automatic |

## `self` vs `cls`

| | `self` | `cls` |
|---|---|---|
| Is | the **object** the method was called on | the **class** the method was called on |
| Appears in | instance methods, properties, special methods | class methods |
| Use it for | `self.name`, `self.other_method()` | `cls.count`, `cls(...)` to create objects |
| Passed by | Python, automatically | Python, automatically |
| A keyword? | no, a convention | no, a convention |

## Attributes

| | Instance attribute | Class attribute |
|---|---|---|
| Create | `self.x = …` in `__init__` | `x = …` in the class body |
| Copies | one per object | one shared |
| Change for everyone | n/a | `ClassName.x = …` (never through an object!) |
| Mutable lists/dicts | ✅ here | ❌ shared by accident |

Lookup: `obj.x` → object → class → `AttributeError`. Plain `x` → Local → Enclosing → Global → Built-in.

## Naming conventions

| Name | Meaning |
|------|---------|
| `ClassName` | classes: CapitalizedWords |
| `method_name`, `attribute` | snake_case |
| `_internal` | "please don't use from outside" (convention only) |
| `__private` | name-mangled to `_ClassName__private` |
| `__special__` | Python's reserved special methods |
| `CONSTANT` | class/global constants |

## Top 15 mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `self` in a method | `def f(self, …)` |
| `name = name` in `__init__` | `self.name = name` |
| `__int__` / `_init_` typos | exactly `__init__` |
| Returning a value from `__init__` | return nothing |
| Mutable default `def __init__(self, items=[])` | `items=None` → new list inside |
| List/dict in the class body | create it in `__init__` |
| `self.count += 1` for a class counter | `ClassName.count += 1` |
| Assigning a class attribute through an object | assign through the class |
| Bare class attribute name inside a method (`PI`) | `self.PI` / `ClassName.PI` |
| Calling a sibling method without `self.` | `self.other()` |
| `self` inside a static/class method | use an instance method, or `cls` |
| Property getter returning `self.x` | store the value in `self._x` |
| Expecting two constructors | defaults or `@classmethod` factories |
| `__eq__` without `__hash__` (sets/dicts break) | add `__hash__` for immutable data |
| Relying on exactly when `__del__` runs | explicit `close()` or `with` |

## Where to go next

- **Inheritance & polymorphism**: classes built on other classes (`class SavingsAccount(BankAccount)`), `super()`
- **`@dataclass`**: auto-generates `__init__`, `__repr__`, `__eq__` for data-holding classes
- **Abstract base classes & protocols**: defining interfaces
- **Type hints** for attributes and methods
