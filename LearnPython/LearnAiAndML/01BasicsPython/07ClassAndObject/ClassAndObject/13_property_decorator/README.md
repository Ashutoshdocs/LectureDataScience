# Lecture 13: `@property`, Pythonic getters, setters & deleters

Run: `python lecture.py`

## The idea

A **property** looks like a normal attribute to the caller (`acc.balance`, `acc.balance = 500`), but behind the scenes Python **calls your methods**. You get the validation of getters/setters without the `get_`/`set_` noise.

```python
class Account:
    def __init__(self, owner, balance=0):
        self._owner = owner
        self.balance = balance            # goes through the setter below!

    @property
    def balance(self):                    # GETTER: runs on  acc.balance
        return self._balance

    @balance.setter
    def balance(self, value):             # SETTER: runs on  acc.balance = value
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    @balance.deleter
    def balance(self):                    # DELETER: runs on  del acc.balance
        print("closing balance")
        del self._balance
```

| Caller writes | Python runs |
|---------------|-------------|
| `acc.balance` | the `@property` getter |
| `acc.balance = 500` | the `@balance.setter` |
| `acc.balance += 500` | getter, then setter |
| `del acc.balance` | the `@balance.deleter` |

### The three rules

1. The getter, setter and deleter **all have the same name** (`balance`).
2. The getter comes first with `@property`; the others use `@<name>.setter` / `@<name>.deleter`.
3. Store the real value under a **different** name (`self._balance`). Using `self.balance` inside the getter would call the getter again, forever → `RecursionError`.

## Read-only properties

Define only the getter. Assigning raises `AttributeError: property 'owner' of 'Account' object has no setter`:

```python
@property
def owner(self):
    return self._owner
```

## Computed properties

Values calculated on the fly, always up to date, never stored:

```python
class Rectangle:
    def __init__(self, w, h):
        self.width, self.height = w, h

    @property
    def area(self):
        return self.width * self.height      # r.area, no brackets
```

Change `width` and `area` updates automatically. Compare with storing `self.area` in `__init__`, which goes stale.

## Validation in `__init__` for free

Write `self.balance = balance` (no underscore) in `__init__`. The assignment goes through the setter, so the **same rules** apply at creation and afterwards. No duplicated checks.

## Converting a public attribute into a property later

Start simple: `self.price = price`. Months later you need validation? Add a property named `price` and store the value in `_price`. **Every existing `obj.price` line in your program keeps working.** This is why Python programmers don't write getter/setter methods up front.

## The `property()` function (older style)

The decorators are shorthand for:

```python
class Temp:
    def _get(self): return self._c
    def _set(self, v): self._c = v
    celsius = property(_get, _set, doc="temperature in °C")
```

You'll see this in older code. It does exactly the same thing.

## Methods vs getter/setter methods vs properties

| | `get_x()` / `set_x()` methods | `@property` |
|---|---|---|
| Caller syntax | `obj.get_x()`, `obj.set_x(5)` | `obj.x`, `obj.x = 5` |
| Validation | ✅ | ✅ |
| Read-only | no setter method | no `.setter` |
| Computed values | ✅ | ✅ |
| Can be added later without changing callers | ❌ | ✅ |
| Pythonic? | works, but Java-style | ✅ |

**When should something be a method instead of a property?** If it **takes arguments**, is **slow** (database, network), or **changes things** (`deposit`, `save`), make it a method. Properties should feel like reading a variable: fast and without surprises.

## Exercises

1. Add a read-only `owner` property and try to assign it.
2. Add a `Temperature` class with a `celsius` property (≥ −273.15) and a computed `fahrenheit` property **with a setter** that converts back to Celsius.
3. Make `Rectangle.width` a property that rejects values ≤ 0.
4. Write a getter that accidentally uses `self.balance` instead of `self._balance`. What error do you get?

<details><summary>Solutions</summary>

```python
@property
def fahrenheit(self):
    return self.celsius * 9 / 5 + 32

@fahrenheit.setter
def fahrenheit(self, f):
    self.celsius = (f - 32) * 5 / 9     # reuses the celsius validation
```
4. `RecursionError: maximum recursion depth exceeded`.
</details>

**Next →** [Lecture 14: Scope in classes](../14_scope_in_classes/)
