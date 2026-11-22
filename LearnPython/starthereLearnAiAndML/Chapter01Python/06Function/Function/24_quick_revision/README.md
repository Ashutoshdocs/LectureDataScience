# Lecture 24: Quick revision: the whole course on one page

Run: `python lecture.py` for a 25-question self-test (prints the answers and checks every snippet).

## 1. Defining & calling (Lectures 01–02)

```python
def greet(name):
    """Return a greeting."""        # docstring
    return f"Hello, {name}"

greet("Asha")       # call → runs the body; greet without () is the function object
```
- **Why functions:** reuse (DRY), organise, test, name an idea.
- Each call gets a **frame** on the **call stack**. Tracebacks read bottom-up for the error.
- `if __name__ == "__main__": main()` runs code only when the file is run directly.

## 2. Parameters & arguments (03, 06–08)

| Kind | Syntax | Notes |
|------|--------|-------|
| positional | `f(1, 2)` | matched by order |
| keyword | `f(b=2, a=1)` | matched by name; order free |
| default | `def f(a, b=10)` | **never** a mutable default → use `None` |
| `*args` | `def f(*args)` | extra positionals → **tuple** |
| `**kwargs` | `def f(**kwargs)` | extra keywords → **dict** |
| keyword-only | `def f(a, *, b)` | `b` must be named |
| positional-only | `def f(a, /, b)` | `a` can't be named |

Full order: `def f(pos_only, /, normal, default=1, *args, kw_only, **kwargs)`
Unpacking at the call: `f(*my_list)`, `f(**my_dict)`. Arguments are passed by **object reference**: mutating a list inside a function changes it outside.

## 3. Return (04)

- `return` ends the function. No `return` means `None`.
- `return a, b` returns a tuple → `x, y = f()`.
- **Return, don't print**, so the caller can use the value. Use guard clauses for early exits.

## 4. Scope: LEGB (05)

**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in. Assigning makes a name local unless declared `global x` / `nonlocal x`. Avoid globals; don't shadow built-ins (`list`, `sum`, `max`…).

## 5. Type hints & docstrings (09)

`def area(w: float, h: float) -> float:` documents types, but they're **not enforced** at runtime. Check them with `mypy`. Docstrings: first-line summary, Args, Returns, Raises; examples can run as doctests.

## 6. Functions are objects (10–12)

- Assign, store in lists/dicts (**dispatch tables**), pass as arguments (**callbacks**), return from functions.
- `lambda x: x * 2` makes a small, one-expression function. Use it for `key=` and short callbacks.
- `sorted(items, key=...)`, `max(..., key=...)`, `map`, `filter` (lazy), `functools.reduce`, `any`, `all`, `zip`, `enumerate`.
- Prefer comprehensions to `map`/`filter` with a lambda.

## 7. Closures (13)

An inner function **remembers** variables from the enclosing scope after the outer function returns. Use them for function factories (`make_multiplier(3)`), private state (counters with `nonlocal`), and configuration.

## 8. Decorators (14–15)

```python
import functools

def decorator(func):
    @functools.wraps(func)                 # keep name & docstring
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper

@decorator             # same as: f = decorator(f)
def f(): ...
```
- **Why:** add the same behaviour to many functions without editing them: logging, timing, retry, validation, access control, caching, registration.
- **With arguments:** three levels → `def repeat(n): def decorator(func): def wrapper(...)`.
- **Stacking:** `@a @b def f` → `a(b(f))`. The decorator nearest `def` wraps first.
- **Built-ins:** `@functools.lru_cache`, `@functools.cache`, `@property`, `@classmethod`, `@staticmethod`.

## 9. Recursion (16)

Base case + recursive case on a smaller problem. The limit is about 1000 deep (`RecursionError`). It suits trees and nested data. Add `@lru_cache` for overlapping sub-problems.

## 10. Generators (17)

`yield` makes a lazy, resumable function. It saves memory, works for infinite streams, and can only be used once. Generator expression: `(x * x for x in data)`. Delegate with `yield from`.

## 11. Errors (18)

Validate early. `raise ValueError("clear message")`. Use `try / except Specific / else / finally`. Return `None` for "not found"; raise for misuse. Custom: `class MyError(Exception)`. Chain with `raise ... from e`. `assert` is for bugs only.

## 12. Best practices (19)

Write pure functions where possible, give each function one job, use verb names, keep them short with few parameters, avoid globals and mutating arguments, return consistent types, add docstrings and hints, and test with `assert`/pytest.

## When to use what

| Need | Use |
|------|-----|
| repeat code / name a step | a function |
| optional settings | default parameters / keyword-only |
| unknown number of inputs | `*args` / `**kwargs` |
| short throwaway function for `key=` | `lambda` |
| choose behaviour by name | dict of functions (dispatch table) |
| function with memory / configuration | closure |
| same extra behaviour on many functions | decorator |
| expensive repeated pure calls | `@lru_cache` |
| nested / tree data | recursion |
| huge or infinite sequences | generator |
| bad input | `raise` a specific exception |

← [Back to course map](../README.md)
