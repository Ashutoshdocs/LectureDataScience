# LAB 6 — Python `pathlib` Module

## Purpose
Work with filesystem paths.

## What you will learn
`Path` represents a filesystem path. The `/` operator joins path components. Methods such as `mkdir()`, `write_text()`, `read_text()`, and `glob()` make common file tasks readable.

## Code

```python
from pathlib import Path

# Create a folder and a file.
folder = Path("pathlib_practice")
folder.mkdir(exist_ok=True)

file_path = folder / "notes.txt"
file_path.write_text("Learning pathlib", encoding="utf-8")

print("File exists:", file_path.exists())
print("Is a file:", file_path.is_file())
print("File name:", file_path.name)
print("File suffix:", file_path.suffix)
print("Parent folder:", file_path.parent)
print("File content:", file_path.read_text(encoding="utf-8"))

print("Python files in current folder:", list(Path(".").glob("*.py")))
```

## Run the lab

From this lab's folder:

```bash
python3 lab.py
```

On Windows, you can use:

```powershell
py lab.py
```

## Expected result
The script prints example values demonstrating the module. Some values are intentionally different on each run or machine (for example, random numbers, current date/time, paths, and platform information).

## Try it yourself
Compare `pathlib` path operations with the `os.path` approach. This lab creates a `pathlib_practice` folder and `notes.txt`.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
