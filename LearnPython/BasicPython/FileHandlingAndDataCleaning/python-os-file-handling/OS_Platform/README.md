# Python `os` and `platform` Modules — From Scratch to Practical Projects

A beginner-to-advanced teaching guide to understanding the operating system from Python, managing files and folders safely, reading environment information, and identifying the Python runtime and machine platform.

> **Important distinction:** `os` is mainly for interacting with operating-system services such as paths, directories, environment variables, and process-related information. `platform` is mainly for describing the system and Python runtime: OS name, release, architecture, processor information, and Python implementation/version.

---

## Repository layout

All project files are kept inside their own folders. Data, generated output, and logs are not scattered across the repository.

```text
Python_OS_Platform_Toolkit/
│
├── README.md
├── requirements.txt
│
├── project_01_system_inspector/
│   ├── README.md
│   ├── main.py
│   ├── system_info.py
│   ├── environment_info.py
│   ├── config/
│   │   └── settings.json
│   └── output/
│       └── .gitkeep
│
└── project_02_file_environment_manager/
    ├── README.md
    ├── main.py
    ├── file_manager.py
    ├── query_examples.py
    ├── data/
    │   ├── input/
    │   │   ├── notes.txt
    │   │   └── report.csv
    │   └── archive/
    │       └── .gitkeep
    ├── output/
    │   └── .gitkeep
    └── logs/
        └── .gitkeep
```

Run commands from the repository root unless a project README says otherwise. The examples build paths relative to the script location, so they do not depend on the terminal's current folder.

## Learning outcomes

By the end, learners should be able to:

1. Explain why Python needs operating-system interfaces.
2. Import and use `os` and `platform`.
3. Distinguish an operating system from a Python runtime/platform description.
4. Read the current working directory and the script's own directory.
5. Build cross-platform paths with `os.path.join`.
6. List, create, rename, move, and remove files and directories.
7. Read environment variables and set environment variables for the current process.
8. Inspect OS name, release, architecture, processor, Python version, and implementation.
9. Use `os.walk()` to search folder trees.
10. Use safe file operations, exception handling, and `pathlib` where appropriate.
11. Build two practical projects with organized input, output, config, and log folders.

---

# Part 1 — Foundations

## Chapter 1 — What is an operating system?

An operating system (OS) is the system software that manages the computer's hardware and provides services to applications.

Examples:
- Windows
- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS

The OS manages resources such as:
- Files and directories
- Processes and running programs
- Memory and devices
- User accounts and permissions
- Network interfaces
- Environment variables and system configuration

A Python program does not usually control hardware directly. It asks the operating system to perform tasks through interfaces exposed by Python and the OS.

### Analogy

Think of Python as a person working in an office:
- Python code is the employee's request.
- The operating system is the office administration.
- The file system is the filing room.
- Environment variables are configuration instructions.
- Processes are running tasks.

Python asks the OS to create a folder, inspect a file, or read an environment setting. The OS performs the operation and returns a result or an error.

## Chapter 2 — Why do we need the `os` module?

Without an OS interface, a Python application would have difficulty doing common system tasks in a portable way.

The `os` module provides functions that allow Python to interact with operating-system features.

Common uses:

| Requirement | Example |
|---|---|
| Find current folder | `os.getcwd()` |
| Change current folder | `os.chdir()` |
| Create a directory | `os.mkdir()` / `os.makedirs()` |
| List directory contents | `os.listdir()` |
| Join path segments safely | `os.path.join()` |
| Check whether a path exists | `os.path.exists()` |
| Read environment variable | `os.getenv()` |
| Walk a directory tree | `os.walk()` |
| Rename or move a path | `os.rename()` / `os.replace()` |
| Remove a file | `os.remove()` |

`os` is part of Python's standard library. You do not install it with `pip`.

## Chapter 3 — Why do we need the `platform` module?

The `platform` module provides information about the system on which Python is running.

