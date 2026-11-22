# Lecture 17: Dates & time series

Run: `python lecture.py`

## Getting real dates

```python
pl.read_csv("sales.csv", try_parse_dates=True)              # at load time
pl.col("date").str.to_date("%Y-%m-%d")                      # from text
pl.col("date").str.to_date("%d/%m/%Y", strict=False)        # bad values → null
pl.col("ts").str.to_datetime("%Y-%m-%d %H:%M:%S")
pl.date(2025, 3, 1)                                         # a literal date inside expressions
pl.date_range(pl.date(2025, 1, 1), pl.date(2025, 12, 31), "1d", eager=True)
```

| Type | Holds |
|------|-------|
| `Date` | a calendar day |
| `Datetime("us")` | date + time (optionally with time zone) |
| `Duration` | a length of time (the result of subtracting dates) |
| `Time` | time of day only |

## The `.dt` namespace

| Expression | Gives |
|------------|-------|
| `.dt.year()`, `.dt.month()`, `.dt.day()` | numbers |
| `.dt.quarter()`, `.dt.week()`, `.dt.ordinal_day()` | calendar parts |
| `.dt.weekday()` | **1 = Monday … 7 = Sunday** (pandas uses 0–6!) |
| `.dt.strftime("%b")`, `.dt.to_string("%d %b %Y")` | text |
| `.dt.truncate("1mo")` | round **down** to the start of the month / week (`"1w"`) / quarter (`"1q"`) |
| `.dt.month_start()` / `.dt.month_end()` | first / last day of the month |
| `.dt.offset_by("1mo")` | calendar-aware shift (`"7d"`, `"-1y"`) |
| `.dt.total_days()` | on a Duration: number of days |
| `.dt.epoch("s")` | seconds since 1970 |

Duration strings: `"1d"` day, `"1w"` week, `"1mo"` month, `"1q"` quarter, `"1y"` year, `"1h"`, `"30m"`, `"10s"`.

## Date maths

```python
pl.col("date") - pl.col("joined")                     # a Duration
(pl.col("date") - pl.col("joined")).dt.total_days()   # as a number
pl.col("date").dt.offset_by("1mo")                    # one calendar month later
```

## Filtering

```python
df.filter(pl.col("date") >= pl.date(2025, 7, 1))
df.filter(pl.col("date").is_between(pl.date(2025, 3, 1), pl.date(2025, 3, 31)))
df.filter(pl.col("date").dt.month() == 3)
```

## Time-series grouping: `group_by_dynamic`

Like pandas `resample`. Groups rows into **calendar windows**:

```python
(sales.sort("date")
      .group_by_dynamic("date", every="1mo")        # monthly buckets
      .agg(pl.col("revenue").sum()))
```

Options: `every` (window step), `period` (window length, if different), `by` (separate series per group), `label` (`"left"`/`"right"`), `closed`. The column **must be sorted**.

The simpler alternative is `group_by(pl.col("date").dt.truncate("1mo"))`.

## Rolling windows

| Expression | Does |
|------------|------|
| `pl.col("x").rolling_mean(window_size=7)` | 7-**row** moving average |
| `pl.col("x").rolling_sum(7)`, `rolling_max`, `rolling_std` | other stats |
| `df.rolling("date", period="30d").agg(...)` | **time-based** window: last 30 *days*, not rows |
| `.shift(1)`, `.diff()`, `.pct_change()` | previous value, change, % change |
| `.cum_sum()` | running total |

## Filling gaps in a daily series

Days with no orders simply don't exist as rows. Build a full calendar and join:

```python
calendar = pl.DataFrame({"date": pl.date_range(start, end, "1d", eager=True)})
calendar.join(daily, on="date", how="left").fill_null(0)
```

or use `df.upsample("date", every="1d")`.

## Exercises

1. Which weekday has the most revenue?
2. Revenue per quarter.
3. Month-on-month growth %. Which month grew most?
4. 30-day rolling average of daily revenue (with gaps filled). What's the maximum?
5. Days between a customer joining and their first order.

<details><summary>Solutions</summary>

```python
sales.group_by(pl.col("date").dt.strftime("%A")).agg(pl.col("revenue").sum()).sort("revenue").tail(1)
sales.group_by(pl.col("date").dt.quarter()).agg(pl.col("revenue").sum())
monthly.with_columns(growth=pl.col("revenue").pct_change() * 100)
daily_full.with_columns(pl.col("revenue").rolling_mean(30)).max()
(first_order - joined).dt.total_days()
```
</details>

**Next →** [Lecture 18: Lazy API & query optimisation](../18_lazy_api_query_optimization/)
