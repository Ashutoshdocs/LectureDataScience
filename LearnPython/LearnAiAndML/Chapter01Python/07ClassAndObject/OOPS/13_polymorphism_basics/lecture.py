"""Lecture 13: Polymorphism: built-in examples, shapes, removing type checks, singledispatch."""
import functools
import math

print("=== 1. You already use polymorphism ===")
for obj in ["hello", [1, 2, 3], {"a": 1}, range(10)]:
    print(f"  len({obj!r}) = {len(obj)}")
print("  1 + 2 =", 1 + 2, "| 'a' + 'b' =", "a" + "b", "| [1] + [2] =", [1] + [2])

print("\n=== 2. The type-check way (hard to extend) ===")


def area_by_type(shape):
    if shape["type"] == "circle":
        return round(math.pi * shape["r"] ** 2, 2)
    elif shape["type"] == "square":
        return shape["s"] ** 2
    raise ValueError(f"unknown shape {shape['type']!r}: edit this function to add it!")


for s in [{"type": "circle", "r": 1}, {"type": "square", "s": 3}, {"type": "triangle", "b": 4, "h": 3}]:
    try:
        print("  ", s["type"], area_by_type(s))
    except ValueError as e:
        print("  ", e)

print("\n=== 3. The polymorphic way ===")


class Shape:
    def area(self):
        raise NotImplementedError(f"{type(self).__name__} must implement area()")

    def describe(self):                                   # shared code using the interface
        return f"{type(self).__name__:<9} area = {self.area():>7.2f}"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


class Triangle(Shape):                                    # added later: no other code changes
    def __init__(self, base, height):
        self.base, self.height = base, height

    def area(self):
        return 0.5 * self.base * self.height


def total_area(shapes):
    return round(sum(s.area() for s in shapes), 2)


def largest(shapes):
    return max(shapes, key=lambda s: s.area())


shapes = [Circle(1), Square(3), Triangle(4, 3), Circle(2)]
for s in shapes:
    print("  ", s.describe())
print("   total area:", total_area(shapes), "| largest:", type(largest(shapes)).__name__)


class Blob(Shape):
    pass


try:
    Blob().describe()
except NotImplementedError as e:
    print("   NotImplementedError:", e)

print("\n=== 4. Same message, different channels ===")


class Email:
    def __init__(self, address):
        self.address = address

    def send(self, msg):
        return f"EMAIL to {self.address}: {msg}"


class SMS:
    def __init__(self, phone):
        self.phone = phone

    def send(self, msg):
        return f"SMS to {self.phone}: {msg[:20]}{'...' if len(msg) > 20 else ''}"


class Push:
    def send(self, msg):
        return f"PUSH: {msg.upper()}"


def broadcast(channels, msg):                             # polymorphic function
    return [c.send(msg) for c in channels]


for line in broadcast([Email("asha@mail.com"), SMS("98765-43210"), Push()], "Your order has shipped today"):
    print("  ", line)

print("\n=== 5. No method overloading: the last def wins ===")


class Calc:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c=0):                             # replaces the one above   # noqa: F811
        return a + b + c


print("  Calc().add(1, 2)    =", Calc().add(1, 2))
print("  Calc().add(1, 2, 3) =", Calc().add(1, 2, 3))

print("\n=== 6. Choosing behaviour by argument type: singledispatch ===")


@functools.singledispatch
def describe(x):
    return f"something: {x!r}"


@describe.register
def _(x: int):
    return f"an integer, {'even' if x % 2 == 0 else 'odd'}"


@describe.register
def _(x: str):
    return f"a string of {len(x)} characters"


@describe.register
def _(x: list):
    return f"a list of {len(x)} items"


for value in [7, "hello", [1, 2], 3.5]:
    print(f"  describe({value!r}) -> {describe(value)}")
