# Folder 2 – Put common logic in one module

Files:
- `common.py` – reusable functions
- `program1.py` – uses the area function
- `program2.py` – uses the perimeter function

Run from this folder:

```bash
python3 program1.py
python3 program2.py
```

`import common` loads the `common.py` module. Use the module name and a dot to access its functions, such as `common.calculate_area(...)`.
