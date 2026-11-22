"""Lecture 07 — Shape & dtype: dimensions, attributes, astype, overflow."""
import numpy as np

print("=== 1D, 2D, 3D ===")
v = np.array([1, 2, 3, 4, 5])
m = np.array([[1, 2, 3],
              [4, 5, 6]])
t = np.array([[[1, 2], [3, 4]],
              [[5, 6], [7, 8]]])

print(v, "ndim:", v.ndim, "shape:", v.shape)
print(m)
print("ndim:", m.ndim, "shape:", m.shape)
print(t)
print("ndim:", t.ndim, "shape:", t.shape)

try:
    np.array([[1, 2], [3]])
except ValueError as e:
    print("ragged rows fail ->", str(e).split(".")[0])

print("\n=== Attributes ===")
print("ndim    :", m.ndim)       # number of dimensions
print("shape   :", m.shape)      # (rows, columns)
print("size    :", m.size)       # total elements
print("dtype   :", m.dtype)      # type of each element
print("itemsize:", m.itemsize)   # bytes per element
print("nbytes  :", m.nbytes)     # total bytes
print("len     :", len(m))       # length of first axis = rows

rows, cols = m.shape             # shape is a tuple - unpack it
print(f"{rows} rows x {cols} cols")

try:
    m.shape()
except TypeError as e:
    print("m.shape() fails ->", e)

z = np.zeros((3, 4, 5))
print("zeros((3,4,5)):", z.ndim, z.shape, z.size, z.dtype, z.nbytes)

print("\n=== astype: converting types ===")
nums = np.array([1.7, 2.2, -3.9])
print(nums.astype(int))            # cut toward zero
print(nums.round().astype(int))    # round first

words = np.array(["10", "20", "30"])
print(words.dtype)
print(words.astype(int) + 1)       # text -> numbers
print(np.array(["1.5", "2"]).astype(float))

flags = np.array([0, 3, 0, 5]).astype(bool)
print(flags)
print(flags.astype(int))

print("\n=== Overflow ===")
tiny = np.array([126, 127], dtype=np.int8)
print(tiny + 1)                    # 127 + 1 wraps to -128!
print(np.array([126, 127], dtype=np.int16) + 1)
print("int8 range :", np.iinfo(np.int8).min, "to", np.iinfo(np.int8).max)
print("int64 range:", np.iinfo(np.int64).min, "to", np.iinfo(np.int64).max)
