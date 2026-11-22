# Lecture 20: Project: calculator

Run: `python lecture.py` (it runs a scripted demo; set `INTERACTIVE = True` at the top to type your own input)

A calculator built **entirely from small functions**, using most of the course.

## Features

- Basic operations: `+ - * / // % **`, plus `sqrt` and `!` (factorial)
- Expressions typed as text: `"12 * 3"`, `"sqrt 16"`, `"5 !"`
- Input validation with clear error messages
- History of results; `ans` reuses the last answer
- Statistics on a list of numbers: `stats 4 8 15 16 23 42`

## How it's built

| Function | Lecture | Role |
|----------|---------|------|
| `add`, `subtract`, … | 01, 04 | one tiny pure function per operation |
| `OPERATIONS` / `UNARY` dicts | 10 | **dispatch tables** instead of a long `if/elif` |
| `lambda` entries | 11 | one-liners such as `"//"` |
| `factorial` | 16 | recursion with a base case |
| `@log_history` | 14 | decorator that records each result |
| `@safe` | 14, 18 | decorator that turns exceptions into friendly messages |
| `parse_number(text, last)` | 03, 18 | validation, `ans` support, raises `ValueError` |
| `calculate(expression, *, history)` | 08 | keyword-only parameter |
| `stats(*numbers)` | 06 | any number of values; returns a dict |
| `make_rounder(places)` | 13 | closure for consistent rounding |
| `main()` + `if __name__ == "__main__"` | 02 | program entry point |

## Example session (the real output of `lecture.py`)

```
> 12 * 3                 = 36
> ans + 4                = 40
> 10 / 0                 ! Error: cannot divide by zero
> sqrt 2                 = 1.4142
> 5 !                    = 120
> 2 ^ 3                  ! Error: unknown operator '^' (use one of + - * / // % **)
> 7 // 2                 = 3
> 2 ** 10                = 1024
> ten + 1                ! Error: 'ten' is not a number
> sqrt -9                ! Error: cannot take the square root of a negative number
> stats 4 8 15 16 23 42  = count 6, total 108, mean 18, min 4, max 42
> stats                  ! Error: stats needs at least one number
```

## Extension exercises

1. Add `%` of a value: `"20 % of 150"`.
2. Add `undo` to remove the last history entry.
3. Support three-number expressions like `2 + 3 * 4` (hint: use the precedence of `*` over `+`).
4. Save the history to a file when the program ends.

**Next →** [Lecture 21: Project: employee management](../21_project_employee_management/)
