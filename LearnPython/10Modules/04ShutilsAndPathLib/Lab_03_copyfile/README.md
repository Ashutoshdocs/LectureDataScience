# LAB 3 — `shutil.copyfile()`: Copy file contents

## Purpose
Learn how to use `shutil.copyfile()` in a small practical exercise.

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

# copyfile() copies the contents only.
shutil.copyfile("source.txt", "backup3.txt")

print(Path("backup3.txt").read_text(encoding="utf-8"))
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

'Hello Python'

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

copyfile() copies the contents of one file to another. Unlike copy() and copy2(), it does not copy permission bits.

## Lab note

The source and destination must be different files.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
