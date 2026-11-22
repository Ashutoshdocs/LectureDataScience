# Lecture 01: Your first function

Run: `python lecture.py`

## What is a function?

A **function** is a named, reusable block of code that does one job. You write it **once** and **call** it whenever you need that job done.

```python
def greet():                 # 1. definition: def + name + () + :
    """Print a welcome message."""   # 2. docstring (optional, recommended)
    print("Welcome to Python!")      # 3. body: indented

greet()                      # 4. call: name + ()
greet()                      #    as many times as you like
```

```
   def  greet  ( )  :
    │     │     │   └── colon starts the body
    │     │     └────── parentheses hold parameters (none here)
    │     └──────────── the function's name
    └────────────────── keyword meaning "define a function"
```

## Why use functions?

| Benefit | Meaning |
|---------|---------|
| **Reuse (DRY: Don't Repeat Yourself)** | write logic once, use it everywhere |
| **Fix once** | a bug fixed in the function is fixed for every caller |
| **Readability** | `average(marks)` says *what* happens; the loop inside says *how* |
| **Abstraction** | callers don't need to know the details |
| **Testing** | a small function is easy to test on its own |
| **Organisation** | big programs become a set of small, named pieces |

## When should you write a function?

- You're about to **copy-paste** code (the "rule of three": by the third copy, write a function).
- A block of code does **one identifiable job** you could name (`calculate_tax`, `send_email`).
- A section is **long** and would read better split into named steps.
- You want to **test** a piece of logic separately.

## Defining is not running

`def` only **stores** the function. Nothing in the body runs until you call it:

```python
def boom():
    print(1 / 0)      # no error yet!

print("defined fine") # runs
boom()                # NOW the ZeroDivisionError happens
```

## Naming rules & conventions

| Rule / convention | Example |
|-------------------|---------|
| letters, digits, `_`; can't start with a digit | `get_total`, `step2` ✅ · `2step` ❌ |
| `snake_case` (PEP 8) | `calculate_average` ✅ · `CalculateAverage` (that's for classes) |
| start with a **verb** for actions | `send_email`, `load_file`, `is_valid` |
| `is_`/`has_`/`can_` for yes/no answers | `is_even(n)`, `has_passed(marks)` |
| don't reuse built-in names | not `list`, `sum`, `print`, `max` |

## Docstrings

A string literal on the first line of the body documents the function. Tools read it:

```python
def area(width, height):
    """Return the area of a rectangle."""
    return width * height

help(area)           # shows the docstring
area.__doc__         # 'Return the area of a rectangle.'
```

## An empty function: `pass`

```python
def todo_later():
    pass             # a placeholder; the body can't be empty
```

## Exercises

1. Write `show_menu()` that prints three menu options; call it twice.
2. Rewrite the copy-paste average code from Lecture 00 as `average(numbers)` (peek at Lecture 03/04 for parameters and return).
3. Define a function containing an error but don't call it. Does the program crash?

<details><summary>Solutions</summary>

```python
def average(numbers):
    return sum(numbers) / len(numbers)
```
3. No. The error only happens when the function is called.
</details>

**Next →** [Lecture 02: Calling functions](../02_calling_functions/)