It is useful when:
- Your code behaves differently on Windows and Linux.
- You are writing installation scripts.
- You need to print diagnostic information.
- You need to check Python version or implementation.
- You are troubleshooting a deployment on a VM, container, or developer laptop.

Examples:

```python
import platform

print(platform.system())       # Windows, Linux, Darwin, etc.
print(platform.release())      # OS release
print(platform.version())      # OS version details
print(platform.machine())      # Machine architecture, e.g. x86_64
print(platform.processor())    # Processor description (may be blank)
print(platform.python_version())
print(platform.python_implementation())  # Usually CPython
```

## Chapter 4 — `os` vs `platform`

| `os` module | `platform` module |
|---|---|
| Interacts with OS services | Describes the running platform |
| Works with directories and files | Reports OS and runtime details |
| Reads environment variables | Reports Python implementation/version |
| Provides process and path utilities | Reports architecture and machine information |
| Example: `os.makedirs()` | Example: `platform.system()` |

They complement one another. `platform` tells you what kind of environment you are running on; `os` helps you work with that environment.

## Chapter 5 — Setup and first program

No third-party package is required.

Check Python:

```bash
python --version
```

On some Linux installations:

```bash
python3 --version
```

Create a file named `first_os_platform.py`:

```python
import os
import platform

print("Operating system:", platform.system())
print("Current working directory:", os.getcwd())
print("Python version:", platform.python_version())
```

Run:

```bash
python first_os_platform.py
```

### What does `import` do?

`import os` loads the standard-library module named `os`, making its functions available through the `os.` prefix.

`import platform` does the same for the `platform` module.

---

# Part 2 — The `os` module in detail

## Chapter 6 — Current working directory vs script directory

These two locations are not necessarily the same.

- **Current working directory (CWD):** the folder from which the Python process was launched.
- **Script directory:** the folder containing the `.py` file.

```python
import os

print("Current working directory:", os.getcwd())
print("Script directory:", os.path.dirname(os.path.abspath(__file__)))
```

Why it matters: a relative path such as `"data/input.txt"` is normally resolved from the current working directory, not automatically from the script directory.

For reliable project paths, anchor paths to the script:

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
```

## Chapter 7 — Understanding paths

A path identifies a file or folder.

Windows example:

```text
C:\Users\Student\Documents\notes.txt
```

Linux/macOS example:

```text
/home/student/Documents/notes.txt
```

Do not manually concatenate path strings:

```python
# Fragile: separators differ across operating systems.
full_path = folder + "/" + filename
```

Use:

```python
import os

full_path = os.path.join(folder, filename)
```

Useful functions:

```python
os.path.basename("/home/student/report.csv")  # report.csv
os.path.dirname("/home/student/report.csv")   # /home/student
os.path.splitext("report.csv")                 # ("report", ".csv")
os.path.abspath("report.csv")                  # absolute path
os.path.normpath("folder/../report.csv")       # normalized path
```

## Chapter 8 — Check whether a path exists

```python
import os

path = "data/input/report.csv"

print(os.path.exists(path))
print(os.path.isfile(path))
print(os.path.isdir(path))
```

Difference:
- `exists()` checks whether a path exists.
- `isfile()` checks whether it is a file.
- `isdir()` checks whether it is a directory.

Always validate a path before reading or deleting it.

## Chapter 9 — Create directories

Create one directory:

```python
import os

os.mkdir("output")
```

Create nested directories:

```python
os.makedirs("data/archive/2026", exist_ok=True)
```

`exist_ok=True` prevents an error if the directory already exists.

A reusable pattern:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
for folder in ["data/input", "data/archive", "output", "logs"]:
    (BASE_DIR / folder).mkdir(parents=True, exist_ok=True)
```

`pathlib` is a modern path-oriented alternative. This course focuses on `os`, but learners should recognize both.

## Chapter 10 — List files and folders

```python
import os

for name in os.listdir("."):
    print(name)
```

`os.listdir()` returns names, not full paths.

To build a full path:

```python
for name in os.listdir("."):
    full_path = os.path.join(".", name)
    print(full_path)
```

