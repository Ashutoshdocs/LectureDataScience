# Lecture 08 — Indexing & slicing

Run: `python lecture.py`

## 1. Index: one element

Positions start at **0**; negative positions count from the end.

```
value:      10   20   30   40   50
index:       0    1    2    3    4
negative:   -5   -4   -3   -2   -1
```

```python
a[0]    # 10
a[-1]   # 50
a[1] = 99      # arrays are mutable
```

> ⚠️ The array **keeps its dtype**. `a[0] = 7.9` in an integer array stores `7` — silently.

> ℹ️ In the interactive shell NumPy 2 shows `a[0]` as `np.int64(10)`. It's just the number 10 stored as a NumPy integer; `print()` shows `10`.

## 2. Slicing: `[start:stop:step]`

Like `range()`, **stop is excluded**. Leave a part empty to mean "from the start" / "to the end".

| Slice | Means |
|-------|-------|
| `a[1:4]` | index 1, 2, 3 |
| `a[:3]` | first 3 |
| `a[-3:]` | last 3 |
| `a[::2]` | every 2nd element |
| `a[::-1]` | reversed |

NumPy extra: assign **one value to a whole slice**: `a[:2] = 0`. (Lists can't do this.)

## 3. 2D indexing: `m[row, column]`

```
m = [[ 1,  2,  3,  4],     row 0
     [ 5,  6,  7,  8],     row 1
     [ 9, 10, 11, 12]]     row 2
       c0  c1  c2  c3
```

| Code | Selects |
|------|---------|
| `m[1, 2]` | one element → 7 |
| `m[0]` | whole row 0 |
| `m[:, 1]` | whole column 1 (`:` = "all rows") |
| `m[-1, -1]` | bottom-right → 12 |
| `m[:2, 1:3]` | sub-block: rows 0–1, columns 1–2 |
| `m[::2, ::3]` | the four corners |

> With lists of lists you'd write `m[1][2]`, and a column needs a loop. NumPy's `m[:, 1]` grabs it directly.

## 4. Fancy indexing: a list of positions

```python
a = np.array([10, 20, 30, 40, 50])
a[[0, 2, 4]]        # [10 30 50]
a[[4, 0]]           # [50 10] — any order, repeats allowed
```

## Exercises

1. What does `a[5]` do on a 5-element array? Read the `IndexError`.
2. Get the middle three elements of `np.arange(10, 100, 10)`.
3. Set every second element to `-1`.
4. Select the last column of `m`.

<details><summary>Solutions</summary>

1. `IndexError: index 5 is out of bounds for axis 0 with size 5`
2. `a[3:6]` → `[40 50 60]`
3. `a[::2] = -1`
4. `m[:, -1]` → `[ 4  8 12]`
</details>

**Next →** [Lecture 09: Boolean masks](../09_boolean_masks/)
