"""
STEP 1 — An EMPTY __init__.py makes a folder a package
Run from this folder:   python main.py
"""

# The folder 'cafe' has an EMPTY __init__.py, so Python treats it as a package.
# We reach the module inside it with a dotted path:  package.module
from cafe.menu import show_menu

print("Menu (via 'from cafe.menu import show_menu'):")
show_menu()

# Another way: import the module, then use dots
import cafe.menu
print("\nTea costs Rs", cafe.menu.PRICES["tea"])

# What does importing just the package give us?
import cafe
print("\ncafe is a package loaded from:", cafe.__file__)

# Gotcha: the empty __init__.py does NOT import menu for you.
# It only works above because we already wrote 'import cafe.menu'.
# In a fresh program, 'import cafe' then 'cafe.menu' would raise AttributeError.
# Step 3 shows how __init__.py can fix that.
