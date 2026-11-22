"""Lecture 06 — Creating arrays: array, zeros/ones/full, arange/linspace, eye/diag."""
import numpy as np

print("=== 1. From a list ===")
a = np.array([10, 20, 30, 40])
b = np.array([1.5, 2.5, 3.5])
c = np.array([1, 2.5, 3])          # mixed int and float
d = np.array([True, False, True])
e = np.array([1, 2, "3"])          # one string -> all text
print(a, a.dtype)
print(b, b.dtype)
print(c, c.dtype)
print(d, d.dtype)
print(e, e.dtype)
print(np.array([1, 2, 3], dtype=float))
print(np.array((7, 8, 9)))         # tuples work too

print("\n=== 2. zeros, ones, full ===")
print(np.zeros(5))
print(np.ones(4))
print(np.full(5, 7))
print(np.zeros((2, 3)))            # 2 rows, 3 columns
print(np.ones((2, 2), dtype=int))
print(np.full((2, 4), 9.5))
print(np.zeros(4, dtype=bool))
print(np.zeros_like(a))

scores = np.zeros(3)               # start empty, fill in later
scores[0] = 88
scores[2] = 91
print("scores:", scores)

try:
    np.zeros(2, 3)
except TypeError as err:
    print("np.zeros(2, 3) fails ->", err)

print("\n=== 3. arange vs linspace ===")
print(np.arange(5))                # 0 up to 5 (5 excluded)
print(np.arange(1, 11))            # 1 to 10
print(np.arange(0, 20, 5))         # step of 5
print(np.arange(0, 1, 0.25))       # float steps work too
print(np.arange(10, 0, -3))        # counting down
print(np.linspace(0, 10, 5))       # 5 values, 10 included
print(np.linspace(0, 1, 3))
print("odd 1..19:", np.arange(1, 20, 2))

print("\n=== 4. Special matrices ===")
print(np.eye(3))                   # identity matrix
print(np.diag([4, 5, 6]))          # values on the diagonal
print(np.tri(3, dtype=int))        # lower triangle
