"""Lecture 15: persist vs compute vs dask.compute, and memory-friendly habits."""
import sys
import time
from pathlib import Path
import dask
import dask.dataframe as dd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data, ensure_big_parquet   # noqa: E402

BIG = ensure_big_data()
DTYPES = {"units": "float64", "unit_price": "int64", "customer_id": "int64"}


def cleaned():
    raw = dd.read_csv(BIG / "sales_2025-*.csv", parse_dates=["timestamp"], dtype=DTYPES)
    clean = raw.dropna(subset=["units"])
    return clean.assign(revenue=clean.units * clean.unit_price,
                        month=clean.timestamp.dt.month)


def three_summaries(df):
    return (df.groupby("region").revenue.sum(),
            df.groupby("product").units.mean(),
            df.groupby("month").order_id.count())


def timed(label, fn):
    t = time.perf_counter()
    fn()
    s = time.perf_counter() - t
    print(f"  {label:<48} {s:6.2f} s")
    return s


print("=== 1. Three separate computes, no persist (each re-reads 12 CSVs) ===")
a, b, c = three_summaries(cleaned())
no_persist = timed("3 x compute()", lambda: (a.compute(), b.compute(), c.compute()))

print("\n=== 2. One dask.compute (shared reading) ===")
shared = timed("dask.compute(a, b, c)", lambda: dask.compute(*three_summaries(cleaned())))

print("\n=== 3. persist once, then compute three times ===")
t = time.perf_counter()
clean = cleaned().persist()
persist_cost = time.perf_counter() - t
print(f"  persist() took {persist_cost:.2f} s (reads + cleans once)")
a, b, c = three_summaries(clean)
after = timed("3 x compute() on persisted data", lambda: (a.compute(), b.compute(), c.compute()))
print(f"  total with persist: {persist_cost + after:.2f} s vs {no_persist:.2f} s without")
extra = timed("a 4th question costs only", lambda: clean.groupby("category").revenue.mean().compute())

print("\n=== 4. Persisted data is still Dask ===")
print("  type:", type(clean).__name__, "| partitions:", clean.npartitions)
print(f"  in memory: {clean.memory_usage(deep=True).sum().compute() / 1e6:.0f} MB")
del clean                                                        # free it

print("\n=== 5. Filter & select early (the optimiser often does it for you) ===")
pq = dd.read_parquet(ensure_big_parquet())
timed("all columns, then filter + sum",
      lambda: pq[pq.region == "North"].units.sum().compute())
timed("read 2 columns + filter while reading",
      lambda: dd.read_parquet(ensure_big_parquet(), columns=["region", "units"],
                              filters=[("region", "==", "North")]).units.sum().compute())
print("  About the same: Dask's optimiser already pushed the column selection and the filter")
print("  into read_parquet for the first version. It can only do that for steps it can SEE,")
print("  so persisting/computing before filtering still costs you. Filter early anyway.")

print("\n=== 6. dtypes and memory ===")
df = pq[["region", "product", "category"]]
as_str = df.memory_usage(deep=True).sum().compute() / 1e6
as_cat = df.astype("category").memory_usage(deep=True).sum().compute() / 1e6
print(f"  3 text columns as string  : {as_str:6.1f} MB")
print(f"  3 text columns as category: {as_cat:6.1f} MB ({as_str / as_cat:.0f}x smaller)")

print("\n=== 7. Reduce, then compute ===")
summary = pq.groupby("region").units.sum().compute()
print(f"  a groupby result is {summary.memory_usage(deep=True) / 1e3:.1f} KB; "
      f"pq.compute() would be {pq.memory_usage(deep=True).sum().compute() / 1e6:.0f} MB in one process")
