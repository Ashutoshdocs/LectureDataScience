"""Lecture 04 — Why NumPy is compact: list vs array memory."""
import sys
import numpy as np

n = 1_000
nums = list(range(n))
arr = np.arange(n)

# A list stores pointers to separate int objects
list_bytes = sys.getsizeof(nums) + sum(sys.getsizeof(x) for x in nums)
print("List of 1000 ints :", list_bytes, "bytes")

# An array stores raw numbers side by side
print("Array of 1000 ints:", arr.nbytes, "bytes")
print("Bytes per item    :", arr.itemsize)

# Choose a smaller type when the values are small
small = np.arange(n, dtype=np.int16)
print("As int16          :", small.nbytes, "bytes")

print("\n--- nbytes = size * itemsize ---")
print(arr.size, "*", arr.itemsize, "=", arr.size * arr.itemsize)

print("\n--- Bytes per item for common dtypes ---")
for dt in [np.int8, np.uint8, np.int16, np.int32, np.int64, np.float32, np.float64]:
    print(f"{np.dtype(dt).name:8} {np.dtype(dt).itemsize} byte(s)")

print("\n--- Overflow when the dtype is too small ---")
print(np.arange(126, 130, dtype=np.int8))

print("\n--- One million items ---")
big = 1_000_000
big_list = list(range(big))
big_list_mb = (sys.getsizeof(big_list) + sum(sys.getsizeof(x) for x in big_list)) / 1e6
print(f"list : {big_list_mb:5.1f} MB")
print(f"int64: {np.arange(big).nbytes / 1e6:5.1f} MB")
print(f"int32: {np.arange(big, dtype=np.int32).nbytes / 1e6:5.1f} MB")

print("\n--- A Full-HD colour photo ---")
photo = np.zeros((1080, 1920, 3), dtype=np.uint8)
print(f"uint8  : {photo.nbytes / 1e6:5.1f} MB")
print(f"float64: {photo.astype(np.float64).nbytes / 1e6:5.1f} MB")
