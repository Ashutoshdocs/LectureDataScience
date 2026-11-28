# Python `pathlib` and `shutil` — From Scratch to Practical Projects

A beginner-to-advanced teaching package explaining how Python works with file-system paths and how it copies, moves, archives, and manages files and folders.

## First understand the roles

- **`pathlib`** provides an object-oriented way to represent and work with filesystem paths. It helps build paths, inspect them, create folders, read/write files, and navigate directory trees.
- **`shutil`** provides higher-level file operations such as copying, moving, deleting directory trees, and creating/extracting archives.

They work well together:
- Use `pathlib` to describe and inspect the source and destination paths.
- Use `shutil` to perform higher-level operations on those paths.

Both are part of Python's standard library. No `pip install` is needed.

---

## Repository structure

```text
Python_Pathlib_Shutil_Toolkit/
│
├── README.md
├── requirements.txt
│
├── project_01_pathlib_file_explorer/
│   ├── README.md
│   ├── main.py
│   ├── path_queries.py
│   ├── data/
│   │   ├── input/
│   │   │   ├── notes.txt
│   │   │   └── employees.csv
│   │   └── nested/
│   │       └── sample.log
│   └── output/
│
└── project_02_shutil_backup_archiver/
    ├── README.md
    ├── main.py
    ├── backup_manager.py
    ├── data/
    │   ├── source/
    │   │   ├── report.txt
    │   │   └── records.csv
    │   └── destination/
    ├── backups/
    ├── archives/
    └── logs/
```

Input files, generated output, backups, archives, and logs are kept in separate folders. Project code does not scatter generated files beside source files.

## Learning outcomes

By the end, learners should be able to:
1. Explain why path handling is needed in real Python applications.
2. Explain the difference between `pathlib` and `shutil`.
3. Create `Path` objects and join paths using `/`.
4. Understand absolute paths, relative paths, parent, name, suffix, and stem.
5. Check whether paths exist and whether they are files or directories.
6. Create, list, search, read, write, rename, and remove files using `pathlib`.
7. Use `glob()` and `rglob()` to search files.
8. Copy files and folders using `shutil`.
9. Move and safely remove directories.
10. Create and extract ZIP archives.
11. Compare file metadata and disk usage.
12. Build a file explorer and a backup/archive utility.

---

# Part 1 — Foundations

## Chapter 1 — Why do we need path handling?

A path tells a program where a file or folder is located.

Examples:

Windows:
```text
C:\Users\Student\Documents\report.txt
```

Linux/macOS:
```text
/home/student/Documents/report.txt
```

A Python program often needs to:
- Find a configuration file.
- Read input data.
- Save generated reports.
- Create folders for output.
- Move processed files into an archive.
- Back up project data.
- Search folders for particular file types.

If paths are written in a machine-specific way, the program may work on one computer and fail on another.

## Chapter 2 — What is `pathlib`?

`pathlib` is a standard-library module that represents filesystem paths as objects.

```python
from pathlib import Path

project_folder = Path("my_project")
data_folder = project_folder / "data"
input_file = data_folder / "input.txt"

print(input_file)
```

The `/` operator joins path parts. It does not divide numbers here.

Why is this useful?
- Cleaner path construction.
- Less manual separator handling.
- Convenient methods such as `.exists()`, `.is_file()`, `.mkdir()`, `.read_text()`, and `.write_text()`.
- Easier navigation with `.parent`, `.name`, `.stem`, and `.suffix`.

## Chapter 3 — What is `shutil`?

`shutil` means shell utilities. It provides high-level operations on files and collections of files.

Typical uses:
- `shutil.copy()` — copy a file.
- `shutil.copy2()` — copy a file and attempt to preserve metadata.
- `shutil.copytree()` — copy a directory tree.
- `shutil.move()` — move a file or directory.
- `shutil.rmtree()` — remove a directory tree.
- `shutil.make_archive()` — create an archive.
- `shutil.unpack_archive()` — extract an archive.
- `shutil.disk_usage()` — inspect disk usage.

## Chapter 4 — `pathlib` vs `shutil`

