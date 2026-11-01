"""
LESSON 3: __all__ — controlling `from module import *`
======================================================
Run:  python lesson3_all.py

__all__ is a plain list of strings. It answers ONE question:
"When someone writes  from X import *  — which names do they get?"
"""

print("=" * 50)
print("PART A: A module WITHOUT __all__")
print("=" * 50)
import sys
import types


def star_import(module_name):
    """Run 'from <module_name> import *' in a fresh, empty namespace
    and return the names it created. (Helper for this lesson only.)"""
    namespace = {}
    exec(f"from {module_name} import *", namespace)
    return sorted(n for n in namespace if n != "__builtins__")


# Build a tiny module on the fly (as if it were a file no_all.py):
#     import math
#     def greet(): ...
#     def _secret(): ...
#     counter = 0
no_all = types.ModuleType("no_all")
exec(
    "import math\n"
    "def greet(): return 'hello'\n"
    "def _secret(): return 'hidden'\n"
    "counter = 0\n",
    no_all.__dict__,
)
sys.modules["no_all"] = no_all       # make it importable

print("  'from no_all import *' gives:", star_import("no_all"))
print("  Notice: 'math' leaked in! Imported modules get exported too.")
print("  '_secret' is skipped because it starts with an underscore.")


print()
print("=" * 50)
print("PART B: A module WITH __all__")
print("=" * 50)
import shapes.circle as circle_mod
print("  shapes/circle.py defines:  __all__ =", circle_mod.__all__)

print("  'from shapes.circle import *' gives:", star_import("shapes.circle"))
print("  'math', 'round2', '_PI_LABEL' were NOT imported. __all__ won.")


print()
print("=" * 50)
print("PART C: __all__ in a package's __init__.py")
print("=" * 50)
import shapes
print("  shapes.__all__ =", shapes.__all__)
print("  'from shapes import *' gives:", star_import("shapes"))
print("  'VERSION' in __all__?", "VERSION" in shapes.__all__)


print()
print("=" * 50)
print("PART D: __all__ is NOT a lock!")
print("=" * 50)
from shapes.circle import _PI_LABEL, round2   # explicit imports still work
print("  Explicitly imported _PI_LABEL =", _PI_LABEL)
print("  Explicitly imported round2(3.14159) =", round2(3.14159))
print("  __all__ only affects  import *  (and tells readers/tools")
print("  which names are the public API).")


print()
print("=" * 50)
print("PART E: Common mistake — a typo in __all__")
print("=" * 50)
bad = types.ModuleType("bad")
exec("def hello(): pass\n__all__ = ['helo']\n", bad.__dict__)  # typo!
sys.modules["bad"] = bad
try:
    star_import("bad")
except AttributeError as e:
    print("  AttributeError:", e)
print("  Every string in __all__ must be a real name in the module.")


print()
print("KEY TAKEAWAYS")
print(" 1. __all__ = ['name1', 'name2']  is a list of STRINGS.")
print(" 2. It decides what  'from X import *'  gives you.")
print(" 3. Without it, * takes every name not starting with '_'")
print("    (including modules you imported — messy!).")
print(" 4. It does NOT stop explicit imports like  from X import _hidden.")
print(" 5. Best practice: avoid  import *  in real code; still define")
print("    __all__ to document your public API.")
