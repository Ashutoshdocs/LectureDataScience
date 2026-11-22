"""Lecture 13 — Matrix operations and whole-array comparisons."""
import numpy as np

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

print("A * B (element-wise):")
print(A * B)
print("A @ B (matrix product):")
print(A @ B)
print("B @ A (order matters!):")
print(B @ A)

I = np.eye(2, dtype=int)
print("A @ I == A ?", np.array_equal(A @ I, A))   # identity leaves A unchanged
print("dot:", np.dot([1, 2, 3], [4, 5, 6]))       # 1*4 + 2*5 + 3*6

print("\n--- Shapes in matrix multiplication ---")
M = np.ones((2, 3))
N = np.ones((3, 4))
print(M.shape, "@", N.shape, "->", (M @ N).shape)
try:
    M @ M
except ValueError as e:
    print("(2,3) @ (2,3) fails ->", str(e)[:70], "...")

print("\n--- Transpose, inverse, solve ---")
print("A.T =\n", A.T)
A_inv = np.linalg.inv(A)
print("inv(A) =\n", A_inv)
print("A @ inv(A) close to I ?", np.allclose(A @ A_inv, np.eye(2)))
print("solve 2x+y=5, x+3y=10 ->", np.linalg.solve([[2, 1], [1, 3]], [5, 10]))

print("\n--- Total bill with a dot product ---")
qty = np.array([2, 1, 5])
price = np.array([40, 250, 10])
print("bill =", np.dot(qty, price), "=", qty @ price)

print("\n--- Comparisons, any() and all() ---")
temps = np.array([31, 35, 29, 40, 38, 33, 27])
hot = temps > 35
print(hot)
print("Any day over 35?", hot.any())
print("All days over 25?", (temps > 25).all())
print("Hot days:", np.count_nonzero(hot))
print("Which days:", np.where(hot)[0])

a = np.array([1, 2, 3])
print(a == np.array([1, 5, 3]))
print(np.array_equal(a, [1, 2, 3]))
print("0.1 + 0.2 == 0.3 ?", 0.1 + 0.2 == 0.3, "| allclose:", np.allclose(0.1 + 0.2, 0.3))