Use `os.scandir()` when you want efficient directory entries with file-type information:

```python
with os.scandir(".") as entries:
    for entry in entries:
        print(entry.name, "directory?", entry.is_dir())
```

## Chapter 11 — Create and write a file

```python
import os

os.makedirs("output", exist_ok=True)
file_path = os.path.join("output", "message.txt")

with open(file_path, "w", encoding="utf-8") as file:
    file.write("Hello from Python and the operating system!\n")
```

Modes:
- `"r"` read
- `"w"` write (replaces existing content)
- `"a"` append
- `"x"` create only if it does not exist
- `"b"` binary mode modifier, e.g. `"rb"`
- `"+"` read and write modifier

Use `with` so the file is closed reliably.

## Chapter 12 — Read a file

```python
with open("output/message.txt", "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

Read line by line for large files:

```python
with open("output/message.txt", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        print(line_number, line.rstrip())
```

## Chapter 13 — Rename, move, and remove

```python
import os

os.rename("output/old.txt", "output/new.txt")
```

To move a file across directories on the same or different filesystems, `shutil.move()` is often more suitable:

```python
import shutil
shutil.move("output/new.txt", "data/archive/new.txt")
```

Remove a file:

```python
os.remove("data/archive/new.txt")
```

Remove an empty directory:

```python
os.rmdir("empty_folder")
```

For recursive directory removal, `shutil.rmtree()` exists, but it permanently removes a directory tree. Never run it on a path you have not validated. In teaching exercises, use a dedicated temporary folder.

## Chapter 14 — Environment variables

Environment variables are key-value settings available to a process.

Examples:
- `PATH`
- `HOME` on many Unix-like systems
- `USER` on many Unix-like systems
- `TEMP` on Windows
- Application-specific values such as `APP_ENV`

Read a variable:

```python
import os

home = os.getenv("HOME")
print(home)
```

Cross-platform example:

```python
home = os.getenv("USERPROFILE") or os.getenv("HOME")
print("Home folder:", home)
```

Set a variable for the current Python process and its child processes:

```python
os.environ["APP_ENV"] = "development"
print(os.getenv("APP_ENV"))
```

Important:
- Setting `os.environ` changes the current process environment; it does not permanently change the user's operating-system settings.
- Do not hard-code passwords, API keys, or tokens in source code.
- Environment variables are configuration, not a secure secret vault.

## Chapter 15 — Read all environment variables

```python
import os

for key, value in os.environ.items():
    print(key, "=", value)
```

Be careful: environment variables can contain secrets. Do not dump them into logs, screenshots, or public reports.

Safer diagnostic:

```python
for key in ["PATH", "HOME", "USERPROFILE", "TEMP", "APP_ENV"]:
    print(key, "=", os.getenv(key, "<not set>"))
```

## Chapter 16 — Walk through nested directories

`os.walk()` traverses a directory tree.

```python
import os

for root, directories, files in os.walk("data"):
    print("Folder:", root)

    for directory in directories:
        print("  Directory:", directory)

    for filename in files:
        print("  File:", filename)
```

The three values:
- `root`: current directory path.
- `directories`: child directory names.
- `files`: file names in the current directory.

## Chapter 17 — Search for files by extension

```python
import os

for root, directories, files in os.walk("data"):
    for filename in files:
        if filename.lower().endswith(".csv"):
            print(os.path.join(root, filename))
```

This is useful for log collection, data discovery, and cleanup utilities.

## Chapter 18 — File metadata

```python
import os
from datetime import datetime

path = "data/input/notes.txt"

if os.path.isfile(path):
    details = os.stat(path)

    print("Size in bytes:", details.st_size)
    print("Last modified:", datetime.fromtimestamp(details.st_mtime))
    print("Last accessed:", datetime.fromtimestamp(details.st_atime))
```

Modification timestamps and permissions can vary by filesystem and operating system.

## Chapter 19 — OS name and process ID

```python
import os

print("OS family name:", os.name)
print("Process ID:", os.getpid())
print("Parent process ID:", os.getppid())
```

`os.name` is commonly `"nt"` on Windows and `"posix"` on Linux/macOS. It is not as descriptive as `platform.system()`.

## Chapter 20 — Execute a command safely

Use `subprocess` for running external commands rather than building shell commands from untrusted strings.

```python
import subprocess
import platform

if platform.system() == "Windows":
    command = ["cmd", "/c", "echo", "Hello"]
else:
    command = ["echo", "Hello"]

result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    check=True
)

