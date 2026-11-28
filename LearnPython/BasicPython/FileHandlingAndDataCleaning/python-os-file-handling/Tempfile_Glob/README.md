# Python `tempfile` and `glob` — From Scratch to Practical Projects

A detailed beginner-to-advanced teaching guide to temporary files and folders, wildcard patterns, and searching for files in organized directory structures.

## 1. What are these modules?

### `tempfile`

`tempfile` is a Python standard-library module for creating temporary files and directories safely.

Why do we need it?
- A program may need a temporary place to process a downloaded file.
- An application may generate intermediate data before producing a final report.
- A test may need temporary files without polluting the project folder.
- A program may unpack or transform data and then clean it up.
- Multiple program runs should avoid accidentally using the same temporary filename.

Typical functions:
- `tempfile.TemporaryDirectory()`
- `tempfile.TemporaryFile()`
- `tempfile.NamedTemporaryFile()`
- `tempfile.mkstemp()`
- `tempfile.mkdtemp()`
- `tempfile.gettempdir()`

### `glob`

`glob` is a standard-library module for finding file paths using wildcard patterns.

Why do we need it?
- Find all `.csv` files in a folder.
- Find files whose names begin with `report`.
- Find files with a specific naming pattern.
- Collect matching files for batch processing.
- Search directory trees with recursive patterns.

Typical functions:
- `glob.glob()`
- `glob.iglob()`
- `glob.escape()`

The `pathlib` module also provides `.glob()` and `.rglob()` methods. This course teaches the standalone `glob` module and compares it with `pathlib`.

Both modules are included with Python. No `pip install` is required.

---

## Repository structure

```text
Python_Tempfile_Glob_Toolkit/
│
├── README.md
├── requirements.txt
│
├── project_01_tempfile_workspace/
│   ├── README.md
│   ├── main.py
│   ├── temp_operations.py
│   ├── data/
│   │   └── input/
│   │       └── source.txt
│   ├── output/
│   └── logs/
│
└── project_02_glob_file_search/
    ├── README.md
    ├── main.py
    ├── search_tools.py
    ├── data/
    │   ├── incoming/
    │   │   ├── sales_jan.csv
    │   │   ├── sales_feb.csv
    │   │   ├── notes.txt
    │   │   └── report_2026.txt
    │   └── nested/
    │       ├── archive/
    │       │   └── sales_mar.csv
    │       └── logs/
    │           ├── app_001.log
    │           └── app_002.log
    └── output/
```

Temporary files created by Project 1 are managed in the operating system's temporary area, not scattered throughout the repository. Project 2 keeps sample search data in `data/` and its generated inventory in `output/`.

## Learning outcomes

By the end, learners should be able to:
1. Explain what temporary files and directories are.
2. Explain why temporary storage is useful.
3. Identify the system temporary directory.
4. Create temporary files and folders.
5. Understand automatic cleanup using context managers.
6. Use `TemporaryDirectory`, `TemporaryFile`, and `NamedTemporaryFile`.
7. Understand file handles, file names, and cleanup behavior.
8. Create temporary files that need a visible path.
9. Use wildcard patterns such as `*`, `?`, and character ranges.
10. Search files with `glob`, `iglob`, and recursive patterns.
11. Escape wildcard characters in literal filenames.
12. Compare `glob` with `pathlib.glob()` and `os.walk()`.
13. Build a temporary processing workspace.
14. Build a file discovery and inventory tool.

---

# Part 1 — Foundations

## Chapter 1 — What is a temporary file?

A temporary file is a file created for short-term use. A program may need to store intermediate output before it is copied, uploaded, transformed, or deleted.

Example workflow:

1. Download or generate some data.
2. Save it temporarily.
3. Process it.
4. Produce a final output.
5. Remove the temporary data.

Temporary data is not necessarily unimportant. It may contain sensitive information, so cleanup and access permissions matter.

## Chapter 2 — Why not create a normal file?

Suppose every program run creates:

```text
processing.txt
```

Problems:
- Another program run may use the same name.
- Existing content may be overwritten.
- The program may crash and leave old files behind.
- Multiple users or processes may conflict.
- Cleanup becomes the developer's responsibility.

The `tempfile` module helps create temporary resources with unique names and suitable defaults.

## Chapter 3 — What is the system temporary directory?

Python can identify the default temporary directory:

```python
import tempfile

print(tempfile.gettempdir())
```

The result depends on the operating system and environment. It may be a location such as a temporary folder on Windows or `/tmp` on Linux.

Do not hard-code a temporary folder path. Ask Python for the configured location.

## Chapter 4 — What is `glob`?

A glob pattern is a filename pattern that uses wildcard characters.

For example:

```text
*.csv
```

means filenames ending in `.csv`.

Glob is useful when you want to process a group of files based on naming rules rather than typing each filename manually.