| `pathlib` | `shutil` |
|---|---|
| Represents and navigates paths | Performs high-level file operations |
| Checks whether a path exists | Copies files and folders |
| Creates directories | Moves files and folders |
| Reads and writes text/bytes | Creates and extracts archives |
| Searches with `glob()` and `rglob()` | Removes directory trees |
| Example: `Path("data").mkdir()` | Example: `shutil.copy2(src, dst)` |

They are not competitors. In real applications, use both together.

## Chapter 5 — Setup and first program

No external installation is required.

```bash
python --version
```

Create `first_pathlib_shutil.py`:

```python
from pathlib import Path
import shutil

current_folder = Path.cwd()
print("Current folder:", current_folder)

print("Free/total/used disk bytes:", shutil.disk_usage(current_folder))
```

Run:

```bash
python first_pathlib_shutil.py
```

---

# Part 2 — `pathlib` from beginner to advanced

## Chapter 6 — Create a Path object

```python
from pathlib import Path

path = Path("data/input/notes.txt")

print(path)
print(type(path))
```

A `Path` object represents a location. Creating a `Path` object does not create the file or folder on disk.

## Chapter 7 — Join paths

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
INPUT_FILE = INPUT_DIR / "notes.txt"

print(INPUT_FILE)
```

Use `/` to combine path components. This is portable across Windows, Linux, and macOS.

## Chapter 8 — Current directory, script directory, and absolute path

```python
from pathlib import Path

print("Current working directory:", Path.cwd())
print("Script file:", Path(__file__))
print("Script directory:", Path(__file__).resolve().parent)
print("Absolute path:", Path("data/input.txt").resolve())
```

- `Path.cwd()` is the process's current working directory.
- `Path(__file__)` identifies the current script file.
- `.resolve()` produces an absolute, normalized path (subject to filesystem and platform behavior).
- `.parent` gets the containing directory.

The current working directory and script directory can be different.

## Chapter 9 — Path components

```python
from pathlib import Path

path = Path("reports/annual/sales_2026.csv")

print(path.name)       # sales_2026.csv
print(path.stem)       # sales_2026
print(path.suffix)     # .csv
print(path.parent)     # reports/annual
print(path.parts)      # individual path components
```

For a name with multiple suffixes:

```python
path = Path("backup.tar.gz")
print(path.suffix)       # .gz
print(path.suffixes)     # ['.tar', '.gz']
```

## Chapter 10 — Check whether a path exists

```python
from pathlib import Path

path = Path("data/input/notes.txt")

print(path.exists())
print(path.is_file())
print(path.is_dir())
```

- `.exists()` checks whether the path exists.
- `.is_file()` checks whether it is a file.
- `.is_dir()` checks whether it is a directory.

## Chapter 11 — Create directories

```python
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

nested_dir = Path("data/archive/2026")
nested_dir.mkdir(parents=True, exist_ok=True)
```

- `parents=True` creates missing parent folders.
- `exist_ok=True` avoids an exception if the folder already exists.

## Chapter 12 — List directory contents

```python
from pathlib import Path

folder = Path("data")

for item in folder.iterdir():
    print(item, "file?", item.is_file(), "directory?", item.is_dir())
```

`iterdir()` lists direct children only; it does not recursively search subfolders.

## Chapter 13 — Search with `glob()`

Search direct children matching a pattern:

```python
from pathlib import Path

folder = Path("data/input")

for csv_file in folder.glob("*.csv"):
    print(csv_file)
```

Examples:
- `"*.txt"` — text files directly in the folder.
- `"report*"` — names beginning with `report`.
- `"*.csv"` — CSV files directly in the folder.

## Chapter 14 — Search recursively with `rglob()`

```python
from pathlib import Path

root = Path("data")

for csv_file in root.rglob("*.csv"):
    print(csv_file)
```

`rglob()` searches through nested directories too.

## Chapter 15 — Read text files

```python
from pathlib import Path

file_path = Path("data/input/notes.txt")
content = file_path.read_text(encoding="utf-8")
print(content)
```

For large files, stream line by line:

```python
with Path("data/input/notes.txt").open("r", encoding="utf-8") as file:
    for line in file:
        print(line.rstrip())
