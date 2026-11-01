# Python Imports Demo 🐍

A tiny, **standard-library-only** app that shows every common way to import
built-in modules and packages in Python, with live results in a web page.

```
imports-demo/
├── app.py            # web server + all import examples
├── index.html        # front-end that displays the results
├── README.md
└── toolkit/          # our own example package
    ├── __init__.py   # makes the folder a package
    ├── mathx.py      # submodule
    └── textx.py      # submodule
```

## Run it

```bash
python app.py          # open http://localhost:8000
python app.py --cli    # or print the examples in the terminal
```

Requires Python 3.8+. Nothing to install.

## Key terms

| Term | Meaning | Example |
|------|---------|---------|
| **Module** | A single `.py` file | `math`, `json`, `toolkit/mathx.py` |
| **Package** | A folder of modules with `__init__.py` | `os`, `http`, `urllib`, `toolkit/` |
| **Built-in / standard library** | Ships with Python, no `pip` needed | `datetime`, `random`, `collections` |

## Import styles covered

```python
import math                                # 1. whole module      -> math.sqrt(9)
import datetime as dt                      # 2. module alias      -> dt.date.today()
from statistics import mean, median        # 3. specific names    -> mean([1, 2])
from urllib.parse import urlparse as p     # 4. name alias        -> p(url)
import os.path                             # 5. package submodule -> os.path.basename(f)
import toolkit                             # 6. own package (runs __init__.py)
from toolkit import mathx                  # 7. submodule from package
from toolkit.textx import shout            # 8. function from submodule
from .textx import shout                   # 9. relative import (inside a package)
importlib.import_module("hashlib")         # 10. dynamic import at runtime
```

## `import` vs `from` — when to use which

- **`import module`** – keeps names clear (`math.pi`), avoids name clashes. Good default.
- **`from module import name`** – shorter code when you use a name often.
- **`as alias`** – shorten long names or avoid conflicts.
- **Avoid `from module import *`** – it hides where names come from.
  (`__all__` in `toolkit/__init__.py` controls what `*` would export.)

## Good to know

- `if __name__ == "__main__":` runs code only when the file is executed directly,
  not when it is imported.
- A module is loaded **once**; later imports reuse it from `sys.modules`.
- Python finds modules using `sys.path` (the script's folder comes first),
  which is why `import toolkit` works from `app.py`.

## Try next

1. Add `toolkit/dates.py` and import it with `from toolkit import dates`.
2. Print `sys.path` and `sys.modules.keys()` in `app.py`.
3. Rename a module to `random.py` and see how it *shadows* the built-in one.