## Chapter 5 — Glob wildcard symbols

| Pattern | Meaning | Example |
|---|---|---|
| `*` | Any number of characters, including none | `report*.csv` |
| `?` | Exactly one character | `file?.txt` |
| `[abc]` | One character from the set | `file[123].txt` |
| `[0-9]` | One character in a range | `log[0-9].txt` |
| `[!abc]` | One character not in the set | `file[!0].txt` |

Examples:
- `*.txt` — all `.txt` files in the searched folder.
- `sales_*.csv` — CSV files beginning with `sales_`.
- `report_202?.txt` — one-character wildcard after `202`.
- `image_[0-9].png` — image files with one digit in that position.

Patterns are matched against path names. Case sensitivity can differ by operating system and filesystem.

---

# Part 2 — `tempfile` from beginner to advanced

## Chapter 6 — Import and first temporary directory

```python
import tempfile

print("Temporary directory:", tempfile.gettempdir())
```

This only reports the location. It does not create a new directory.

## Chapter 7 — Create a temporary directory

Use `TemporaryDirectory()`:

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    print("Temporary folder:", temp_path)

    sample_file = temp_path / "sample.txt"
    sample_file.write_text("Temporary data", encoding="utf-8")

    print(sample_file.read_text(encoding="utf-8"))
```

When execution leaves the `with` block, Python cleans up the temporary directory and its contents.

This is usually the recommended pattern for temporary workspaces.

## Chapter 8 — Why use a context manager?

A context manager manages setup and cleanup.

Without a context manager, a program must remember to clean up even if an error occurs.

With `with`:

```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Use temporary resources here.
    pass

# Cleanup has happened after the block.
```

The cleanup occurs when the block exits normally or due to an exception, subject to the platform and filesystem allowing cleanup.

## Chapter 9 — Create a temporary file with `TemporaryFile`

```python
import tempfile

with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as temp_file:
    temp_file.write("Temporary content")
    temp_file.seek(0)
    print(temp_file.read())
```

`TemporaryFile()` creates a temporary file-like object. On some platforms the file may not have a normal visible filename, or it may be removed/unlinked immediately. Use it when you need a temporary file handle rather than a persistent path.

## Chapter 10 — Understand file modes

Common modes:
- `"w+t"` — text mode, write and read.
- `"w+b"` — binary mode, write and read.
- `"r+t"` — text mode, read and write an existing file.
- `"w"` — write text.
- `"wb"` — write bytes.

`TemporaryFile()` commonly starts with a readable/writable mode. Choose the mode that matches your data.

## Chapter 11 — Create a named temporary file

Use `NamedTemporaryFile()` when you need a temporary file with a filesystem name:

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".txt",
    prefix="python_demo_",
    delete=True,
    encoding="utf-8",
) as temp_file:
    print("Temporary file path:", temp_file.name)
    temp_file.write("A named temporary file")

    # Flush so another reader can see the written content.
    temp_file.flush()
    print(Path(temp_file.name).read_text(encoding="utf-8"))
```

Platform note: on Windows, reopening a named temporary file while it is still open can have sharing/deletion constraints. If another process must open the file by name, consider `delete=False`, close it first, and then remove it explicitly. Always clean up.

## Chapter 12 — Keep a named temporary file after closing

```python
import os
import tempfile
from pathlib import Path

temp_path = None

try:
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8",
    ) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write("This file remains after the context closes.")

    print(temp_path.read_text(encoding="utf-8"))
finally:
    if temp_path is not None:
        temp_path.unlink(missing_ok=True)
```

`delete=False` means Python does not automatically remove the file when it closes. You are responsible for deleting it.

## Chapter 13 — Create a temporary file with `mkstemp()`

```python
import os
import tempfile

file_descriptor, file_path = tempfile.mkstemp(
    prefix="report_",
    suffix=".tmp",
)

try:
    with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
        file.write("Created using mkstemp")
    print("File path:", file_path)
finally:
    if os.path.exists(file_path):
        os.remove(file_path)
```

`mkstemp()` returns:
- A low-level file descriptor.
- The path to the created file.

Close the descriptor. If you wrap it with `os.fdopen()`, closing the file object closes the descriptor.

## Chapter 14 — Create a temporary directory with `mkdtemp()`

```python
import tempfile
import shutil

temp_dir = tempfile.mkdtemp(prefix="python_lab_")
print("Created:", temp_dir)

try:
    # Perform temporary work here.
    pass
finally:
    shutil.rmtree(temp_dir)
```

Unlike `TemporaryDirectory()`, `mkdtemp()` does not automatically clean itself up. You must remove the directory.

Prefer `TemporaryDirectory()` for ordinary application code.

## Chapter 15 — Prefix and suffix

You can make temporary names easier to identify:

