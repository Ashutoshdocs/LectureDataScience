# `__init__` and `__all__` — Python from scratch

Three short, runnable lessons. Run them in order from this folder:

```
python lesson1_class_init.py
python lesson2_package_init.py
python lesson3_all.py
```

| Lesson | Topic | One-line idea |
|---|---|---|
| 1 | `__init__` method | Runs automatically when you create an object; sets up its data via `self`. |
| 2 | `__init__.py` file | Marks a folder as a package and runs once on first import; can expose names (`shapes.Circle`). |
| 3 | `__all__` list | Decides what `from X import *` gives you. Not a lock — explicit imports still work. |

## Folder layout
```
python_init_all_demo/
├── lesson1_class_init.py
├── lesson2_package_init.py
├── lesson3_all.py
└── shapes/
    ├── __init__.py   # package init + __all__ = ["Circle", "Square"]
    ├── circle.py     # module with its own __all__
    ├── square.py
    └── _helpers.py   # private helper (underscore = internal)
```

## Practice exercises
1. Add a `Rectangle(width, height)` class in `shapes/rectangle.py` with an `area()` method.
2. Expose it in `shapes/__init__.py` so `shapes.Rectangle(2, 3)` works.
3. Add it to `__all__` and confirm `from shapes import *` now includes it.
4. Add `"VERSION"` to `__all__` and rerun lesson 3 — what changes?
5. Remove the `print` from `shapes/__init__.py`. Does the package still work? (Yes — the file can even be empty.)
