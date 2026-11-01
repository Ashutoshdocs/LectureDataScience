# 🔥 BlazeCalc (Python) — Using a Module from Another Folder

This demo teaches you how to **build a reusable Python module (package) in one folder** and **import it into an interactive desktop app in another folder**.

```
blazecalc-python-demo/
├── BlazeCalc/                     ← Folder 1: the calculator MODULE
│   ├── pyproject.toml             ← tells pip how to install it
│   ├── src/
│   │   └── BlazeCalc/             ← the actual importable package
│   │       ├── __init__.py        ← entry point: decides what gets exported
│   │       ├── operations.py      ← add, subtract, multiply, divide, percent, power, sqrt
│   │       └── calculator.py      ← Calculator class + safe evaluate("12 + 3 * 4")
│   └── tests/
│       └── test_blazecalc.py
│
└── frontend-app/                  ← Folder 2: the interactive APP that USES the module
    ├── requirements.txt           ← contains:  -e ../BlazeCalc
    └── app.py                     ← import BlazeCalc
```

---

## 🚀 Quick start

You need **Python 3.8+**. The app uses **Tkinter**, which ships with Python on Windows and macOS (python.org installers).
On Linux you may need: `sudo apt install python3-tk` (Ubuntu/Debian) or `sudo dnf install python3-tkinter` (Fedora).

```bash
cd blazecalc-python-demo

# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

# 2. Install BlazeCalc into this environment (from the folder next door)
cd frontend-app
pip install -r requirements.txt

# 3. Run the app 🎉
python app.py
```

A calculator window opens:

- Click the buttons **or type straight into the display** (`12 + 3 * 4`, `(2+3)**2`, `-5 + 2`)
- A **live preview** shows the answer while you type
- **Enter** = calculate · **Esc** = clear
- `√`, `x²`, `%`, `±` act on whatever is currently in the display
- **History** panel on the right — click any line to reuse its result
- Errors (like `10 ÷ 0`) appear in red instead of crashing the app

The window lives in `frontend-app/`, but **every calculation is done by BlazeCalc**.

---

## 📚 How it works — step by step

### Step 1 — Write the module (`BlazeCalc/src/BlazeCalc/operations.py`)

Plain functions:

```python
def add(a, b):
    _check_numbers(a, b)
    return a + b

def divide(a, b):
    _check_numbers(a, b)
    if b == 0:
        raise ZeroDivisionError("BlazeCalc: cannot divide by zero")
    return a / b
```

### Step 2 — A folder with `__init__.py` is a *package*

In Python, a **module** is one `.py` file. A **package** is a folder of modules with an `__init__.py` inside.
The folder name is the name you import, so this folder is imported as `BlazeCalc`.

`__init__.py` is the "front door". It runs on `import BlazeCalc` and decides what users can reach:

```python
from .operations import add, subtract, multiply, divide, percent, power, sqrt
from .calculator import Calculator, evaluate

__version__ = "1.0.0"
```

The dot in `.operations` means *"from this same package"* — a **relative import**.

### Step 3 — Make it installable (`BlazeCalc/pyproject.toml`)

```toml
[project]
name = "blazecalc"     # the name pip shows (pip names are lowercase by convention)
version = "1.0.0"

[tool.setuptools.packages.find]
where = ["src"]        # look inside src/ for packages → finds BlazeCalc/
```

| Name | Where it's used |
|---|---|
| `blazecalc` | what **pip** calls it: `pip list`, `pip uninstall blazecalc` |
| `BlazeCalc` | what **Python** imports: `import BlazeCalc` (the folder name) |

> 💡 Why the `src/` folder? It stops Python from accidentally importing the local folder instead of the installed package — so you always test what users actually get.

### Step 4 — Link it into the frontend (`frontend-app/requirements.txt`)

```
-e ../BlazeCalc
```

- `../BlazeCalc` → *"the package is in the folder next door, not on PyPI"*
- `-e` = **editable** install → pip doesn't copy the code, it points Python at your folder

So **any change you save in `BlazeCalc/` is used the next time you run `app.py`** — no reinstall.

Check it worked:

```bash
pip show blazecalc     # "Editable project location" points at your BlazeCalc folder
```

### Step 5 — Import and use it (`frontend-app/app.py`)

```python
import BlazeCalc

BlazeCalc.add(2, 3)                    # 5
BlazeCalc.evaluate("12 + 3 * 4")       # 24
calc = BlazeCalc.Calculator()
```

