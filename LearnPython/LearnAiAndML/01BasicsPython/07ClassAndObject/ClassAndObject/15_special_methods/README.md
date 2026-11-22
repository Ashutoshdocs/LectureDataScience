# Lecture 15: Special ("dunder") methods

Run: `python lecture.py`

**Special methods** have double underscores on both sides (`__init__`, `__str__`). **You define them; Python calls them** at the right moment, when you use built-in syntax on your objects. You've already met three: `__init__`, `__del__` and (briefly) `__enter__`/`__exit__`.

## Text: `__str__` and `__repr__`

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):                 # for humans: print(p), str(p), f"{p}"
        return f"({self.x}, {self.y})"

    def __repr__(self):                # for developers: repr(p), lists, the shell
        return f"Point(x={self.x}, y={self.y})"
```

| | `__str__` | `__repr__` |
|---|---|---|
| Audience | end users | programmers / debugging |
| Used by | `print`, `str()`, f-strings | `repr()`, the shell, **items inside lists/dicts** |
| Goal | readable | unambiguous; ideally valid code to recreate the object |
| Fallback | uses `__repr__` if no `__str__` | default `<__main__.Point object at 0x…>` |

> If you write only one, write `__repr__`. `print` falls back to it.

## Comparison: `__eq__`, `__lt__` & friends

By default `a == b` is the same as `a is b` (same object?). Define `__eq__` to compare **by data**:

```python
def __eq__(self, other):
    if not isinstance(other, Point):
        return NotImplemented            # let Python try other options / return False
    return (self.x, self.y) == (other.x, other.y)
```

| Operator | Method |
|----------|--------|
| `==` / `!=` | `__eq__` / `__ne__` (`!=` uses `__eq__` automatically) |
| `<` `<=` `>` `>=` | `__lt__` `__le__` `__gt__` `__ge__` |

Defining `__lt__` makes `sorted(objects)`, `min()` and `max()` work without a `key=`.

> ⚠️ Defining `__eq__` makes objects **unhashable** (can't go in a `set` or be dict keys) unless you also define `__hash__`. If your object is immutable, add `def __hash__(self): return hash((self.x, self.y))`.

## Arithmetic: `__add__`, `__sub__`, `__mul__`

```python
def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)   # p1 + p2 returns a NEW object
```

Also `__sub__` (`-`), `__mul__` (`*`), `__truediv__` (`/`), and `__iadd__` for `+=`.

## Containers: `__len__`, `__getitem__`, `__contains__`, `__iter__`

Make your object behave like a list:

| You write | Python calls |
|-----------|--------------|
| `len(cart)` | `cart.__len__()` |
| `cart[0]` | `cart.__getitem__(0)` |
| `"pen" in cart` | `cart.__contains__("pen")` |
| `for item in cart:` | `cart.__iter__()` |
| `if cart:` | `__bool__`, or `__len__` ≠ 0 |

## Callable objects: `__call__`

```python
class Multiplier:
    def __init__(self, n): self.n = n
    def __call__(self, x): return x * self.n

triple = Multiplier(3)
triple(10)        # 30: the object is used like a function
```

## Cheat sheet

| Category | Methods | Triggered by |
|----------|---------|--------------|
| Lifecycle | `__init__`, `__del__` | creation, destruction |
| Text | `__str__`, `__repr__`, `__format__` | `print`, `repr`, f-strings |
| Compare | `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__hash__` | `==`, `<`, `sorted`, sets/dicts |
| Maths | `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__iadd__` | `+ - * / +=` |
| Container | `__len__`, `__getitem__`, `__setitem__`, `__contains__`, `__iter__`, `__bool__` | `len`, `[]`, `in`, `for`, `if` |
| Call | `__call__` | `obj(...)` |
| Context | `__enter__`, `__exit__` | `with` |

> Never call special methods directly (`p.__str__()`); use the built-in syntax (`str(p)`). And don't invent new `__names__`; they're reserved for Python.

## Exercises

1. Remove `__str__` from `Point`. What does `print(p)` show now?
2. Add `__sub__` and `__mul__` (multiply by a number).
3. Make `Money` objects sortable and put them in a set.
4. Add `__getitem__` and `__iter__` to `Cart` and loop over it.

<details><summary>Solutions</summary>

1. The `__repr__` text, `Point(x=3, y=4)`.
See `lecture.py` for 2–4.
</details>

**Next →** [Lecture 16: Working with objects](../16_working_with_objects/)
