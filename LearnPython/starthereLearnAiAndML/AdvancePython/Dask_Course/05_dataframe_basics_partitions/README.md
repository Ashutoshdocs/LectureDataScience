# Lecture 05: Dask DataFrame basics & partitions

Run: `python lecture.py`

## A Dask DataFrame = many pandas DataFrames

```
          Dask DataFrame (12 partitions)
 ┌──────────┬──────────┬──────────┬─────┬──────────┐
 │ pandas   │ pandas   │ pandas   │ ... │ pandas   │
 │ Jan rows │ Feb rows │ Mar rows │     │ Dec rows │
 └──────────┴──────────┴──────────┴─────┴──────────┘
   ↑ each partition is a normal pandas DataFrame, split by ROWS
```

- Every partition has the **same columns and dtypes**.
- An operation like `ddf.units * 2` becomes "do `units * 2` on each partition".
- A reduction like `ddf.units.sum()` sums each partition, then combines the results.

## Creating one

| Code | Use |
|------|-----|
| `dd.read_csv("data/big/*.csv")` | **most common**: from files (Lecture 06) |
| `dd.read_parquet("folder/")` | the best format for Dask |
| `dd.from_pandas(pdf, npartitions=4)` | from an in-memory pandas DataFrame (testing, small data) |
| `dd.from_dict({...}, npartitions=2)` | from a dict |
| `dd.from_delayed([...])` | from delayed functions that each return a pandas DataFrame |

## What you can inspect *without* computing

| Attribute | Gives | Cost |
|-----------|-------|------|
| `ddf.columns`, `ddf.dtypes` | column names and types | free (from `meta`) |
| `ddf.npartitions` | number of partitions | free |
| `ddf.divisions` | index boundaries of partitions (if known) | free |
| `ddf._meta` | an empty pandas DataFrame with the right columns/dtypes | free |
| `print(ddf)` | the structure, without the data | free |

## What triggers computation

| Call | Note |
|------|------|
| `ddf.head(n)` | reads only the **first partition**, so it's fast |
| `ddf.tail(n)` | reads only the last partition |
| `len(ddf)` / `ddf.shape[0].compute()` | **reads everything** |
| `ddf.compute()` | turns the **whole** thing into pandas, so it must fit in memory! |
| `ddf.describe().compute()` | full pass |
| `ddf.partitions[i].compute()` | one partition as pandas |
| `ddf.map_partitions(len).compute()` | rows per partition |

> ⚠️ `ddf.compute()` on a 50 GB dataset will try to load 50 GB into RAM. Reduce first (filter, groupby, aggregate), *then* compute.

## Partition size: the most important tuning knob

| Partition size (in memory) | Effect |
|----------------------------|--------|
| < 10 MB | too many tiny tasks, so overhead dominates |
| **~100 MB** | ✅ recommended |
| > 1 GB | few tasks, little parallelism, memory pressure |

```python
ddf.memory_usage_per_partition(deep=True).compute() / 1e6    # MB per partition
ddf = ddf.repartition(partition_size="100MB")                 # resize
ddf = ddf.repartition(npartitions=8)
```

Rule of thumb: **at least as many partitions as cores**, ideally a few times more.

## Exercises

1. Create a Dask DataFrame from `sales.csv` via pandas with 5 partitions. How many rows does each have?
2. Print `ddf._meta`. What is it?
3. Read the 12 big files. How many partitions? How many MB is each in memory?
4. Repartition to 4 partitions and check again.

<details><summary>Solutions</summary>

1. 48 each: `ddf.map_partitions(len).compute()`.
2. An empty pandas DataFrame carrying the column names and dtypes. Dask uses it to know the result structure without computing.
3. 12 partitions (one per file, since each ~13 MB file is smaller than the 64 MB `blocksize`), about 17 MB each in memory. That's on the small side; for real work you'd aim for ~100 MB.
4. `big.repartition(npartitions=4)` gives 4 partitions of about 56 MB each.
</details>

**Next →** [Lecture 06: Reading & writing files](../06_reading_writing_files/)