```python
import tempfile

with tempfile.NamedTemporaryFile(
    prefix="student_",
    suffix=".csv",
    mode="w",
    encoding="utf-8",
) as file:
    print(file.name)
```

- `prefix` adds text before the generated name.
- `suffix` adds an extension or text after the generated name.
- The random portion helps avoid filename collisions.

## Chapter 16 — Choose a parent directory

```python
import tempfile
from pathlib import Path

custom_parent = Path("output")
custom_parent.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory(dir=custom_parent, prefix="work_") as temp_dir:
    print("Temporary workspace:", temp_dir)
```

Use this when temporary work must be placed on a specific volume or within a controlled directory. Ensure the parent directory has suitable permissions and enough space.

## Chapter 17 — Temporary binary data

```python
import tempfile

with tempfile.TemporaryFile(mode="w+b") as temp_file:
    temp_file.write(b"\x00\x01\x02\x03")
    temp_file.seek(0)
    data = temp_file.read()
    print(data)
```

Binary mode is useful for byte content such as compressed data or file transformations.

## Chapter 18 — Security and cleanup

- Use `tempfile` instead of guessing a temporary filename.
- Do not create predictable temporary names manually.
- Do not put secrets in temporary files unless necessary.
- Restrict permissions when handling sensitive data.
- Use context managers for automatic cleanup.
- Do not assume a temporary file is encrypted.
- Remember that cleanup may fail if another process holds a file open or permissions prevent removal.
- Do not use `delete=False` without a clear cleanup plan.

---

# Part 3 — `glob` from beginner to advanced

## Chapter 19 — First glob search

Create a folder with a few files, then:

```python
import glob

matches = glob.glob("data/incoming/*.csv")

for path in matches:
    print(path)
```

`glob.glob()` returns a list of matching path strings.

## Chapter 20 — Search for different extensions

```python
import glob

for pattern in ["*.txt", "*.csv", "*.log"]:
    print("Pattern:", pattern)
    for match in glob.glob(f"data/incoming/{pattern}"):
        print(match)
```

Each pattern is a separate search.

## Chapter 21 — Prefix and suffix patterns

```python
import glob

print(glob.glob("data/incoming/sales_*.csv"))
print(glob.glob("data/incoming/report_*.txt"))
```

Use patterns to find files that follow a naming convention.

## Chapter 22 — One-character wildcard `?`

```python
import glob

print(glob.glob("data/incoming/sales_???.csv"))
```

This matches exactly three characters after `sales_` before `.csv`.

For example, `sales_jan.csv` matches, while `sales_january.csv` does not.

## Chapter 23 — Character sets and ranges

```python
import glob

print(glob.glob("data/incoming/report_[0-9].txt"))
print(glob.glob("data/incoming/file[abc].txt"))
```

- `[0-9]` matches one digit.
- `[abc]` matches one of the listed characters.
- `[!0-9]` matches one character that is not a digit.

## Chapter 24 — Recursive glob

```python
import glob

matches = glob.glob("data/**/*.csv", recursive=True)

for match in matches:
    print(match)
```

With `recursive=True`, `**` can match zero or more directory levels.

This is useful when files are stored in nested folders.

## Chapter 25 — Use `iglob()` for iteration

```python
import glob

for match in glob.iglob("data/**/*.log", recursive=True):
    print(match)
```

`iglob()` returns an iterator instead of building a complete list first. It can be useful when many paths may match.

## Chapter 26 — Escape special wildcard characters

If a real filename contains wildcard characters such as `[` or `]`, use `glob.escape()` when constructing a literal pattern:

```python
import glob

filename = "data/incoming/report[final].txt"
pattern = glob.escape(filename)

print(glob.glob(pattern))
```

Without escaping, the brackets may be interpreted as a character set.

## Chapter 27 — Return only filenames or full paths

```python
import glob
import os

matches = glob.glob("data/incoming/*.csv")

for path in matches:
    print("Full path:", path)
    print("Filename:", os.path.basename(path))
```

Glob usually returns paths in the same general form as the search pattern. Use `os.path.basename()` or `pathlib.Path(path).name` when you only need the filename.

## Chapter 28 — Sort search results

The order of results is not guaranteed. Sort them when deterministic output is required:

```python
import glob

matches = sorted(glob.glob("data/**/*.csv", recursive=True))

for match in matches:
    print(match)
```

## Chapter 29 — Glob with `pathlib`

```python
from pathlib import Path

data_dir = Path("data")

for csv_file in data_dir.rglob("*.csv"):
    print(csv_file)
```

Comparison:
- `glob.glob()` returns path strings.
- `Path.glob()` returns `Path` objects for direct pattern matches.
- `Path.rglob()` searches recursively.
- `glob.iglob()` is useful for lazy iteration.

## Chapter 30 — Glob vs `os.walk()`

