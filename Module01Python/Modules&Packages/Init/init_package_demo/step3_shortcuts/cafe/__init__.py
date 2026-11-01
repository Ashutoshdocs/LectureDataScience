"""
cafe/__init__.py — the package's "front desk".

We import the useful names from the inner modules HERE, so users can write
    from cafe import Order, show_menu
instead of having to know the files:
    from cafe.orders import Order
    from cafe.menu import show_menu
"""

from .menu import show_menu, PRICES
from .orders import Order
