# Lecture 11 — Element-wise maths & universal functions (ufuncs)

Run: `python lecture.py`

## 1. Element-wise arithmetic

Two arrays of the **same shape** combine element by element: first with first, second with second…

```
  [10, 20, 30, 40]
+ [ 1,  2,  3,  4]
= [11, 22, 33, 44]
```

Every Python operator works: `+  -  *  /  //  %  **`. As in plain Python, `/` always gives floats.

> ⚠️ `a * b` is **not** matrix multiplication — it multiplies matching elements. Matrix multiplication is `@` (Lecture 13).

> ⚠️ Shapes must be compatible: `(4,) + (3,)` → `ValueError: operands could not be broadcast together`.

## 2. Universal functions (ufuncs)

A **ufunc** is a NumPy maths function that runs on every element at once — vectorization packaged as a function.

| Function | Does |
|----------|------|
| `np.sqrt`, `np.square` | square root, square |
| `np.abs` | remove the sign |
| `np.round`, `np.floor`, `np.ceil` | nearest, round down, round up |
| `np.exp`, `np.log`, `np.log10`, `np.log2` | exponentials & logs |
| `np.sin`, `np.cos`, `np.tan`, `np.radians`, `np.degrees` | trigonometry |
| `np.maximum(a, b)`, `np.minimum(a, b)` | element-wise max/min of two arrays |
| `np.clip(a, lo, hi)` | squash values into a range |

> `math.sqrt()` takes **one** number. `np.sqrt()` takes a whole array — that's the difference.

> ⚠️ `np.round` rounds halves to the nearest **even** number ("banker's rounding"): `2.5 → 2`, `3.5 → 4`, `-0.5 → -0`. This avoids bias in large datasets.

## 3. `np.where` — vectorized if/else

```python
np.where(condition, value_if_true, value_if_false)
```

## 4. Special values: `nan` and `inf`

```python
np.array([1, 0]) / 0      # [inf nan] + a RuntimeWarning
np.sqrt(-1)               # nan + a RuntimeWarning
```

- `np.nan` = "Not a Number" (a missing/invalid value).
- `np.isnan(a)` finds them; `np.nanmean(a)` ignores them.
- `nan == nan` is `False` — always use `np.isnan`.

## Exercises

1. What happens with `a + np.array([1, 2, 3])`? Read the error.
2. Percentage change: `(a - b) / b * 100`.
3. `np.log10([1, 10, 100, 1000])`.
4. Compare `np.round(2.5)` with `np.round(3.5)`.

<details><summary>Solutions</summary>

1. `ValueError: operands could not be broadcast together with shapes (4,) (3,)`
2. `[900. 900. 900. 900.]`
3. `[0. 1. 2. 3.]`
4. `2.0` and `4.0` — round-half-to-even.
</details>

**Next →** [Lecture 12: Broadcasting](../12_broadcasting/)
