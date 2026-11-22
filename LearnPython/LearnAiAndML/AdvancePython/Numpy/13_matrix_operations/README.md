# Lecture 13 — Matrix operations: `@` vs `*`, dot, transpose, any/all

Run: `python lecture.py`

## Two kinds of multiplication

| `A * B` | `A @ B` |
|---------|---------|
| element-wise: multiply matching positions | matrix product: row × column, then add |
| `[[1×5, 2×6], [3×7, 4×8]]` | top-left = 1×5 + 2×7 = 19 |
| shapes must match (or broadcast) | inner sizes must match: `(m, n) @ (n, p) → (m, p)` |

```
A = [[1, 2],      B = [[5, 6],
     [3, 4]]           [7, 8]]

A @ B = [[1*5 + 2*7,  1*6 + 2*8],   = [[19, 22],
         [3*5 + 4*7,  3*6 + 4*8]]      [43, 50]]
```

## Dot product

`np.dot(a, b)` of two 1D arrays = multiply matching values and add them up:

```python
np.dot([1, 2, 3], [4, 5, 6])    # 1*4 + 2*5 + 3*6 = 32
```

Real use — a total bill: `np.dot(quantities, prices)`.

## Transpose and identity

- `A.T` swaps rows and columns.
- `np.eye(n)` is the identity matrix: `A @ I == A`.
- `np.linalg.inv(A)` gives the inverse: `A @ inv(A) ≈ I`.
- `np.linalg.solve(A, b)` solves the system `A x = b`.

## Comparing whole arrays

| Call | Answers |
|------|---------|
| `mask.any()` | is **at least one** True? |
| `mask.all()` | are **all** True? |
| `np.count_nonzero(mask)` | how many are True? |
| `np.where(mask)[0]` | **which positions** are True? |
| `np.array_equal(a, b)` | same shape **and** same values? |
| `np.allclose(a, b)` | equal within floating-point tolerance? |

> ⚠️ `if a == b:` fails for arrays — `a == b` is many answers, not one. Use `np.array_equal(a, b)` or `(a == b).all()`.

> Matrix maths is the core of machine learning and graphics. NumPy runs it with highly optimised libraries (BLAS/LAPACK), so it is extremely fast.

## Exercises

1. Is `A @ B` the same as `B @ A`? Check.
2. Solve: `2x + y = 5`, `x + 3y = 10`.
3. Total bill for quantities `[2, 1, 5]` and prices `[40, 250, 10]`.

<details><summary>Solutions</summary>

1. No — matrix multiplication isn't commutative. `B @ A = [[23 34] [31 46]]`.
2. `np.linalg.solve([[2, 1], [1, 3]], [5, 10])` → `[1. 3.]`
3. `np.dot([2, 1, 5], [40, 250, 10])` → `380`
</details>

**Next →** [Lecture 14: Statistics](../14_statistics/)
