"""Lecture 11: lambda: syntax, good uses, limits, the late-binding trap, alternatives."""
import operator

print("=== 1. Syntax ===")
square = lambda x: x * x                     # noqa: E731 (shown for learning; prefer def)
add = lambda a, b: a + b                     # noqa: E731
greet = lambda name="you": f"Hi {name}"      # noqa: E731
print("  square(5) =", square(5), "| add(2, 3) =", add(2, 3), "|", greet(), "|", greet("Asha"))
print("  its name is:", square.__name__)

print("\n=== 2. Where lambdas shine: key= / map / filter ===")
students = [("Asha", 88), ("Ravi", 74), ("Dev", 91), ("Meena", 74)]
print("  sorted by marks           :", sorted(students, key=lambda s: s[1]))
print("  by marks desc, then name  :", sorted(students, key=lambda s: (-s[1], s[0])))
print("  top student               :", max(students, key=lambda s: s[1]))
words = ["kiwi", "fig", "banana", "apple", "date"]
print("  by length, then alphabet  :", sorted(words, key=lambda w: (len(w), w)))
print("  by last letter            :", sorted(words, key=lambda w: w[-1]))
nums = [1, 2, 3, 4, 5, 6]
print("  evens (filter)            :", list(filter(lambda n: n % 2 == 0, nums)))
print("  F from C (map)            :", list(map(lambda c: c * 9 / 5 + 32, [0, 37, 100])))
people = [{"name": "Ravi", "age": 30}, {"name": "Asha", "age": 25}, {"name": "Dev", "age": 25}]
print("  people by age, then name  :", [p["name"] for p in sorted(people, key=lambda p: (p["age"], p["name"]))])

print("\n=== 3. Conditional expression inside a lambda ===")
label = lambda m: "pass" if m >= 40 else "fail"   # noqa: E731
print("  labels:", [label(m) for m in [35, 40, 90]])

print("\n=== 4. Limits: no statements allowed ===")
for src in ["lambda x: return x", "lambda x: y = x", "lambda x: if x: 1"]:
    try:
        compile(src, "<test>", "eval")
    except SyntaxError as e:
        print(f"  {src!r:<24} -> SyntaxError: {e.msg}")

print("\n=== 5. Tracebacks: <lambda> vs a real name ===")
bad_lambda = lambda x: 1 / x                 # noqa: E731


def bad_def(x):
    return 1 / x


for f in (bad_lambda, bad_def):
    try:
        f(0)
    except ZeroDivisionError as e:
        tb = e.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        print(f"  error raised inside: {tb.tb_frame.f_code.co_name}")

print("\n=== 6. The late-binding trap ===")
funcs = [lambda: i for i in range(3)]
print("  [lambda: i ...]     ->", [f() for f in funcs], "<- all see the final i")
funcs = [lambda i=i: i for i in range(3)]
print("  [lambda i=i: i ...] ->", [f() for f in funcs])

print("\n=== 7. Often-clearer alternatives ===")
print("  comprehension instead of map   :", [x * 2 for x in nums])
print("  comprehension instead of filter:", [x for x in nums if x > 3])
print("  operator.itemgetter(1)         :", sorted(students, key=operator.itemgetter(1))[:2])
print("  operator.itemgetter('age')     :", [p["name"] for p in sorted(people, key=operator.itemgetter("age"))])
