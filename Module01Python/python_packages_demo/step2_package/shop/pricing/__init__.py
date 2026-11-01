"""shop.pricing - a SUB-PACKAGE (a package nested inside a package)."""

print("[shop.pricing] sub-package initialised")

from .discounts import apply_discount
from .tax import add_tax, GST_RATE

__all__ = ["apply_discount", "add_tax", "GST_RATE"]
