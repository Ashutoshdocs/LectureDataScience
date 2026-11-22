# Simple Python Package: `calculator`

A tiny package for learning how Python packages work. Every line of code has a
comment explaining what it does.

## Folder layout

```
simple_package/
├── README.md            <- this file
├── main.py              <- the program that USES the package
└── calculator/          <- the PACKAGE (a folder with __init__.py)
    ├── __init__.py      <- runs on import; exposes the functions
    ├── basic.py         <- module: add(), subtract()
    └── advanced.py      <- module: power(), square_root()
```

## How to run

```bash
cd simple_package     # go into the project folder
python main.py        # run the program (use python3 on Mac/Linux if needed)
```

## Expected output

```
Step 1: importing the package...
calculator package loaded

Step 2: using the package version
Version: 1.0

Step 3: short names (thanks to __init__.py)
add(5, 3) = 8
subtract(10, 4) = 6
power(2, 3) = 8
square_root(16) = 4.0

Step 4: other ways to import
add(1, 2) = 3
power(3, 2) = 9
subtract(9, 1) = 8

Step 5: handling an error
Error caught: Cannot take the square root of a negative number
```

## Key words

| Word | Meaning |
|---|---|
| **Module** | One `.py` file, such as `basic.py` |
| **Package** | A folder of modules that contains an `__init__.py` file, such as `calculator/` |
| **`__init__.py`** | Makes the folder a package and runs the first time it is imported |
| **`__all__`** | A list of names that `from calculator import *` gives you |

## What each file does

### `calculator/__init__.py`

The package's front desk. It:

1. Prints a message, so you can see **when** it runs. Notice in the output
   that it prints only **once**, even though `main.py` imports twice.
2. Sets `__version__ = "1.0"`, a variable you can read as `calculator.__version__`.
3. Imports the functions from `basic.py` and `advanced.py`. The dot in
   `from .basic import add` means "from this same package".
4. Sets `__all__`, the list of names exported by `import *`.

Because of step 3, you can write the short form:

```python
calculator.add(5, 3)              # short: works thanks to __init__.py
```

instead of the long form:

```python
calculator.basic.add(5, 3)        # long: always works
```

### `calculator/basic.py`

A module with two simple functions, `add(a, b)` and `subtract(a, b)`.

### `calculator/advanced.py`

A module that imports Python's built-in `math` module and defines
`power(base, exponent)` and `square_root(number)`. `square_root` raises a
`ValueError` if the number is negative.

### `main.py`

Uses the package in five steps:

| Step | Shows |
|---|---|
| 1 | `import calculator` runs `__init__.py` only once |
| 2 | Reading a package variable (`__version__`) |
| 3 | Calling functions with short names |
| 4 | Three ways to import: `from calculator import add`, `from calculator.advanced import power`, `from calculator import *` |
| 5 | Catching an error with `try` / `except` |

## Ways to import, side by side

```python
import calculator                       # whole package -> calculator.add(1, 2)
from calculator import add              # one name      -> add(1, 2)
from calculator.basic import subtract   # long path     -> subtract(5, 1)
from calculator import *                # all in __all__ (avoid in real code)
```

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Running `python main.py` from a different folder | `ModuleNotFoundError: No module named 'calculator'` | `cd simple_package` first |
| Running `python calculator/basic.py` directly when it uses `.` imports | `ImportError: attempted relative import with no known parent package` | Run `main.py` instead |
| Forgetting a name in `__init__.py` | `AttributeError: module 'calculator' has no attribute ...` | Import the name in `__init__.py`, or use the long path |

## Try it yourself

1. Add `multiply(a, b)` and `divide(a, b)` to `basic.py`. Make `divide` raise a
   `ValueError` when `b` is 0.
2. Import both in `calculator/__init__.py` and add them to `__all__`.
3. Call them in `main.py` with `calculator.multiply(4, 5)`.
4. Delete the `print` line in `__init__.py`. Does the package still work? (Yes.)
5. Create a new module `calculator/stats.py` with `average(numbers)` and expose it the same way.
