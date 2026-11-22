# Folder 3 – Create and use a Python package

## Folder structure

```text
03_package_creation/
├── main.py
└── shop/
    ├── __init__.py
    ├── products.py
    └── billing.py
```

## What is a package?

A package is a folder that groups related Python modules. In this example:
- `shop` is the package.
- `products.py` and `billing.py` are modules inside the package.
- `__init__.py` marks the folder as a regular Python package.

## Import package modules

```python
from shop import products
from shop import billing
```

Then call their functions:

```python
products.list_products()
billing.calculate_total(500, 3)
```

## Run

Open a terminal in this folder:

```bash
python3 main.py
```

## Try this

1. Add a function named `apply_discount()` to `billing.py`.
2. Import and call it from `main.py`.
3. Create another module named `customers.py` inside `shop`.
4. Add a function to display a customer name and call it from `main.py`.

## Remember

- A **module** is a Python file (`.py`).
- A **package** is a folder that groups modules.
- `__init__.py` can be empty; it can also contain package initialization code.
