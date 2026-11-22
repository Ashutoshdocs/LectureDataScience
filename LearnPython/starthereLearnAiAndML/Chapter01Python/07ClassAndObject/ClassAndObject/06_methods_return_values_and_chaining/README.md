# Lecture 06: Return values, methods calling methods, chaining & global functions

Run: `python lecture.py`

## 1. Parameters and return values

Methods work like ordinary functions: parameters after `self`, and `return` to hand back a result.

```python
class Rectangle:
    def set_size(self, width, height):     # "setter-style": stores data, returns None
        self.width = width
        self.height = height

    def area(self):                        # "calculation": returns a result
        return self.width * self.height
```

> **Prefer `return` over `print`** inside methods. Then the caller decides what to do with the result: print it, store it, compare it, double it.

## 2. Methods calling other methods: `self.method()`

```python
class Order:
    def subtotal(self):
        return sum(self.prices)

    def tax(self):
        return self.subtotal() * 0.1           # call a sibling method through self

    def total(self):
        return self.subtotal() + self.tax()
```

A bare `subtotal()` raises `NameError`. Methods are **not** global names; they live on the class and are reached through `self`.

Control flow for `o.total()`:

```
 total ─► subtotal ─► (150) ─► back in total
       ─► tax ─► subtotal ─► (150) ─► back in tax (15.0) ─► back in total
       ─► returns 165.0
```

Small methods that call each other are easier to read, test and change.

## 3. Method chaining (fluent interface)

If a method **returns `self`**, calls can be chained:

```python
class Query:
    def where(self, cond):
        self.conditions.append(cond)
        return self                 # ← the trick

    def limit(self, n):
        self.n = n
        return self

q = Query("users").where("age > 18").where("city = 'Pune'").limit(10)
```

Common in libraries (pandas, Polars and SQL builders all work this way).

## 4. Global function vs method

Both can do the same job. The difference is **where the function lives** and **how the object gets in**.

```python
def area_of(rect):                 # global function
    return rect.width * rect.height

class Rect:
    def area(self):                # method
        return self.width * self.height

area_of(r)                         # object passed explicitly
r.area()                           # object passed automatically as self
```

| | Global function | Method |
|---|---|---|
| Defined | top level of the file | inside a class |
| Called as | `area_of(r)` | `r.area()` |
| Object arrives | as a normal argument | automatically, as `self` |
| `type(...)` | `function` | `method` (when reached through an object) |
| Best for | work involving **several unrelated things**, or general utilities | behaviour that **belongs to one object** |

**Rule of thumb:** if a function mostly works with one object's data, it probably belongs inside that object's class.

## Exercises

1. Add `is_square(self)` returning `True`/`False`.
2. Add `scale(self, factor)` that multiplies both sides and **returns `self`** so it can be chained: `r.scale(2).area()`.
3. Add `discount(self)` to `Order` and subtract it in `total`.
4. Write a global function `bigger(r1, r2)` that returns the rectangle with the larger area.

<details><summary>Solutions</summary>

```python
def is_square(self):
    return self.width == self.height

def scale(self, factor):
    self.width *= factor
    self.height *= factor
    return self

def bigger(r1, r2):
    return r1 if r1.area() >= r2.area() else r2
```
</details>

**Next →** [Lecture 07: The constructor `__init__`](../07_constructor_init/)
