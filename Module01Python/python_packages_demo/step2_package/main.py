"""main.py - using the shop package.

Run from inside step2_package/:
    python main.py
"""

print("=== 1. Import the package (runs shop/__init__.py and shop/pricing/__init__.py) ===")
import shop

print("Version:", shop.__version__)

print("\n=== 2. Use a name re-exported by __init__.py ===")
from shop import Cart

cart = Cart()
cart.add("Python Book", 500).add("USB Drive", 300, 2)
print(cart)
print("Total (with 18% GST):      ", cart.total())
print("Total with STUDENT10 code: ", cart.total("STUDENT10"))

print("\n=== 3. Absolute import of a module deep inside the package ===")
from shop.pricing.discounts import DISCOUNT_CODES

print("Available codes:", list(DISCOUNT_CODES))

print("\n=== 4. Import a sub-package ===")
import shop.pricing as pricing

print("GST rate:", pricing.GST_RATE)
print("1000 after FESTIVE20:", pricing.apply_discount(1000, "FESTIVE20"))

print("\n=== 5. Package vs module ===")
print("shop.__path__   ->", shop.__path__)      # only packages have __path__
print("shop.cart has __path__?", hasattr(shop.cart, "__path__"))
