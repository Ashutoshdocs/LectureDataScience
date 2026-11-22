# Lecture 04: The return statement

Run: `python lecture.py`

## `return` sends a value back to the caller

```python
def square(n):
    return n * n          # 1. compute  2. hand back  3. leave the function

result = square(4)        # the call expression becomes 16
print(square(3) + square(4))   # 25: results can be used in expressions
```

## `return` vs `print`: the most important beginner distinction

| | `print(x)` | `return x` |
|---|---|---|
| Does | shows text on the screen | gives the value back to the caller |
| The call's value | `None` | `x` |
| Reusable? | ❌ the value is gone | ✅ store it, compare it, pass it on |
| Who decides what to do with it | the function | the **caller** |

```python
def add_print(a, b): print(a + b)
def add_return(a, b): return a + b

x = add_print(2, 3)     # prints 5, but x is None
y = add_return(2, 3)    # prints nothing, y is 5
y * 10                  # 50
x * 10                  # TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

> **Rule:** functions that *compute* something should `return` it. Only functions whose *job* is output (`show_report`) should print.

## No `return` → `None`

A function that ends without `return`, or with a bare `return`, returns `None`.

## `return` ends the function immediately

Code after a `return` in the same block never runs. This allows **early returns** (guard clauses):

```python
def grade(marks):
    if marks < 0 or marks > 100:
        return "invalid"           # leave early for bad input
    if marks >= 85:
        return "A"
    if marks >= 70:
        return "B"
    return "C"                     # the default case
```

Guard clauses avoid deeply nested `if/else` pyramids.

## Returning several values

`return a, b` actually returns a **tuple**, which you can **unpack**:

```python
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([4, 9, 1])     # unpacking
pair = min_max([4, 9, 1])          # (1, 9), a tuple
```

For more than 3–4 values, return a **dict** (or a small class / `namedtuple`) so the caller can use names instead of positions:

```python
return {"min": lo, "max": hi, "mean": avg}
```

## Returning different kinds of things

| Return | Example use |
|--------|-------------|
| a number / string | `area()`, `full_name()` |
| a `bool` | `is_valid_email()`, used directly in `if` |
| a list / dict | `get_passed_students()` |
| `None` to mean "not found" | `find_user(id)`. The caller must check `if user is None:` |
| another function | function factories (Lecture 13) |

> ⚠️ Be **consistent**: don't return a number on one path and a string on another unless callers expect it. Mixing makes bugs.

## Exercises

1. Write `is_even(n)` that returns a bool, and use it in an `if`.
2. Write `stats(numbers)` returning `(count, total, average)`, then unpack it.
3. Rewrite a nested `if/else` grading function using early returns.
4. Write `find(names, target)` that returns the index or `None`.

<details><summary>Solutions</summary>

```python
def stats(numbers):
    total = sum(numbers)
    return len(numbers), total, total / len(numbers)

def find(names, target):
    for i, n in enumerate(names):
        if n == target:
            return i
    return None
```
</details>

**Next →** [Lecture 05: Variable scope](../05_variable_scope/)
