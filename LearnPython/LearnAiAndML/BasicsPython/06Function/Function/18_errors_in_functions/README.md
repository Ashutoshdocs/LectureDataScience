# Lecture 18: Errors in functions: validate, raise, handle

Run: `python lecture.py`

A function should either **do its job correctly** or **clearly refuse**. Silently returning a wrong answer is the worst outcome.

## Validate inputs & `raise`

```python
def withdraw(balance, amount):
    if not isinstance(amount, (int, float)):
        raise TypeError("amount must be a number")
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError(f"insufficient funds: balance {balance}, requested {amount}")
    return balance - amount
```

`raise` stops the function immediately and sends the error up the call stack until some `try/except` handles it (or the program stops with a traceback).

### Which exception to raise?

| Situation | Raise |
|-----------|-------|
| right type, bad value (negative age, empty name) | `ValueError` |
| wrong type (string instead of number) | `TypeError` |
| a key / item that doesn't exist | `KeyError` / `LookupError` |
| operation not allowed in the current state | `RuntimeError`, or your own exception |
| your application's specific problems | a **custom exception** (below) |

Always write a **helpful message**: what was wrong, and the value received.

## Handling errors: `try / except / else / finally`

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return None                # handle the expected problem
    else:
        return round(result, 2)    # runs only if no exception
    finally:
        print("division attempted")   # ALWAYS runs (cleanup)
```

Rules:
- Catch **specific** exceptions: `except ValueError:`, not a bare `except:`.
- Keep the `try` block **small**: only the lines that can fail.
- Don't silence errors you can't handle. Let them propagate.

## Raise or return a special value?

| Return `None` / a default | Raise an exception |
|---------------------------|--------------------|
| "not found" is a **normal, expected** outcome (`find_user` → `None`) | the caller made a **mistake** or something **went wrong** |
| the caller is expected to check the result | ignoring it would be dangerous |
| e.g. `dict.get(key)` | e.g. `dict[key]`, `int("abc")` |

The Python style is "**EAFP**: Easier to Ask Forgiveness than Permission": try the operation and handle the exception, rather than checking every condition first ("LBYL: Look Before You Leap"). Both are fine; EAFP avoids race conditions and duplicated checks.

## Custom exceptions

```python
class InsufficientFunds(Exception):
    """Raised when a withdrawal exceeds the balance."""

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(f"need {amount - balance} more")
```

Callers can then catch **exactly** your error: `except InsufficientFunds:`.

## Re-raising with context

```python
try:
    value = int(text)
except ValueError as e:
    raise ValueError(f"bad 'age' field in row 7: {text!r}") from e
```

`from e` keeps the original error attached. The traceback shows both.

## `assert`: for bugs, not for user input

```python
assert len(items) > 0, "items must not be empty"
```

`assert` checks **your own assumptions** while developing. It can be disabled (`python -O`), so **never** use it to validate user input or data from files.

## Exercises

1. Write `parse_age(text)` that returns an int 0–130 or raises a clear `ValueError`.
2. Write `safe_int(text, default=0)` that never raises.
3. Create `class InvalidMarks(ValueError)` and raise it from `grade(marks)`.
4. Process a list of strings with `parse_age`, collecting errors instead of stopping.

<details><summary>Solutions</summary>

```python
def safe_int(text, default=0):
    try:
        return int(text)
    except (TypeError, ValueError):
        return default
```
</details>

**Next →** [Lecture 19: Pure functions & best practices](../19_pure_functions_best_practices/)
