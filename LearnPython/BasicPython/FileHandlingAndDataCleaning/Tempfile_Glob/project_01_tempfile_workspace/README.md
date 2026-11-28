# Project 1 — Temporary Processing Workspace

## Goal

Understand how to create a temporary workspace, process data inside it, save a permanent result, and allow Python to clean up the temporary folder.

## Folder structure

```text
project_01_tempfile_workspace/
├── README.md
├── main.py
├── temp_operations.py
├── data/
│   └── input/
│       └── source.txt
├── output/
└── logs/
```

- `data/input/`: permanent input data.
- `output/`: final result that must remain after execution.
- `logs/`: application log.
- Temporary working files: created in the OS temporary location and automatically removed.

## Run

From repository root:

```bash
python project_01_tempfile_workspace/main.py
```

Or:

```bash
cd project_01_tempfile_workspace
python main.py
```

The project directory is resolved relative to the script, not the terminal's current directory.

## What the program demonstrates

1. Read a permanent input file.
2. Create a temporary directory with `TemporaryDirectory()`.
3. Create intermediate files inside the temporary directory.
4. Read and process the intermediate content.
5. Save the final result in the permanent `output/` folder.
6. Exit the `with` block and allow automatic cleanup.

## Student exercises

1. Change the temporary directory prefix.
2. Create two temporary files in the same temporary directory.
3. Write a word count into the final report.
4. Add a timestamp to the output filename.
5. Demonstrate cleanup when an exception occurs inside the `with` block.
6. Compare `TemporaryDirectory()` with `mkdtemp()` and explain who is responsible for cleanup.
7. Create a named temporary file with `delete=False`, read it after closing, and remove it in a `finally` block.
8. Store a generated CSV file permanently under `output/`.
