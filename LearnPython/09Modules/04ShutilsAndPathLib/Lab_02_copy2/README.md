# LAB 2 — `shutil.copy2()`: Copy a file and preserve metadata

## Purpose
Learn how to use `shutil.copy2()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil
from pathlib import Path

Path("source.txt").write_text("Hello Python", encoding="utf-8")

# copy2() attempts to preserve metadata such as modification time.
shutil.copy2("source.txt", "backup2.txt")

print(Path("backup2.txt").read_text(encoding="utf-8"))
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

'Hello Python'

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

copy2() copies file data and attempts to preserve metadata, including timestamps and permission bits.

## Lab note

Metadata preservation depends on the operating system and filesystem.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
