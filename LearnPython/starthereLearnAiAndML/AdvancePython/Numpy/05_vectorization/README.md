# Lecture 05 — Vectorization: say *what*, not *how*

Run: `python lecture.py`

## Definition

> **Vectorization** = expressing an operation on a **whole array at once** instead of writing a loop over its elements.

The loop still exists — but it runs inside NumPy's compiled code, not in your Python code.

## Why it is needed

| Problem with loops | What vectorization gives you |
|--------------------|-----------------------------|
| Slow: the Python interpreter runs every iteration | Fast: one call to compiled C (Lecture 03) |
| Long: empty list, loop, compute, append | Short: one expression |
| Error-prone: off-by-one, wrong index, forgot to append | Nothing to get wrong — no indexes |
| Hard to read: you see the mechanics, not the maths | Reads like the formula in a textbook |

## Example: add 18% tax to every price

```python
prices = [120, 560, 999, 45]

# Loop — tells Python HOW, step by step
with_tax = []
for p in prices:
    with_tax.append(round(p * 1.18, 2))

# Vectorized — says WHAT you want
arr = np.array(prices)
np.round(arr * 1.18, 2)
```

## Step-through: what the loop actually does

| Step | Line | `p` | `with_tax` |
|------|------|-----|------------|
| 1 | `with_tax = []` | – | `[]` |
| 2 | loop | 120 | `[141.6]` |
| 3 | loop | 560 | `[141.6, 660.8]` |
| 4 | loop | 999 | `[141.6, 660.8, 1178.82]` |
| 5 | loop | 45 | `[141.6, 660.8, 1178.82, 53.1]` |

The NumPy version finishes in **a single step** — no visible loop.

## `np.where` — an if/else for every element

Loops with an `if` inside are also vectorizable:

```python
np.where(condition, value_if_true, value_if_false)

np.where(arr > 500, arr * 0.9, arr)   # 10% off only prices over 500
```

## How to vectorize any loop — a recipe

1. Turn the input list into an array.
2. Write the body of the loop as if `p` *were* the whole array: `p * 1.18` → `arr * 1.18`.
3. Replace `if/else` with `np.where` (or a boolean mask, Lecture 09).
4. Replace `sum += ...` accumulations with `.sum()`, `.mean()`, etc.
5. Replace `math.sqrt`, `math.sin` … with `np.sqrt`, `np.sin` …

| Loop pattern | Vectorized |
|--------------|-----------|
| `[x * 2 for x in a]` | `a * 2` |
| `[x + y for x, y in zip(a, b)]` | `a + b` |
| `[math.sqrt(x) for x in a]` | `np.sqrt(a)` |
| `[x for x in a if x > 0]` | `a[a > 0]` |
| `[x if x > 0 else 0 for x in a]` | `np.where(a > 0, a, 0)` |
| `total = 0; for x in a: total += x` | `a.sum()` |
| `count = 0; for x in a: if x > 5: count += 1` | `(a > 5).sum()` |

## Expected output (first part)

```
[141.6, 660.8, 1178.82, 53.1]
[ 141.6   660.8  1178.82   53.1 ]
[120.  504.  899.1  45. ]
```

## Exercises

1. Label prices: `np.where(arr > 500, "costly", "cheap")`.
2. Add a 5% delivery charge only to prices under 100.
3. Vectorize: `result = [x**2 - 3*x + 2 for x in range(10)]`.

<details><summary>Solutions</summary>

```python
np.where(arr > 500, "costly", "cheap")      # ['cheap' 'costly' 'costly' 'cheap']
np.where(arr < 100, arr * 1.05, arr)        # [120. 560. 999. 47.25]
x = np.arange(10); x**2 - 3*x + 2           # [ 2  0  0  2  6 12 20 30 42 56]
```
</details>

**Next →** [Lecture 06: Creating arrays](../06_creating_arrays/)
