# Lecture 00: Prerequisites

Run: `python lecture.py`

Functions package up code you already know how to write. Before starting, be comfortable with:

| Skill | Example | Why functions need it |
|-------|---------|-----------------------|
| Variables & assignment | `price = 120` | Parameters are variables |
| Basic types | `int`, `float`, `str`, `bool`, `None` | What you pass in and get back |
| Collections | `list`, `tuple`, `dict`, `set` | Common arguments and return values |
| Operators | `+ - * / // % **`, `== != < >`, `and or not` | The work inside a function |
| `if / elif / else` | `if marks >= 40:` | Decisions inside functions |
| Loops | `for x in items:` / `while n > 0:` | Repetition inside functions |
| Indentation | 4 spaces define a block | A function's body is an indented block |
| f-strings | `f"{name} scored {marks}"` | Building output |
| Mutable vs immutable | lists can change in place; ints and strings can't | Explains what happens when you pass them to a function (Lecture 03) |

## The problem functions solve

`lecture.py` computes the average of three lists of marks **without** functions. The same four lines are copied three times. Copy-paste code means:

- **Bugs get copied too.** Fix one copy, forget the others.
- **Long, hard-to-read files.**
- **No name for the idea.** The reader must work out "this block computes an average".

Lecture 01 replaces the three copies with **one function** called three times.

## Mutable vs immutable: a quick check

```python
a = [1, 2]; b = a; b.append(3)    # a is now [1, 2, 3]: same list
x = 5;      y = x; y += 1         # x is still 5: ints can't change, y is a new int
```

Keep this in mind for Lecture 03, where passing a list to a function lets the function change it.

## Exercises

1. Write a loop that prints the squares of 1–5.
2. Write an `if/elif/else` that labels a number "negative", "zero" or "positive".
3. Make two names for one list, append through one, and print the other.

**Next →** [Lecture 01: Basic function](../01_basic_function/)
