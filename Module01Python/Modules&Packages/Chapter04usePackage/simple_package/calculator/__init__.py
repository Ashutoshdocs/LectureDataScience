# calculator/__init__.py
# ----------------------
# This file makes the folder "calculator" a Python PACKAGE.
# It runs automatically the first time someone writes "import calculator".

print("calculator package loaded")  # Shows WHEN this file runs (only once per program)

__version__ = "1.0"  # A package-level variable, used as: calculator.__version__

from .basic import add, subtract  # Bring add() and subtract() up from basic.py ("." = this package)
from .advanced import power, square_root  # Bring power() and square_root() up from advanced.py

__all__ = ["add", "subtract", "power", "square_root"]  # Names given by: from calculator import *
