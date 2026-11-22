"""Lecture 01: What is Dask? Partitions, laziness, and the five collections at a glance."""
from pathlib import Path
import dask
import dask.array as da
import dask.bag as db
import dask.dataframe as dd
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
print("Dask version:", dask.__version__)

print("\n=== A Dask DataFrame is many pandas DataFrames ===")
pdf = pd.read_csv(DATA / "sales.csv")
ddf = dd.from_pandas(pdf, npartitions=4)
print(ddf)                                       # structure only: no data shown
print("partitions:", ddf.npartitions)
print("rows per partition:", ddf.map_partitions(len).compute().tolist())
print("partition 0 is a", type(ddf.partitions[0].compute()).__name__)

print("\n=== Lazy until .compute() ===")
total = ddf["units"].sum()
print("before compute:", type(total).__name__, "->", total)
print("after compute :", type(total.compute()).__name__, "->", total.compute())
print("same as pandas:", pdf["units"].sum())

print("\n=== The pandas API you already know ===")
by_region = ddf.groupby("region")["units"].sum()
print(by_region.compute().sort_index())

print("\n=== The other collections, briefly ===")
x = da.ones((4000, 4000), chunks=(1000, 1000))     # 16 NumPy chunks
print("Array :", x, "-> sum =", x.sum().compute())

b = db.from_sequence(["tea", "coffee", "tea", "juice"], npartitions=2)
print("Bag   :", b.frequencies().compute(scheduler="threads"))


@dask.delayed
def square(n):
    return n * n


lazy_total = dask.delayed(sum)([square(i) for i in range(5)])
print("Delayed:", lazy_total, "->", lazy_total.compute())
