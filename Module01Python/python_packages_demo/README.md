# Python Modules & Packages — Class Demo

A hands-on lesson in three steps:

| Step | Folder | What students learn |
|------|--------|---------------------|
| 1 | `step1_modules/` | What a module is, all the import styles, `__name__`, `__all__`, caching, `sys.path` |
| 2 | `step2_package/` | What a package is, `__init__.py`, sub-packages, relative vs absolute imports, `python -m` |
| 3 | `step3_installable/` | Making a package installable with `pyproject.toml`, `pip install -e .`, CLI entry points |

**Requirements:** Python 3.8+ (no third-party libraries needed).
**Duration:** ~60–75 minutes (theory 20 min, demos 40 min, exercises 15 min).

```
python_packages_demo/
├── README.md
├── step1_modules/
│   ├── mathutils.py          # a module with functions, a constant, a private helper
│   ├── stringutils.py        # a module that uses __all__
│   └── main.py               # shows 8 different import patterns
├── step2_package/
│   ├── main.py               # uses the package
│   └── shop/                 # ← package
│       ├── __init__.py       # package initialiser + re-exports
│       ├── __main__.py       # lets you run `python -m shop`
│       ├── cart.py           # module inside the package
│       └── pricing/          # ← sub-package
│           ├── __init__.py
│           ├── discounts.py
│           └── tax.py
└── step3_installable/
    ├── pyproject.toml        # packaging metadata
    ├── README.md
    ├── use_textkit.py
    └── src/
        └── textkit/          # ← installable package
            ├── __init__.py
            ├── core.py
            └── cli.py        # command-line entry point
```

---

## Part A — Theory

### 1. Why do we need modules and packages?

As programs grow, keeping everything in one file becomes unmanageable. Modules and packages let us:

- **Organise** code into logical, smaller pieces
- **Reuse** code across many programs without copy-pasting
- **Avoid name clashes** — each module has its own *namespace* (`math.sqrt` and `numpy.sqrt` can co-exist)
- **Share** code with others (via pip / PyPI)

> Analogy: a **module** is a *chapter*, a **package** is a *book* made of chapters, and a **library / distribution** is the *published book* others can buy (install).

### 2. What is a module?

A **module is any `.py` file**. The filename (without `.py`) is the module name.

```python
# mathutils.py   → module name is "mathutils"
PI = 3.14159
def add(a, b):
    return a + b
```

Three kinds of modules:

| Kind | Example | Where it comes from |
|------|---------|---------------------|
| Built-in / standard library | `math`, `os`, `random`, `datetime` | Ships with Python |
| Third-party | `requests`, `numpy`, `pandas` | Installed with `pip` |
| Your own | `mathutils.py` | Files you write |

### 3. Ways to import

| Syntax | What you get | Usage |
|--------|--------------|-------|
| `import mathutils` | The module object | `mathutils.add(1, 2)` |
| `import mathutils as mu` | Module with an alias | `mu.add(1, 2)` |
| `from mathutils import add` | Just that name | `add(1, 2)` |
| `from mathutils import add as plus` | Name with an alias | `plus(1, 2)` |
| `from mathutils import *` | All public names (or those in `__all__`) | **Avoid** in real code — it pollutes your namespace |

### 4. What happens when you `import`?

1. Python checks **`sys.modules`** (a cache). If the module is already loaded, it reuses it — **the module's code runs only once**.
2. Otherwise it searches the folders in **`sys.path`**, in order:
   - the folder of the script you ran (or the current directory)
   - folders in the `PYTHONPATH` environment variable
   - the standard library
   - `site-packages` (where `pip` installs things)
3. It executes the file top to bottom and creates a module object.
4. It binds the name in your file.

> ⚠️ **Common bug:** naming your own file `random.py` or `math.py` *shadows* the standard library module, because your folder is searched first.

### 5. `if __name__ == "__main__":`

Every module has a built-in variable `__name__`:

- When **run directly** (`python mathutils.py`) → `__name__ == "__main__"`
- When **imported** (`import mathutils`) → `__name__ == "mathutils"`

So code under this guard runs only when the file is executed as a script — perfect for quick tests or demos that shouldn't run on import.

### 6. Public vs private names, and `__all__`

- Names starting with `_` (e.g. `_helper`) are **private by convention** and are skipped by `import *`.
- `__all__ = ["a", "b"]` explicitly lists what `from module import *` exports.
- Neither is enforced: `from module import _helper` still works. Python trusts developers ("we're all consenting adults").

### 7. What is a package?

A **package is a folder of modules**, traditionally marked by an **`__init__.py`** file.

```
shop/                 ← package
├── __init__.py
├── cart.py           ← module  → shop.cart
└── pricing/          ← sub-package → shop.pricing
    ├── __init__.py
    └── tax.py        ← module  → shop.pricing.tax
```

Dots in import paths mirror folders: `import shop.pricing.tax` ↔ `shop/pricing/tax.py`.

**What does `__init__.py` do?**
- Marks the folder as a regular package
- Runs **once**, when the package is first imported
- Can define package-level things (`__version__`)
- Can **re-export** names so users write `from shop import Cart` instead of `from shop.cart import Cart` (a cleaner public API)
- Can be empty — that's fine too