```

## Chapter 16 — Write and append text

```python
from pathlib import Path

output_file = Path("output/message.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

output_file.write_text("First line\n", encoding="utf-8")
```

Append using `.open()`:

```python
with output_file.open("a", encoding="utf-8") as file:
    file.write("Another line\n")
```

Be aware: `write_text()` replaces existing file content.

## Chapter 17 — Read and write bytes

For images, PDFs, ZIP files, and other binary content:

```python
from pathlib import Path

source = Path("data/sample.bin")
destination = Path("output/sample_copy.bin")

binary_content = source.read_bytes()
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_bytes(binary_content)
```

For large binary files, prefer streaming or use `shutil.copy2()` rather than loading the entire file into memory.

## Chapter 18 — Rename and replace

```python
from pathlib import Path

old_path = Path("output/old_name.txt")
new_path = Path("output/new_name.txt")

old_path.rename(new_path)
```

`rename()` changes the path name. Behavior when the destination already exists can vary by platform.

`replace()` replaces the destination if permitted:

```python
source = Path("output/new_name.txt")
destination = Path("output/final_name.txt")
source.replace(destination)
```

Use these carefully; they change filesystem state.

## Chapter 19 — Delete files and empty directories

```python
from pathlib import Path

file_path = Path("output/temporary.txt")
if file_path.exists() and file_path.is_file():
    file_path.unlink()
```

Remove an empty directory:

```python
empty_folder = Path("output/empty_folder")
if empty_folder.exists() and empty_folder.is_dir():
    empty_folder.rmdir()
```

- `.unlink()` removes a file or symlink.
- `.rmdir()` removes an empty directory only.
- Neither is a recursive directory-tree deletion tool.

## Chapter 20 — File metadata

```python
from pathlib import Path
from datetime import datetime

file_path = Path("data/input/notes.txt")

if file_path.is_file():
    details = file_path.stat()
    print("Size:", details.st_size, "bytes")
    print("Modified:", datetime.fromtimestamp(details.st_mtime))
```

Metadata availability and timestamp precision depend on the operating system and filesystem.

## Chapter 21 — Find the parent and navigate upwards

```python
from pathlib import Path

path = Path("project/data/input/notes.txt")

print(path.parent)
print(path.parent.parent)
print(path.parents[0])
print(path.parents[1])
```

`.parents` is an indexed sequence of ancestor paths. Index `0` is the immediate parent.

## Chapter 22 — Relative paths

```python
from pathlib import Path

project = Path("/home/student/project")
file_path = Path("/home/student/project/data/input.csv")

print(file_path.relative_to(project))
```

`.relative_to()` requires the target path to be under the base path; otherwise it raises `ValueError`.

## Chapter 23 — Resolve symlinks and normalize

```python
from pathlib import Path

path = Path("data/../data/input.txt")
print(path.resolve())
```

On supported systems, `resolve()` resolves path components and symlinks. Exact behavior can depend on whether paths exist and on the platform.

## Chapter 24 — Handle errors

```python
from pathlib import Path

file_path = Path("missing.txt")

try:
    text = file_path.read_text(encoding="utf-8")
except FileNotFoundError:
    print("File was not found.")
except PermissionError:
    print("Permission denied.")
except OSError as error:
    print("Filesystem error:", error)
```

Common errors include `FileNotFoundError`, `FileExistsError`, `PermissionError`, `IsADirectoryError`, and `NotADirectoryError`.

---

# Part 3 — `shutil` from beginner to advanced

## Chapter 25 — Import and understand `shutil`

```python
import shutil

print(shutil.__doc__[:300])
```

`shutil` works with filesystem paths. You can pass `Path` objects to its common functions.

## Chapter 26 — Copy a file with `copy()`

```python
from pathlib import Path
import shutil

source = Path("data/input/notes.txt")
destination_dir = Path("output/copies")
destination_dir.mkdir(parents=True, exist_ok=True)

destination = destination_dir / source.name
shutil.copy(source, destination)
```

`copy()` copies file content and permission mode. It does not preserve all metadata.

## Chapter 27 — Copy a file with `copy2()`

```python
import shutil
from pathlib import Path

source = Path("data/input/notes.txt")
destination = Path("output/notes_backup.txt")

destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, destination)
```

`copy2()` attempts to preserve additional metadata such as modification times. Some metadata may not be preserved on every platform.

## Chapter 28 — Copy an entire directory

```python
import shutil
from pathlib import Path

