"""Lecture 12: map, filter, reduce, laziness, comprehensions, and function-friendly built-ins."""
import math
from functools import reduce

print("=== 1. map ===")
print("  map(str.upper):", list(map(str.upper, ["a", "b"])))
print("  map(int)      :", list(map(int, "3 8 1 9".split())))
print("  two iterables :", list(map(lambda a, b: a + b, [1, 2], [10, 20])))

print("\n=== 2. filter ===")
print("  filter(str.isdigit):", list(filter(str.isdigit, ["12", "ab", "7"])))
print("  filter(None, ...)  :", list(filter(None, [0, 1, "", "x", None, []])))
emails = ["asha@mail.com", "ravi.mail.com", "dev@x.in"]
print("  valid emails       :", list(filter(lambda e: "@" in e, emails)))

print("\n=== 3. reduce (with a trace) ===")


def add_verbose(acc, x):
    print(f"    acc={acc:<3} + x={x} -> {acc + x}")
    return acc + x


print("  result:", reduce(add_verbose, [1, 2, 3, 4], 0))
print("  product via reduce:", reduce(lambda a, b: a * b, [1, 2, 3, 4, 5]), "| math.prod:", math.prod([1, 2, 3, 4, 5]))
print("  longest via reduce:", reduce(lambda a, b: a if len(a) >= len(b) else b, ["fig", "banana", "kiwi"]),
      "| max(key=len):", max(["fig", "banana", "kiwi"], key=len))

print("\n=== 4. Lazy, and single-use ===")
m = map(str.upper, ["a", "b"])
print("  map object:", type(m).__name__)
print("  first list(m):", list(m), "| second list(m):", list(m))


def noisy_double(x):
    print(f"    doubling {x}")
    return x * 2


lazy = map(noisy_double, [1, 2, 3])
print("  map created: nothing computed yet")
print("  next(lazy) =", next(lazy))

print("\n=== 5. map/filter vs comprehension ===")
nums = [-2, 5, 0, 7, -1, 3]
a = list(map(lambda x: x * 2, filter(lambda x: x > 0, nums)))
b = [x * 2 for x in nums if x > 0]
print("  map+filter:", a, "| comprehension:", b, "| equal:", a == b)

print("\n=== 6. Function-friendly built-ins ===")
names = ["Asha", "Ravi", "Dev", "Meena"]
marks = [88, 35, 91, 62]
results = dict(zip(names, marks))
print("  zip -> dict:", results)
for i, (name, m) in enumerate(zip(names, marks), start=1):
    print(f"   {i}. {name:<6} {m}")
print("  sorted desc by marks:", sorted(results, key=results.get, reverse=True))
print("  top:", max(results, key=results.get), "| lowest:", min(results, key=results.get))
print("  any failed (<40)?", any(m < 40 for m in marks), "| all passed?", all(m >= 40 for m in marks))
print("  total marks:", sum(marks), "| reversed names:", list(reversed(names)))
print("  callable(print):", callable(print), "| callable(42):", callable(42))


def check(m):
    print(f"    checking {m}")
    return m < 40


print("  any() short-circuits:")
any(check(m) for m in marks)
