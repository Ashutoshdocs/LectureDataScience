"""shapes/circle.py — a normal module inside the package."""
import math

from ._helpers import round2

# __all__ in a MODULE: only Circle is exported by `from shapes.circle import *`
# (math, round2 and _PI_LABEL stay hidden)
__all__ = ["Circle"]

_PI_LABEL = "π"   # leading underscore = "private, please don't use"


class Circle:
    def __init__(self, radius):          # constructor (Lesson 1!)
        self.radius = radius

    def area(self):
        return round2(math.pi * self.radius ** 2)

    def __repr__(self):
        return f"Circle(radius={self.radius})"
