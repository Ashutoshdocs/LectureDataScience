# Lecture 19: Performance: Polars vs pandas, and how to stay fast

Run: `python lecture.py`. It races both libraries on the same 5-million-row table (needs pandas installed, about 30 seconds).

## The race

`lecture.py` times the same task in pandas and Polars:

| Task | What it does |
|------|--------------|
| Read CSV | load 1M rows from disk |
| Filter | keep one region with units ≥ 3 |
| New column | revenue = units × price |
| Group by | revenue sum/mean per region × product |
| Join | attach a 50k-row customer table |
| Sort | by two columns |
| String op | upper-case + contains on a text column |
| Pipeline | filter → new column → group → sort (Polars lazy) |

It prints a table of times and the speed-up. Here is one real run on a small **2-thread** cloud machine (pandas 3.0.5, Polars 2.1):

| Task | pandas ms | Polars ms | Speed-up |
|------|-----------|-----------|----------|
| read CSV (1M rows) | 359 | 64 | 5.6× |
| filter | 124 | 34 | 3.6× |
| new column | 11 | 10 | 1.1× |
| group by (sum, mean) | 348 | 46 | 7.6× |
| join 50k customers | 438 | 79 | 5.6× |
| sort by 2 columns | 749 | 920 | 0.8× |
| string upper+contains | 361 | 395 | 0.9× |
| pipeline (lazy) | 247 | 37 | 6.7× |

What this shows honestly:
- **Big wins** on reading, filtering, grouping, joining and whole pipelines.
- **No win** on simple column arithmetic. Both hand it to compiled code.
- On only 2 threads, **sorting and string work came out even or slightly slower**. These depend most on parallelism, so on a typical 8–16 core laptop expect Polars to pull ahead there too.

**Run it yourself.** Your numbers depend on your CPU and core count.

## Why Polars wins (recap)

1. **All cores**: group-bys, joins, sorts and expression lists run in parallel.
2. **Rust + Arrow**: compiled code on columnar memory, plus native string handling.
3. **Query optimiser**: lazy plans skip unneeded columns and rows.
4. **No index**: no hidden index alignment or copying.

## When pandas is fine (or better)

- Small data (a few thousand rows). Both are instant.
- Libraries that require pandas (some plotting, stats and ML tools). Convert with `.to_pandas()` at the end.
- Code that relies on the index (time-series alignment, `.loc` by label).

## Staying fast in Polars: the anti-patterns

| Slow | Fast | Why |
|------|------|-----|
| `pl.col("x").map_elements(lambda v: ...)` | native expressions (`when/then`, `.str`, `.dt`, arithmetic) | `map_elements` calls Python **once per value**, single-threaded. Polars even warns you |
| `for row in df.iter_rows(): ...` | expressions / `group_by` | Python loop |
| `df.to_pandas()` in the middle of a pipeline | stay in Polars, convert only at the end | copies the data |
| `pl.read_csv(...)` on a huge file, then filter | `pl.scan_csv(...).filter(...).collect()` | pushdown |
| Many separate `with_columns` calls for independent columns | put them in **one** `with_columns` | one parallel pass |
| CSV for repeated work | Parquet | fast and typed |
| `pl.concat` inside a loop | build a list, `pl.concat` once | avoids repeated copying |

If you truly need custom Python per value, `map_batches` (one call per **column**, e.g. a NumPy function) is far better than `map_elements` (one call per **value**).

## Exercises

1. Increase `N` to 10 million. Does the gap grow?
2. Run with `POLARS_MAX_THREADS=1 python lecture.py`. How much of Polars' advantage comes from multi-threading?
3. Rewrite the `map_elements` example in the lecture with `when/then` and time both.

<details><summary>Hint</summary>

With 1 thread, Polars is usually still faster than pandas (Rust + Arrow + optimiser), but the gap shrinks a lot. That shows how much comes from parallelism.
</details>

**Next →** [Lecture 20: SQL & interop](../20_sql_and_interop/)
