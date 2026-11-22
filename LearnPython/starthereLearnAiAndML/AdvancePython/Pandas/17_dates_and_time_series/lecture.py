"""Lecture 17: Dates & time series: to_datetime, .dt, filtering, resample, rolling."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 140)

sales = pd.read_csv(DATA / "sales.csv", parse_dates=["date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
customers = pd.read_csv(DATA / "customers.csv", parse_dates=["joined"])
print("date dtype:", sales["date"].dtype)

print("\n=== Parsing different formats ===")
print(pd.to_datetime(pd.Series(["03/04/2025", "15/08/2025"]), format="%d/%m/%Y").tolist())
print(pd.to_datetime(pd.Series(["03/04/2025"]), dayfirst=True).tolist())
print(pd.to_datetime(pd.Series(["2025-01-15", "not known"]), errors="coerce").tolist())

print("\n=== .dt parts ===")
parts = pd.DataFrame({
    "date": sales["date"],
    "year": sales["date"].dt.year,
    "month": sales["date"].dt.month,
    "month_name": sales["date"].dt.month_name(),
    "weekday": sales["date"].dt.day_name(),
    "quarter": sales["date"].dt.quarter,
    "period": sales["date"].dt.to_period("M"),
    "pretty": sales["date"].dt.strftime("%d %b %Y"),
})
print(parts.head())

print("\n=== Grouping by date parts ===")
by_day = sales.groupby(sales["date"].dt.day_name())["revenue"].sum()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(by_day.reindex(order))
print("best weekday:", by_day.idxmax())

print("\n=== Date maths ===")
print("a week later  :", (sales["date"] + pd.Timedelta(days=7)).iloc[0].date())
print("a month later :", (sales["date"] + pd.DateOffset(months=1)).iloc[0].date())
first_order = sales.groupby("customer_id")["date"].min()
joined = customers.set_index("customer_id")["joined"]
wait = (first_order - joined).dt.days.dropna()
print("days from joining to first order: median", wait.median(), "| min", wait.min(), "| max", wait.max())

print("\n=== Filtering by date ===")
print("from July  :", len(sales[sales["date"] >= "2025-07-01"]), "orders")
print("in March   :", len(sales[sales["date"].between("2025-03-01", "2025-03-31")]), "orders")
ts = sales.set_index("date").sort_index()
print("ts.loc['2025-03'] rows      :", len(ts.loc["2025-03"]))
print("ts.loc['2025-03':'2025-05'] :", len(ts.loc["2025-03":"2025-05"]))

print("\n=== resample ===")
monthly = ts["revenue"].resample("ME").sum()
print(pd.DataFrame({"revenue": monthly,
                    "growth_%": (monthly.pct_change() * 100).round(1),
                    "ytd": monthly.cumsum()}))
print("best growth month:", monthly.pct_change().idxmax().strftime("%B"))
print("\nquarterly:\n", ts["revenue"].resample("QE").sum())
print("\nweekly orders (first 5):\n", ts["order_id"].resample("W").count().head())

print("\n=== rolling and shift ===")
daily = ts["revenue"].resample("D").sum()          # fills days with no orders with 0
print("days in year:", len(daily), "| days with no orders:", (daily == 0).sum())
smooth = pd.DataFrame({"daily": daily, "7d_avg": daily.rolling(7).mean().round(0),
                       "yesterday": daily.shift(1)})
print(smooth.iloc[6:12])
print("max 30-day average:", round(daily.rolling(30).mean().max()))

print("\n=== date_range ===")
print(pd.date_range("2025-01-01", periods=5, freq="MS").strftime("%b %Y").tolist())