Use glob when matching names with patterns is the main goal.

Use `os.walk()` when you need explicit control over each directory and its subdirectories, for example pruning folders or collecting detailed traversal information.

## Chapter 31 — Common glob mistakes

1. Forgetting `recursive=True` when using `**` with `glob.glob()`.
2. Searching the wrong current working directory.
3. Assuming results are sorted.
4. Assuming case matching behaves identically on every OS/filesystem.
5. Expecting `*.csv` to search all nested folders without `**`.
6. Forgetting that `glob()` normally returns strings, not `Path` objects.
7. Forgetting to escape literal bracket characters in filenames.

---

# Part 4 — Combining `tempfile` and `glob`

## Chapter 32 — Find files and process them in a temporary workspace

```python
import glob
import tempfile
import shutil
from pathlib import Path

source_folder = Path("data/incoming")

with tempfile.TemporaryDirectory(prefix="csv_work_") as temp_dir:
    workspace = Path(temp_dir)

    for source_name in glob.glob(str(source_folder / "*.csv")):
        source_path = Path(source_name)
        destination = workspace / source_path.name
        shutil.copy2(source_path, destination)

    print("Temporary workspace files:")
    for item in workspace.iterdir():
        print(item.name)
```

This example:
1. Finds CSV files.
2. Creates a temporary workspace.
3. Copies matching files into it.
4. Lists the temporary copies.
5. Automatically cleans the workspace when the block exits.

## Chapter 33 — Process and produce a permanent output

A temporary workspace is for intermediate work. If the result must be retained, explicitly copy or write it to a permanent output folder before leaving the context manager.

```python
import tempfile
import shutil
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
final_file = output_dir / "final_result.txt"

with tempfile.TemporaryDirectory() as temp_dir:
    working_file = Path(temp_dir) / "result.txt"
    working_file.write_text("Processed successfully", encoding="utf-8")

    shutil.copy2(working_file, final_file)

print("Permanent output:", final_file)
```

---

# Part 5 — Practical projects

## Project 1 — Temporary Processing Workspace

Location: `project_01_tempfile_workspace/`

Build a program that:
- Reads a permanent sample input file.
- Creates a temporary working directory.
- Writes an intermediate file.
- Processes the content.
- Saves a permanent result under `output/`.
- Logs the operation.
- Automatically cleans the temporary workspace.

Run:

```bash
python project_01_tempfile_workspace/main.py
```

Read the project README for its detailed walkthrough and exercises.

## Project 2 — Glob File Search and Inventory

Location: `project_02_glob_file_search/`

Build a file-discovery tool that:
- Searches `.csv`, `.txt`, and `.log` files.
- Uses wildcard patterns.
- Searches recursively.
- Sorts the results.
- Reports file sizes.
- Writes a CSV inventory to `output/`.

Run:

```bash
python project_02_glob_file_search/main.py
```

Read the project README for its detailed walkthrough and exercises.

---

# Part 6 — Practice questions

1. What is a temporary file?
2. Why should programs avoid predictable temporary filenames?
3. What does `tempfile.gettempdir()` return?
4. What is the difference between `TemporaryFile()` and `NamedTemporaryFile()`?
5. What does `TemporaryDirectory()` clean up?
6. Why is a `with` statement useful with temporary resources?
7. What does `delete=False` mean?
8. What does `mkstemp()` return?
9. Why is `mkdtemp()` easier to misuse than `TemporaryDirectory()`?
10. What are `prefix` and `suffix` used for?
11. What does `*` mean in a glob pattern?
12. What does `?` mean?
13. What does `[0-9]` match?
14. What is the purpose of `glob.escape()`?
15. What is the difference between `glob.glob()` and `glob.iglob()`?
16. What does `recursive=True` enable with `**`?
17. Why should glob results be sorted for reports?
18. What is the difference between `glob` and `Path.rglob()`?
19. When might `os.walk()` be a better fit?
20. How can you preserve a result created inside a temporary directory?

## Final teaching sequence

1. Explain why programs need temporary storage.
2. Demonstrate the system temporary directory.
3. Create a `TemporaryDirectory()` and observe automatic cleanup.
4. Compare temporary file APIs.
5. Explain `delete=False` and manual cleanup.
6. Introduce glob wildcards.
7. Search by extension, prefix, and character pattern.
8. Search recursively with `**`.
9. Compare `glob`, `iglob`, and `pathlib` glob methods.
10. Combine glob search with a temporary workspace.
11. Build Project 1.
12. Build Project 2.
13. Ask students to change the working directory and verify that project paths still work.

## Key takeaway

Use **`tempfile` for safe short-lived files and directories** and **`glob` to discover files using naming patterns**. Use context managers for cleanup, explicit permanent output folders for results that must remain, and recursive glob patterns when files are nested.
