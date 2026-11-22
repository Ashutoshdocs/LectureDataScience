# Lecture 21 — Recap: why NumPy wins + cheat sheet

Run: `python lecture.py`

## NumPy in one table

| | Python list | NumPy array |
|---|---|---|
| **Types** | anything, mixed | one `dtype` for all |
| **Maths** | needs loops | vectorized: `arr * 2` |
| **Speed** | interpreted, item by item | compiled C, often 10–100× faster |
| **Memory** | pointers to objects | packed raw numbers |
| **Dimensions** | lists of lists | true n-D with `shape`, `axis` |
| **Slicing** | copies | views (use `.copy()`) |
| **Ecosystem** | — | pandas, Matplotlib, SciPy, scikit-learn, OpenCV, PyTorch… |
| **Best for** | small mixed collections; frequent appends | numbers, tables, images, signals |

## The three reasons, one more time

1. **One dtype** → no per-item type checks.
2. **Packed memory** → compact and cache-friendly.
3. **Compiled loops** → vectorized operations run in C.

## Cheat sheet

### Create
```python
np.array(lst)          np.zeros(n)        np.ones((r, c))     np.full(n, v)
np.arange(a, b, step)  np.linspace(a, b, n)   np.eye(n)       np.diag(v)
rng = np.random.default_rng(42);  rng.integers(lo, hi, size);  rng.random(n);  rng.normal(m, s, n)
```

### Inspect
```python
a.shape   a.ndim   a.size   a.dtype   a.itemsize   a.nbytes   a.astype(t)
```

### Select
```python
a[i]   a[-1]   a[i:j]   a[::-1]   m[r, c]   m[:, c]   m[r]   a[[0, 2]]
a[a > x]   a[(a > x) & (a < y)]   np.where(cond)[0]
```

### Compute
```python
a + b   a * 2   a ** 2   np.sqrt(a)   np.abs(a)   np.round(a, 2)   np.clip(a, lo, hi)
np.where(cond, x, y)   np.select([c1, c2], [v1, v2], default)   A @ B   np.dot(a, b)
```

### Summarise
```python
a.sum()  a.mean()  a.min()  a.max()  a.argmin()  a.argmax()  a.std()
np.median(a)  np.percentile(a, p)  np.cumsum(a)  np.diff(a)  np.unique(a, return_counts=True)
m.sum(axis=0)   # per column        m.sum(axis=1)   # per row
```

### Reshape & combine
```python
a.reshape(r, c)   a.reshape(-1, 1)   m.T   m.flatten()
np.sort(a)   np.argsort(a)   np.concatenate([a, b])   np.vstack([a, b])   np.hstack([a, b])
a.copy()   a.tolist()
```

## Top 10 beginner mistakes

| Mistake | Fix |
|---------|-----|
| `np.zeros(2, 3)` | `np.zeros((2, 3))` |
| `a.shape()` | `a.shape` |
| `(a > 1) and (a < 5)` | `(a > 1) & (a < 5)` |
| `a > 1 & a < 5` | brackets around each condition |
| `if a == b:` | `np.array_equal(a, b)` |
| `a * b` for matrix product | `a @ b` |
| Changing a slice and losing the original | `.copy()` |
| Overflow with small ints | use a larger dtype |
| Python loop over an array | vectorize it |
| `np.append` inside a loop | collect in a list, convert once |

## When **not** to use NumPy

For a handful of mixed items (names, settings), or when you constantly append one item at a time, a list is simpler. NumPy shines when you have **many numbers** and do the **same thing to all of them**.

## Where to go next

- **pandas** — labelled tables (DataFrames) built on NumPy
- **Matplotlib** — plot your arrays
- **SciPy** — statistics, optimisation, signal processing
- **scikit-learn** — machine learning on arrays
- Official docs: https://numpy.org/doc/stable/

## Final exercises

1. Rewrite one of your old list-and-loop programs using NumPy.
2. Explore `help(np.where)` or any function you met.
