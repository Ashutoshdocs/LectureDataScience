# Project 2 — File and Environment Manager

## Goal

Create a practical utility that manages files inside a controlled project folder. It lists files, searches by extension, reads text and CSV data, copies input files to an archive, and writes a report and log.

## Folder layout

```text
project_02_file_environment_manager/
├── README.md
├── main.py
├── file_manager.py
├── query_examples.py
├── data/
│   ├── input/
│   │   ├── notes.txt
│   │   └── report.csv
│   └── archive/
├── output/
└── logs/
```

All source data is in `data/input/`. Archived copies go to `data/archive/`. Reports go to `output/`. Logs go to `logs/`.

## Run

From repository root:

```bash
python project_02_file_environment_manager/main.py
```

Or:

```bash
cd project_02_file_environment_manager
python main.py
```

## Queries / commands demonstrated

The project demonstrates these Python operations:

```python
os.listdir(input_dir)                 # List files in a folder
os.path.join(input_dir, filename)     # Build a safe path
os.path.isfile(full_path)             # Confirm it is a file
os.path.splitext(filename)            # Get file extension
os.walk(input_dir)                    # Search nested folders
os.stat(full_path).st_size             # Get file size
os.makedirs(archive_dir, exist_ok=True)
shutil.copy2(source, destination)      # Copy a file with metadata
os.getenv("APP_ENV", "development")    # Read a configuration variable
```

See `query_examples.py` for small runnable examples.

## Try a different environment value

Linux/macOS:

```bash
APP_ENV=testing python main.py
```

PowerShell:

```powershell
$env:APP_ENV = "testing"
python main.py
```

The value is available to the current process. It is not a permanent OS-wide change.

## Student exercises

1. Add support for `.json` files.
2. Search for files larger than 1 KB.
3. Count how many `.txt`, `.csv`, and `.json` files exist.
4. Add a dry-run mode that prints copy actions without copying.
5. Add a command-line argument for the extension to search.
6. Prevent overwriting an archive file unless the user confirms.
7. Add a timestamp to the report filename.
8. Create a nested directory under `data/input/` and confirm `os.walk()` finds its files.

## Safety

The script only copies files from this project's `data/input/` folder. It does not delete source files. Avoid modifying the project to recursively delete arbitrary paths.
