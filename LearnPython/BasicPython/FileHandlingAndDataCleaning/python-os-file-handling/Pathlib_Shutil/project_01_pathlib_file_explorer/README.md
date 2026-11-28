# Project 1 — Pathlib File Explorer

## Goal

Build a simple file explorer/report generator using `pathlib`. It does not delete or move source data.

## Folder structure

```text
project_01_pathlib_file_explorer/
├── README.md
├── main.py
├── path_queries.py
├── data/
│   ├── input/
│   │   ├── notes.txt
│   │   └── employees.csv
│   └── nested/
│       └── sample.log
└── output/
```

## Run from repository root

```bash
python project_01_pathlib_file_explorer/main.py
```

Or:

```bash
cd project_01_pathlib_file_explorer
python main.py
```

The code uses `Path(__file__).resolve().parent`, so it finds the project files regardless of the terminal's starting directory.

## Queries demonstrated

```python
Path.cwd()                       # Current working directory
Path(__file__).resolve()         # Absolute script path
path.name                        # File/folder name
path.stem                        # File name without final suffix
path.suffix                      # File extension
path.parent                      # Parent folder
path.exists()                    # Does it exist?
path.is_file()                   # Is it a file?
path.is_dir()                    # Is it a directory?
folder.iterdir()                 # Direct children
folder.glob("*.csv")             # Matching direct children
folder.rglob("*.csv")            # Matching files recursively
path.stat().st_size              # File size in bytes
path.read_text(encoding="utf-8") # Read text
```

## Output

The project writes `output/file_inventory.csv` with the discovered file paths, names, suffixes, and sizes.

## Student exercises

1. Search for `.txt` files instead of `.csv`.
2. Search for all files recursively.
3. Add a column containing the parent directory.
4. Ignore files whose names begin with a dot.
5. Add a filter for files larger than 100 bytes.
6. Read `employees.csv` and count its data rows.
7. Create a `processed/` folder and write a summary text file there.
8. Run the script while your terminal is in a different folder and explain why the paths still work.
