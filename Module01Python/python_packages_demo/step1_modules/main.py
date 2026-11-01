"""main.py - shows every common way to import a module.

Run from inside step1_modules/:
    python main.py
"""

print("=== 1. import module ===")
import mathutils

print(mathutils.add(2, 3))
print(mathutils.PI)

print("\n=== 2. import module again (no second 'loaded' message - modules are cached) ===")
import mathutils  # noqa: F811  -> nothing printed: Python reuses sys.modules['mathutils']
import sys
print("'mathutils' in sys.modules ->", "mathutils" in sys.modules)

print("\n=== 3. from module import name ===")
from mathutils import area_of_circle

print(area_of_circle(2))

print("\n=== 4. import with an alias ===")
import stringutils as su

print(su.shout("hello"))

print("\n=== 5. from module import name as alias ===")
from stringutils import reverse as rev

print(rev("python"))

print("\n=== 6. from module import *  (respects __all__) ===")
from stringutils import *  # noqa: F403

print(shout("star import"))           # in __all__ -> available
print("'whisper' imported by * ?", "whisper" in dir())  # not in __all__ -> False

print("\n=== 7. Inspecting a module ===")
print("File:", mathutils.__file__)
print("Public names:", [n for n in dir(mathutils) if not n.startswith("_")])

print("\n=== 8. Where does Python look for modules? (sys.path) ===")
for p in sys.path[:3]:
    print("  ", p)
