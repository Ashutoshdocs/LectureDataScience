"""Lecture 05: Dask DataFrame basics: partitions, meta, what is free vs what computes."""
import sys
import time
from pathlib import Path
import dask.dataframe as dd
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data          # noqa: E402

BIG = ensure_big_data()

print("=== 1. From pandas ===")
pdf = pd.read_csv(DATA / "sales.csv")
ddf = dd.from_pandas(pdf, npartitions=5)
print(ddf)
print("rows per partition:", ddf.map_partitions(len).compute().tolist())
print("divisions (index boundaries):", ddf.divisions)

print("\n=== 2. Free information (no computation) ===")
print("columns    :", list(ddf.columns))
print("npartitions:", ddf.npartitions)
print("dtypes:\n", ddf.dtypes)
print("_meta (an EMPTY pandas DataFrame with the right structure):")
print(repr(ddf._meta))

print("\n=== 3. One partition is just pandas ===")
part = ddf.partitions[2].compute()
print(type(part).__name__, part.shape)
print(part.head(3))

print("\n=== 4. Reading 12 big files ===")
big = dd.read_csv(BIG / "sales_2025-*.csv", parse_dates=["timestamp"])
print("partitions:", big.npartitions)

t = time.perf_counter()
print("head():")
print(big.head(3))
print(f"  took {time.perf_counter() - t:.2f} s (first partition only)")

t = time.perf_counter()
n = len(big)
print(f"len(): {n:,} rows, took {time.perf_counter() - t:.2f} s (reads everything)")

mb = big.memory_usage_per_partition(deep=True).compute() / 1e6
print("MB per partition in memory:", mb.round(1).tolist())
print(f"total in memory if loaded into pandas: {mb.sum():.0f} MB")

print("\n=== 5. Repartitioning ===")
fewer = big.repartition(npartitions=4)
print("npartitions=4 ->", fewer.npartitions,
      "| MB each:", (fewer.memory_usage_per_partition(deep=True).compute() / 1e6).round(0).tolist())
by_size = big.repartition(partition_size="25MB")
print("partition_size='25MB' ->", by_size.npartitions, "partitions")

print("\n=== 6. Reduce first, then compute ===")
summary = big.groupby("product").units.sum().compute()      # small result: safe to compute
print(type(summary).__name__, summary.shape)
print(summary.sort_values(ascending=False))
