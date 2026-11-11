# LAB 1 — `shutil.copy()`: Copy a file

## Purpose
Learn how to use `shutil.copy()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil

# Create a sample source file for this exercise.
with open("source.txt", "w", encoding="utf-8") as file:
    file.write("Hello Python")

# Copy the file to a new name.
shutil.copy("source.txt", "backup.txt")

with open("backup.txt", encoding="utf-8") as file:
    print(file.read())
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

'Hello Python'

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

copy() copies a file to a destination. It also copies file permission bits where supported.

## Lab note

Run this lab in its own folder. It creates source.txt and backup.txt.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
