"""Lecture 16: Performance: Dask vs pandas, honestly measured."""
import os
import sys
import time
from pathlib import Path
import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client, LocalCluster

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data, ensure_big_parquet   # noqa: E402

DTYPES = {"units": "float64", "unit_price": "int64", "customer_id": "int64"}
results = []


def best_of(fn, repeat=2):
    times = []
    for _ in range(repeat):
        t = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t)
    return min(times)


def race(name, pandas_fn, dask_fn, repeat=2):
    p, d = best_of(pandas_fn, repeat), best_of(dask_fn, repeat)
    ratio = max(p, d) / min(p, d)
    winner = "tie" if ratio < 1.1 else ("pandas" if p < d else "Dask")
    results.append((name, winner))
    print(f"{name:<40}{p:9.3f}{d:9.3f}   {winner}" + ("" if winner == "tie" else f" x{ratio:.1f}"))


def score(text):
    """Deliberately pure-Python per-row work (e.g. custom parsing)."""
    return sum(ord(ch) % 7 for ch in text * 20)


def main():
    big = ensure_big_data()
    pq = ensure_big_parquet()
    files = sorted(big.glob("sales_2025-*.csv"))
    print(f"cores: {os.cpu_count()}\n")
    print(f"{'test':<40}{'pandas s':>9}{'Dask s':>9}   winner")
    print("-" * 72)

    small = pd.read_csv(DATA / "sales.csv")
    race("tiny (240 rows) groupby",
         lambda: small.groupby("region").units.sum(),
         lambda: dd.from_pandas(small, npartitions=2).groupby("region").units.sum().compute(), repeat=5)

    mem = pd.read_parquet(pq)
    race("2.4M rows in memory: groupby",
         lambda: mem.groupby(["region", "product"]).units.sum(),
         lambda: dd.from_pandas(mem, npartitions=8).groupby(["region", "product"]).units.sum().compute())

    race("12 CSV files: read + groupby",
         lambda: pd.concat([pd.read_csv(f, dtype=DTYPES) for f in files]).groupby("region").units.sum(),
         lambda: dd.read_csv(big / "sales_2025-*.csv", dtype=DTYPES).groupby("region").units.sum().compute())

    race("Parquet: read + groupby",
         lambda: pd.read_parquet(pq).groupby("region").units.sum(),
         lambda: dd.read_parquet(pq).groupby("region").units.sum().compute())

    def pandas_filter():
        d = pd.read_parquet(pq, columns=["region", "units"])
        return d[d.region == "North"].units.sum()

    def dask_filter():
        d = dd.read_parquet(pq)                     # the optimiser reads only 2 columns
        return d[d.region == "North"].units.sum().compute()

    race("Parquet: read 2 columns + filter + sum", pandas_filter, dask_filter)

    sample = mem["product"].head(300_000)
    with LocalCluster(n_workers=os.cpu_count(), threads_per_worker=1, dashboard_address=":0") as c, Client(c):
        dsample = dd.from_pandas(sample.to_frame(), npartitions=8)["product"]
        race("pure-Python apply on 300k rows",
             lambda: sample.apply(score),
             lambda: dsample.map_partitions(lambda s: s.apply(score), meta=("product", "int64")).compute(),
             repeat=1)

    print("\nSummary:")
    for name, winner in results:
        print(f"  {winner:>6}: {name}")
    print("\nDask pays fixed costs (graph, scheduling, moving data). They dominate on small data")
    print("and vanish on big data. And when data is bigger than RAM, pandas can't run at all.")


if __name__ == "__main__":
    main()
