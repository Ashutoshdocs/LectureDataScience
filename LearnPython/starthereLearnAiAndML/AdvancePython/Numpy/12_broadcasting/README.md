# Lecture 12 — Broadcasting

Run: `python lecture.py`

## 1. Array with a single number

When you combine an array with a single number, NumPy "stretches" the number to match:

```
[0, 18.5, 25, 37, 100] * 9
behaves like
[0, 18.5, 25, 37, 100] * [9, 9, 9, 9, 9]
```

So a formula written for **one** value works unchanged for a million values:

```python
fahrenheit = celsius * 9 / 5 + 32      # exactly the textbook formula
```

> NumPy doesn't actually build the array of 9s — it only behaves as if it did. No extra memory.

## 2. Arrays of different shapes

Broadcasting also works between arrays of **different shapes**, if they line up.

### The rule

Compare the shapes **from the right**. Each pair of sizes must be:
- **equal**, or
- one of them is **1** (it gets stretched).

A missing dimension counts as 1.

| Shapes | OK? | Why |
|--------|-----|-----|
| `(3, 4)` and `(4,)` | ✅ | 4 = 4; the row is repeated for every row |
| `(3, 4)` and `(3, 1)` | ✅ | 1 stretches to 4; the column is repeated across |
| `(3, 1)` and `(1, 4)` | ✅ | both stretch → `(3, 4)` |
| `(3, 4)` and `(3,)` | ❌ | 3 ≠ 4 on the right |

### Picture

```
sold (3,4)          price (4,)               result (3,4)
[[10  5  0  8]      [20 50 100 10]   →     [[200 250   0  80]
 [ 3 12  7  1]   ×  [20 50 100 10]   →      [ 60 600 700  10]
 [ 6  6  6  6]]     [20 50 100 10]   →      [120 300 600  60]]
                    (row repeated)
```

This multiplies a whole sales table by a price list in one line — a job that needs two nested loops with lists.

## 3. Making a column: `reshape(-1, 1)` or `[:, np.newaxis]`

```python
bonus = np.array([1, 2, 3])
bonus[:, np.newaxis]     # shape (3, 1)
bonus.reshape(-1, 1)     # same
```

## 4. Classic uses

- **Normalising columns:** `(data - data.mean(axis=0)) / data.std(axis=0)`
- **Times tables / grids:** `np.arange(1, 11)[:, None] * np.arange(1, 11)`
- **Distances between all pairs of points**

## Exercises

1. Fix the failing line in `lecture.py` using `np.array([[1], [2], [3]])`.
2. Apply a different discount per product: `price * np.array([1, 0.9, 0.8, 1])`.
3. Build a 5 × 5 multiplication table with broadcasting.

<details><summary>Solutions</summary>

```python
sold + np.array([[1], [2], [3]])
price * np.array([1, 0.9, 0.8, 1])          # [20. 45. 80. 10.]
np.arange(1, 6)[:, None] * np.arange(1, 6)
```
</details>

**Next →** [Lecture 13: Matrix operations](../13_matrix_operations/)
