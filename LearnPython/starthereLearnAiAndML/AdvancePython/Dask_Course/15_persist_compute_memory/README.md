# Lecture 15: `persist`, `compute` & memory

Run: `python lecture.py`

## Three ways to "run" a Dask object

| Call | Returns | Data lives | Use when |
|------|---------|-----------|----------|
| `x.compute()` | pandas / NumPy / Python value | your process's memory | the **result is small** (a summary, a filtered sample) |
| `x.persist()` | a **Dask** object whose partitions are already computed | worker memory (distributed) or your RAM (local schedulers) | you'll **reuse** an intermediate result several times and it fits in (cluster) memory |
| `dask.compute(a, b, c)` | a tuple of results | n/a | several results from the **same** data: shared work is done once |

```python
clean = raw.dropna().assign(revenue=...)      # lazy
clean = clean.persist()                       # computed once, kept in memory
clean.groupby("region").revenue.sum().compute()     # fast: starts from memory
clean.groupby("product").units.mean().compute()     # fast
```

Without `persist`, **every** `.compute()` re-reads the files and redoes the cleaning.

## Measured in `lecture.py` (12 CSVs, 2.4M rows, 2 cores)

| Approach for 3 summaries | Time |
|--------------------------|------|
| 3 × `.compute()`, no persist (re-reads the CSVs 3 times) | 7.6 s |
| one `dask.compute(a, b, c)` | 2.8 s |
| `persist()` once (3.1 s) + 3 × `.compute()` (0.23 s) | 3.3 s, and **each extra question costs ~0.1 s** |

Converting 3 text columns from `string` to `category` cut their memory from 128 MB to 26 MB (~5×).

## When NOT to persist

- The data **doesn't fit** in memory, so you'd get spilling or crashes. Write to Parquet instead and read back.
- You use the result **only once**. Persisting just wastes memory.
- Before filtering. Persist the **small, cleaned** version, not the raw data.

## Memory-friendly habits

| Habit | Why |
|-------|-----|
| **Select columns and filter early** | Less data flows through every later step. In `lecture.py`, Dask's optimiser pushed a later filter into `read_parquet` automatically, so both versions took ~0.15 s. It can only do that for steps it can see in one lazy plan; a `persist()` or `compute()` in between blocks it |
| Reduce before `compute()` | `ddf.compute()` on 50 GB = crash; `ddf.groupby(...).sum().compute()` = a few KB |
| Use efficient dtypes | `category` for repeated strings, `float32` / `int32` where precision allows |
| Parquet instead of CSV | typed, compressed, column-selective |
| Delete persisted collections you no longer need (`del x`) | frees worker memory |
| Partitions around ~100 MB | big enough to be efficient, small enough to fit many in memory |
| Watch the dashboard Memory tab | orange/grey bars = spilling to disk = slow |

## Measuring memory

```python
ddf.memory_usage(deep=True).sum().compute() / 1e6          # MB if fully loaded
ddf.memory_usage_per_partition(deep=True).compute() / 1e6  # MB per partition
```

## Exercises

1. Time three different summaries on the cleaned data, with and without `persist()`.
2. Time the same three with a single `dask.compute(...)` and no persist.
3. Compare memory use of `region` as `string` vs `category`.
4. Why is `ddf.compute()` usually a bad idea at the end of a pipeline?

<details><summary>Solutions</summary>

See `lecture.py`. 4: it converts the *whole* dataset to pandas in one process, losing both the parallelism and the larger-than-memory ability.
</details>

**Next →** [Lecture 16: Performance: when Dask helps](../16_performance_when_dask_helps/)
