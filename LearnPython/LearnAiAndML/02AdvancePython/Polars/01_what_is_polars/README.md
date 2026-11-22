# Lecture 01: What is Polars, and why use it?

Run: `python lecture.py`

## Definition

**Polars** is a fast DataFrame library for working with tables of data. It's written in **Rust**, uses the **Apache Arrow** columnar memory format, runs on **all your CPU cores**, and has a **query optimiser** that rewrites your code to do less work.

You use it from Python (`import polars as pl`), but the heavy lifting happens in compiled Rust.

## Where it fits

```
 Python lists/dicts → NumPy (fast arrays) → pandas (labelled tables, 2008) → Polars (fast tables, 2020)
```

pandas and Polars solve the same problems: load, clean, filter, group, join, reshape. Polars was designed later, with lessons learned and modern hardware in mind.

## Why is Polars fast?

| Reason | What it means |
|--------|---------------|
| **Rust core** | Compiled, memory-safe code with no Python interpreter in the hot loop |
| **Multi-threaded** | Work is split across all CPU cores automatically. pandas mostly uses one |
| **Apache Arrow memory** | Columnar, cache-friendly layout, the same as many modern data tools |
| **Expressions** | You describe *what* to compute, so Polars can plan *how* (and run expressions in parallel) |
| **Lazy evaluation + optimiser** | Builds a query plan, then skips unneeded columns and rows *before* reading them |
| **Streaming** | Can process data larger than RAM in chunks |

## Polars vs pandas at a glance

| | pandas | **Polars** |
|---|---|---|
| Written in | Python + C (NumPy) | Rust |
| CPU cores used | mostly 1 | all |
| Row index | yes (`.loc`, `set_index`) | **no index**, rows are just positions |
| Style | many ways to do one thing | one consistent expression API |
| Missing values | `NaN` / `None` / `NaT` / `<NA>` | one `null` for every type |
| Lazy queries | no | yes (`scan_csv`, `.lazy()`) |
| Larger-than-memory data | hard | streaming engine |
| Speed | good | often 5–30× faster on big data |
| Ecosystem | huge, everything accepts it | growing; converts to pandas in one call |
| Best for | small/medium data, wide library support | medium/large data, speed, clean pipelines |

> Polars isn't "pandas but faster". The **API is different**. No index, no `.loc`, and expressions instead of `apply`. Lecture 23 has a full pandas → Polars translation table.

## The two modes

```python
df = pl.read_csv("sales.csv")       # EAGER: runs now, returns a DataFrame
lf = pl.scan_csv("sales.csv")       # LAZY: returns a plan (LazyFrame); nothing is read yet
result = lf.filter(...).group_by(...).agg(...).collect()   # optimise + run
```

You'll use eager mode while learning (Lectures 02–17) and lazy mode for real pipelines (Lecture 18 onwards).

## Your first Polars DataFrame

```python
import polars as pl
df = pl.DataFrame({"name": ["Asha", "Ravi"], "maths": [78, 92]})
print(df)
```
```
shape: (2, 2)
┌──────┬───────┐
│ name ┆ maths │
│ ---  ┆ ---   │
│ str  ┆ i64   │      ← every column shows its type
╞══════╪═══════╡
│ Asha ┆ 78    │
│ Ravi ┆ 92    │
└──────┴───────┘
```

Notice: there's **no index column** on the left, and the **dtype** is printed under each name.

## Exercises

1. Run `lecture.py`. How many CPU threads does Polars use on your machine?
2. Add a `science` column to the DataFrame in `lecture.py`.
3. Compare the printed output of a pandas and a Polars DataFrame. List three differences.

<details><summary>Solutions</summary>

1. `pl.thread_pool_size()`, usually your number of logical cores.
3. Polars shows `shape`, dtypes under the names, and no index column. pandas shows an index and no types.
</details>

**Next →** [Lecture 02: Series & DataFrame](../02_series_and_dataframe/)
