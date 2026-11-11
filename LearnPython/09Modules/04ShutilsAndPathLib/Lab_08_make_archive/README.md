# LAB 8 — `shutil.make_archive()`: Create a ZIP archive

## Purpose
Learn how to use `shutil.make_archive()` in a small practical exercise.

## Before you start
1. Open a terminal.
2. Change into this lab's folder.
3. Start Python Shell with `python3` (Windows: `py` or `python`).
4. Type the code from `lab.py` one line at a time, or run the complete file as shown below.

## Code

```python
import shutil
from pathlib import Path

# Prepare a small project directory.
project = Path("project")
project.mkdir(exist_ok=True)
(project / "app.txt").write_text("Application file", encoding="utf-8")
(project / "notes.txt").write_text("Project notes", encoding="utf-8")

# Creates project_backup.zip in the current folder.
archive_path = shutil.make_archive(
    "project_backup",
    "zip",
    root_dir=".",
    base_dir="project"
)

print("Created:", archive_path)
print("ZIP exists:", Path(archive_path).exists())
```

## Run the complete lab

```bash
python3 lab.py
```

## Expected result

Created: project_backup.zip, then ZIP exists: True

Exact paths, disk values, executable locations, and terminal dimensions can vary by machine.

## Explanation

make_archive() creates an archive. Here, root_dir selects the starting directory and base_dir selects the project folder inside the archive.

## Lab note

This lab creates its own project/ directory and project_backup.zip.

## Try it yourself

- Change the sample filename or directory name.
- Print the result after the operation.
- Observe what changed in this lab folder.
