# LAB 4 — `shutil.copytree()`: Copy a complete directory

## Purpose
Learn how to use `shutil.copytree()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil
from pathlib import Path

project = Path("project")
project.mkdir(exist_ok=True)
(project / "app.txt").write_text("Application file", encoding="utf-8")

# The destination must not already exist.
shutil.copytree("project", "project_backup")

print(list(Path("project_backup").iterdir()))
print((Path("project_backup") / "app.txt").read_text(encoding="utf-8"))
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

A listing containing app.txt, followed by 'Application file'.

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

copytree() recursively copies a directory and its contents. By default, the destination directory must not already exist.

## Lab note

This lab creates project/ and project_backup/.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
