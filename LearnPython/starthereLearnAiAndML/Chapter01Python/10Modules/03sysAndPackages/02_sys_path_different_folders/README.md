# Folder 2 – Import modules from a different folder using `sys.path`

## Folder structure

```text
02_sys_path_different_folders/
├── app/
│   └── main.py
└── modules/
    ├── operations.py
    └── messages.py
```

The main program is inside `app`, while the reusable modules are inside `modules`.

Python normally searches locations listed in `sys.path` when importing modules. In `main.py`, we add the `modules` folder:

```python
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "..", "modules")
sys.path.append(os.path.abspath(MODULES_DIR))
```

After adding the folder, these imports work:

```python
import operations
import messages
```

## Run

Run from this folder:

```bash
python3 app/main.py
```

## Important

- `sys.path` is a Python list of locations searched for modules.
- `sys.path.append()` adds another search location for the current Python process.
- This is a beginner demonstration. For larger applications, packages and proper project installation are usually easier to maintain.
