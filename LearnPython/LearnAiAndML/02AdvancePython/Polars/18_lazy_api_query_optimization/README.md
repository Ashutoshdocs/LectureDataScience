# Lecture 18: The lazy API & query optimisation

Run: `python lecture.py`. It creates a 5-million-row Parquet file (~30 MB) in `output/` the first time, which takes a few seconds.

## Eager vs lazy

| | Eager (`DataFrame`) | Lazy (`LazyFrame`) |
|---|---|---|
| Created by | `pl.read_csv`, `pl.DataFrame(...)` | `pl.scan_csv`, `pl.scan_parquet`, `df.lazy()` |
| Each step | runs **immediately** | is **recorded** in a query plan |
| Result | data | a plan, until you call **`.collect()`** |
| Optimised? | no, each step on its own | **yes**, the whole query at once |

```python
result = (
    pl.scan_parquet("big.parquet")          # nothing read yet
      .filter(pl.col("region") == "North")
      .group_by("product")
      .agg(pl.col("revenue").sum())
      .sort("revenue", descending=True)
      .collect()                            # optimise, then run
)
```

The code is identical to eager code, apart from `scan_*` at the start and `.collect()` at the end.

## What the optimiser does

| Optimisation | Meaning | Benefit |
|--------------|---------|---------|
| **Projection pushdown** | read only the columns the query uses | 4 of 8 columns in this lecture's query |
| **Predicate pushdown** | apply filters *while reading* the file | skip rows (and whole Parquet row groups) early |
| **Slice pushdown** | `.head(10)` stops reading after 10 rows | instant previews of huge files |
| **Common subexpression elimination** | compute a repeated expression once | less CPU |
| **Simplification / reordering** | e.g. filter before join | smaller intermediate tables |

## Measured in `lecture.py` (5M rows, desktop CPU)

| | Time |
|---|---|
| Eager: `read_parquet` → filter → group | ~250 ms |
| Lazy: `scan_parquet` → filter → group → `collect` | ~35 ms (**~7× faster**, same result) |
| Preview with `scan_parquet(...).head(3)` | ~5 ms |

## Seeing the plan

```python
lf.explain()                     # optimised plan (read it bottom → top)
lf.explain(optimized=False)      # what you literally wrote
```

In the optimised plan, look for:
```
Parquet SCAN [big.parquet]
PROJECT 4/8 COLUMNS                   ← projection pushdown
SELECTION: col("region") == "North"   ← predicate pushdown
```

## Streaming: bigger than memory

```python
lf.collect(engine="streaming")                     # process in chunks
lf.sink_parquet("result.parquet")                  # stream straight to a file, never fully in RAM
```

## Lazy-only habits

| Want | Lazy way |
|------|----------|
| Column names / types without running | `lf.collect_schema()` |
| A quick preview | `lf.head(5).collect()` (slice pushdown makes it fast) |
| Debug one step | `.collect()` early, inspect, then remove |
| Several outputs from one scan | `pl.collect_all([lf1, lf2])` |
| A DataFrame into a lazy pipeline | `df.lazy()` |

> `pivot` and a few other operations need to see the data first, so they're eager-only. Collect, pivot, then `.lazy()` again if needed.

## When should you use lazy?

- **Always** for files you scan (`scan_parquet` / `scan_csv`), especially big ones
- Long pipelines: let the optimiser reorder and prune them
- In exploration, eager is fine (and easier to inspect)

## Exercises

1. Print the unoptimised and optimised plans for a query of your own. Spot the differences.
2. Time `read_parquet(...).filter(...)` against `scan_parquet(...).filter(...).collect()`.
3. Use `sink_parquet` to save only Furniture orders without collecting.
4. Use `pl.collect_all` to compute two summaries in one pass.

<details><summary>Solutions</summary>

See the sections in `lecture.py`. Projection and predicate pushdown appear only in the optimised plan.
</details>

**Next →** [Lecture 19: Performance: Polars vs pandas](../19_performance_polars_vs_pandas/)
