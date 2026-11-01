"""
STEP 4 — A real-world package: settings, setup, shortcuts, subpackages
Run from this folder:   python main.py
"""

import cafe

print("Version:", cafe.__version__)
print("\nToday's menu:")
cafe.show_menu()

# Orders get numbers from the private helper cafe/_counter.py
o1 = cafe.Order("Meera")
o1.add("coffee")
o1.add("samosa")

o2 = cafe.Order("Kiran")
o2.add("tea")

print()
print(o1)
print(o2)

# Subpackage: reached through cafe.payments thanks to both __init__.py files
print()
print(cafe.payments.pay_cash(o1, given=100))
print(cafe.payments.pay_upi(o2, upi_id="kiran@upi"))

# You can also import straight from the subpackage
from cafe.payments import pay_cash
try:
    pay_cash(o1, given=10)
except ValueError as e:
    print("Error:", e)
