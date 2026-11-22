"""Lecture 02: Lazy evaluation, task graphs, the optimiser, and compute() vs dask.compute()."""
import sys
import time
from pathlib import Path
import dask
import dask.dataframe as dd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data          # noqa: E402

BIG = ensure_big_data()

print("=== 1. Building is instant, computing is not ===")
t = time.perf_counter()
ddf = dd.read_csv(BIG / "sales_2025-*.csv", parse_dates=["timestamp"])
big_orders = ddf[ddf.units >= 4]
total = (big_orders.units * big_orders.unit_price).sum()
print(f"built the plan in {(time.perf_counter() - t) * 1000:.0f} ms -> {total}")

t = time.perf_counter()
value = total.compute()
print(f"computed {value:,.0f} in {time.perf_counter() - t:.2f} s (read 12 files, 2.4M rows)")

print("\n=== 2. Looking at the graph ===")
print("partitions:", ddf.npartitions)
print("tasks in graph:", len(total.__dask_graph__()))

# The expression tree. Shown on a small in-memory table, because CSV readers print a lot of detail.
import pandas as pd
small = dd.from_pandas(pd.read_csv(DATA / "sales.csv"), npartitions=3)
small_total = (small[small.units >= 4].units * small[small.units >= 4].unit_price).sum()
print("\nexpression tree as written:")
small_total.pprint()
print("\nafter optimisation: one fused step per partition, then a tree reduction:")
small_total.optimize().pprint()
print("\nNote 'columns=[\'units\', \'unit_price\']' at the source: only 2 of 8 columns are read.")
print("The same projection is applied to the 12 CSV files above.")

try:
    dask.delayed(sum)([1, 2, 3]).visualize(filename=str(Path(__file__).parent / "graph.png"))
    print("\nsaved graph.png")
except Exception as e:                                 # Graphviz not installed
    print("\n(.visualize skipped:", type(e).__name__, "- install Graphviz to draw graphs)")

print("\n=== 3. Too many compute() calls ===")
regions = ["North", "South", "East", "West"]
t = time.perf_counter()
slow = {r: ddf[ddf.region == r].units.sum().compute() for r in regions}
slow_t = time.perf_counter() - t

t = time.perf_counter()
fast = dict(zip(regions, dask.compute(*[ddf[ddf.region == r].units.sum() for r in regions])))
fast_t = time.perf_counter() - t

t = time.perf_counter()
best = ddf.groupby("region").units.sum().compute()
best_t = time.perf_counter() - t
print(f"4 separate compute(): {slow_t:5.2f} s")
print(f"one dask.compute()  : {fast_t:5.2f} s")
print(f"one groupby         : {best_t:5.2f} s")
print("same answers:", slow == fast == best.to_dict())

print("\n=== 4. Previews are cheap ===")
t = time.perf_counter()
print(ddf.head(3))
print(f"head() took {(time.perf_counter() - t) * 1000:.0f} ms (only the first partition is read)")

print("\n=== 5. Sharing work with dask.compute ===")
a = ddf.units.sum()
b = ddf.unit_price.mean()
t = time.perf_counter(); a.compute(); b.compute(); two = time.perf_counter() - t
t = time.perf_counter(); dask.compute(a, b); one = time.perf_counter() - t
print(f"a.compute() + b.compute(): {two:.2f} s | dask.compute(a, b): {one:.2f} s")
