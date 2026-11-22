# LAB 5 — Python `sys` Module

## Purpose
Inspect the Python runtime.

## What you will learn
`sys` provides information and controls related to the Python interpreter. `sys.argv` contains command-line arguments, and `sys.path` lists locations Python searches when importing modules.

## Code

```python
import sys

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Platform:", sys.platform)
print("Command-line arguments:", sys.argv)
print("Module search paths:")
for location in sys.path:
    print(" -", location)

print("Maximum recursion depth:", sys.getrecursionlimit())
```

## Run the lab

From this lab's folder:

```bash
python3 lab.py
```

On Windows, you can use:

```powershell
py lab.py
```

## Expected result
The script prints example values demonstrating the module. Some values are intentionally different on each run or machine (for example, random numbers, current date/time, paths, and platform information).

## Try it yourself
Run with an argument, for example: `python3 lab.py hello 123`. Then inspect `sys.argv`.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
