# LAB 7 — `shutil.which()`: Find an executable

## Purpose
Learn how to use `shutil.which()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil

print("python :", shutil.which("python"))
print("python3:", shutil.which("python3"))
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

Executable paths when found; otherwise None.

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

which() searches directories listed in the PATH environment variable and returns the executable path if found.

## Lab note

Executable names vary by operating system. On Windows, try 'python' or 'py'.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
