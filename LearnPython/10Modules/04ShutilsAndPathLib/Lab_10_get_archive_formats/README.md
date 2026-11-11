# LAB 10 — `shutil.get_archive_formats()`: List supported archive formats

## Purpose
Learn how to use `shutil.get_archive_formats()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil

for name, description in shutil.get_archive_formats():
    print(name, "-", description)
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

A list of archive format names and descriptions; available formats depend on Python and the platform.

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

get_archive_formats() lists formats supported for creating archives through shutil.

## Lab note

ZIP is commonly available without extra packages.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
