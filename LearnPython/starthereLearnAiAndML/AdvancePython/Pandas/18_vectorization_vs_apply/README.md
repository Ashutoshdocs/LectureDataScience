# Lecture 18: Vectorization vs loops vs `apply`, and why it matters

Run: `python lecture.py` (it builds a 1,000,000-row table and races the methods)

## The same idea as NumPy

pandas columns are arrays, so the NumPy lesson applies directly: **one operation on a whole column runs in compiled code**. A loop or `apply` calls a Python function once per row, which is the slow path.

## The speed ladder (fastest → slowest)

| Rank | Method | Example | Typical speed |
|------|--------|---------|---------------|
| 1 | **Vectorized column maths** | `df["a"] * df["b"]` | ⚡ fastest |
| 2 | **Built-in vectorized helpers** | `np.where`, `np.select`, `.str.*`, `.dt.*`, `.map(dict)`, `pd.cut` | ⚡ fast |
| 3 | `Series.apply(func)` | `df["a"].apply(lambda x: x * 2)` | 🐢 10–100× slower |
| 4 | `df.apply(func, axis=1)` | row by row | 🐌 very slow |
| 5 | `for i, row in df.iterrows()` | manual loop | 🐌🐌 slowest |

`lecture.py` prints real timings on your machine. In testing, vectorized maths beat `apply(axis=1)` by ~1,500× and `iterrows` by ~7,000× on a million rows.

## Why `apply` and loops are slow

1. A Python function call **per row** (interpreter overhead).
2. Each value is boxed into a Python object, so the compiled fast path is lost.
3. `iterrows` also builds a new **Series for every row**.

## Translating common `apply` calls

| Slow | Fast |
|------|------|
| `df.apply(lambda r: r["a"] * r["b"], axis=1)` | `df["a"] * df["b"]` |
| `df["x"].apply(lambda v: "hi" if v > 5 else "lo")` | `np.where(df["x"] > 5, "hi", "lo")` |
| several `if/elif` in a function | `np.select([c1, c2], [v1, v2], default)` |
| `df["s"].apply(lambda s: s.upper())` | `df["s"].str.upper()` |
| `df["d"].apply(lambda d: d.year)` | `df["d"].dt.year` |
| `df["code"].apply(lambda c: lookup[c])` | `df["code"].map(lookup)` |
| loop to bucket numbers | `pd.cut(df["x"], bins=...)` |
| loop with a running total | `df["x"].cumsum()` |
| loop comparing to previous row | `df["x"].diff()` / `.shift()` |
| loop per group | `groupby(...).transform(...)` |

## When `apply` is fine

- Small data (thousands of rows), where clarity matters more than milliseconds
- Truly custom logic with no vectorized equivalent (calling an external library per value)
- `groupby(...).apply(func)` for complex per-group logic

## Other performance tips

- Read only the columns you need: `usecols=[...]`
- Use `category` for repeated text (Lecture 11)
- Use smaller numeric types: `float32`, `int32`
- Avoid growing a DataFrame row by row in a loop. Collect a list of dicts and build the DataFrame once.
- Huge files: `pd.read_csv(..., chunksize=100_000)` to process in pieces, or the Parquet format

## Exercises

1. Rewrite a row-wise `apply` that computes `units * unit_price * 1.18`.
2. Rewrite a three-tier `if/elif/else` function with `np.select`.
3. Time `df["s"].apply(str.upper)` against `df["s"].str.upper()`.

<details><summary>Solutions</summary>

```python
df["units"] * df["unit_price"] * 1.18
np.select([df["rev"] >= 100_000, df["rev"] >= 20_000], ["gold", "silver"], default="bronze")
# Surprise: for text they're often about the same speed (see the note below).
```
</details>

## A note on text columns

Numbers are where vectorization gives huge wins (hundreds to thousands of times faster). Text is different: strings are variable-length, so `.str` methods still do per-string work underneath. In `lecture.py`, `.str.upper()` and `apply(str.upper)` are about the same speed. Prefer `.str` anyway, because it **handles missing values safely** (`None.upper()` would crash) and reads more clearly.

**Next →** [Lecture 19: Plotting](../19_plotting/)