> Since Python 3.3, a folder *without* `__init__.py` can still be imported as a **namespace package**. For a class, stick to regular packages with `__init__.py` — they're explicit and predictable.

### 8. Absolute vs relative imports

Inside a package:

```python
# absolute — full path from the top-level package
from shop.pricing.tax import add_tax

# relative — relative to the current module's location
from .pricing import add_tax       # .  = current package
from ..utils import helper         # .. = parent package
```

- Relative imports **only work inside a package** (not in a script you run directly with `python file.py`).
- PEP 8 recommends absolute imports for clarity; relative imports are fine within a package.

### 9. `__main__.py` and `python -m`

- `python -m shop` runs the file `shop/__main__.py`, treating `shop` as a package so imports work properly.
- `python -m pip`, `python -m venv`, `python -m http.server` all use this same mechanism.

### 10. Module vs package vs library — summary

| Term | Is a… | Example |
|------|-------|---------|
| Module | single `.py` file | `tax.py` |
| Package | folder of modules (with `__init__.py`) | `shop/` |
| Sub-package | package inside a package | `shop/pricing/` |
| Library / distribution | one or more packages bundled for installation with `pip` | `requests`, `textkit-demo` |

### 11. Making a package installable

To use your package from **any** folder (or share it), describe it in a **`pyproject.toml`** file and install it with `pip`:

- `[build-system]` — which tool builds it (here, setuptools)
- `[project]` — name, version, dependencies
- `[project.scripts]` — creates terminal commands
- The **src layout** (`src/textkit/`) prevents accidentally importing the local folder instead of the installed package.

`pip install -e .` = **editable install**: pip links to your source folder, so edits take effect immediately without reinstalling. Ideal while developing.

---

## Part B — Demo Steps

Open a terminal in the `python_packages_demo` folder. Use `python3` instead of `python` if that's what your system needs.

### Demo 1 — Modules (≈ 12 min)

```bash
cd step1_modules
python main.py
```

**Walk through the output section by section:**

1. `import mathutils` prints `[mathutils] loaded (__name__ = 'mathutils')` — the module's top-level code ran on import.
2. The second `import mathutils` prints **nothing** — point out caching via `sys.modules`.
3–5. Different import styles produce the same results.
6. `import *` brought in `shout` but **not** `whisper` — because of `__all__` in `stringutils.py`.
7. `__file__` shows where the module lives; `dir()` lists its contents (`_private_helper` is hidden by our filter).
8. `sys.path[0]` is the script's folder — that's why Python found `mathutils.py`.

**Now show `__name__`:**

```bash
python mathutils.py
```

Output shows `__name__ = '__main__'` and the self-test runs. Compare with step 1, where the self-test did *not* run.

**Live experiment (optional):** create a file named `random.py` in this folder, then run `python -c "import random; print(random.__file__)"` — it picks your file, not the standard library! Delete it afterwards.

**Interactive exploration:**

```bash
python
>>> import mathutils
>>> help(mathutils)          # shows the docstrings
>>> mathutils._private_helper()   # private by convention only
>>> exit()
```

### Demo 2 — Packages (≈ 15 min)

```bash
cd ../step2_package
python main.py
```

**Point out:**

1. Importing `shop` printed messages from **both** `shop/__init__.py` and `shop/pricing/__init__.py` — because `shop/__init__.py` imports `cart`, which imports `pricing`.
2. `from shop import Cart` works because `__init__.py` re-exports `Cart`. Open `shop/__init__.py` and show the line `from .cart import Cart`.
3. Absolute import into a deep module: `from shop.pricing.discounts import DISCOUNT_CODES`.
4. Importing a sub-package with an alias.
5. Packages have `__path__`; plain modules don't — the technical difference between them.

**Open `shop/cart.py`** to show the relative import `from .pricing import apply_discount, add_tax`.

**Run the package as a program:**

```bash
python -m shop
```

This runs `shop/__main__.py`.

**Show why relative imports fail in scripts:**

```bash
python shop/cart.py
```

You'll get `ImportError: attempted relative import with no known parent package`. Explain: running a file directly makes it `__main__`, with no parent package, so `.` means nothing. Use `python -m` or import it from outside instead.

**Show the package isn't visible elsewhere:**

```bash
cd ..
python -c "import shop"
```

→ `ModuleNotFoundError`. The `shop` folder isn't on `sys.path` from here. This motivates Demo 3.

### Demo 3 — Installable package (≈ 13 min)

```bash
cd step3_installable
```

**1. Open `pyproject.toml`** and explain each section (see Theory §11). Note that the pip name (`textkit-demo`) differs from the import name (`textkit`) — just like `pip install scikit-learn` → `import sklearn`.

