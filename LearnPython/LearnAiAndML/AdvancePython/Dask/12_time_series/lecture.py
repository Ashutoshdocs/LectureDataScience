"""Lecture 12: Time series: datetime index, .loc slicing, resample, rolling, map_overlap."""
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

raw = dd.read_parquet(ensure_big_parquet())
raw = raw.assign(revenue=raw.units * raw.unit_price)

print("=== 1. Sorted datetime index ===")
ts = raw.set_index("timestamp", sorted=True).persist()
print("known_divisions:", ts.known_divisions, "| partitions:", ts.npartitions)
print("partition 0 covers", ts.divisions[0], "->", ts.divisions[1])

print("\n=== 2. Time slicing with .loc ===")
t = time.perf_counter()
valentine = ts.loc["2025-02-14"].compute()
print(f"orders on 14 Feb: {len(valentine):,} ({(time.perf_counter() - t) * 1000:.0f} ms, 1 partition read)")
q2 = ts.loc["2025-04":"2025-06"]
print("Q2 partitions:", q2.npartitions, "| Q2 revenue: Rs", f"{q2.revenue.sum().compute():,.0f}")

print("\n=== 3. Resample: millions of rows -> a small table, then pandas ===")
try:
    ts.revenue.resample("ME").sum().compute()                # month-END labels
except ValueError as e:
    print("resample('ME') failed:", str(e)[:60], "...")
    print("  -> partitions start a few seconds into each month, so month-END bins straddle them.")
monthly = ts.revenue.resample("MS").sum().compute()           # month-START labels work: 12 numbers
alt = ts.revenue.resample("1D").sum().compute().resample("ME").sum()   # or: days in Dask, months in pandas
print("'MS' in Dask and 'D' in Dask + 'ME' in pandas agree:", (monthly.to_numpy() == alt.to_numpy()).all())
report = pd.DataFrame({"revenue_cr": monthly / 1e7, "growth_%": monthly.pct_change() * 100})
report.index = report.index.strftime("%b")
print(report)
print("best growth month:", report["growth_%"].idxmax())

weekly = ts.order_id.resample("W").count().compute()
print("weekly orders, first 4:", weekly.head(4).tolist())

print("\n=== 4. Busiest hour (no index needed) ===")
by_hour = raw.groupby(raw.timestamp.dt.hour).order_id.count().compute().sort_index()
print("busiest hour:", by_hour.idxmax(), "| quietest:", by_hour.idxmin(),
      "| range:", f"{by_hour.min():,}-{by_hour.max():,} orders")

print("\n=== 5. Rolling windows ===")
daily = ts.revenue.resample("1D").sum()                     # still Dask, ~365 rows
daily_df = daily.to_frame("revenue")
daily_df["roll_7d"] = daily_df.revenue.rolling("7D").mean()  # time-based window across partitions
out = daily_df.compute()
print(out.loc["2025-01-28":"2025-02-05"])                     # crosses the Jan/Feb partition boundary

print("\n=== 6. Row-based rolling over the raw orders ===")
roll50 = ts.revenue.rolling(50).mean()
first, boundary = dask.compute(roll50.head(55, compute=False), roll50.loc["2025-02-01 00:00":"2025-02-01 00:05"])
print("NaN rows at the very start (a 50-row window needs 49 earlier rows):", first.isna().sum())
print("rows just after the Jan/Feb boundary have values:", boundary.notna().all())

print("\n=== 7. map_overlap for your own function ===")
def change_vs_week_ago(df):
    return df.assign(vs_week=df.revenue - df.revenue.shift(7))     # 7 rows = 7 days here

no_overlap = daily_df[["revenue"]].map_partitions(change_vs_week_ago, meta={"revenue": "f8", "vs_week": "f8"})
with_overlap = daily_df[["revenue"]].map_overlap(change_vs_week_ago, before=7, after=0,
                                                meta={"revenue": "f8", "vs_week": "f8"})
a, b = dask.compute(no_overlap.loc["2025-02-01":"2025-02-03"], with_overlap.loc["2025-02-01":"2025-02-03"])
print("map_partitions (Feb can't see January):")
print(a)
print("map_overlap(before=7) borrows the last 7 January rows:")
print(b)
