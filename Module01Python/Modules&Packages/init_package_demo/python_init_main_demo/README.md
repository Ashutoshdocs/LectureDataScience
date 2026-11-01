# Python Package Demo: `__init__.py`, `main.py`, and Calling a Package

This small project demonstrates how Python packages work, what `__init__.py` does,
how to write code in `main.py`, and how another Python file can import and call it.

## 1. Project structure

```text
python_init_main_demo/
├── calculator/
│   ├── __init__.py
│   └── main.py
├── use_package.py
└── README.md
```

- `calculator/` is the package directory.
- `main.py` contains the actual calculator functions.
- `__init__.py` makes the directory a regular Python package and controls
  what is conveniently available when someone imports `calculator`.
- `use_package.py` is the client program that imports and calls the package.

## 2. Understand `main.py`

Open `calculator/main.py`:

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference between two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b, preventing division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

These are ordinary Python functions. `main.py` is just a Python module;
the filename `main.py` has no special package behaviour by itself.

## 3. Understand `__init__.py`

Open `calculator/__init__.py`:

```python
from .main import add, subtract, multiply, divide

__all__ = ["add", "subtract", "multiply", "divide"]
```

The dot in `.main` means: import from the `main.py` module in this same package.

This file makes the functions available directly from the package:

```python
from calculator import add
```

Without these imports in `__init__.py`, you can still import the function
using its full module path:

```python
from calculator.main import add
```

`__all__` documents the names intended for `from calculator import *`.
It does not prevent other names from being imported explicitly.

## 4. Call the package

Open `use_package.py`:

```python
from calculator import add, subtract, multiply, divide

print("Addition:", add(10, 5))
print("Subtraction:", subtract(10, 5))
print("Multiplication:", multiply(10, 5))
print("Division:", divide(10, 5))
```

Expected output:

```text
Addition: 15
Subtraction: 5
Multiplication: 50
Division: 2.0
```

You can also call a function through the module path:

```python
from calculator.main import add

print(add(20, 7))
```

## 5. Run it step by step

1. Install Python 3 if it is not already installed.
2. Extract this project ZIP file.
3. Open a terminal or command prompt.
4. Change directory to the `python_init_main_demo` folder (the folder containing
   `use_package.py`).
5. Run:

   ```bash
   python use_package.py
   ```

   On some Linux systems, use `python3 use_package.py`.

6. Compare the output with the expected output above.
7. Open `calculator/__init__.py`. Temporarily remove the `from .main import ...`
   line, save it, and run `use_package.py` again. The package-level import will
   fail because `add` is no longer exposed by `calculator`.
8. Restore the line. Then change the import in `use_package.py` to
   `from calculator.main import add` and test the direct module import.

## 6. Important difference: `__init__.py` vs `main.py`

| File | Purpose |
|---|---|
| `__init__.py` | Package initialization; commonly exposes selected package functions/classes |
| `main.py` | A normal module where you place application or package logic |
| `use_package.py` | A separate program that imports and uses the package |

**Remember:** importing a package executes its `__init__.py`. It does not
automatically execute a file named `main.py`; `main.py` is loaded here because
`__init__.py` explicitly imports from it.

## 7. Common mistakes

- **Wrong working directory:** run the command from the folder containing
  `use_package.py`, so Python can find the `calculator` folder.
- **Misspelled filename:** use exactly `__init__.py` (two underscores on each side).
- **Wrong import:** `from .main import add` is a relative import and belongs inside
  the package. In the external caller, use `from calculator import add` or
  `from calculator.main import add`.
- **Naming conflicts:** avoid naming your own files `calculator.py`, `random.py`,
  or other names that conflict with packages/modules you intend to import.

## 8. Practice tasks

1. Add a `power(a, b)` function to `main.py`.
2. Export `power` from `__init__.py`.
3. Import and call `power(2, 3)` in `use_package.py`.
4. Add a `modulus(a, b)` function and test it.

This demonstrates the basic flow:

```text
use_package.py
      |
      | from calculator import add
      v
calculator/__init__.py
      |
      | from .main import add
      v
calculator/main.py
      |
      v
    add(10, 5)
      |
      v
    result: 15
```
