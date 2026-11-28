# Project 1 — System Inspector

## Goal

Create a small diagnostic application that inspects the OS and Python runtime and saves a JSON report.

## Folder layout

```text
project_01_system_inspector/
├── README.md
├── main.py
├── system_info.py
├── environment_info.py
├── config/
│   └── settings.json
└── output/
```

- `main.py`: application entry point.
- `system_info.py`: functions that use `platform` and `os`.
- `environment_info.py`: reads only selected safe environment variables.
- `config/settings.json`: controls report settings.
- `output/`: generated JSON report is saved here.

## Run it

From the repository root:

```bash
python project_01_system_inspector/main.py
```

Or enter the project folder:

```bash
cd project_01_system_inspector
python main.py
```

The script resolves its folders relative to `__file__`, so both methods work.

## What to observe

1. Compare `platform.system()` with `os.name`.
2. Compare `os.getcwd()` with the script directory.
3. Check `platform.machine()` on different computers.
4. Open the generated JSON file in `output/`.
5. Run the project on Windows and Linux and compare the report.

## Student exercises

1. Add `platform.node()` to report the computer's network name.
2. Add `platform.python_version()` and `platform.python_implementation()`.
3. Add a `report_created_at` field using `datetime`.
4. Add a check that warns if Python is older than a version you choose.
5. Add a command-line option to choose the output filename.

## Important

The report deliberately reads only a small allowlist of environment variables. Do not dump all environment variables because they may contain credentials or tokens.
