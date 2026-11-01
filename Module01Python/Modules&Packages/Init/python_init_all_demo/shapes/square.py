"""shapes/square.py — another module inside the package."""
from ._helpers import round2

__all__ = ["Square"]


class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return round2(self.side ** 2)

    def __repr__(self):
        return f"Square(side={self.side})"