print(result.stdout)
```

Avoid `shell=True` unless you understand the security implications. Never insert untrusted user input into a shell command.

## Chapter 21 — Error handling for OS operations

Common errors:
- `FileNotFoundError`
- `FileExistsError`
- `PermissionError`
- `NotADirectoryError`
- `IsADirectoryError`
- `OSError`

```python
import os

try:
    os.remove("output/not_here.txt")
except FileNotFoundError:
    print("The file does not exist.")
except PermissionError:
    print("You do not have permission.")
except OSError as error:
    print("Operating-system error:", error)
```

Catch specific exceptions where possible. A broad `except Exception` can hide programming mistakes.

---

# Part 3 — The `platform` module in detail

## Chapter 22 — Identify the operating system

```python
import platform

system_name = platform.system()
print(system_name)
```

Typical values:
- Windows
- Linux
- Darwin (macOS)

Use this when your application needs an OS-specific branch.

## Chapter 23 — OS release and version

```python
import platform

print("System:", platform.system())
print("Release:", platform.release())
print("Version:", platform.version())
```

`release()` is a concise release identifier. `version()` may contain more detailed OS build information. Exact output depends on the operating system.

## Chapter 24 — Architecture and processor

```python
import platform

print("Machine:", platform.machine())
print("Processor:", platform.processor())
print("Architecture:", platform.architecture())
```

Examples of machine strings include `x86_64`, `AMD64`, and `aarch64`. Do not assume every system returns the same spelling.

## Chapter 25 — Python runtime information

```python
import platform
import sys

print("Python version:", platform.python_version())
print("Version tuple:", platform.python_version_tuple())
print("Implementation:", platform.python_implementation())
print("Executable:", sys.executable)
print("Prefix:", sys.prefix)
```

This helps diagnose virtual environments and Python installations.

## Chapter 26 — Full platform string

```python
import platform

print(platform.platform())
```

This returns a human-readable platform identifier. It is useful for diagnostics, but do not parse it as a stable machine-readable API because its format can vary.

## Chapter 27 — Conditional logic by operating system

```python
import platform

system_name = platform.system()

if system_name == "Windows":
    print("Use Windows-specific instructions.")
elif system_name == "Linux":
    print("Use Linux-specific instructions.")
elif system_name == "Darwin":
    print("Use macOS-specific instructions.")
else:
    print("Unknown or unsupported operating system.")
```

Prefer capability checks over OS-name checks when possible. For example, check whether a path exists rather than assuming a particular folder layout.

## Chapter 28 — Build a diagnostic report

```python
import platform
import os
import sys

report = {
    "os_name": platform.system(),
    "os_release": platform.release(),
    "architecture": platform.machine(),
    "processor": platform.processor(),
    "python_version": platform.python_version(),
    "python_implementation": platform.python_implementation(),
    "python_executable": sys.executable,
    "working_directory": os.getcwd(),
}

for key, value in report.items():
    print(f"{key}: {value}")
