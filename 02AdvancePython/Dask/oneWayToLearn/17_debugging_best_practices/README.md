# Lecture 17: Debugging & best practices

Run: `python lecture.py`. It triggers each common error on purpose and shows the fix.

## Why Dask errors are confusing

Because Dask is lazy, an error often appears at `.compute()` time, **far from the line that caused it**, and inside a worker thread or process. Tracebacks can be long and full of Dask internals.

## Debugging toolkit

| Tool | Use |
|------|-----|
| `dask.config.set(scheduler="synchronous")` | run everything in one thread: normal tracebacks, `print()` and `pdb` work |
| `ddf.head()` | quick check; only runs the first partition |
| `ddf.partitions[i].compute()` | inspect one partition as pandas |
| `ddf._meta` / `ddf.dtypes` | what Dask *thinks* the columns and types are |
| `x.pprint()` / `len(x.__dask_graph__())` | the plan and its size |
| `client.get_task_stream()`, the dashboard | where time goes |
| Develop on `dd.from_pandas(small_sample)` | fast iteration, then switch to the full data |

```python
with dask.config.set(scheduler="synchronous"):
    result.compute()            # an error here has a plain, readable traceback
```

## The usual suspects

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ValueError: Mismatched dtypes found in pd.read_csv` | dtypes inferred from the first file's sample; a later file differs | `dtype={"col": "float64"}` in `read_csv`, or use Parquet |
| Wrong columns or dtype after `map_partitions` / `apply` | `meta` guessed wrong | pass `meta=` explicitly |
| `NotImplementedError` (e.g. `iloc` on rows) | that pandas feature doesn't exist in Dask | filter by column, `head`, `map_partitions` |
| Results differ from pandas for rank, mean-centering, shift | per-partition computation | global value first, `map_overlap`, or a shuffle |
| `KilledWorker` / memory errors | partitions too large, or a huge `.compute()` | smaller partitions, reduce before `compute`, more memory per worker |
| Very slow, dashboard shows tiny tasks | partitions too small / too many tasks | `repartition(partition_size="100MB")` |
| Very slow, lots of red (transfer) | shuffles | broadcast small tables, `set_index` once and save |
| Script re-runs or hangs when starting a cluster | missing `if __name__ == "__main__":` | add the guard |
| Same result every time from a random function (futures) | identical tasks are cached | `pure=False` |
| `resample` error about the index | partition boundaries don't align with the bins | `"MS"` instead of `"ME"`, or resample daily first |

## Best-practice checklist

**Data**
1. Store data as **Parquet**, partitioned sensibly (~100 MB per partition).
2. Declare `dtype=` when reading CSV.
3. Use `category` for repeated strings.

**Code**
4. Prototype in **pandas on a sample**; switch to Dask for the full data.
5. **Filter and select columns early.**
6. Avoid `apply(axis=1)`; use vectorized code or `map_partitions`.
7. Provide `meta=` for `map_partitions`.
8. Avoid shuffles when you can (broadcast joins, aggregate before joining).

**Execution**
9. One `dask.compute(...)` for many results; `persist()` reused intermediates.
10. Reduce before `.compute()`. Never `ddf.compute()` on huge data.
11. Use the **distributed scheduler** and **watch the dashboard**.
12. Don't use Dask when pandas is enough.

## Exercises

1. Reproduce the dtype mismatch error and fix it two different ways.
2. Run a failing `map_partitions` with the threaded and the synchronous scheduler. Compare the tracebacks.
3. Find the partition containing a bad value with `ddf.partitions[i]`.

**Next →** [Lecture 18: Project: big sales pipeline](../18_project_big_sales_pipeline/)
