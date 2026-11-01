# Learn `__init__.py` from scratch

A hands-on lesson in four small steps. Each step is its own folder with a
`cafe` package and a `main.py` to run. Read a section, open the files, run the
code and compare what you see with what is described here.

```
init_package_demo/
├── README.md                 <- you are here (the lesson)
├── step1_empty_init/         <- an empty __init__.py makes a package
├── step2_runs_on_import/     <- __init__.py is code that runs on import
├── step3_shortcuts/          <- __init__.py as the package's "front desk"
└── step4_real_package/       <- settings, setup, subpackages, private modules
```

**How to run any step**

```bash
cd step1_empty_init
python main.py
```

Always run `main.py` from **inside** its step folder, so Python can find the `cafe` folder next to it.

---

## Before we start: modules and packages

| Word | What it is | Example |
|---|---|---|
| **Module** | One `.py` file | `menu.py` |
| **Package** | A folder of modules that you import as a group | `cafe/` |
| **`__init__.py`** | A special file inside the folder that makes it a package | `cafe/__init__.py` |

Real projects grow past one file. Packages let you organise related files under one name, the same way folders organise documents on your computer.

> ⚠️ **Don't confuse the two `__init__`s**
> - `def __init__(self):` inside a **class** sets up a new **object**.
> - `__init__.py` inside a **folder** sets up a **package**.
>
> They share a name because both mean "initialise", but they are unrelated.

---

## Step 1: An empty `__init__.py` makes a package

📁 `step1_empty_init/`

```
step1_empty_init/
├── main.py
└── cafe/
    ├── __init__.py      <- completely EMPTY
    └── menu.py
```

The file `cafe/__init__.py` has nothing in it. Just being there tells Python
that `cafe` is a package, so you can reach the modules inside it with **dots**:

```python
from cafe.menu import show_menu     # package.module -> name
import cafe.menu                    # or import the module itself
cafe.menu.PRICES["tea"]
```

▶️ Run `python main.py`. You should see the menu and the path to `cafe/__init__.py`.

### 🪤 Gotcha: an empty `__init__.py` does not load the modules

Try this from inside `step1_empty_init/`:

```bash
python -c "import cafe; print(cafe.menu)"
```

```
AttributeError: module 'cafe' has no attribute 'menu'
```

`import cafe` only runs `cafe/__init__.py`. Since that file is empty, nothing
else gets loaded. You have to import `cafe.menu` yourself, or let
`__init__.py` do it for you (Step 3).

> 💡 Since Python 3.3, a folder **without** `__init__.py` can sometimes still be
> imported (a "namespace package"). That is an advanced feature. As a beginner,
> **always add an `__init__.py`**; it makes your intent clear and avoids surprises.

**✅ Remember:** an `__init__.py` file turns a folder into a package, even when it's empty.

---

## Step 2: `__init__.py` is code that runs on import

📁 `step2_runs_on_import/`

`__init__.py` is an ordinary Python file. Whatever you write in it **runs the
first time the package is imported**.

```python
# cafe/__init__.py
print(">>> cafe/__init__.py is running (the shop is opening!)")
SHOP_NAME = "Chai Corner"      # becomes cafe.SHOP_NAME
```

▶️ Run `python main.py` and watch the **order** of the lines:

```
1. Before any import
>>> cafe/__init__.py is running (the shop is opening!)
2. After 'import cafe'  ->  shop name: Chai Corner
3. After importing cafe a SECOND time (no >>> line above!)
>>> cafe/menu.py is running
4. After 'from cafe import menu'
```

What this shows:

1. `import cafe` **runs** `__init__.py`.
2. Variables created there become **attributes of the package**: `cafe.SHOP_NAME`.
3. Importing again does **nothing**. Python keeps loaded modules in a cache
   (`sys.modules`), so `__init__.py` runs **only once** per program.
4. Importing a module inside the package (`cafe.menu`) runs that module's code.
   If the package's `__init__.py` hasn't run yet, Python runs it **first**.

**✅ Remember:** `__init__.py` runs once, the first time anything from the package is imported.

---

## Step 3: `__init__.py` as the front desk (shortcuts)

📁 `step3_shortcuts/`

```
cafe/
├── __init__.py
├── menu.py        <- show_menu(), PRICES
└── orders.py      <- class Order
```

Without help, users must know which file holds what:

```python
from cafe.menu import show_menu
from cafe.orders import Order
```

Instead, `__init__.py` imports the useful names **once**, at the package level:

```python
# cafe/__init__.py
from .menu import show_menu, PRICES
from .orders import Order
```

Now anyone can simply write:

```python
import cafe
cafe.show_menu()
order = cafe.Order("Ravi")
```

Think of `__init__.py` as the **front desk** of a shop: customers ask
the desk, and don't need to know which room in the back has each thing.
You can even reorganise the files later without breaking anyone's code,
as long as the front desk still hands out the same names.

### Relative imports: the dot

Inside a package, modules import each other with a **dot**:

| You write | Means |
|---|---|
| `from .menu import PRICES` | from `menu.py` in **this same** package |
| `from . import menu` | the `menu` module of this package |
| `from .. import SHOP_NAME` | from the **parent** package (used in Step 4) |

`orders.py` uses `from .menu import PRICES`. That's shorter than
`from cafe.menu import PRICES`, and it keeps working if you rename the package.

