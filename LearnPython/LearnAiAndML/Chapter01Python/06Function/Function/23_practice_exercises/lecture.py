"""Lecture 23: Checker for the practice exercises.

    python lecture.py             -> checks solutions.py (should be 20/20)
    python lecture.py exercises   -> checks YOUR exercises.py
"""
import importlib
import inspect
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
target = sys.argv[1] if len(sys.argv) > 1 else "solutions"
mod = importlib.import_module(target)


def expect(call_text, actual, expected):
    if actual != expected:
        raise AssertionError(f"{call_text} returned {actual!r}, expected {expected!r}")


def raises(call_text, func, exc_type):
    try:
        result = func()
    except exc_type:
        return
    except Exception as e:
        raise AssertionError(f"{call_text} raised {type(e).__name__}, expected {exc_type.__name__}")
    raise AssertionError(f"{call_text} returned {result!r}, expected it to raise {exc_type.__name__}")


def check_01(m):
    expect("greet('Asha')", m.greet("Asha"), "Hello, Asha!")
    expect("greet('Ravi', 'Hi')", m.greet("Ravi", "Hi"), "Hi, Ravi!")


def check_02(m):
    expect("area_of_rectangle(3, 4)", m.area_of_rectangle(3, 4), 12)


def check_03(m):
    expect("min_max([4, 1, 9])", m.min_max([4, 1, 9]), (1, 9))


def check_04(m):
    expect("[is_even(n) for n in (4, 7, 0)]", [m.is_even(n) for n in (4, 7, 0)], [True, False, True])


def check_05(m):
    expect("count_vowels('Hello World')", m.count_vowels("Hello World"), 3)
    expect("count_vowels('AEIOU xyz')", m.count_vowels("AEIOU xyz"), 5)


def check_06(m):
    c1, c2 = m.make_counter(), m.make_counter()
    expect("three calls of one counter", [c1(), c1(), c1()], [1, 2, 3])
    expect("a second, independent counter", c2(), 1)


def check_07(m):
    expect("average(2, 4, 6)", m.average(2, 4, 6), 4.0)
    expect("average()", m.average(), 0)


def check_08(m):
    expect("build_profile('Asha', age=25, city='Pune')", m.build_profile("Asha", age=25, city="Pune"),
           {"name": "Asha", "age": 25, "city": "Pune"})


def check_09(m):
    expect("safe_divide(10, 4)", m.safe_divide(10, 4), 2.5)
    expect("safe_divide(1, 0)", m.safe_divide(1, 0), None)
    expect("safe_divide(1, 0, default=0)", m.safe_divide(1, 0, default=0), 0)
    raises("safe_divide(1, 0, 0)  (default must be keyword-only)", lambda: m.safe_divide(1, 0, 0), TypeError)


def check_10(m):
    expect("apply_twice(lambda x: x + 3, 1)", m.apply_twice(lambda x: x + 3, 1), 7)
    expect("apply_twice(str.upper, 'hi')", m.apply_twice(str.upper, "hi"), "HI")


def check_11(m):
    people = [("Asha", 30), ("Ravi", 22), ("Dev", 27)]
    expect("sort_by_age(people)", m.sort_by_age(people), [("Ravi", 22), ("Dev", 27), ("Asha", 30)])
    expect("original list unchanged", people[0], ("Asha", 30))


def check_12(m):
    expect("squares_of_evens([1, 2, 3, 4, 6])", list(m.squares_of_evens([1, 2, 3, 4, 6])), [4, 16, 36])


def check_13(m):
    triple = m.make_multiplier(3)
    expect("make_multiplier(3)(5)", triple(5), 15)
    expect("make_multiplier(10)(2)", m.make_multiplier(10)(2), 20)


def check_14(m):
    @m.shout
    def hello(name):
        return f"hello {name}"
    expect("@shout hello('asha')", hello("asha"), "HELLO ASHA")
    expect("@shout keeps __name__", hello.__name__, "hello")


def check_15(m):
    @m.count_calls
    def ping():
        return "pong"
    ping(), ping(), ping()
    expect("ping.calls after 3 calls", getattr(ping, "calls", None), 3)
    expect("ping() still returns", ping(), "pong")


def check_16(m):
    @m.repeat(3)
    def roll():
        return 6
    expect("@repeat(3) roll()", roll(), [6, 6, 6])


def check_17(m):
    expect("factorial(5)", m.factorial(5), 120)
    expect("factorial(0)", m.factorial(0), 1)


def check_18(m):
    expect("flatten([1, [2, [3, [4]]], 5])", m.flatten([1, [2, [3, [4]]], 5]), [1, 2, 3, 4, 5])


def check_19(m):
    gen = m.countdown(3)
    expect("countdown is a generator", inspect.isgenerator(gen), True)
    expect("list(countdown(3))", list(gen), [3, 2, 1])


def check_20(m):
    expect("parse_age('42')", m.parse_age("42"), 42)
    for bad in ["abc", "-1", "131", "4.5"]:
        raises(f"parse_age({bad!r})", lambda b=bad: m.parse_age(b), ValueError)


CHECKS = [(name, func) for name, func in sorted(globals().items()) if name.startswith("check_")]
NAMES = ["greet", "area_of_rectangle", "min_max", "is_even", "count_vowels", "make_counter", "average",
         "build_profile", "safe_divide", "apply_twice", "sort_by_age", "squares_of_evens", "make_multiplier",
         "shout", "count_calls", "repeat", "factorial", "flatten", "countdown", "parse_age"]

print(f"Checking {target}.py\n")
score = 0
for (check_name, check), fname in zip(CHECKS, NAMES):
    num = check_name.split("_")[1]
    try:
        check(mod)
    except Exception as e:
        print(f"  ✘ {num} {fname}: {type(e).__name__ + ': ' if not isinstance(e, AssertionError) else ''}{e}")
    else:
        score += 1
        print(f"  ✔ {num} {fname}")
print(f"\n  Score: {score} / {len(CHECKS)}")

if target == "solutions" and score != len(CHECKS):
    sys.exit(1)        # the reference solutions must always pass
