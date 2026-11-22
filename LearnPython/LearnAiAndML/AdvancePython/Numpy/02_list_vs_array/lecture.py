"""Lecture 02 — List vs array: the same operator, a different meaning."""
import numpy as np

prices = [100, 250, 80]
arr = np.array(prices)

print(prices * 2)      # list: repeats the list
print(arr * 2)         # array: doubles every value

print(prices + [5])    # list: joins two lists
print(arr + 5)         # array: adds 5 to every value

# To do maths with a list you need a loop:
print([p * 2 for p in prices])

print("\n--- Comparisons ---")
print("arr > 100 :", arr > 100)
try:
    prices > 100
except TypeError as e:
    print("prices > 100 fails ->", e)

print("\n--- Two arrays: matching elements combine ---")
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print("a + b =", a + b)
print("a * b =", a * b)
print("b / a =", b / a)
print("list a + list b joins instead:", [1, 2, 3] + [10, 20, 30])

print("\n--- Converting back and forth ---")
back = arr.tolist()
print(back, type(back), type(back[0]))
