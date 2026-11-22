# Lecture 12: Time series with Dask

Run: `python lecture.py`

Time-series data (logs, sensors, transactions) is one of Dask's best fits: it's usually huge, append-only and naturally split by time.

## Step 1: a sorted datetime index with known divisions

```python
ddf = dd.read_parquet("sales/")                         # already in time order
ddf = ddf.set_index("timestamp", sorted=True)           # cheap: just records divisions
ddf.known_divisions                                     # True
```

Most time-series features need this:

| Feature | Needs a datetime index with known divisions? |
|---------|----------------------------------------------|
| `.dt.month`, `.dt.hour`, … on a column | no |
| `groupby(ddf.timestamp.dt.month)` | no |
| `ddf.loc["2025-03"]` (fast time slicing) | **yes** |
| `ddf.resample("1D").sum()` | **yes** |
| `ddf.rolling("7D").mean()` (time-based windows) | **yes** |
| `ddf.rolling(50).mean()` (row-based windows) | no (neighbouring rows are borrowed across partitions) |

## Resampling

```python
daily = ddf.revenue.resample("1D").sum()          # still Dask: one value per day
monthly = ddf.revenue.resample("MS").sum().compute()   # see the gotcha below
weekly_orders = ddf.order_id.resample("W").count()
```

Frequency codes (pandas): `"h"` hour, `"D"` day, `"W"` week, `"MS"` month start, `"ME"` month end, `"QE"` quarter end.

> ⚠️ **Resample gotcha.** Dask resamples each partition separately, so each output bin must fit inside the partition boundaries. Here each partition starts at the **first order of the month** (e.g. `2025-02-01 00:00:11`), not exactly midnight. Month-**end** bins (`"ME"`) then straddle partitions, and Dask raises:
> ```
> ValueError: Index is not contained within new index. This can often be resolved by using larger partitions…
> ```
> Fixes (both in `lecture.py`):
> - use month-**start** labels: `resample("MS")` ✅
> - resample to **days** in Dask (`"1D"` always works), then `.compute()` and resample to months in pandas ✅

Typical pattern: **resample in Dask** (shrinks millions of rows to hundreds), **then compute** and continue in pandas (`pct_change`, plots).

## Rolling windows across partition boundaries

A 7-day window near the start of February needs the end of January, which sits in another partition. Dask handles this with **overlap**: each partition borrows the rows it needs from its neighbour before computing.

```
 partition Jan            partition Feb
 [ ......... last 7 days ] [ first 7 days ......... ]
                    └──── borrowed ────┘
```

You can use the same mechanism for your own functions:

```python
ddf.map_overlap(my_func, before=7, after=0)                    # borrow 7 ROWS from the previous partition
ddf.map_overlap(my_func, before=pd.Timedelta("8D"), after=0)   # or a TIME span (make it a bit wider than you need)
```

`lecture.py` compares the two on daily revenue: with `map_partitions`, the first week of each month gets `NaN` for "change vs a week ago" because February can't see January. With `map_overlap(before=7)` the values are filled in.

## Exercises

1. Monthly revenue and month-on-month growth (resample in Dask, `pct_change` in pandas).
2. Hourly order count: which hour of the day is busiest?
3. 7-day rolling mean of **daily** revenue.
4. All orders on 14 February 2025, using `.loc`.

<details><summary>Solutions</summary>

See `lecture.py` sections 2–5.
</details>

**Next →** [Lecture 13: Schedulers & LocalCluster](../13_schedulers_and_local_cluster/)
