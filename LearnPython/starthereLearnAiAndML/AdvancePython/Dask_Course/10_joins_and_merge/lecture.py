"""Lecture 10: Joins: broadcast vs shuffle vs aligned, and making joins fast."""
import sys
import time
from pathlib import Path
import dask.dataframe as dd
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_parquet, BIG  # noqa: E402

pd.set_option("display.width", 140)
pd.set_option("display.float_format", "{:,.0f}".format)
orders = dd.read_parquet(ensure_big_parquet())
orders = orders.assign(revenue=orders.units * orders.unit_price)
customers_pd = pd.read_csv(BIG / "customers_big.csv")
print(f"orders: {len(orders):,} rows / {orders.npartitions} partitions | customers: {len(customers_pd):,} rows (pandas)\n")


def timed(label, fn):
    t = time.perf_counter()
    result = fn()
    print(f"{label:<52} {time.perf_counter() - t:5.2f} s")
    return result


print("=== 1. Large x small (pandas): broadcast join ===")
joined = orders.merge(customers_pd, on="customer_id", how="left")
print(joined[["order_id", "customer_id", "city", "segment", "revenue"]].head(3))
table = timed("broadcast join + groupby(city, segment)",
              lambda: joined.groupby(["city", "segment"]).revenue.sum().compute().unstack())
print((table / 1e7).round(1).rename_axis(columns="Rs crore"))

print("\n=== 2. Large x large: the same join, other side as Dask (4 partitions) ===")
customers_dd = dd.from_pandas(customers_pd, npartitions=4)
timed("shuffle join (both sides Dask)",
      lambda: orders.merge(customers_dd, on="customer_id", how="left")
                    .groupby(["city", "segment"]).revenue.sum().compute())
timed("same, but broadcast=True forces a broadcast",
      lambda: orders.merge(customers_dd, on="customer_id", how="left", broadcast=True)
                    .groupby(["city", "segment"]).revenue.sum().compute())

print("\n=== 3. Aggregate first, then join (tiny join) ===")
spend = timed("groupby customer, then join 20k rows in pandas",
              lambda: orders.groupby("customer_id").revenue.sum().compute()
                            .reset_index().merge(customers_pd, on="customer_id"))
print(spend.groupby("segment").revenue.agg(["count", "mean"]))

print("\n=== 4. Unmatched keys ===")
partial = customers_pd[customers_pd.customer_id <= 19_000]          # pretend 1,000 customers are missing
check = orders.merge(partial, on="customer_id", how="left")
print(f"orders with no matching customer: {check.city.isna().sum().compute():,}")

print("\n=== 5. Aligned join on a sorted index ===")
left = orders[["customer_id", "revenue"]].set_index("customer_id")
right = dd.from_pandas(customers_pd.set_index("customer_id"), npartitions=4)
print("known divisions:", left.known_divisions, right.known_divisions)
aligned = left.join(right, how="left")
timed("set_index (shuffle) + aligned join + groupby",
      lambda: aligned.groupby("segment").revenue.sum().compute())
print("This time includes the set_index shuffle. The pay-off comes when you reuse the indexed data")
print("for many joins/lookups (save it as Parquet, Lecture 09).")

print("\n=== 6. The duplicate-key trap ===")
dup = pd.concat([customers_pd, customers_pd.head(100)])
bad = orders.merge(dup, on="customer_id")
print(f"rows: {len(orders):,} -> {len(bad):,} (duplicated customers multiplied their orders)")

print("\n=== 7. concat ===")
h1 = orders[orders.timestamp < "2025-07-01"]
h2 = orders[orders.timestamp >= "2025-07-01"]
both = dd.concat([h1, h2])
print("partitions:", h1.npartitions, "+", h2.npartitions, "->", both.npartitions, "| rows:", f"{len(both):,}")
