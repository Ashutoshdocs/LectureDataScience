"""
cafe — a small but realistic package.

A typical __init__.py does four jobs, in this order:
"""

# 1. Package-level information (metadata / settings)
__version__ = "1.0.0"
SHOP_NAME = "Chai Corner"

# 2. One-time setup code (runs once, on first import)
print(f"[{SHOP_NAME} v{__version__} is open]")

# 3. Shortcuts: pull the public names up to the package level
from .menu import show_menu, PRICES
from .orders import Order
from . import payments          # make the subpackage reachable as cafe.payments

# 4. Declare the public API (what `from cafe import *` gives)
__all__ = ["show_menu", "PRICES", "Order", "payments", "SHOP_NAME"]

# Note: order matters! SHOP_NAME is defined BEFORE `from . import payments`,
# because payments/upi.py does `from .. import SHOP_NAME` while it loads.
