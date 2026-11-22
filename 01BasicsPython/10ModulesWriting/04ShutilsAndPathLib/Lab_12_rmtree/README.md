# LAB 12 — `shutil.rmtree()`: Delete a directory tree

## Purpose
Learn how to use `shutil.rmtree()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil
from pathlib import Path

# Create a clearly named practice directory and a file inside it.
target = Path("project_backup")
target.mkdir(exist_ok=True)
(target / "app.txt").write_text("Temporary practice file", encoding="utf-8")

print("Exists before deletion:", target.exists())

# Safety: delete only the practice directory created above.
shutil.rmtree(target)

print("Exists after deletion:", target.exists())
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

Exists before deletion: True, then Exists after deletion: False

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

rmtree() recursively removes a directory and everything inside it. This operation is destructive and generally cannot be undone.

## Lab note

Run only against a directory you intentionally created for practice. Never point it at important folders.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