```

For a JSON report, use the `json` module and write it to a project output folder.

## Chapter 29 — Containers and virtual machines

A Python process may run:
- On a physical laptop.
- Inside an Azure VM or another cloud VM.
- Inside a Docker container.
- Inside a Kubernetes Pod.
- Inside a virtual environment.

`platform` describes the environment visible to the process. In a container, it may describe the container's Linux environment and kernel details, not the physical host in the way a beginner might expect.

A Python virtual environment changes Python package isolation and interpreter paths; it does not create a new operating system.

---

# Part 4 — Good practices

## Chapter 30 — Keep paths organized

Recommended structure:

```text
my_project/
├── main.py
├── config/
│   └── settings.json
├── data/
│   ├── input/
│   └── archive/
├── output/
└── logs/
```

Rules:
1. Keep input files in `data/input/`.
2. Put generated reports in `output/`.
3. Keep configuration in `config/`.
4. Keep logs in `logs/`.
5. Build paths from `__file__` or a known project root.
6. Do not depend on a developer's personal absolute path such as `C:\Users\Name\Desktop`.

## Chapter 31 — Use `os.path` and `pathlib`

`os.path` is useful and widely used:

```python
import os
path = os.path.join("data", "input", "file.txt")
```

`pathlib` provides an object-oriented approach:

```python
from pathlib import Path

path = Path("data") / "input" / "file.txt"
print(path.exists())
```

Both are valid. Do not mix them unnecessarily in one small program.

## Chapter 32 — Security and safety checklist

- Validate paths before deleting or overwriting files.
- Do not run recursive deletion on user-provided paths without strict validation.
- Do not log all environment variables.
- Do not store secrets in source code or committed configuration files.
- Avoid `shell=True` with untrusted input.
- Handle missing files and permission errors.
- Use UTF-8 explicitly for text files.
- Keep project data inside known input/output folders.

---

# Part 5 — Practical projects

## Project 1 — System Inspector

Location: `project_01_system_inspector/`

Build a diagnostic tool that reports:
- OS name, release, version, architecture, and processor.
- Python version and implementation.
- Python executable and current working directory.
- Selected safe environment variables.
- A JSON report saved to the project's `output/` directory.

Run:

```bash
python project_01_system_inspector/main.py
```

Read the project's own README for the walkthrough and exercises.

## Project 2 — File and Environment Manager

Location: `project_02_file_environment_manager/`

Build a small file-management utility that:
- Lists files under `data/input/`.
- Searches for files by extension.
- Reads text and CSV examples.
- Copies files to `data/archive/`.
- Writes a report into `output/`.
- Logs actions to `logs/`.
- Reads a non-secret environment variable such as `APP_ENV`.

Run:

```bash
python project_02_file_environment_manager/main.py
```

Read the project's own README for the walkthrough and exercises.

---

# Part 6 — Practice questions

1. What is an operating system?
2. Why does Python provide the `os` module?
3. What is the difference between `os.name` and `platform.system()`?
4. What is the difference between current working directory and script directory?
5. Why is `os.path.join()` better than manually adding `/`?
6. What does `os.makedirs(..., exist_ok=True)` do?
7. What is the difference between `os.path.exists()`, `isfile()`, and `isdir()`?
8. What does `os.walk()` return?
9. What is an environment variable?
10. Does changing `os.environ` permanently change the operating system?
11. Why should you avoid printing every environment variable?
12. What does `platform.machine()` report?
13. What does `platform.python_implementation()` report?
14. Does a Python virtual environment create a new OS?
15. Why is `platform.platform()` not ideal for parsing?
16. Which exception may occur when deleting a missing file?
17. Why is `shell=True` potentially dangerous?
18. Where should generated reports be stored in a well-organized project?
19. Why should paths be built relative to the script or project root?
20. When would you choose `pathlib` over `os.path`?

## Final teaching sequence

1. Explain OS and why applications need it.
2. Demonstrate `os.getcwd()` and `__file__`.
3. Build and inspect paths.
4. Create/list/read/write files and directories.
5. Demonstrate environment variables without exposing secrets.
6. Use `os.walk()` to search nested folders.
7. Introduce `platform` and compare Windows/Linux/macOS outputs.
8. Build Project 1 as a class demonstration.
9. Build Project 2 as a student lab.
10. Ask students to run both projects on Windows and Linux and compare results.

## Key takeaway

Use **`os` to interact with the operating system** and **`platform` to inspect the system and Python runtime**. Build paths safely, organize files into clear folders, handle errors, and never assume every machine behaves exactly like your own.
