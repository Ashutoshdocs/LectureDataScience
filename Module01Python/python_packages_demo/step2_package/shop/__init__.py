"""shop - a PACKAGE.

A package is a directory containing an __init__.py file.
This file runs when the package is first imported, and it decides
what `import shop` exposes directly.
"""

print("[shop] package initialised")

__version__ = "1.0.0"

# Re-export the most useful names so users can write
#   from shop import Cart
# instead of
#   from shop.cart import Cart
from .cart import Cart  # relative import: "." means "this package"

__all__ = ["Cart", "__version__"]
