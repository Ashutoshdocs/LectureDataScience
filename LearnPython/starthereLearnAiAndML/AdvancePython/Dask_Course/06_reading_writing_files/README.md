# Lecture 06: Reading & writing files

Run: `python lecture.py` (writes into `output/`)

## Reading many files as one table

```python
ddf = dd.read_csv("data/big/sales_2025-*.csv")          # glob pattern
ddf = dd.read_csv(["a.csv", "b.csv"])                    # explicit list
ddf = dd.read_csv("s3://bucket/logs/*.csv")              # cloud storage (with s3fs)
ddf = dd.read_csv("data/big/*.csv", include_path_column=True)   # add a "path" column
```

| Reader | Notes |
|--------|-------|
| `dd.read_csv` | accepts most `pd.read_csv` options |
| `dd.read_parquet` | **best**: fast, typed, reads only needed columns |
| `dd.read_json(..., lines=True)` | JSON lines |
| `dd.read_sql_table` / `read_sql_query` | databases (needs an index column to split on) |
| `dd.from_delayed` | anything else: write a loader function |

## `blocksize`: how CSVs become partitions

Dask splits each CSV into **blocks** (default 64 MB of *file* size). Each block becomes one partition. Small files give one partition each; large files are split.

```python
dd.read_csv("big.csv", blocksize="25MB")    # more, smaller partitions
dd.read_csv("big.csv", blocksize=None)      # one partition per file (needed for compressed .gz files)
```

## ⚠️ dtype inference from a sample

Dask guesses column types from the **first few rows of the first file**. If a later file contains something different (missing values in an int column, text in a number column), you get an error **at compute time**:

```
ValueError: Mismatched dtypes found in `pd.read_csv`/`pd.read_table`.
+--------+---------+----------+
| Column | Found   | Expected |
| units  | float64 | int64    |
```

Fix it by declaring types up front:

```python
dd.read_csv("*.csv", dtype={"units": "float64", "customer_id": "int64"})
```

Lecture 17 reproduces this error on purpose.

## Writing

| Method | Output |
|--------|--------|
| `ddf.to_parquet("folder/")` | **one file per partition** in a folder: fast, typed, compressed |
| `ddf.to_parquet("folder/", partition_on=["region"])` | sub-folders `region=North/…`: filters on region skip whole folders |
| `ddf.to_csv("out/part-*.csv", index=False)` | one CSV per partition (`*` = partition number) |
| `ddf.to_csv("one.csv", single_file=True, index=False)` | a single file (written sequentially, so slower) |
| `ddf.compute().to_excel(...)` | small results only: compute to pandas first |

## CSV vs Parquet with Dask

| | CSV | Parquet |
|---|---|---|
| Read speed | slow (text parsing) | fast |
| Reads only needed columns | ❌ | ✅ (projection pushdown) |
| Skips row groups by filter | ❌ | ✅ (`filters=[("region", "==", "North")]`) |
| Keeps dtypes | ❌ (guessed again every time) | ✅ |
| Size | large | ~3–10× smaller |

Measured in `lecture.py` on the 2.4M-row dataset: **161 MB of CSV became 42 MB of Parquet**, and the same `groupby` took **2.2 s on CSV vs 0.14 s on Parquet (~16× faster)**.

**Standard Dask workflow:** convert raw CSVs to Parquet **once**, then analyse the Parquet.

## Exercises

1. Read the big files with `include_path_column=True`. How many rows come from each file?
2. Convert the 12 CSVs to Parquet. Compare folder sizes and the time of the same `groupby` on both.
3. Write Parquet partitioned on `region`, then read only `North` with `filters=`.
4. Write the per-product summary as one CSV.

<details><summary>Solutions</summary>

See sections 2–6 of `lecture.py`.
</details>

**Next →** [Lecture 07: DataFrame operations](../07_dataframe_operations/)
