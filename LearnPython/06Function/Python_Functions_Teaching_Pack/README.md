# Python Functions – Beginner to Intermediate Teaching Pack

A module-wise classroom practical for teaching Python functions from scratch.

## Learning outcomes
By the end, students can:
- Define and call functions.
- Explain function execution flow.
- Distinguish local and global scope; understand LEGB and `nonlocal`.
- Use positional, keyword, and default arguments.
- Explain parameters vs arguments.
- Distinguish `print()` from `return`.
- Return multiple values.
- Use `*args` and `**kwargs`.
- Combine argument types in practical programs.

## Requirements
- Python 3.9+ (examples also work on newer Python versions).
- No third-party packages required.

Check Python:
```bash
python --version
```

Run a file:
```bash
python 01_basic_function.py
```
On some Windows systems:
```powershell
py 01_basic_function.py
```

## Module sequence

| File | Topic |
|---|---|
| `01_basic_function.py` | Define a basic function |
| `02_calling_functions.py` | Calling and execution flow |
| `03_variable_scope.py` | Local, global, LEGB, `global`, `nonlocal` |
| `04_parameters_arguments.py` | Non-parameterized, parameterized, positional, keyword, default |
| `05_return_statement.py` | `print` vs `return`, multiple values, early return |
| `06_args.py` | Variable positional arguments and unpacking |
| `07_kwargs.py` | Variable keyword arguments and dictionary access |
| `08_argument_order.py` | Combining arguments and keyword-only parameters |
| `09_calculator.py` | Calculator mini-project |
| `10_employee_management.py` | Employee details with `*args` and `**kwargs` |
| `11_student_result.py` | Student result with variable marks |
| `12_practice_exercises.py` | Student exercises |
| `13_practice_solutions.py` | Suggested solutions |

## Suggested teaching plan

### Session 1 – Fundamentals (60 minutes)
1. Explain function and code reuse.
2. Run Module 1.
3. Trace Module 2 line by line.
4. Demonstrate local/global scope in Module 3.
5. Ask students to predict outputs before running.

### Session 2 – Inputs and outputs (60 minutes)
1. Compare parameterized and non-parameterized functions.
2. Demonstrate positional, keyword and default arguments.
3. Compare `print()` and `return`.
4. Practice returning multiple values.

### Session 3 – Flexible functions and projects (75 minutes)
1. Explain `*args` as a tuple.
2. Explain `**kwargs` as a dictionary.
3. Demonstrate argument ordering and unpacking.
4. Complete the mini-projects.
5. Assign the practice exercises.

## Key concepts to emphasize

- A function body runs when the function is called, not merely when it is defined.
- Parameters are names in the function definition; arguments are values supplied by the caller.
- `print()` displays a value. `return` sends a value back to the caller.
- A function without an explicit return statement returns `None`.
- `*args` collects extra positional arguments into a tuple.
- `**kwargs` collects extra keyword arguments into a dictionary.
- `global` is needed when assigning to a module-level global variable inside a function.
- `nonlocal` is used to rebind a variable in an enclosing function scope.
- Avoid modifying global state unnecessarily in real applications.

## Common errors / gotchas

1. **Calling before defining:** In a normal top-to-bottom script, define a function before calling it.
2. **Wrong number of arguments:** A function with two required parameters cannot receive three positional arguments unless it accepts additional arguments.
3. **Wrong argument order:** Positional arguments are assigned by position.
4. **Missing return:** Printing a result does not make it available to the caller.
5. **Unreachable code:** Statements after `return` in the same execution path do not run.
6. **Local vs global:** Assigning `x = ...` inside a function normally creates/rebinds a local variable.
7. **`*args` / `**kwargs`:** The names `args` and `kwargs` are conventions; the `*` and `**` symbols provide the behavior.
8. **Missing dictionary key:** `kwargs["key"]` raises `KeyError` if the key is absent. Use `kwargs.get("key")` when a key may be optional.

## How to use this pack
Teach one file at a time. First ask students to predict the output, then run the file, then ask them to modify the code. The practice exercises are in `12_practice_exercises.py`; suggested solutions are in `13_practice_solutions.py`.