Or import only what you need:

```python
from BlazeCalc import evaluate, sqrt, Calculator
```

Inside the app, the `=` button simply calls:

```python
result = BlazeCalc.evaluate(text)   # 👈 BlazeCalc does the work
```

### Step 6 — How the interactive app is built (Tkinter basics)

| Concept | In `app.py` |
|---|---|
| Window | `class BlazeCalcApp(tk.Tk)` |
| Layout | `.grid()` for the button pad, `.pack()` for stacked widgets |
| Live-updating text | `tk.StringVar()` + `trace_add("write", ...)` → live preview |
| Button click | `tk.Button(..., command=lambda: self.press(label))` |
| Keyboard | `self.bind("<Return>", ...)`, `self.bind("<Escape>", ...)` |
| Hover effect | bind `<Enter>` / `<Leave>` to change the colour |
| Event loop | `mainloop()` keeps the window open and reacting |

---

## 🧰 BlazeCalc API reference

| Function | Example | Result |
|---|---|---|
| `add(a, b)` | `add(2, 3)` | `5` |
| `subtract(a, b)` | `subtract(9, 4)` | `5` |
| `multiply(a, b)` | `multiply(4, 5)` | `20` |
| `divide(a, b)` | `divide(10, 4)` | `2.5` (raises `ZeroDivisionError` on ÷ 0) |
| `percent(value, pct)` | `percent(200, 15)` | `30.0` |
| `power(base, exp)` | `power(2, 8)` | `256` |
| `sqrt(n)` | `sqrt(81)` | `9.0` |
| `evaluate(expr)` | `evaluate("(2 + 3) ** 2")` | `25` |
| `Calculator(start)` | `Calculator(10).apply("+", 5).apply("*", 2).value` | `30` |
| `calc.get_history()` | | `["10 + 5 = 15", "15 * 2 = 30"]` |
| `calc.record(expr, result)` / `calc.clear()` | | add to / reset history |

**About `evaluate()`:** it supports `+ - * / ** %`, parentheses, negative numbers, and `×` `÷`.
It does **not** use Python's `eval()` (which would run *any* code someone types). Instead it uses the `ast` module to read the expression as a tree and only allows numbers and maths operators, so input like `__import__('os')` is rejected with a `ValueError`.

---

## 🧪 Run the tests

```bash
cd BlazeCalc
python -m unittest discover -s tests -v
```

(Run this with the virtual environment active, after the `pip install` step.)

---

## 🏋️ Try it yourself (exercises)

1. **Add a function.** Add `cube(n)` to `operations.py`, export it in `__init__.py`, then add an `x³` button in `app.py`. Because of the editable install, just re-run `python app.py`.
2. **Write a test** for `cube()` in `tests/test_blazecalc.py`.
3. **Use BlazeCalc from the terminal** — no GUI:
   ```bash
   python -c "import BlazeCalc; print(BlazeCalc.evaluate('2 + 2 * 10'))"
   ```
4. **Build a second frontend.** Create `cli-app/main.py` with an `input()` loop that calls `BlazeCalc.evaluate()`. Two apps, one module — that's the point of modules!
5. **Add a memory feature** (`M+`, `MR`, `MC`) to the `Calculator` class and wire up buttons for it.

---

## ❓ Common problems

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'BlazeCalc'` | Activate the virtual environment, then `pip install -r requirements.txt` inside `frontend-app/` |
| `ModuleNotFoundError: No module named 'tkinter'` | Linux: `sudo apt install python3-tk`. macOS with Homebrew Python: `brew install python-tk` |
| Changes in BlazeCalc don't appear | Make sure you installed with `-e`. Check with `pip show blazecalc` |
| Moved the folders and it broke | The path `../BlazeCalc` is relative — fix it in `requirements.txt` and reinstall |
| `python` not found (Windows) | Try `py` instead of `python` |

---

## 🌍 Going further

- **Publish to PyPI** — `pip install build twine`, then `python -m build` and `twine upload dist/*` (needs a unique name). Then anyone can `pip install blazecalc`.
- **Install from Git** — `pip install "git+https://github.com/your-user/BlazeCalc.git"`.
- **Web frontend instead** — the same module works in Flask or Streamlit apps.

Your app's import line — `import BlazeCalc` — **stays exactly the same** in every case. That's the power of modules.