**2. Create a virtual environment** (keeps the class's global Python clean):

```bash
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

**3. Install in editable mode:**

```bash
pip install -e .
```

**4. Prove it works from anywhere:**

```bash
cd ..
cd ..                       # go somewhere unrelated
python -c "import textkit; print(textkit.word_count('it works from anywhere'))"
pip show textkit-demo
```

**5. Run the example script and the CLI command:**

```bash
python path/to/step3_installable/use_textkit.py
textkit count "Python packages are fun"       # → 4
textkit palindrome "Never odd or even"        # → True
textkit title "hello class"                   # → Hello Class
textkit --help
```

`textkit` became a real terminal command because of `[project.scripts]` in `pyproject.toml`.

**6. Show editable install in action:** edit `src/textkit/core.py` (e.g. make `title_case` add `"!"` at the end), then run `textkit title "hello"` again — the change is live with no reinstall.

**7. (Optional) Build distributable files:**

```bash
pip install build
python -m build             # creates dist/*.whl and dist/*.tar.gz
```

These are the files you'd upload to PyPI (with `twine`) so anyone could `pip install` your package.

**8. Clean up:**

```bash
pip uninstall textkit-demo -y
deactivate
```

---

## Expected output (for reference)

<details>
<summary>Demo 1 — <code>python main.py</code></summary>

```
=== 1. import module ===
[mathutils] loaded  (__name__ = 'mathutils')
5
3.14159

=== 2. import module again (no second 'loaded' message - modules are cached) ===
'mathutils' in sys.modules -> True

=== 3. from module import name ===
12.56636

=== 4. import with an alias ===
HELLO!

=== 5. from module import name as alias ===
nohtyp

=== 6. from module import *  (respects __all__) ===
STAR IMPORT!
'whisper' imported by * ? False

=== 7. Inspecting a module ===
File: .../step1_modules/mathutils.py
Public names: ['PI', 'add', 'area_of_circle']

=== 8. Where does Python look for modules? (sys.path) ===
   .../step1_modules
   ...
```
</details>

<details>
<summary>Demo 2 — <code>python main.py</code></summary>

```
=== 1. Import the package (runs shop/__init__.py and shop/pricing/__init__.py) ===
[shop] package initialised
[shop.pricing] sub-package initialised
Version: 1.0.0

=== 2. Use a name re-exported by __init__.py ===
Cart(2 items, subtotal=1100.00)
Total (with 18% GST):       1298.0
Total with STUDENT10 code:  1168.2

=== 3. Absolute import of a module deep inside the package ===
Available codes: ['STUDENT10', 'FESTIVE20']

=== 4. Import a sub-package ===
GST rate: 0.18
1000 after FESTIVE20: 800.0

=== 5. Package vs module ===
shop.__path__   -> ['.../step2_package/shop']
shop.cart has __path__? False
```
</details>

---

## Common errors & fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'x'` | Module isn't in any `sys.path` folder | Run from the right folder, `pip install` it, or check spelling |
| `ImportError: attempted relative import with no known parent package` | Ran a package module directly with `python file.py` | Use `python -m package.module` or absolute imports |
| `ImportError: cannot import name 'X' from partially initialized module` | **Circular import** (A imports B, B imports A) | Move shared code into a third module, or import inside the function |
| Your `random.py` breaks `import random` | Shadowing a standard-library name | Rename your file (and delete `__pycache__`) |
| Changes to a module don't show in the REPL | Module is cached in `sys.modules` | Restart the REPL, or `importlib.reload(module)` |

> **About `__pycache__/`:** Python saves compiled bytecode (`.pyc`) here to speed up future imports. It's safe to delete and should be in `.gitignore`.

---

## Part C — Class Exercises

1. **Module:** Create `geometry.py` with `rectangle_area(w, h)` and `PI`. Import it three different ways in a new script.
2. **`__name__`:** Add an `if __name__ == "__main__":` block to `geometry.py` that tests your functions. Confirm it doesn't run on import.
3. **Package:** Add a `shop/pricing/shipping.py` module with `shipping_cost(amount)` (free above ₹500, else ₹50). Expose it from `shop/pricing/__init__.py` and use it in `Cart.total()`.
4. **Re-export:** Make `from shop import apply_discount` work by editing only `shop/__init__.py`.
5. **Installable:** Add a `vowel_count` function to `textkit` and a new CLI action `vowels`. Test it with `textkit vowels "education"` (→ 5).
6. **Challenge:** Deliberately create a circular import between two modules, observe the error, then fix it.

## Quick quiz

1. What's the difference between a module and a package?
2. How many times does a module's top-level code run if it's imported in 5 different files?
3. What is the value of `__name__` when a file is imported? When it is run directly?
4. What does `from . import x` mean, and where can it be used?
5. Why is `from module import *` discouraged?
6. What does `pip install -e .` do differently from `pip install .`?

<details>
<summary>Answers</summary>

1. A module is a single `.py` file; a package is a folder of modules (with `__init__.py`).
2. Once — later imports reuse the cached module in `sys.modules`.
3. The module's name (e.g. `"mathutils"`) when imported; `"__main__"` when run directly.
4. Import `x` from the current package; only inside a package (not a directly-run script).
5. It hides where names come from and can silently overwrite existing names.
6. Editable mode links to your source folder, so code changes apply without reinstalling; `pip install .` copies a snapshot.
</details>
