# Lecture 03: Parameters & arguments

Run: `python lecture.py`

## Parameter vs argument

```python
def greet(name, greeting):      # name, greeting  → PARAMETERS (placeholders in the definition)
    print(f"{greeting}, {name}!")

greet("Asha", "Hello")          # "Asha", "Hello" → ARGUMENTS (actual values in the call)
```

When the call runs, each parameter becomes a **local variable** holding its argument.

## 1. Positional arguments: matched by position

```python
def describe(name, age, city): ...
describe("Asha", 25, "Pune")       # name="Asha", age=25, city="Pune"
describe(25, "Asha", "Pune")       # runs, but WRONG: name=25, age="Asha"
```

Order matters. Wrong order gives a silent bug or a confusing error.

## 2. Keyword arguments: matched by name

```python
describe(city="Pune", name="Asha", age=25)    # any order, self-documenting
describe("Asha", city="Pune", age=25)         # mix: positional FIRST, then keyword
```

| Positional | Keyword |
|-----------|---------|
| short | longer, but **readable** (`send(to=..., cc=...)`) |
| order matters | order doesn't matter |
| fine for 1–2 obvious arguments | best for many arguments or booleans (`resize(img, keep_ratio=True)`) |

Rules:
- Positional arguments must come **before** keyword arguments: `f(name="A", 25)` is a `SyntaxError`.
- You can't give the same parameter twice: `f("Asha", name="Ravi")` is a `TypeError`.

## 3. Default parameter values: optional arguments

```python
def power(base, exponent=2):        # exponent is optional
    return base ** exponent

power(5)          # 25
power(5, 3)       # 125
power(5, exponent=0)
```

- Parameters **with** defaults must come **after** those without: `def f(a=1, b)` is a `SyntaxError`.
- Use defaults for the **common case**, so simple calls stay simple.

## ⚠️ The mutable default trap

Defaults are evaluated **once, when `def` runs**, not on every call. A mutable default (list, dict, set) is therefore **shared across calls**:

```python
def add_item(item, basket=[]):       # ONE list, created once
    basket.append(item)
    return basket

add_item("pen")      # ['pen']
add_item("book")     # ['pen', 'book']   ← surprise!
```

**Fix:** use `None` as the default and create a new list inside:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

## 4. Passing mutable vs immutable arguments

Python passes **references to objects** ("pass by object reference"):

| Argument type | Can the function change the caller's value? |
|---------------|---------------------------------------------|
| immutable (`int`, `str`, `tuple`) | ❌ reassigning inside only changes the local name |
| mutable (`list`, `dict`, `set`, objects) | ✅ **in-place** changes (`append`, `d[k] = v`) are visible to the caller |

```python
def add_bonus(marks):      marks.append(5)        # caller's list CHANGES
def reset(n):              n = 0                  # caller's int does NOT change
```

If you don't want to modify the caller's list, work on a copy: `marks = marks.copy()`, or return a new list.

## Common errors

| Error | Cause |
|-------|-------|
| `TypeError: f() missing 1 required positional argument: 'age'` | too few arguments |
| `TypeError: f() takes 2 positional arguments but 3 were given` | too many |
| `TypeError: f() got an unexpected keyword argument 'nmae'` | typo in a keyword |
| `TypeError: f() got multiple values for argument 'name'` | same parameter twice |

## Exercises

1. Write `make_email(first, last, domain="company.com")`.
2. Call `describe` with all keyword arguments in reverse order.
3. Reproduce the mutable-default bug, then fix it.
4. Write `remove_negatives(numbers)` that returns a new list **without** changing the original.

<details><summary>Solutions</summary>

```python
def make_email(first, last, domain="company.com"):
    return f"{first.lower()}.{last.lower()}@{domain}"

def remove_negatives(numbers):
    return [n for n in numbers if n >= 0]
```
</details>

**Next →** [Lecture 04: The return statement](../04_return_statement/)
