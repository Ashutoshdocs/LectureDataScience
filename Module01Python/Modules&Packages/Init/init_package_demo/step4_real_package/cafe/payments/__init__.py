"""
cafe/payments/__init__.py — a SUBPACKAGE (a package inside a package).

It has its own __init__.py, and works exactly like the parent:
it marks the folder as a package and acts as its front desk.
"""

from .cash import pay_cash
from .upi import pay_upi
