# Lecture 07: Properties: getters, setters & computed attributes

Run: `python lecture.py`

## The problem

You start with a plain attribute:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

t.celsius = -500     # physically impossible, but nothing stops it
```

The Java-style fix is to write `get_celsius()` / `set_celsius()` methods, but then **every user must change** `t.celsius` to `t.get_celsius()`. Python has a better tool.

## `@property`: methods that look like attributes

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius          # goes through the setter below!

    @property
    def celsius(self):                  # GETTER: runs on  t.celsius
        return self._celsius

    @celsius.setter
    def celsius(self, value):           # SETTER: runs on  t.celsius = value
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):               # COMPUTED, read-only
        return self._celsius * 9 / 5 + 32
```

| You write | Python runs |
|-----------|-------------|
| `t.celsius` | the getter → `return self._celsius` |
| `t.celsius = 30` | the setter → validate, then store in `self._celsius` |
| `t.fahrenheit` | the getter → calculated fresh each time |
| `t.fahrenheit = 50` | `AttributeError`: no setter, so it's read-only |
| `del t.celsius` | the deleter, if you define `@celsius.deleter` |

The real value lives in a **differently named** attribute (`_celsius`). If the getter returned `self.celsius`, it would call itself forever (`RecursionError`).

## When to use what

| Situation | Use |
|-----------|-----|
| simple data, no rules | a **plain attribute** (`self.name = name`). Don't add properties "just in case": you can switch later without breaking users |
| value must be validated | property **with setter** |
| value must not be changed from outside | property **without setter** (read-only) |
| value is derived from others (area, age, full_name) | **computed** property: always in sync, never stale |
| work is slow (database, network) | a **method** (`load_orders()`), because property access looks cheap and readers won't expect a delay |
| expensive but fixed | `@functools.cached_property`: computed once, then stored |

## Why properties are a big deal: you can change your mind later

Version 1 ships with `self.price = price`. Months later you need validation. Turn it into a property and **no calling code changes**: `item.price = 10` still works, now with checks. That's encapsulation without the boilerplate.

## Classic patterns

```python
@property
def full_name(self):                    # computed
    return f"{self.first} {self.last}"

@full_name.setter
def full_name(self, text):              # setter that updates several attributes
    self.first, self.last = text.split(" ", 1)

@property
def balance(self):                      # read-only view of private data
    return self._balance
```

## Common mistakes

| Mistake | Effect |
|---------|--------|
| getter returns `self.celsius` | infinite recursion → `RecursionError` |
| setter named differently from the getter (`@celsius.setter def set_c`) | creates a separate property; the original stays read-only |
| calling it like a method: `t.fahrenheit()` | `TypeError: 'float' object is not callable` |
| storing in `self._celsius` in `__init__` directly | skips validation; assign `self.celsius` instead |

## Exercises

1. Add a read-only `kelvin` property to `Temperature`.
2. Write `Product` with a `price` property that rejects negatives and rounds to 2 decimals.
3. Write `Person` with `first`, `last` and a `full_name` property with a setter.
4. Use `@functools.cached_property` for a "slow" `report` attribute and show it's computed once.

**Next →** [Lecture 08: Class methods & static methods](../08_classmethod_staticmethod/)
