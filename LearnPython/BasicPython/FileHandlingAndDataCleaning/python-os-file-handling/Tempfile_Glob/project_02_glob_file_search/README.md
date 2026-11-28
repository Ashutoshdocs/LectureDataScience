# Project 2 — Glob File Search and Inventory

## Goal

Build a file discovery utility that searches an organized data folder using wildcard patterns and creates a CSV inventory.

## Folder structure

```text
project_02_glob_file_search/
├── README.md
├── main.py
├── search_tools.py
├── data/
│   ├── incoming/
│   └── nested/
│       ├── archive/
│       └── logs/
└── output/
```

## Run

From repository root:

```bash
python project_02_glob_file_search/main.py
```

Or:

```bash
cd project_02_glob_file_search
python main.py
```

## Patterns used

```python
glob.glob("*.csv")                         # CSV files in current folder
glob.glob("sales_*.csv")                   # Files beginning sales_
glob.glob("report_202?.txt")               # One character after 202
glob.glob("data/**/*.csv", recursive=True) # Recursive CSV search
glob.iglob("data/**/*.log", recursive=True)# Lazy recursive iteration
```

The script anchors its search to the project's `data/` directory, so it works even if the terminal starts elsewhere.

## Output

The program writes `output/file_inventory.csv` with:
- Relative path
- Filename
- Extension
- Size in bytes

## Student exercises

1. Search only for `.txt` files.
2. Search for files whose names begin with `sales_`.
3. Search recursively for `.log` files.
4. Add a pattern for `report_202?.txt`.
5. Sort by filename instead of full path.
6. Add a column for the parent folder.
7. Ignore files smaller than 10 bytes.
8. Compare `glob.glob()` with `glob.iglob()`.
9. Add a second search implementation using `Path.rglob()`.
10. Create a filename containing brackets and demonstrate `glob.escape()`.

## Important

Glob results are not guaranteed to be sorted. The project sorts them before generating the report. Matching case behavior can differ across platforms.
