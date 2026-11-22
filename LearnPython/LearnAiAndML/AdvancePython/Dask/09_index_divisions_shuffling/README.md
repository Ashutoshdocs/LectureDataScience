# Lecture 09: Index, divisions & shuffling

Run: `python lecture.py`

## Divisions: the index boundaries of each partition

If a Dask DataFrame's index is **sorted**, Dask records where each partition starts and ends. These are the **divisions**:

```
 index: timestamp (sorted)
 partition 0: 2025-01-01 … 2025-01-31
 partition 1: 2025-02-01 … 2025-02-28      divisions = (2025-01-01, 2025-02-01, 2025-03-01, …, 2025-12-31)
 partition 2: 2025-03-01 … 2025-03-31
```

```python
ddf.known_divisions     # True / False
ddf.divisions           # (start0, start1, …, end) or (None, None, …)
```

With known divisions Dask can **jump straight to the right partitions**:

| Operation | Unknown divisions | Known divisions |
|-----------|-------------------|-----------------|
| `ddf.loc["2025-03-15"]` | scans every partition | reads **one** partition |
| `ddf.loc["2025-03":"2025-04"]` | scans everything | reads 2 partitions |
| join on the index | full shuffle | partition-to-partition (cheap) |
| `resample`, time-based `rolling` | ❌ / limited | ✅ |
| `groupby` on the index | shuffle | partition-local |

## `set_index`: sorting the whole dataset

```python
ddf = ddf.set_index("timestamp")             # sorts ALL rows by timestamp
ddf = ddf.set_index("timestamp", sorted=True)   # data is already sorted: just record divisions (cheap)
```

`set_index` on unsorted data needs a **shuffle**:

```
 1. sample the column to choose partition boundaries
 2. every partition sends each row to the partition that owns its range  ← all-to-all data movement
 3. sort inside each new partition
```

A shuffle moves (nearly) every row across partitions. On a cluster that means across the **network**. It's the single most expensive operation in Dask.

## Measured in `lecture.py` (2.4M rows, 12 partitions)

| | Time |
|---|---|
| `set_index("timestamp", sorted=True)` (already in order) | ~1.0 s |
| `set_index("customer_id")` (needs a shuffle) | ~1.7 s |
| one day's orders by **filtering a column** | ~400 ms (scans all 12 partitions) |
| one day's orders by **`.loc` on the sorted index** | **~8 ms** (reads 1 partition) |
| all orders of one customer via `.loc` on a customer index | ~5 ms |

## Rules of thumb

| Do | Avoid |
|----|-------|
| `set_index` **once**, early, on a column you'll filter/join/resample by often | calling `set_index` repeatedly |
| use `sorted=True` when the files are already in order (e.g. one file per month) | sorting data that's already sorted |
| store the result as **Parquet**; divisions can be recovered on read | shuffling the same data again in every script |
| prefer aggregations that don't need shuffles | `groupby().apply`, `sort_values` on huge data unless needed |

## Other shuffling operations

`sort_values`, `ddf.shuffle(on="col")` (put equal keys in the same partition), `groupby().apply`, `merge` of two large tables on a non-index column, `drop_duplicates(split_out>1)`, `pivot_table` on unknown categories.

## Exercises

1. Check `known_divisions` after `read_parquet`. Then `set_index("timestamp")`. What are the divisions?
2. Time `ddf.loc["2025-06-15"]` with and without a timestamp index.
3. Compare `set_index(..., sorted=True)` and `set_index(...)` timings.
4. Shuffle by `customer_id`. Check that each customer lives in only one partition.

<details><summary>Solutions</summary>

See `lecture.py`. With known divisions, the `.loc` lookup touches only 1 of 12 partitions.
</details>

**Next →** [Lecture 10: Joins & merge](../10_joins_and_merge/)
