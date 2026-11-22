"""Lecture 08: GroupBy: tree reductions, named aggs, split_out, custom Aggregation."""
import sys
import time
from pathlib import Path
import dask
import dask.dataframe as dd
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_parquet       # noqa: E402

pd.set_option("display.width", 140)
pd.set_option("display.float_format", "{:,.1f}".format)
ddf = dd.read_parquet(ensure_big_parquet())
ddf = ddf.assign(revenue=ddf.units * ddf.unit_price)
print(f"{len(ddf):,} rows in {ddf.npartitions} partitions\n")

print("=== 1. The pandas syntax works ===")
t = time.perf_counter()
print(ddf.groupby("region").revenue.sum().compute().sort_values(ascending=False))
print(f"took {time.perf_counter() - t:.2f} s")

print("\n=== 2. Named aggregation ===")
summary = ddf.groupby("region").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    avg_order=("revenue", "mean"),
    max_order=("revenue", "max"),
    avg_units=("units", "mean"),
).compute().sort_values("revenue", ascending=False)
print(summary.round(1))

print("\n=== 3. Two keys, then unstack in pandas ===")
table = ddf.groupby(["product", "region"]).units.mean().compute().unstack().round(3)
print(table)

print("\n=== 4. nunique and several results in one pass ===")
customers, products_per_region = dask.compute(
    ddf.groupby("region").customer_id.nunique(),
    ddf.groupby("region")["product"].nunique(),
)
print(pd.DataFrame({"customers": customers, "products": products_per_region}).sort_index())

print("\n=== 5. The graph is a tree reduction ===")
g = ddf.groupby("region").revenue.sum()
print("tasks:", len(g.__dask_graph__()), "| result partitions:", g.npartitions)

print("\n=== 6. Many groups: split_out ===")
per_customer = ddf.groupby("customer_id").revenue.sum(split_out=4)
print("result partitions:", per_customer.npartitions)
top = per_customer.nlargest(5).compute()
print("top 5 customers by spend:\n", top)

print("\n=== 7. Custom aggregations ===")
price_range = dd.Aggregation(
    name="range",
    chunk=lambda s: (s.max(), s.min()),
    agg=lambda mx, mn: (mx.max(), mn.min()),
    finalize=lambda mx, mn: mx - mn,
)
# chunk() receives a GROUPED series (SeriesGroupBy), not a plain Series, so use group methods
bulk_share = dd.Aggregation(
    name="bulk_share",
    chunk=lambda g: (g.apply(lambda s: (s >= 4).sum()), g.count()),
    agg=lambda bulk, n: (bulk.sum(), n.sum()),
    finalize=lambda bulk, n: bulk / n,
)
print(ddf.groupby("category").unit_price.agg(price_range).compute())
custom = ddf.groupby("region").units.agg(bulk_share).compute().sort_index()
simple = ddf.assign(bulk=ddf.units >= 4).groupby("region").bulk.mean().compute().sort_index()
print(pd.DataFrame({"custom Aggregation": custom, "mean of a True/False column": simple})
      .to_string(float_format="{:.4f}".format))
print("They differ slightly: count() skips the missing units, but NaN >= 4 is False and still")
print("counts as a row in the mean. Decide how missing values should count before you aggregate!")
print("Often a helper column + a built-in aggregation is simpler than a custom Aggregation.")

print("\n=== 8. Median by group: approximate vs exact ===")
t = time.perf_counter()
med = ddf.groupby("product").revenue.median(shuffle_method="tasks").compute().sort_index()
print(med)
print(f"exact median via shuffle: {time.perf_counter() - t:.2f} s (more expensive than sum/mean)")
