"""Lecture 01 — What is NumPy? Your first array."""
import numpy as np

print("NumPy version:", np.__version__)

marks = [72, 85, 90, 64]      # a normal Python list
arr = np.array(marks)         # the same data as a NumPy array

print(marks)                  # printed WITH commas
print(arr)                    # printed WITHOUT commas
print(type(marks))
print(type(arr))
print(arr.dtype)              # the single type shared by every element

print("\n--- The three basic attributes ---")
print("dtype:", arr.dtype)
print("shape:", arr.shape)    # (4,) -> 4 elements in 1 dimension
print("ndim :", arr.ndim)

print("\n--- Familiar built-ins still work ---")
print("len :", len(arr))
print("sum :", arr.sum())
print("max :", arr.max())

print("\n--- One type for all elements ---")
print(np.array([1.5, 2, 3]), np.array([1.5, 2, 3]).dtype)   # ints become floats
print(np.array([1, 2, "3"]), np.array([1, 2, "3"]).dtype)   # everything becomes text
