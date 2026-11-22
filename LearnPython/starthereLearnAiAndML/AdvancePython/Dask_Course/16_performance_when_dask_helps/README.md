# Lecture 16: Performance: when Dask helps (and when it doesn't)

Run: `python lecture.py` (about 20 seconds)

Dask's own documentation says it plainly: **if your data fits comfortably in memory, pandas is often faster.** This lecture measures where that line is on your machine.

## What `lecture.py` measures

| Test | pandas | Dask |
|------|--------|------|
| Tiny data (240 rows) groupby | in memory | `from_pandas` + compute |
| 2.4M rows **already in memory** groupby | ✅ | `from_pandas` |
| 2.4M rows **from 12 CSV files** (read + groupby) | `pd.concat([pd.read_csv(f) ...])` | `dd.read_csv("*.csv")` |
| Same from **Parquet** | `pd.read_parquet` | `dd.read_parquet` |
| CPU-heavy per-row Python function | `.apply` (1 core) | `map_partitions` + processes |

## Where the time goes in Dask

| Cost | Size |
|------|------|
| Building + optimising the graph | ~10–50 ms per `compute` |
| Scheduling each task | ~0.1–1 ms per task |
| Moving data between processes / machines | depends on size: the big one on clusters |
| Shuffles | the most expensive operation |

On tiny data these fixed costs dominate, so Dask loses. On big data they become negligible, and parallel reading and processing wins.

## Results on the 2-core test machine

| Test | pandas | Dask | Winner |
|------|--------|------|--------|
| tiny (240 rows) groupby | 0.000 s | 0.022 s | pandas (~70×) |
| 2.4M rows already in memory: groupby | 0.15 s | 0.54 s | pandas (3.5×) |
| 12 CSV files: read + groupby | 2.5 s | 2.3 s | Dask (1.1×) |
| Parquet: read + groupby | 0.27 s | 0.14 s | Dask (1.9×) |
| Parquet: 2 columns + filter + sum | 0.11 s | 0.11 s | tie |
| pure-Python `apply` on 300k rows | 1.8 s | 0.93 s | Dask (1.9×, = 2 cores) |

Close contests (the CSV and 2-column tests) **flip between runs**. On a second run the CSV test was a tie and the filter test went to pandas. Only clear gaps (2× or more) are meaningful.

What this shows:
- **Tiny or already-in-memory data: pandas wins.** Dask's fixed costs dominate.
- **Reading files and CPU-heavy Python: Dask wins** by roughly the number of cores (only 2 here).
- **Bigger than RAM:** not in the table, because pandas can't run at all. That's Dask's main reason to exist.

On a machine with 8+ cores, Dask's wins grow roughly with core count; pandas' wins on small data stay.

## A decision guide

```
Does the data fit in memory comfortably (< ~1/5 of your RAM)?
├── yes → pandas (or Polars). Is it slow?
│         ├── slow because of pure-Python loops → vectorize first; then Dask delayed/processes
│         └── slow because one machine isn't enough → Dask
└── no  → Dask (or Polars streaming / DuckDB for single-machine SQL-style work)
           Will it outgrow one machine, or do you need custom parallel Python? → Dask
```

## Performance checklist

1. **Parquet**, not CSV.
2. Partitions of **~100 MB**, and at least 2–4× more partitions than cores.
3. **Filter and select columns early.**
4. One `dask.compute(...)` for many results; `persist()` reused intermediates.
5. Avoid shuffles: broadcast small tables, `set_index` once and save.
6. Vectorized pandas inside `map_partitions`, never `apply(axis=1)` if avoidable.
7. Use the **distributed scheduler** and **watch the dashboard**: idle gaps = too few or too small tasks; red = data transfer; orange memory = spilling.

## Exercises

1. Run the script. At what size does Dask start to win on your machine?
2. Double the dataset (copy the files) and run again. Does the gap change?
3. Re-run with `LocalCluster(n_workers=os.cpu_count())`. Does the CPU-heavy test improve?

**Next →** [Lecture 17: Debugging & best practices](../17_debugging_best_practices/)
