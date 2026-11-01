"""
shapes/__init__.py  —  the PACKAGE's __init__ file
=================================================
1. Its presence marks the folder 'shapes' as a Python package.
2. It runs ONCE, the first time anyone does `import shapes`.
3. Whatever you import here becomes available as shapes.<name>,
   so users don't need to know the internal file layout.
4. __all__ here controls what `from shapes import *` gives you.
"""

print("  [shapes/__init__.py is running — package is being imported]")

# Pull the important names up to the package level
from .circle import Circle
from .square import Square

VERSION = "1.0"

# Only these names are exported by:  from shapes import *
# (VERSION and the private _helpers module are NOT included)
__all__ = ["Circle", "Square"]
