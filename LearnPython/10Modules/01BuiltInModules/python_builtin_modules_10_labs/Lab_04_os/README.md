# LAB 4 — Python `os` Module

## Purpose
Interact with the operating system.

## What you will learn
`os` provides operating-system interactions such as reading the current directory, listing files, creating directories, checking paths, and joining path components.

## Code

```python
import os

print("Operating system name:", os.name)
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir("."))

# Create a practice directory if it does not exist.
os.makedirs("os_practice", exist_ok=True)
print("Directory exists:", os.path.exists("os_practice"))

# Build a path safely for the current operating system.
file_path = os.path.join("os_practice", "hello.txt")
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Created using Python os module")

print("File path:", file_path)
print("File exists:", os.path.isfile(file_path))
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
Run the script from a practice location. It creates an `os_practice` directory and a text file inside it.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