> ⚠️ Relative imports only work **inside a package**. If you run
> `python cafe/orders.py` directly, you'll get
> `ImportError: attempted relative import with no known parent package`.
> Always run the program from outside the package (here, through `main.py`).

▶️ Run `python main.py`. Notice `Same class? True`: the shortcut and the long
path give you the **same** object, not a copy.

**✅ Remember:** import your public names in `__init__.py` so users can write `cafe.Order` instead of `cafe.orders.Order`.

---

## Step 4: A real-world package

📁 `step4_real_package/`

```
cafe/
├── __init__.py          <- the four jobs (below)
├── menu.py
├── orders.py
├── _counter.py          <- private helper (leading underscore)
└── payments/            <- a SUBPACKAGE
    ├── __init__.py      <- its own front desk
    ├── cash.py
    └── upi.py
```

A typical `__init__.py` does **four jobs, in this order**:

```python
# 1. Package information
__version__ = "1.0.0"
SHOP_NAME = "Chai Corner"

# 2. One-time setup
print(f"[{SHOP_NAME} v{__version__} is open]")

# 3. Shortcuts to the public names
from .menu import show_menu, PRICES
from .orders import Order
from . import payments

# 4. Public API list (what `from cafe import *` gives)
__all__ = ["show_menu", "PRICES", "Order", "payments", "SHOP_NAME"]
```

### Subpackages

`payments/` is a package **inside** a package. It needs its **own**
`__init__.py`, which works the same way as the parent's:

```python
# cafe/payments/__init__.py
from .cash import pay_cash
from .upi import pay_upi
```

So you can write `cafe.payments.pay_upi(...)` or `from cafe.payments import pay_cash`.

`upi.py` goes **up** to the parent package with two dots:

```python
from .. import SHOP_NAME        # = from cafe import SHOP_NAME
```

### Order inside `__init__.py` matters

`SHOP_NAME` is defined **before** `from . import payments`. Why? While
`payments/upi.py` is loading, it asks the parent for `SHOP_NAME`. If that line
came later, the name wouldn't exist yet and you'd get an `ImportError`.
`__init__.py` runs top to bottom like any script.

### Private modules

`_counter.py` starts with an underscore. That's a convention meaning
*"internal, don't use this from outside."* The package uses it (to number
orders), but `__init__.py` deliberately does **not** expose it.

▶️ Run `python main.py`:

```
[Chai Corner v1.0.0 is open]
...
Order #1 for Meera: ['coffee', 'samosa']
Order #2 for Kiran: ['tea']

Paid cash for order #1. Change: Rs 45
Paid Rs 20 by UPI from kiran@upi to Chai Corner for order #2
```

**✅ Remember:** `__init__.py` holds settings, setup, shortcuts and the public API, and subpackages have their own `__init__.py`.

---

## Good practice

| ✅ Do | ❌ Avoid |
|---|---|
| Keep `__init__.py` short: settings, imports, `__all__` | Putting large amounts of logic in it (put that in modules) |
| Expose only the names users need | Exposing private helpers like `_counter` |
| Use relative imports (`from .menu import ...`) inside the package | Running a package module directly (`python cafe/orders.py`) |
| Define names in `__init__.py` before importing submodules that need them | Slow work at import time (network calls, big files): every import pays for it |

---

## Practice exercises

Work in a copy of `step4_real_package/`.

1. **New module:** add `cafe/staff.py` with a function `on_duty()` that returns `["Asha", "Vikram"]`.
   Use it in `main.py` with `from cafe.staff import on_duty`.
2. **Shortcut:** expose `on_duty` in `cafe/__init__.py` so `cafe.on_duty()` works. Add it to `__all__`.
3. **Prove "runs once":** add `print("payments loaded")` to `cafe/payments/__init__.py`.
   Import `cafe` twice in `main.py`. How many times does it print?
4. **New subpackage:** create `cafe/delivery/` with `__init__.py` and `zomato.py`
   containing `deliver(order, address)`. Make `cafe.delivery.deliver(...)` work.
5. **Break it on purpose:** in `cafe/__init__.py`, move `SHOP_NAME = ...` *below*
   `from . import payments`. Run `main.py`, read the error and explain why it happens.
6. **Empty it:** delete all the code in `cafe/__init__.py` (keep the empty file).
   Which lines in `main.py` now fail, and how would you fix them **without** touching `__init__.py`?

<details>
<summary>Hint for exercise 5</summary>

`upi.py` runs `from .. import SHOP_NAME` while `cafe/__init__.py` is still only
halfway done. At that moment, `SHOP_NAME` hasn't been created yet.
</details>

<details>
<summary>Hint for exercise 6</summary>

Use full paths: `from cafe.orders import Order`, `from cafe.menu import show_menu`,
`from cafe.payments.cash import pay_cash`, and so on.
</details>

---

## One-minute summary

1. **`__init__.py` makes a folder a package**, even if it is empty.
2. **It runs once**, the first time anything from the package is imported.
3. **Names defined or imported in it** become `package.name`, a clean front desk.
4. **Inside a package, use relative imports**: `.` means this package, `..` means the parent.
5. **Subpackages** are folders inside the package, each with their own `__init__.py`.
6. **Keep it small**: settings, shortcuts and `__all__`. Real logic goes in modules.