source_dir = Path("data/source_folder")
destination_dir = Path("output/source_folder_copy")

shutil.copytree(source_dir, destination_dir)
```

By default, the destination must not already exist. To merge into an existing destination on supported Python versions:

```python
shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
```

Use `dirs_exist_ok=True` only when merging/overwriting behavior is intended.

## Chapter 29 — Move files and folders

```python
import shutil
from pathlib import Path

source = Path("output/processed.txt")
destination = Path("data/archive/processed.txt")
destination.parent.mkdir(parents=True, exist_ok=True)

shutil.move(str(source), str(destination))
```

`shutil.move()` can move a file or directory. Depending on filesystem boundaries, it may use a rename or copy-and-remove strategy.

## Chapter 30 — Remove a directory tree

```python
import shutil
from pathlib import Path

temporary_folder = Path("output/temporary_work")

if temporary_folder.exists() and temporary_folder.is_dir():
    shutil.rmtree(temporary_folder)
```

**Danger:** `rmtree()` recursively deletes the folder and its contents. Validate the target path, keep it inside a dedicated test folder, and never use an unchecked user-provided path.

## Chapter 31 — Create ZIP archives

```python
import shutil
from pathlib import Path

project_folder = Path("data")
archive_base = Path("archives/data_backup")

archive_base.parent.mkdir(parents=True, exist_ok=True)

created_archive = shutil.make_archive(
    str(archive_base),
    "zip",
    root_dir=str(project_folder)
)

print(created_archive)
```

`make_archive()` returns the created archive path. The archive format must be supported by the Python build and platform.

## Chapter 32 — Extract archives

```python
import shutil
from pathlib import Path

archive_path = Path("archives/data_backup.zip")
extract_dir = Path("output/extracted")
extract_dir.mkdir(parents=True, exist_ok=True)

shutil.unpack_archive(str(archive_path), str(extract_dir))
```

Only extract archives from trusted sources. Archives can contain unexpected paths or large amounts of data; inspect untrusted archives and use safe extraction practices.

## Chapter 33 — Disk usage

```python
import shutil
from pathlib import Path

usage = shutil.disk_usage(Path.cwd())

print("Total:", usage.total)
print("Used:", usage.used)
print("Free:", usage.free)
```

Values are bytes. Convert to GiB:

```python
print("Free GiB:", round(usage.free / (1024 ** 3), 2))
```

## Chapter 34 — Which copy function should I use?

| Function | Typical purpose |
|---|---|
| `copy()` | Copy content and permission mode |
| `copy2()` | Copy and attempt to preserve more metadata |
| `copyfile()` | Copy file content only |
| `copytree()` | Copy a directory tree |
| `move()` | Move a file or directory |
| `rmtree()` | Recursively delete a directory tree |
| `make_archive()` | Create an archive |
| `unpack_archive()` | Extract an archive |

## Chapter 35 — Copy with error handling

```python
import shutil
from pathlib import Path

source = Path("data/input/notes.txt")
destination = Path("output/notes.txt")

try:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    print("Copy completed.")
except FileNotFoundError:
    print("Source file or destination folder was not found.")
except PermissionError:
    print("Permission denied.")
except shutil.SameFileError:
    print("Source and destination refer to the same file.")
except OSError as error:
    print("Copy failed:", error)
```

## Chapter 36 — Disk and file operations are not database transactions

A copy or move can fail partway because of permissions, disk space, network filesystems, or device errors. For important data:
- Keep the original until the new copy is verified.
- Use checksums when integrity matters.
- Log operations.
- Test recovery procedures.
- Do not assume a successful function call means a complete backup strategy.

---

# Part 4 — Combining `pathlib` and `shutil`

## Chapter 37 — Recommended pattern

```python
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "data" / "input"
BACKUP_DIR = BASE_DIR / "backups"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

