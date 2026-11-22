# Lecture 09: Type hints & docstrings: documenting functions

Run: `python lecture.py`

## Type hints (annotations)

```python
def total_price(price: float, qty: int = 1, discount: float = 0.0) -> float:
    return price * qty * (1 - discount)
```

- `param: type` describes what each parameter should be.
- `-> type` describes what the function returns.
- Stored in `total_price.__annotations__`.

> ⚠️ **Python does NOT enforce hints at runtime.** With `def double(n: int) -> int: return n * 2`, calling `double("5")` runs without complaint and returns `"55"`. Hints are for **humans, editors and checkers** like `mypy`, which catch such mistakes **before** running.

### Why use them?

| Benefit | How |
|---------|-----|
| Readable signatures | the types are documentation you can't forget to update |
| Editor help | autocomplete and warnings while typing |
| Catch bugs early | `mypy file.py` finds type mistakes without running |
| Safer refactoring | change a type; the checker shows every call to fix |

### Common hints (Python 3.10+)

| Hint | Meaning |
|------|---------|
| `int`, `float`, `str`, `bool` | basic types |
| `list[int]`, `dict[str, float]`, `tuple[int, int]`, `set[str]` | collections with element types |
| `int \| None` | an int **or** None (e.g. "not found") |
| `int \| float` | either type |
| `-> None` | returns nothing useful |
| `Callable[[int], int]` (from `collections.abc`) | a function taking an int, returning an int |
| `Any` (from `typing`) | anything: opts out of checking |
| `*args: int`, `**kwargs: str` | the type of **each** extra argument |

## Docstrings

A docstring is the first statement of a function body: a string that explains it.

```python
def bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index.

    Args:
        weight_kg: Weight in kilograms (must be > 0).
        height_m: Height in metres (must be > 0).

    Returns:
        The BMI rounded to 1 decimal place.

    Raises:
        ValueError: If weight or height is not positive.

    Example:
        >>> bmi(70, 1.75)
        22.9
    """
```

| Part | Content |
|------|---------|
| First line | a one-sentence summary, in the imperative ("Calculate…", "Return…") |
| Args | each parameter: meaning, units, constraints |
| Returns | what comes back |
| Raises | errors the caller should expect |
| Example | a sample call (can be tested with `doctest`) |

Read it with `help(bmi)` or `bmi.__doc__`. Editors show it on hover.

### Docstring vs comment

| Docstring `"""…"""` | Comment `# …` |
|---------------------|---------------|
| **what** the function does and how to call it | **why** a tricky line is written that way |
| for the caller | for the person editing the code |
| available at runtime (`help`) | ignored by Python |

## Testing examples in docstrings: `doctest`

```python
import doctest
doctest.testmod()     # runs every >>> example in the file's docstrings and checks the output
```

`lecture.py` does this.

## Exercises

1. Add type hints and a docstring to `make_email(first, last, domain="company.com")`.
2. Call a hinted function with the wrong type. Does Python stop you?
3. Write `find_user(users: list[dict], name: str) -> dict | None`.
4. Add a `>>>` example to a docstring and run `doctest`.

<details><summary>Solutions</summary>

2. No. Hints aren't enforced at runtime. A checker like `mypy` would flag it.
</details>

**Next →** [Lecture 10: Functions as objects](../10_functions_as_objects/)
