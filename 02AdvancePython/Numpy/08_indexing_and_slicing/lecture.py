"""Lecture 08 — Indexing & slicing in 1D and 2D."""
import numpy as np

print("=== 1. One element ===")
a = np.array([10, 20, 30, 40, 50])
print(a[0])          # first
print(a[2])          # third
print(a[-1])         # last
print(a[-2])         # second last

a[1] = 99            # change an element
print(a)

a[0] = 7.9           # a float into an int array -> 7
print(a)

try:
    a[5]
except IndexError as e:
    print("a[5] ->", e)

print("\n=== 2. Slicing ===")
a = np.arange(10, 100, 10)
print(a)
print(a[1:4])        # index 1, 2, 3
print(a[:3])         # first three
print(a[-3:])        # last three
print(a[3:6])        # middle three
print(a[::2])        # every second element
print(a[::-1])       # reversed

a[:2] = 0            # set a whole slice at once
print(a)

print("\n=== 3. 2D indexing ===")
m = np.array([[ 1,  2,  3,  4],
              [ 5,  6,  7,  8],
              [ 9, 10, 11, 12]])
print(m[1, 2])       # row 1, column 2
print(m[0])          # whole first row
print(m[:, 1])       # whole second column
print(m[:, -1])      # last column
print(m[-1, -1])     # bottom-right corner
print(m[:2, 1:3])    # top two rows, middle columns
print(m[::2, ::3])   # four corners

m[:, 0] = 0          # overwrite a whole column
print(m)

print("\n=== 4. Fancy indexing ===")
a = np.array([10, 20, 30, 40, 50])
print(a[[0, 2, 4]])
print(a[[4, 0, 0]])