for source_file in SOURCE_DIR.glob("*"):
    if source_file.is_file():
        destination = BACKUP_DIR / source_file.name
        shutil.copy2(source_file, destination)
```

`pathlib` builds and checks paths. `shutil` performs the copy.

## Chapter 38 — Organize a real project

```text
application/
├── main.py
├── config/
├── data/
│   ├── input/
│   └── processed/
├── backups/
├── archives/
├── output/
└── logs/
```

Keep:
- Original input in `data/input/`.
- Processed data in `data/processed/`.
- Backups in `backups/`.
- Compressed archives in `archives/`.
- Reports in `output/`.
- Logs in `logs/`.

## Chapter 39 — Backup safety checklist

1. Confirm the source folder is correct.
2. Confirm the destination is not inside an unintended source path.
3. Do not delete source files after copying until the backup is verified.
4. Use unique backup names or a clear overwrite policy.
5. Log what was copied and when.
6. Check file counts and sizes; use hashes for stronger integrity checks.
7. Test restoring files from the backup.
8. Protect backups because they may contain sensitive information.

---

# Part 5 — Practical projects

## Project 1 — Pathlib File Explorer

Location: `project_01_pathlib_file_explorer/`

Build a small command-line explorer that:
- Shows the project and current working directories.
- Lists direct children.
- Searches recursively by extension.
- Shows file name, suffix, size, and parent folder.
- Reads a sample text file.
- Writes a file inventory report under `output/`.

Run:

```bash
python project_01_pathlib_file_explorer/main.py
```

See that project's README for its detailed walkthrough and exercises.

## Project 2 — Shutil Backup and Archiver

Location: `project_02_shutil_backup_archiver/`

Build a backup tool that:
- Copies source files using `copy2()`.
- Copies a complete folder tree using `copytree()`.
- Creates a ZIP archive.
- Extracts the ZIP into a separate restore folder.
- Reports disk usage.
- Writes an operation log.
- Keeps the original source files untouched.

Run:

```bash
python project_02_shutil_backup_archiver/main.py
```

See that project's README for the detailed walkthrough and exercises.

---

# Part 6 — Practice questions

1. What is a filesystem path?
2. Why is `pathlib` preferred over manual string concatenation?
3. Does creating a `Path` object create a file?
4. What is the difference between `Path.cwd()` and `Path(__file__).resolve().parent`?
5. What do `.name`, `.stem`, `.suffix`, and `.parent` return?
6. What is the difference between `glob()` and `rglob()`?
7. What does `mkdir(parents=True, exist_ok=True)` do?
8. What is the difference between `.unlink()` and `.rmdir()`?
9. Why can `write_text()` overwrite existing data?
10. What is the difference between `shutil.copy()` and `copy2()`?
11. When should you use `copytree()`?
12. What can `shutil.move()` do?
13. Why is `shutil.rmtree()` dangerous?
14. What does `make_archive()` return?
15. What does `unpack_archive()` do?
16. What does `disk_usage()` report?
17. Why should backups be verified?
18. Why should untrusted archives not be extracted blindly?
19. How do `pathlib` and `shutil` complement each other?
20. Why should source, backup, archive, and output folders be separate?

## Final teaching sequence

1. Explain paths with Windows and Linux examples.
2. Introduce `Path` objects and path joining.
3. Demonstrate current directory vs script directory.
4. Inspect path components and existence.
5. Create folders, list files, and search recursively.
6. Read/write text and inspect metadata.
7. Introduce `shutil.copy()` and `copy2()`.
8. Demonstrate `copytree()` and `move()`.
9. Explain the risk of `rmtree()`.
10. Create and extract ZIP archives.
11. Build Project 1 in class.
12. Build Project 2 as a student lab.
13. Ask students to run both projects from a different working directory.

## Key takeaway

Use **`pathlib` to represent, build, inspect, and navigate paths**. Use **`shutil` for higher-level operations such as copying, moving, archiving, and deleting directory trees**. Together they make file-management code cleaner and more maintainable.
