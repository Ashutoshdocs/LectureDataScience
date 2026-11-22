# Lecture 16 — Reshape, sort, join & unique

Run: `python lecture.py`

## 1. Reshape, flatten, transpose

`.reshape()` changes the shape **without changing the data**. Values fill row by row.

| Tool | Does |
|------|------|
| `a.reshape(r, c)` | new shape, same values |
| `-1` in a shape | "calculate this size for me" |
| `m.T` | transpose: row 0 becomes column 0 |
| `m.flatten()` | any shape → 1D **copy** |
| `m.ravel()` | any shape → 1D (a **view** when possible) |

> ⚠️ **The total must match.** 12 elements can be 3×4, 4×3, 2×6, 6×2, 12×1 … but **not** 5×2 = 10 → `ValueError: cannot reshape array of size 12 into shape (5,2)`.

## 2. Sorting

| `np.sort(a)` | `a.sort()` |
|---|---|
| returns a **new** sorted array | sorts **in place** |
| original unchanged | returns `None` |

Both sort ascending. For descending: `np.sort(a)[::-1]`.

### `argsort` — sort one array by another

`np.argsort(a)` returns the **positions** that would sort `a`. Use them to reorder a *related* array:

```python
order = np.argsort(scores)[::-1]   # best first
names[order]                       # names ranked by score
```

## 3. Joining arrays

| Function | Result for two `(3,)` arrays |
|----------|------------------------------|
| `np.concatenate([a, b])` | `(6,)` — end to end |
| `np.vstack([a, b])` | `(2, 3)` — **v**ertical: each becomes a row |
| `np.hstack([a, b])` | `(6,)` — **h**orizontal: side by side |
| `np.column_stack([a, b])` | `(3, 2)` — each becomes a column |

Pass the arrays in a **list**. For 2D: `axis=0` adds rows, `axis=1` adds columns — the other dimension must match.

> Remember: `+` on arrays **adds values**. To **join** arrays, use these functions.

> ⚠️ Joining in a loop (`arr = np.append(arr, x)` repeatedly) is slow — each call copies the whole array. Collect into a list, then convert once.

## 4. Unique values and counting

```python
kinds, counts = np.unique(votes, return_counts=True)
kinds[counts.argmax()]     # most common
np.bincount([3, 6, 1, 6])  # counts of 0, 1, 2, ... for small non-negative ints
```

## Exercises

1. Fix the error by changing to `reshape(6, 2)`.
2. Try `a.reshape(2, 3, 2)` — a 3D array.
3. Print the top 3 names only.
4. Add a column: `np.hstack([table, np.array([[0], [0]])])`.
5. Find the least popular drink.

<details><summary>Solutions</summary>

```python
a.reshape(6, 2)
a.reshape(2, 3, 2)
names[order][:3]                      # ['Ravi' 'John' 'Asha']
np.hstack([table, [[0], [0]]])
kinds[counts.argmin()]                # 'juice'
```
</details>

**Next →** [Lecture 17: Random numbers](../17_random_numbers/)
