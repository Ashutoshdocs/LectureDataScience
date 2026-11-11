# Folder 4 – Import specific functions using `from`

Instead of importing the complete module, import only the function you need:

```python
from common import calculate_area
```

Then call it directly:

```python
calculate_area(10, 5)
```

You do not need to write `common.calculate_area(...)`.

The shared module also includes `describe_rectangle()` to demonstrate how a module can contain several reusable functions.

Run:

```bash
python3 program1.py
python3 program2.py
```
