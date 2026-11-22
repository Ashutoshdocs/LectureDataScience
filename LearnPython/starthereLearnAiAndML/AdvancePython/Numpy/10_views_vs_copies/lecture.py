"""Lecture 10 — Views vs copies: why changing a slice can change the original."""
import numpy as np

a = np.array([1, 2, 3, 4, 5])

part = a[1:4]        # a slice is a VIEW of a
part[0] = 100
print("a    =", a)   # a changed too!

safe = a[1:4].copy() # a real, separate copy
safe[0] = -1
print("a    =", a)   # a unchanged
print("safe =", safe)

lst = [1, 2, 3, 4, 5]
lst_part = lst[1:4]  # list slices are copies
lst_part[0] = 100
print("lst  =", lst)

print("\n--- Check with np.shares_memory ---")
print("a & part:", np.shares_memory(a, part))
print("a & safe:", np.shares_memory(a, safe))

print("\n--- b = a is NOT a copy ---")
b = a
b[0] = -999
print("a =", a, "| same object?", b is a)

print("\n--- Masks and fancy indexes return copies ---")
a = np.array([1, 2, 3, 4, 5])
big = a[a > 2]
big[:] = 0
print("after changing a[a > 2] copy, a =", a)
a[a > 2] = 0         # direct assignment DOES modify a
print("after a[a > 2] = 0,           a =", a)

print("\n--- reshape is a view too ---")
a = np.arange(6)
grid = a.reshape(2, 3)
grid[0, 0] = 42
print("a =", a)
