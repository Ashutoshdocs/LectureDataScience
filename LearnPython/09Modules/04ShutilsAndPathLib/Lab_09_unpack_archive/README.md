# LAB 9 — `shutil.unpack_archive()`: Extract a ZIP archive

## Purpose
Learn how to use `shutil.unpack_archive()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil
from pathlib import Path

# Prepare an archive for this standalone lab.
project = Path("project")
project.mkdir(exist_ok=True)
(project / "app.txt").write_text("Application file", encoding="utf-8")
shutil.make_archive("project_backup", "zip", root_dir=".", base_dir="project")

# Extract into a new destination folder.
shutil.unpack_archive("project_backup.zip", "extracted_project")

print([item.name for item in Path("extracted_project").iterdir()])
print((Path("extracted_project") / "app.txt").read_text(encoding="utf-8"))
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

['app.txt'] and 'Application file'

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

unpack_archive() extracts an archive into a destination directory. Python detects the archive format from the file extension unless a format is specified.

## Lab note

The destination folder must not already exist. This lab creates its own ZIP first.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
