"""toolkit - a tiny example package.

A folder becomes a *package* when it contains __init__.py.
This file runs the first time the package is imported.
"""

__version__ = "1.0.0"

# Re-export names so users can write: from toolkit import greet
from .textx import shout       # relative import: "." means this package


def greet(name):
    return f"Hello, {name}!"


__all__ = ["greet", "shout", "mathx", "textx"]   # used by: from toolkit import *
