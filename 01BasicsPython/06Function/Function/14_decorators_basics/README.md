# Lecture 14: Decorators: the basics

Run: `python lecture.py`

## The problem decorators solve

You want to add the **same extra behaviour** to many functions (timing, logging, checking permissions, caching), **without editing each function's code**.

Copying the same lines into every function is exactly the duplication functions were meant to remove:

```python
def add(a, b):
    print("calling add")          # logging copied everywhere...
    result = a + b
    print("add returned", result)
    return result
```

## A decorator is a function that wraps another function

A **decorator** takes a function, and returns a **new** function (a *wrapper*) that adds behaviour **before and/or after** calling the original.

```python
def log_calls(func):                          # 1. receives the original function
    def wrapper(*args, **kwargs):             # 2. the new function (a closure!)
        print(f"calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)        # 3. call the original
        print(f"{func.__name__} returned {result}")
        return result                         # 4. pass the result back
    return wrapper                            # 5. return the wrapper

def add(a, b):
    return a + b

add = log_calls(add)                          # replace add with the wrapped version
add(2, 3)
```

```
            ┌───────────────── wrapper ──────────────────┐
 add(2,3) ─►│ print "calling add"                        │
            │      ┌──── original add ────┐              │
            │      │   return 2 + 3       │──► 5          │
            │      └──────────────────────┘              │
            │ print "add returned 5"                     │──► 5
            └────────────────────────────────────────────┘
```

Everything you've learned comes together here:
- functions are **objects** that can be passed and returned (Lecture 10)
- the wrapper is a **closure** that remembers `func` (Lecture 13)
- `*args, **kwargs` lets the wrapper accept and forward **any** arguments (Lectures 06–07)

## The `@` syntax

`@decorator` above a `def` is shorthand for `func = decorator(func)`:

```python
@log_calls
def add(a, b):
    return a + b

# exactly the same as:   add = log_calls(add)
```

The decoration happens **once, when the `def` runs**, not on every call.

## ⚠️ Always use `functools.wraps`

Without it, the decorated function loses its identity: `add.__name__` becomes `"wrapper"`, its docstring disappears, and `help(add)` shows the wrapper. Debugging and documentation tools get confused.

```python
import functools

def log_calls(func):
    @functools.wraps(func)            # copy __name__, __doc__, etc. from func to wrapper
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

`wraps` also stores the original as `add.__wrapped__`.

## The decorator template (memorise this)

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # ... before ...
        result = func(*args, **kwargs)
        # ... after ...
        return result
    return wrapper
```

## Common beginner mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| forgetting `return result` in the wrapper | decorated function returns `None` | `return func(*args, **kwargs)` |
| forgetting `return wrapper` | the name becomes `None` → `TypeError: 'NoneType' object is not callable` | return the wrapper |
| `return wrapper()` (with brackets) | runs once at decoration time; the name becomes a value | return the function, no brackets |
| wrapper without `*args, **kwargs` | `TypeError` when called with arguments | accept and forward both |
| no `@functools.wraps` | wrong `__name__` / docstring | add it |

## Why and when to use decorators

| ✅ Use decorators for **cross-cutting concerns**: the same extra behaviour on many functions | ❌ Don't use them when |
|---|---|
| logging, timing, counting calls | the behaviour is specific to one function. Just write it inside |
| access control / authentication | it would hide important logic the reader needs to see |
| input validation | a plain function call is clearer |
| caching / memoisation | |
| retrying on failure | |
| registering functions (plugins, routes: `@app.route("/")` in Flask) | |

## Exercises

1. Write `@shout` that upper-cases a function's string result.
2. Write `@count_calls` that stores the number of calls in `wrapper.calls`.
3. Remove `@functools.wraps` and print `__name__` and `__doc__`.
4. Write `@debug` that prints arguments and result, and decorate two different functions.

<details><summary>Solutions</summary>

```python
def shout(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
```
</details>

**Next →** [Lecture 15: Decorators: advanced](../15_decorators_advanced/)
