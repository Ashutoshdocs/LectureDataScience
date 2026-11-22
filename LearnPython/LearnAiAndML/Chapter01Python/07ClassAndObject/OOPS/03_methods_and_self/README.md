# Lecture 03: Methods & `self`

Run: `python lecture.py`

## What is a method?

A **method** is a function defined **inside a class**. Attributes are what an object *has*; methods are what it *can do*.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, by=1):     # a method: first parameter is self
        self.count += by

    def show(self):
        print("count =", self.count)

c = Counter()
c.increment(5)
c.show()          # count = 5
```

## The secret: `obj.method(x)` is `Class.method(obj, x)`

| You write | Python actually runs |
|-----------|----------------------|
| `c.increment(5)` | `Counter.increment(c, 5)` |
| `c.show()` | `Counter.show(c)` |

So **`self` is simply the object before the dot**. That's how one method, written once, works on every object: each call passes a different `self`.

```python
a, b = Counter(), Counter()
a.increment()     # self is a → changes a.count only
b.increment(10)   # self is b → changes b.count only
```

## Why methods instead of plain functions?

| Plain function | Method |
|----------------|--------|
| `increment(counter, 5)` | `counter.increment(5)` |
| lives anywhere; you must remember which data it works on | lives **with** the data it works on |
| can't have the same name for different types | `circle.area()` and `square.area()` can co-exist (polymorphism, Lecture 13) |

## Kinds of methods by what they do

| Kind | Example | Returns |
|------|---------|---------|
| **Query** (reads state) | `get_total()`, `is_empty()` | a value; doesn't change the object |
| **Command** (changes state) | `add_item()`, `reset()` | usually `None`, or `self` for chaining |
| **Helper** (internal) | `_recalculate()` | used by other methods; leading `_` = "internal" |

Keep queries and commands separate where you can. It makes code predictable.

## Methods calling other methods

Inside a class, use `self.other_method()`:

```python
class Cart:
    def add(self, item, price):
        self.items.append((item, price))
        self._log(f"added {item}")      # call another method on the same object

    def _log(self, msg):
        self.history.append(msg)
```

Forgetting `self.` (writing `_log(...)`) gives `NameError`: the method isn't a global name.

## Method chaining

If a command returns `self`, calls can be chained:

```python
class Query:
    def where(self, cond):
        self.filters.append(cond)
        return self               # ← makes chaining possible

Query("users").where("age > 18").where("city = 'Pune'").limit(10)
```

## Bound methods

`c.show` without brackets is a **bound method**: a method with its `self` already attached. You can store it and call it later:

```python
action = c.increment      # bound to c
action(3)                 # same as c.increment(3)
```

## Common mistakes

| Mistake | Error |
|---------|-------|
| `def show():` (forgot `self`) | `TypeError: show() takes 0 positional arguments but 1 was given` |
| `count += 1` instead of `self.count += 1` | `UnboundLocalError` / `NameError` |
| `c.show` (no brackets) | no call happens; you get the method object |
| calling `_helper()` instead of `self._helper()` | `NameError` |

## Exercises

1. Add `reset()` and `decrement(by=1)` to `Counter`. Don't let the count go below 0.
2. Give `Cart` a `total()` query and an `apply_discount(percent)` command.
3. Make `add()` return `self` and chain three calls.
4. Call `Counter.show(c)` directly and confirm it matches `c.show()`.

**Next →** [Lecture 04: Class vs instance attributes](../04_class_vs_instance_attributes/)
