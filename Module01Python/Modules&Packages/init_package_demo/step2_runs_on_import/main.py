"""
STEP 2 — __init__.py RUNS when the package is imported (only once)
Run from this folder:   python main.py
Watch the ORDER of the printed lines.
"""

print("1. Before any import")

import cafe                      # runs cafe/__init__.py
print("2. After 'import cafe'  ->  shop name:", cafe.SHOP_NAME)

import cafe                      # already loaded: nothing runs again
print("3. After importing cafe a SECOND time (no >>> line above!)")

from cafe import menu            # runs cafe/menu.py, but NOT __init__.py again
print("4. After 'from cafe import menu'")
menu.show_menu()

# Importing a module inside a package ALWAYS runs the package's __init__.py
# first (if it hasn't run yet). Python caches loaded modules in sys.modules:
import sys
print("\nLoaded cafe modules:", sorted(m for m in sys.modules if m.startswith("cafe")))
