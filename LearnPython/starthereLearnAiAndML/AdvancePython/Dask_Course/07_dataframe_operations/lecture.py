"""Lecture 07: DataFrame operations: the pandas API, lazily, and the parts that differ."""
import sys
from pathlib import Path
import dask
import dask.dataframe as dd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data          # noqa: E402

BIG = ensure_big_data()
ddf = dd.read_csv(BIG / "sales_2025-*.csv", parse_dates=["timestamp"], dtype={"units": "float64"})

print("=== 1. Select & filter ===")
print(ddf[["timestamp", "product", "units"]].head(3))
bulk = ddf[ddf.units >= 4]
print("bulk orders:", f"{len(bulk):,}")
north_big = ddf.query("region == 'North' and units >= 4")
furniture = ddf[ddf["product"].isin(["Desk", "Chair", "Lamp"])]
mid_price = ddf[ddf.unit_price.between(1000, 20000)]
n1, n2, n3 = dask.compute(len(north_big), len(furniture), len(mid_price))   # one pass for three answers
print(f"North & units>=4: {n1:,} | furniture: {n2:,} | price 1k-20k: {n3:,}")

print("\n=== 2. New columns ===")
ddf = ddf.assign(
    revenue=ddf.units * ddf.unit_price,
    month=ddf.timestamp.dt.month,
    weekday=ddf.timestamp.dt.day_name(),
    code=ddf["product"].str.upper().str[:3],
)
ddf["with_gst"] = ddf.revenue * 1.18
print(ddf[["product", "units", "unit_price", "revenue", "with_gst", "month", "weekday", "code"]].head(3))

print("\n=== 3. Conditional columns (where / mask) ===")
ddf["size"] = "single"
ddf["size"] = ddf["size"].mask(ddf.units >= 4, "bulk")
ddf["discount"] = (ddf.revenue * 0.1).where(ddf.category == "Electronics", 0)
print(ddf[["category", "units", "size", "revenue", "discount"]].head(4))
print(ddf["size"].value_counts().compute())

print("\n=== 4. Missing values ===")
missing = ddf.units.isna().sum().compute()
print(f"missing units: {missing:,} ({missing / len(ddf):.2%})")
sample_median = ddf.units.sample(frac=0.05, random_state=1).compute().median()
ddf["units_filled"] = ddf.units.fillna(sample_median)
print("filled with sample median", sample_median, "-> missing now:", ddf.units_filled.isna().sum().compute())
print("dropna rows:", f"{len(ddf.dropna(subset=['units'])):,}")

print("\n=== 5. Reductions & summaries (one pass with dask.compute) ===")
total, avg, n_customers, by_size = dask.compute(
    ddf.revenue.sum(), ddf.revenue.mean(), ddf.customer_id.nunique(), ddf["size"].value_counts())
print(f"revenue Rs {total:,.0f} | avg order Rs {avg:,.0f} | customers {n_customers:,}")
print(ddf[["units", "unit_price", "revenue"]].describe().compute().round(1))

print("\n=== 6. Top N & approximate quantiles ===")
march = ddf[ddf.month == 3]
print(march.nlargest(5, "revenue")[["order_id", "timestamp", "product", "revenue"]].compute())
print("median revenue (approximate):", ddf.revenue.median_approximate().compute())
print("quantiles (approximate):", ddf.revenue.quantile([0.25, 0.75]).compute().tolist())
print(ddf.groupby("weekday").revenue.mean().compute().round(0).sort_values(ascending=False))

print("\n=== 7. What's different from pandas ===")
try:
    ddf.iloc[5]
except NotImplementedError as e:
    print("ddf.iloc[5] ->", str(e)[:80])
print("Dask's own iloc only selects COLUMNS:", list(ddf.iloc[:, :2].columns))
