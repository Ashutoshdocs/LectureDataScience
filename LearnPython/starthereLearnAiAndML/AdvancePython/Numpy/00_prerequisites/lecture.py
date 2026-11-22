"""Lecture 00 — Prerequisites: core Python skills used throughout the course.

No NumPy here on purpose. This file shows the plain-Python tools you need,
and at the end, the kinds of jobs that are awkward without NumPy.
"""

print("--- 1. Numbers and operators ---")
print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)

print("\n--- 2. Lists ---")
marks = [72, 85, 90, 64]
print("first:", marks[0], "last:", marks[-1], "slice:", marks[1:3], "len:", len(marks))
marks.append(99)
print("after append:", marks)
mixed = [1, "hello", 3.5, [1, 2]]          # lists can hold anything
print("mixed list:", mixed)

print("\n--- 3. Lists of lists (tables) ---")
table = [[1, 2, 3],
         [4, 5, 6]]
print("row 1, col 2:", table[1][2])
print("column 2 needs a loop:", [row[2] for row in table])

print("\n--- 4. Loops ---")
prices = [100, 250, 80]
doubled = []
for p in prices:
    doubled.append(p * 2)
print("doubled with a loop:", doubled)

print("\n--- 5. List comprehensions ---")
print("doubled:", [p * 2 for p in prices])
print("cheap  :", [p for p in prices if p < 200])

print("\n--- 6. Functions ---")
def with_tax(price, rate=0.18):
    return round(price * (1 + rate), 2)
print("with tax:", [with_tax(p) for p in prices])

print("\n--- 7. Tuples and unpacking ---")
shape = (3, 4)
rows, cols = shape
print("rows =", rows, "cols =", cols)

print("\n--- 8. Modules ---")
import math
print("math.sqrt(16) =", math.sqrt(16))
try:
    math.sqrt([4, 9, 16])                   # math works on ONE number only
except TypeError as e:
    print("math.sqrt(list) fails ->", e)

print("\n--- 9. Methods vs attributes ---")
name = "numpy"
z = 3 + 4j
print("method   name.upper() ->", name.upper())
print("attribute z.real      ->", z.real)

print("\n--- 10. What is awkward in plain Python ---")
a = [10, 20, 30]
b = [1, 2, 3]
print("a + b joins lists, it does not add:", a + b)
print("adding element-wise needs zip:     ", [x + y for x, y in zip(a, b)])
try:
    a + 5
except TypeError as e:
    print("a + 5 fails ->", e)
print("adding 5 needs a loop:             ", [x + 5 for x in a])
print("mean needs sum/len:                ", sum(a) / len(a))
print("\nNumPy turns every one of these into a single short, fast expression.")
