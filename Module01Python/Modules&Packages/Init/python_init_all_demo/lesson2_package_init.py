"""
LESSON 2: __init__.py — turning a FOLDER into a PACKAGE
=======================================================
Run:  python lesson2_package_init.py

Folder layout:
    shapes/
        __init__.py   <- runs when you `import shapes`
        circle.py
        square.py
        _helpers.py   <- private helper module

Don't confuse the two __init__s:
  * __init__   (method in a class)  -> sets up a new OBJECT
  * __init__.py (file in a folder)  -> sets up a PACKAGE
"""

print("=" * 50)
print("PART A: Importing the package runs __init__.py")
print("=" * 50)
print("About to import shapes...")
import shapes                     # watch: the print inside __init__.py fires
print("Import finished.")

print("\nImporting it AGAIN...")
import shapes                     # nothing printed: Python caches modules
print("  (no message — __init__.py only runs once per program)")


print()
print("=" * 50)
print("PART B: Short imports thanks to __init__.py")
print("=" * 50)
# Without the imports inside __init__.py, you'd have to write:
from shapes.circle import Circle          # long form (always works)
# With them, this short form works too:
c = shapes.Circle(3)
sq = shapes.Square(4)
print("  shapes.Circle(3).area() =", c.area())
print("  shapes.Square(4).area() =", sq.area())
print("  Same class either way?", Circle is shapes.Circle)


print()
print("=" * 50)
print("PART C: Package-level data")
print("=" * 50)
print("  shapes.VERSION =", shapes.VERSION)


print()
print("KEY TAKEAWAYS")
print(" 1. A folder with __init__.py is a 'regular package'.")
print(" 2. __init__.py runs once, on the first import of the package.")
print(" 3. Use it to expose the important names: shapes.Circle instead of")
print("    shapes.circle.Circle.")
print(" 4. It can be empty — just being there is enough to mark a package.")
print("    (Python 3.3+ also allows 'namespace packages' with no __init__.py,")
print("     but beginners should always include one.)")
