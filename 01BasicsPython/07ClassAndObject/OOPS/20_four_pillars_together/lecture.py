"""Lecture 20: All four pillars in one program: shapes on a canvas."""
import functools
import math
from abc import ABC, abstractmethod


# ---------- ABSTRACTION: the contract ----------
@functools.total_ordering
class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

    @abstractmethod
    def perimeter(self):
        ...

    @staticmethod
    def _positive(name, value):                     # ENCAPSULATION: shared validation helper
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{name} must be a positive number, got {value!r}")
        return value

    def describe(self):
        return f"{self!r:<28} area {self.area():>8.2f}   perimeter {self.perimeter():>7.2f}"

    # POLYMORPHISM through operators: compare any two shapes by area
    def __eq__(self, other):
        return isinstance(other, Shape) and math.isclose(self.area(), other.area())

    def __lt__(self, other):
        return self.area() < other.area() if isinstance(other, Shape) else NotImplemented

    __hash__ = None


# ---------- INHERITANCE + ENCAPSULATION ----------
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width                          # goes through the validated setters
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = self._positive("width", value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = self._positive("height", value)

    def area(self):
        return self._width * self._height

    def perimeter(self):
        return 2 * (self._width + self._height)

    def __repr__(self):
        return f"{type(self).__name__}({self._width} x {self._height})"


class Square(Rectangle):                            # a Square IS a Rectangle
    def __init__(self, side):
        super().__init__(side, side)

    @classmethod
    def from_area(cls, area):                       # alternative constructor
        return cls(math.sqrt(area))

    def __repr__(self):
        return f"Square({self._width:g})"


class Circle(Shape):
    def __init__(self, radius):
        self._radius = self._positive("radius", radius)

    @property
    def radius(self):
        return self._radius

    def area(self):
        return math.pi * self._radius ** 2

    def perimeter(self):
        return 2 * math.pi * self._radius

    def __repr__(self):
        return f"Circle(r={self._radius})"


class Triangle(Shape):                              # added later: no changes to Canvas
    def __init__(self, a, b, c):
        a, b, c = (self._positive("side", s) for s in (a, b, c))
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError(f"sides {a}, {b}, {c} can't form a triangle")
        self._sides = (a, b, c)

    def area(self):
        s = self.perimeter() / 2
        a, b, c = self._sides
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

    def perimeter(self):
        return sum(self._sides)

    def __repr__(self):
        return f"Triangle{self._sides}"


# ---------- COMPOSITION: a canvas HAS shapes ----------
class Canvas:
    def __init__(self, name):
        self.name = name
        self._shapes = []

    def add(self, shape):
        if not isinstance(shape, Shape):            # depends only on the abstraction
            raise TypeError(f"can only add Shapes, not {type(shape).__name__}")
        self._shapes.append(shape)
        return self

    def total_area(self):
        return sum(s.area() for s in self._shapes)  # POLYMORPHISM

    def largest(self, n=1):
        return sorted(self._shapes, reverse=True)[:n]

    def __len__(self):
        return len(self._shapes)

    def __iter__(self):
        return iter(self._shapes)


def main():
    canvas = Canvas("demo")
    canvas.add(Rectangle(2, 5)).add(Square(4)).add(Circle(1.5)).add(Triangle(3, 4, 5)).add(Square.from_area(9))

    print(f"=== Canvas '{canvas.name}' with {len(canvas)} shapes ===")
    for shape in canvas:
        print("  ", shape.describe())
    print(f"   total area: {canvas.total_area():.2f}")
    print("   two largest:", canvas.largest(2))
    print("   Square(4) == Rectangle(2, 8) (same area):", Square(4) == Rectangle(2, 8))

    print("\n=== Encapsulation: validation can't be bypassed ===")
    r = Rectangle(2, 3)
    for action, code in [("Rectangle(-1, 2)", lambda: Rectangle(-1, 2)),
                         ("r.width = 0", lambda: setattr(r, "width", 0)),
                         ("Triangle(1, 2, 10)", lambda: Triangle(1, 2, 10)),
                         ("Circle(2).radius = 5", lambda: setattr(Circle(2), "radius", 5))]:
        try:
            code()
        except (ValueError, AttributeError) as e:
            print(f"  {action:<21} -> {type(e).__name__}: {e}")

    print("\n=== Inheritance ===")
    print("  Square MRO:", " -> ".join(c.__name__ for c in Square.__mro__))
    print("  Square inherits area/perimeter from Rectangle:", "area" not in Square.__dict__)

    print("\n=== Abstraction ===")

    class Blob(Shape):
        def area(self):
            return 1

    for cls in (Shape, Blob):
        try:
            cls()
        except TypeError as e:
            print(f"  {cls.__name__}() -> TypeError: {e}")
    try:
        canvas.add("a circle")
    except TypeError as e:
        print("  canvas.add('a circle') -> TypeError:", e)


if __name__ == "__main__":
    main()
