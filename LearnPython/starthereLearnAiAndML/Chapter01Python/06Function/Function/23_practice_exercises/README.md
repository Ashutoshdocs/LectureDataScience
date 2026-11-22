# Lecture 23: Practice exercises (20, auto-checked)

| File | What it is |
|------|------------|
| `exercises.py` | **Your work.** 20 functions with docstrings and `...` bodies. Fill them in. |
| `solutions.py` | Reference solutions. Try first, peek later! |
| `lecture.py` | The checker. `python lecture.py` tests `solutions.py`; `python lecture.py exercises` tests **your** file. |

```
python lecture.py exercises
  ✔ 01 greet
  ✘ 02 area_of_rectangle: area_of_rectangle(3, 4) returned None, expected 12
  …
  Score: 7 / 20
```

## The exercises

| # | Function | Topic (lecture) |
|---|----------|-----------------|
| 01 | `greet(name, greeting="Hello")` | defaults (03) |
| 02 | `area_of_rectangle(length, width)` | return (04) |
| 03 | `min_max(numbers)` → `(min, max)` | multiple returns (04) |
| 04 | `is_even(n)` | boolean return (04) |
| 05 | `count_vowels(text)` | loops in functions (01) |
| 06 | `make_counter()` | closures + `nonlocal` (05, 13) |
| 07 | `average(*numbers)` | `*args` (06) |
| 08 | `build_profile(name, **details)` | `**kwargs` (07) |
| 09 | `safe_divide(a, b, *, default=None)` | keyword-only args, errors (08, 18) |
| 10 | `apply_twice(func, value)` | functions as arguments (10) |
| 11 | `sort_by_age(people)` | `lambda` + `sorted` (11) |
| 12 | `squares_of_evens(numbers)` | `map`/`filter` or a comprehension (12) |
| 13 | `make_multiplier(n)` | function factories (13) |
| 14 | `shout(func)` | decorator: uppercase the result (14) |
| 15 | `count_calls(func)` | decorator with state, `.calls` attribute (15) |
| 16 | `repeat(times)` | decorator with arguments (15) |
| 17 | `factorial(n)` | recursion (16) |
| 18 | `flatten(nested)` | recursion on nested data (16) |
| 19 | `countdown(n)` | generator (17) |
| 20 | `parse_age(text)` | validation + `ValueError` (18) |

## How to practise

1. Open `exercises.py` and read each docstring. It includes examples.
2. Write the body and replace the `...`.
3. Run `python lecture.py exercises`. A failure tells you the call, what you returned, and what was expected.
4. Repeat until you score 20 / 20. Then compare with `solutions.py`: is yours simpler, or longer?

**Next →** [Lecture 24: Quick revision](../24_quick_revision/)
