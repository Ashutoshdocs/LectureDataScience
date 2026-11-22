"""Lecture 23: Checker for the OOP practice exercises.

    python lecture.py             -> checks solutions.py (should be 20/20)
    python lecture.py exercises   -> checks YOUR exercises.py
"""
import dataclasses
import importlib
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
target = sys.argv[1] if len(sys.argv) > 1 else "solutions"
m = importlib.import_module(target)


def expect(what, actual, expected):
    if actual != expected:
        raise AssertionError(f"{what}: got {actual!r}, expected {expected!r}")


def raises(what, func, exc_type):
    try:
        result = func()
    except exc_type:
        return
    except Exception as e:
        raise AssertionError(f"{what}: raised {type(e).__name__}, expected {exc_type.__name__}")
    raise AssertionError(f"{what}: returned {result!r}, expected {exc_type.__name__}")


def check_01():
    r = m.Rectangle(3, 4)
    expect("Rectangle(3, 4).area()", r.area(), 12)
    expect("Rectangle(3, 4).perimeter()", r.perimeter(), 14)


def check_02():
    c = m.Counter()
    expect("new Counter().count", c.count, 0)
    c.increment()
    c.increment(5)
    expect("count after increment() and increment(5)", c.count, 6)
    c.reset()
    expect("count after reset()", c.count, 0)


def check_03():
    start = getattr(m.Student, "count", None)
    if not isinstance(start, int):
        raise AssertionError("Student.count class attribute is missing")
    a, b = m.Student("Asha"), m.Student("Ravi")
    expect("Student.count after creating 2", m.Student.count, start + 2)
    expect("names are per object", (a.name, b.name), ("Asha", "Ravi"))
    expect("'count' is not stored on each object", "count" in vars(a), False)


def check_04():
    t = m.Temperature(100)
    expect("Temperature(100).fahrenheit", t.fahrenheit, 212)
    t.celsius = 0
    expect("fahrenheit after celsius = 0", t.fahrenheit, 32)
    raises("t.celsius = -300", lambda: setattr(t, "celsius", -300), ValueError)
    raises("Temperature(-500)", lambda: m.Temperature(-500), ValueError)
    raises("t.fahrenheit = 50 (read-only)", lambda: setattr(t, "fahrenheit", 50), AttributeError)


def check_05():
    acc = m.BankAccount("Asha", 100)
    expect("deposit(50)", acc.deposit(50), 150)
    expect("withdraw(30)", acc.withdraw(30), 120)
    raises("withdraw(1000)", lambda: acc.withdraw(1000), ValueError)
    raises("deposit(-5)", lambda: acc.deposit(-5), ValueError)
    raises("acc.balance = 999 (read-only)", lambda: setattr(acc, "balance", 999), AttributeError)
    expect("balance", acc.balance, 120)


def check_06():
    p = m.Point.from_string("3,4")
    expect("Point.from_string('3,4') coords", (p.x, p.y), (3, 4))
    expect("Point.distance(Point(0,0), Point(3,4))", m.Point.distance(m.Point(0, 0), m.Point(3, 4)), 5)

    class Point3(m.Point):
        pass
    expect("subclass.from_string returns the subclass", type(Point3.from_string("1,2")).__name__, "Point3")


def check_07():
    raises("Animal('x').speak()", lambda: m.Animal("x").speak(), NotImplementedError)
    expect("Dog('Rex').speak()", m.Dog("Rex").speak(), "Rex says Woof")
    expect("Cat('Tom').speak()", m.Cat("Tom").speak(), "Tom says Meow")
    expect("Dog is an Animal", isinstance(m.Dog("a"), m.Animal), True)


def check_08():
    expect("Employee describe", m.Employee("Asha", 50000).describe(), "Asha earns 50000")
    mgr = m.Manager("Ravi", 90000, 5)
    expect("Manager describe", mgr.describe(), "Ravi earns 90000 and manages 5 people")
    expect("Manager is an Employee", isinstance(mgr, m.Employee), True)


def check_09():
    raises("Shape() (abstract)", lambda: m.Shape(), TypeError)
    expect("Circle(1).area()", round(m.Circle(1).area(), 5), 3.14159)
    expect("Square(3).area()", m.Square(3).area(), 9)

    class Blob(m.Shape):
        pass
    raises("subclass without area()", lambda: Blob(), TypeError)


def check_10():
    b = m.Book("Python", 320)
    expect("str(book)", str(b), "Python (320 pages)")
    expect("repr(book)", repr(b), "Book('Python', 320)")
    expect("book inside a list", str([b]), "[Book('Python', 320)]")


