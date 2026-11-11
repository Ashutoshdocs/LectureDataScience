# LAB 6 — `shutil.disk_usage()`: Check disk space

## Purpose
Learn how to use `shutil.disk_usage()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil

usage = shutil.disk_usage(".")

print("Total bytes:", usage.total)
print("Used bytes :", usage.used)
print("Free bytes :", usage.free)

# Optional: display values in GiB.
gib = 1024 ** 3
print("Total GiB:", round(usage.total / gib, 2))
print("Free GiB :", round(usage.free / gib, 2))
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

Your filesystem's total, used, and free space (values vary).

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

disk_usage() returns a named tuple containing total, used, and free space in bytes.

## Lab note

The path '.' means the current working directory's filesystem.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
