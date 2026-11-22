"""Lecture 19: Dataclasses: generated methods, field(), frozen, order, slots, __post_init__, helpers."""
import dataclasses
from dataclasses import dataclass, field

print("=== 1. Boilerplate vs @dataclass ===")


class PointManual:
    def __init__(self, x, y=0):
        self.x, self.y = x, y

    def __repr__(self):
        return f"PointManual(x={self.x}, y={self.y})"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


@dataclass
class Point:
    x: int
    y: int = 0

    def distance_from_origin(self):            # normal methods are fine
        return (self.x ** 2 + self.y ** 2) ** 0.5


print("  manual  :", PointManual(3, 4), PointManual(3, 4) == PointManual(3, 4))
print("  dataclass:", Point(3, 4), Point(3, 4) == Point(3, 4), "| distance:", Point(3, 4).distance_from_origin())
print("  generated methods:", [m for m in ("__init__", "__repr__", "__eq__") if m in Point.__dict__])
print("  type hints are NOT enforced:", Point("a", "b"))

print("\n=== 2. field(): safe mutable defaults and hidden fields ===")


@dataclass
class Cart:
    owner: str
    items: list = field(default_factory=list)
    _id: int = field(default=0, repr=False, compare=False)

    def add(self, item):
        self.items.append(item)
        return self


a, b = Cart("Asha", _id=1), Cart("Ravi", _id=2)
a.add("pen")
print("  a:", a, "| b:", b, "<- separate lists, _id hidden")
print("  Cart('X', _id=1) == Cart('X', _id=99):", Cart("X", _id=1) == Cart("X", _id=99), "(compare=False)")
try:
    @dataclass
    class Bad:
        items: list = []
except ValueError as e:
    print("  items: list = [] -> ValueError:", e)

print("\n=== 3. __post_init__: validation and derived fields ===")


@dataclass
class Student:
    name: str
    marks: int
    grade: str = field(init=False)

    def __post_init__(self):
        if not 0 <= self.marks <= 100:
            raise ValueError(f"marks must be 0-100, got {self.marks}")
        self.name = self.name.title()
        self.grade = "A" if self.marks >= 85 else "B" if self.marks >= 70 else "PASS" if self.marks >= 40 else "FAIL"


print("  ", Student("asha rao", 92), "|", Student("ravi", 38))
try:
    Student("x", 120)
except ValueError as e:
    print("   Student('x', 120) -> ValueError:", e)

print("\n=== 4. frozen=True: immutable and hashable ===")


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "INR"


m = Money(100)
try:
    m.amount = 5
except dataclasses.FrozenInstanceError as e:
    print("  m.amount = 5 -> FrozenInstanceError:", e)
unique = {Money(100), Money(100), Money(50)}
print("  set of 3 Money objects (2 equal) has", len(unique), "items:", sorted(unique, key=lambda x: x.amount))
print("  replace() makes a modified copy:", dataclasses.replace(m, amount=250), "| original:", m)

print("\n=== 5. order=True: comparisons by fields in order ===")


@dataclass(order=True)
class Task:
    priority: int
    title: str = field(compare=False)


tasks = [Task(3, "write report"), Task(1, "fix bug"), Task(2, "email client")]
print("  sorted:", [t.title for t in sorted(tasks)])
print("  Task(1,'a') < Task(2,'b'):", Task(1, "a") < Task(2, "b"))

print("\n=== 6. slots=True saves memory and blocks typos ===")


@dataclass(slots=True)
class Pixel:
    x: int
    y: int


px = Pixel(1, 2)
try:
    px.colour = "red"
except AttributeError as e:
    print("  px.colour = 'red' -> AttributeError:", e)

print("\n=== 7. Helpers and inheritance ===")


@dataclass
class Person:
    name: str
    age: int


@dataclass
class Employee(Person):
    dept: str = "General"
    skills: list = field(default_factory=list)


e = Employee("Dev", 30, "IT", ["python"])
print("  child dataclass:", e)
print("  asdict         :", dataclasses.asdict(e))
print("  fields         :", [f.name for f in dataclasses.fields(Employee)])
print("  isinstance(e, Person):", isinstance(e, Person))
