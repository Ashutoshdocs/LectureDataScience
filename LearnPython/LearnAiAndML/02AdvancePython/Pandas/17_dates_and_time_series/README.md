# Lecture 17: Dates & time series

Run: `python lecture.py`

## Step 1: make it a real date

CSV files store dates as **text**. Convert them first:

```python
sales["date"] = pd.to_datetime(sales["date"])                 # or parse_dates=["date"] in read_csv
pd.to_datetime(s, format="%d/%m/%Y")                          # tell it the format
pd.to_datetime(s, dayfirst=True)                              # 03/04/2025 = 3 April
pd.to_datetime(s, errors="coerce")                            # bad values → NaT
```

| Format code | Means | Example |
|-------------|-------|---------|
| `%Y` / `%y` | 4- / 2-digit year | 2025 / 25 |
| `%m` | month number | 03 |
| `%d` | day | 07 |
| `%b` / `%B` | month name | Mar / March |
| `%H:%M:%S` | time | 14:05:00 |

## Step 2: pull out parts with `.dt`

| Code | Gives |
|------|-------|
| `.dt.year`, `.dt.month`, `.dt.day` | numbers |
| `.dt.month_name()`, `.dt.day_name()` | `"March"`, `"Monday"` |
| `.dt.dayofweek` | 0 = Monday … 6 = Sunday |
| `.dt.quarter` | 1–4 |
| `.dt.isocalendar().week` | week number |
| `.dt.to_period("M")` | `2025-03` (a month label) |
| `.dt.strftime("%d %b %Y")` | format as text |
| `.dt.days` (on a timedelta) | number of days |

## Date maths

```python
sales["date"] + pd.Timedelta(days=7)            # a week later
sales["date"] + pd.DateOffset(months=1)         # a calendar month later
(sales["date"] - customers["joined"]).dt.days   # days between two dates
pd.Timestamp("today")
```

## Filtering by date

```python
sales[sales["date"] >= "2025-07-01"]
sales[sales["date"].between("2025-03-01", "2025-03-31")]
ts = sales.set_index("date").sort_index()
ts.loc["2025-03"]                    # all of March: partial-string indexing
ts.loc["2025-03":"2025-05"]
```

## Time series tools (need a date index)

| Tool | Does | Example |
|------|------|---------|
| `resample("ME")` | group by calendar period | monthly totals |
| `rolling(7)` | moving window | 7-day moving average |
| `shift(1)` | move values down a row | yesterday's value |
| `pct_change()` | % change vs previous row | month-on-month growth |
| `cumsum()` | running total | year-to-date revenue |
| `pd.date_range(start, end, freq)` | generate dates | a full calendar |
| `asfreq("D")` | fill in missing dates | days with no sales |

Common frequency codes: `"D"` day, `"W"` week, `"ME"` month end, `"MS"` month start, `"QE"` quarter end, `"YE"` year end, `"h"` hour.

> pandas 2.2+ uses `"ME"`, `"QE"`, `"YE"`. Older versions used `"M"`, `"Q"`, `"Y"`.

```python
daily = ts["revenue"].resample("D").sum()          # missing days become 0
daily.rolling(7).mean()                            # smooth the noise
monthly = ts["revenue"].resample("ME").sum()
monthly.pct_change() * 100                         # growth %
```

## Exercises

1. Which weekday has the most revenue?
2. Revenue per quarter.
3. Month-on-month growth %. Which month grew the most?
4. A 30-day rolling average of daily revenue. What's its maximum?
5. How many days after joining did each customer place their first order?

<details><summary>Solutions</summary>

```python
sales.groupby(sales["date"].dt.day_name())["revenue"].sum().idxmax()
ts["revenue"].resample("QE").sum()
g = ts["revenue"].resample("ME").sum().pct_change() * 100; g.idxmax()
ts["revenue"].resample("D").sum().rolling(30).mean().max()
first = sales.groupby("customer_id")["date"].min()
(first - customers.set_index("customer_id")["joined"]).dt.days
```
</details>

**Next →** [Lecture 18: Vectorization vs apply](../18_vectorization_vs_apply/)
