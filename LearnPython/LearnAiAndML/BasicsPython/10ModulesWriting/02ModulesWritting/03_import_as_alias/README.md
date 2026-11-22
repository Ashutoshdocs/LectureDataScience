# Folder 3 – Import a module using `as`

The folder has the same three-file structure as Folder 2. The difference is:

```python
import common as helper
```

`helper` is an alias for the `common` module. Access functions with the alias:

```python
helper.calculate_area(10, 5)
```

Run:

```bash
python3 program1.py
python3 program2.py
```
