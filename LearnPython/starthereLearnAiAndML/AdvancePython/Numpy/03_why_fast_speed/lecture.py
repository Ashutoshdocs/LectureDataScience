"""Lecture 03 — Why NumPy is fast: a speed race between a list and an array."""
import time
import timeit
import numpy as np

n = 1_000_000
nums = list(range(n))           # one million ints in a list
arr = np.arange(n)              # one million ints in an array

t = time.perf_counter()
squares = [x * x for x in nums] # Python: one item at a time
py_time = time.perf_counter() - t

t = time.perf_counter()
squares_np = arr * arr          # NumPy: all at once
np_time = time.perf_counter() - t

print(f"Python list : {py_time * 1000:7.1f} ms")
print(f"NumPy array : {np_time * 1000:7.1f} ms")
print(f"NumPy was about {py_time / np_time:.0f}x faster")

print("\n--- Same answer? ---")
print(squares[:5], squares_np[:5], squares[-1] == squares_np[-1])

print("\n--- A fairer test with timeit (best of 5 runs) ---")
py_best = min(timeit.repeat(lambda: [x * x for x in nums], number=1, repeat=5))
np_best = min(timeit.repeat(lambda: arr * arr, number=1, repeat=5))
print(f"square  : list {py_best*1000:6.1f} ms | NumPy {np_best*1000:6.1f} ms | {py_best/np_best:.0f}x")

py_best = min(timeit.repeat(lambda: sum(nums), number=1, repeat=5))
np_best = min(timeit.repeat(lambda: arr.sum(), number=1, repeat=5))
print(f"sum     : list {py_best*1000:6.1f} ms | NumPy {np_best*1000:6.1f} ms | {py_best/np_best:.0f}x")

print("\n--- Trap: a Python loop over an ARRAY is slow ---")
loop_arr = min(timeit.repeat(lambda: [x * x for x in arr], number=1, repeat=3))
print(f"loop over array: {loop_arr*1000:6.1f} ms  <- slower than the list loop!")
print("The speed comes from vectorized operations, not from the array type itself.")
