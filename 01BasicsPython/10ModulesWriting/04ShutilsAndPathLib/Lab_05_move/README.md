# LAB 5 — `shutil.move()`: Move a file

## Purpose
Learn how to use `shutil.move()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil
from pathlib import Path

# Prepare a source file and destination folder for this standalone lab.
Path("source.txt").write_text("File to move", encoding="utf-8")
Path("backup_folder").mkdir(exist_ok=True)

shutil.move("source.txt", "backup_folder/source.txt")

print(Path("backup_folder/source.txt").exists())
print(Path("source.txt").exists())
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

True, then False

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

move() moves a file or directory to another location. It may use a rename operation when possible or copy-and-delete across filesystems.

## Lab note

This lab prepares its own source file so it can run independently.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
