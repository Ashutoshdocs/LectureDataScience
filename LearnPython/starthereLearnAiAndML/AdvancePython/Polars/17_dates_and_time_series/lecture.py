"""Lecture 17: Dates & time series: parsing, .dt, date maths, group_by_dynamic, rolling."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(160)
pl.Config.set_tbl_cols(12)

sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price"))
           .sort("date"))
customers = pl.read_csv(DATA / "customers.csv", try_parse_dates=True)
print("date dtype:", sales.schema["date"], "| joined dtype:", customers.schema["joined"])

print("\n=== Parsing text ===")
print(pl.DataFrame({"raw": ["03/04/2025", "15/08/2025", "bad"]})
        .with_columns(d=pl.col("raw").str.to_date("%d/%m/%Y", strict=False)))
print(pl.DataFrame({"raw": ["2025-01-15 09:30", "2025-01-15 18:05"]})
        .with_columns(ts=pl.col("raw").str.to_datetime("%Y-%m-%d %H:%M"))
        .with_columns(hour=pl.col("ts").dt.hour()))

print("\n=== .dt parts ===")
print(sales.select(
    "date",
    year=pl.col("date").dt.year(),
    month=pl.col("date").dt.month(),
    month_name=pl.col("date").dt.strftime("%B"),
    weekday=pl.col("date").dt.weekday(),
    day_name=pl.col("date").dt.strftime("%A"),
    quarter=pl.col("date").dt.quarter(),
    month_start=pl.col("date").dt.truncate("1mo"),
    pretty=pl.col("date").dt.to_string("%d %b %Y"),
).head(4))

print("\n=== Revenue by weekday ===")
by_day = (sales.group_by(wd=pl.col("date").dt.weekday(), day=pl.col("date").dt.strftime("%A"))
               .agg(pl.col("revenue").sum()).sort("wd"))
print(by_day)
print("best weekday:", by_day.sort("revenue").row(-1, named=True)["day"])

print("\n=== Date maths ===")
print(sales.select("date",
                   week_later=pl.col("date") + pl.duration(days=7),
                   month_later=pl.col("date").dt.offset_by("1mo"),
                   month_end=pl.col("date").dt.month_end()).head(3))
first = sales.group_by("customer_id").agg(first_order=pl.col("date").min())
wait = (first.join(customers, on="customer_id")
             .with_columns(days=(pl.col("first_order") - pl.col("joined")).dt.total_days()))
print(wait.select(pl.col("days").median().alias("median"), pl.col("days").min().alias("min"),
                  pl.col("days").max().alias("max")))

print("\n=== Filtering ===")
print("from July :", sales.filter(pl.col("date") >= pl.date(2025, 7, 1)).height)
print("March     :", sales.filter(pl.col("date").is_between(pl.date(2025, 3, 1), pl.date(2025, 3, 31))).height)

print("\n=== group_by_dynamic: monthly ===")
monthly = (sales.group_by_dynamic("date", every="1mo")
                .agg(orders=pl.len(), revenue=pl.col("revenue").sum())
                .with_columns(growth_pct=(pl.col("revenue").pct_change() * 100).round(1),
                              ytd=pl.col("revenue").cum_sum()))
print(monthly)
best = monthly.drop_nulls("growth_pct").sort("growth_pct").row(-1, named=True)
print("best growth:", best["date"].strftime("%B"), f"(+{best['growth_pct']}%)")

print("\n=== Quarterly, and weekly per region ===")
print(sales.group_by_dynamic("date", every="1q").agg(pl.col("revenue").sum()))
print(sales.group_by_dynamic("date", every="1w", group_by="region")
           .agg(orders=pl.len()).sort("region", "date").head(4))

print("\n=== Filling gaps: a full daily calendar ===")
daily = sales.group_by("date").agg(pl.col("revenue").sum())
calendar = pl.DataFrame({"date": pl.date_range(pl.date(2025, 1, 1), pl.date(2025, 12, 31), "1d", eager=True)})
daily_full = calendar.join(daily, on="date", how="left").with_columns(pl.col("revenue").fill_null(0))
print("days with orders:", daily.height, "| full calendar:", daily_full.height,
      "| empty days:", (daily_full["revenue"] == 0).sum())

print("\n=== Rolling windows ===")
smooth = daily_full.with_columns(
    avg_7d=pl.col("revenue").rolling_mean(window_size=7).round(0),
    yesterday=pl.col("revenue").shift(1),
    change=pl.col("revenue").diff(),
)
print(smooth.slice(6, 6))
print("max 30-day average:", round(daily_full["revenue"].rolling_mean(30).max()))

print("\n=== Time-based rolling (last 30 days, uneven rows) ===")
print(daily.sort("date").rolling("date", period="30d")
           .agg(rev_30d=pl.col("revenue").sum(), order_days=pl.len()).tail(3))