def check_11():
    p = m.Playlist(["a", "b", "c"])
    expect("len(p)", len(p), 3)
    expect("p[0]", p[0], "a")
    expect("'b' in p", "b" in p, True)
    expect("'z' in p", "z" in p, False)


def check_12():
    v, w = m.Vector(1, 2), m.Vector(3, 4)
    expect("Vector(1,2) + Vector(3,4)", v + w, m.Vector(4, 6))
    expect("v * 3", v * 3, m.Vector(3, 6))
    expect("3 * v", 3 * v, m.Vector(3, 6))
    expect("repr", repr(v), "Vector(1, 2)")
    expect("v unchanged", (v.x, v.y), (1, 2))


def check_13():
    V = m.Version
    expect("1.10 > 1.9", V("1.10") > V("1.9"), True)
    expect("1.2 == 1.2", V("1.2") == V("1.2"), True)
    expect("2.0 <= 1.5", V("2.0") <= V("1.5"), False)
    ordered = sorted([V("2.0"), V("1.10"), V("1.9")])
    expect("sorted() puts 1.9 first and 2.0 last", (ordered[0] == V("1.9"), ordered[-1] == V("2.0")), (True, True))


def check_14():
    a, b = m.Coordinate(1, 2), m.Coordinate(1, 2)
    expect("Coordinate(1,2) == Coordinate(1,2)", a == b, True)
    expect("len of a set of two equal coordinates", len({a, b}), 1)
    expect("works as a dict key", {a: "home"}[b], "home")


def check_15():
    s = m.Stack()
    expect("Stack is not a list subclass", isinstance(s, list), False)
    expect("peek() on empty", s.peek(), None)
    s.push(1)
    s.push(2)
    expect("len after 2 pushes", len(s), 2)
    expect("peek()", s.peek(), 2)
    expect("pop()", s.pop(), 2)
    s.pop()
    raises("pop() on empty", s.pop, IndexError)


def check_16():
    u = m.User("A", "a@b")
    expect("User('A', 'a@b').to_json()", json.loads(u.to_json()), {"name": "A", "email": "a@b"})
    expect("User uses JsonMixin", isinstance(u, m.JsonMixin), True)


def check_17():
    triple = m.Multiplier(3)
    expect("Multiplier(3)(5)", triple(5), 15)
    triple(1)
    expect("calls after 2 calls", triple.calls, 2)


def check_18():
    expect("Product is a dataclass", dataclasses.is_dataclass(m.Product), True)
    p = m.Product("pen", 10.0, 3)
    expect("Product('pen', 10.0, 3).total", p.total, 30.0)
    expect("default qty", m.Product("bag", 500.0).qty, 1)
    expect("== compares fields", m.Product("a", 1.0) == m.Product("a", 1.0), True)


def check_19():
    with m.Tracker() as t:
        expect("events inside the with block", list(t.events), ["enter"])
    expect("events after the block", t.events, ["enter", "exit"])
    t2 = m.Tracker()
    try:
        with t2:
            raise KeyError("boom")
    except KeyError:
        pass
    expect("events after an error (error must not be swallowed)", t2.events, ["enter", "exit"])


def check_20():
    c = m.Countdown(3)
    expect("list(Countdown(3))", list(c), [3, 2, 1])
    expect("second loop over the same object", list(c), [3, 2, 1])
    expect("sum(Countdown(4))", sum(m.Countdown(4)), 10)


TITLES = ["Rectangle", "Counter", "Student.count", "Temperature property", "BankAccount",
          "classmethod & staticmethod", "Animal inheritance", "super() Manager", "Shape ABC",
          "__str__/__repr__", "Playlist container", "Vector operators", "Version ordering",
          "__eq__ + __hash__", "Stack composition", "JsonMixin", "__call__", "dataclass Product",
          "context manager", "iterable Countdown"]
CHECKS = [globals()[f"check_{i:02d}"] for i in range(1, 21)]

print(f"Checking {target}.py\n")
score = 0
for num, (title, check) in enumerate(zip(TITLES, CHECKS), start=1):
    try:
        check()
    except Exception as e:
        kind = "" if isinstance(e, AssertionError) else type(e).__name__ + ": "
        print(f"  ✘ {num:02d} {title:<27} {kind}{e}")
    else:
        score += 1
        print(f"  ✔ {num:02d} {title}")
print(f"\n  Score: {score} / {len(CHECKS)}")

if target == "solutions" and score != len(CHECKS):
    sys.exit(1)
