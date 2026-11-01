"""
STEP 3 — Use __init__.py to create SHORTCUTS (a clean front door)
Run from this folder:   python main.py
"""

import cafe

# Thanks to the imports inside cafe/__init__.py, these work directly:
print("Menu:")
cafe.show_menu()

order = cafe.Order("Ravi")
order.add("tea")
order.add("samosa")
print(f"\n{order.customer}'s total: Rs {order.total()}")

# The long paths still work too, and point to the SAME objects:
from cafe.orders import Order
print("\nSame class?", Order is cafe.Order)

# Unlike Step 1, the submodules are now attributes of the package,
# because __init__.py imported them:
print("cafe.menu is loaded:", cafe.menu.__name__)

# A wrong item gives a clear error:
try:
    order.add("pizza")
except ValueError as e:
    print("Error:", e)
