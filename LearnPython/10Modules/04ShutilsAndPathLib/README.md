# Python `shutil` Module – Practical Labs

A beginner-friendly course containing 12 separate practical lab folders. Each lab has:
- `README.md` with purpose, explanation, expected result, safety notes, and a practice task.
- `lab.py` with the complete runnable example.

## Requirements
- Python 3
- No third-party packages

## How to practise
You can type each code line into Python Shell (`>>>`) as requested, or run the complete script from the lab folder.

Example:

```bash
cd Lab_01_copy
python3 lab.py
```

On Windows, use `py lab.py` or `python lab.py`.

## Recommended learning order
Complete Labs 1–3, then Lab 4, then Labs 5–11, and finish with Lab 12.

Each lab is self-contained and creates its own sample files/directories where needed. This lets you run labs independently without relying on files created by earlier labs.

## Labs included

1. `copy()` – copy a file
2. `copy2()` – copy a file and preserve metadata
3. `copyfile()` – copy file contents
4. `copytree()` – copy a directory tree
5. `move()` – move a file
6. `disk_usage()` – inspect filesystem space
7. `which()` – find an executable in PATH
8. `make_archive()` – create a ZIP archive
9. `unpack_archive()` – extract an archive
10. `get_archive_formats()` – list supported archive formats
11. `get_terminal_size()` – inspect terminal dimensions
12. `rmtree()` – delete a directory tree

## Important safety reminder
`rmtree()` permanently deletes the target directory and its contents. The provided example creates and deletes only its own `project_backup` practice folder. Review the target path before running deletion commands.
