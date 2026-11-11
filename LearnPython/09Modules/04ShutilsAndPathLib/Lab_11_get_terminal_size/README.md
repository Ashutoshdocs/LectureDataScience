# LAB 11 — `shutil.get_terminal_size()`: Get terminal dimensions

## Purpose
Learn how to use `shutil.get_terminal_size()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil

size = shutil.get_terminal_size()

print("Columns (width):", size.columns)
print("Lines (height):", size.lines)
print("Full result:", size)
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

Terminal width and height; fallback dimensions may be returned.

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

get_terminal_size() returns terminal dimensions as columns and lines.

## Lab note

Results depend on the terminal. Non-interactive shells may use fallback values.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
