# Folder 1 – Import two Python files

## Files
- `operations.py` – contains add() and subtract()
- `messages.py` – contains functions for displaying output
- `main.py` – imports and uses both modules

All three files are in the same folder, so Python can find the modules directly.

## Run

Open a terminal in this folder:

```bash
python3 main.py
```

## Key idea

```python
import operations
import messages

operations.add(10, 5)
messages.show_title()
```

The imported filename (without `.py`) becomes the module name.
