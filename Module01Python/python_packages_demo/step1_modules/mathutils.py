"""mathutils.py - a simple MODULE.

A module is just a .py file. Its name (without .py) is the module name.
Everything defined at the top level (functions, classes, variables)
becomes an attribute of the module object.
"""

PI = 3.14159  # module-level constant


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def area_of_circle(radius):
    """Return the area of a circle."""
    return PI * radius * radius


def _private_helper():
    """Leading underscore = 'internal use' by convention.
    It is NOT imported by `from mathutils import *`."""
    return "you found the private helper"


# This line runs once, the FIRST time the module is imported.
print(f"[mathutils] loaded  (__name__ = {__name__!r})")


if __name__ == "__main__":
    # Runs only when executed directly:  python mathutils.py
    # Does NOT run when imported by another file.
    print("Running mathutils as a script - quick self test:")
    print("add(2, 3) =", add(2, 3))
    print("area_of_circle(1) =", area_of_circle(1))
