# Python Functions: From Zero to Confident

A hands-on course in 25 short lectures (00–24) on **Python functions**: the basics, every kind of parameter, scope, `*args`/`**kwargs`, lambdas, closures, **decorators**, recursion, generators and best practices. For each feature you learn **what it is, why it exists, when to use it (and when not to), and how**.

Every lecture folder has:

| File | What it is |
|------|------------|
| `README.md` | The lesson: concepts, diagrams, step-by-step traces, tables, common mistakes, exercises (with solutions) |
| `lecture.py` | Runnable code for the lesson. Read it, run it, change it |

No libraries to install. Everything uses plain **Python 3.10+**.

## How to use this course

1. Work through the folders **in order**.
2. In each folder: read `README.md`, run `python lecture.py`, compare the output.
3. Do the exercises at the bottom of each README. Break the code on purpose and read the error messages.
4. Finish with **23_practice_exercises** (auto-checked) and **24_quick_revision**.

Examples that are *meant* to fail are wrapped in `try/except`, so every file runs to the end and prints the error message for you to read.

## Course map

| # | Lecture | Big idea |
|---|---------|----------|
| 00 | [Prerequisites](00_prerequisites/) | Variables, types, `if`, loops: what you need first |
| 01 | [Basic function](01_basic_function/) | Why functions exist; `def`, body, docstring, naming, DRY |
| 02 | [Calling functions](02_calling_functions/) | Call flow, the call stack, functions calling functions |
| 03 | [Parameters & arguments](03_parameters_arguments/) | Positional, keyword, defaults, the mutable-default trap |
| 04 | [The return statement](04_return_statement/) | `return` vs `print`, multiple values, early return, `None` |
| 05 | [Variable scope](05_variable_scope/) | LEGB, `global`, `nonlocal`, shadowing |
| 06 | [`*args`](06_args/) | Any number of positional arguments |
| 07 | [`**kwargs`](07_kwargs/) | Any number of keyword arguments |
| 08 | [Argument order & special parameters](08_argument_order_and_special_params/) | The ordering rule, keyword-only `*`, positional-only `/`, unpacking at call time |
| 09 | [Type hints & docstrings](09_type_hints_and_docstrings/) | Annotations, `help()`, documenting functions |
| 10 | [Functions as objects](10_functions_as_objects/) | First-class functions, higher-order functions, dispatch tables |
| 11 | [Lambda](11_lambda/) | Anonymous one-line functions, and when not to use them |
| 12 | [map, filter, reduce & built-ins](12_map_filter_reduce_builtins/) | Functional tools vs comprehensions; `sorted(key=)`, `any`, `all`, `zip`, `enumerate` |
| 13 | [Nested functions & closures](13_nested_functions_and_closures/) | Inner functions that remember; function factories |
| 14 | [Decorators: basics](14_decorators_basics/) | Why decorators, the wrapper pattern, `@`, `functools.wraps` |
| 15 | [Decorators: advanced](15_decorators_advanced/) | Decorators with arguments, stacking, real-world decorators, built-in ones |
| 16 | [Recursion](16_recursion/) | Base case, call stack, limits, memoisation with `@lru_cache` |
| 17 | [Generators](17_generators/) | `yield`, lazy sequences, generator expressions |
| 18 | [Errors in functions](18_errors_in_functions/) | Validating input, `raise`, custom exceptions, return-or-raise |
| 19 | [Pure functions & best practices](19_pure_functions_best_practices/) | Side effects, single responsibility, testing with `assert` |
| 20 | [Project: calculator](20_project_calculator/) | Dispatch tables, validation, decorators |
| 21 | [Project: employee management](21_project_employee_management/) | CRUD with functions over a list of dicts |
| 22 | [Project: student result](22_project_student_result/) | Grading pipeline with small composable functions |
| 23 | [Practice exercises](23_practice_exercises/) | 20 auto-checked exercises + solutions |
| 24 | [Quick revision](24_quick_revision/) | The whole course on one page + self-test |

## Run everything at once

```bash
python run_all.py
```
