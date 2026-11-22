# Lecture 14 — Statistics

Run: `python lecture.py`

## 1. Basic aggregates

Each can be written as a **method** (`sales.sum()`) or a **function** (`np.sum(sales)`).

| Method | Gives |
|--------|-------|
| `.sum()` | total |
| `.mean()` | average (always a float) |
| `.min()` / `.max()` | smallest / largest value |
| `.argmin()` / `.argmax()` | **position** of smallest / largest |
| `.prod()` | product of all values |
| `np.ptp(a)` | range = max − min ("peak to peak") |

> "**arg**" means "which position". `max()` answers *how much?*, `argmax()` answers *where?*

The `np.` versions also accept plain lists — NumPy converts them for you.

## 2. Spread and robust measures

| Measure | Tells you |
|---------|-----------|
| `np.mean` | average — **sensitive** to extreme values |
| `np.median` | middle value when sorted — **robust** to outliers |
| `.std()` | standard deviation: how spread out values are |
| `.var()` | variance = std² |
| `np.percentile(a, p)` | value below which p% of the data falls |
| `np.quantile(a, q)` | same, with q from 0 to 1 |

### Mean vs median

```
salaries (thousands): 25 28 30 32 35 38 40 250
mean   = 59.75   ← dragged up by one huge salary
median = 33.5    ← barely moves
```

Use the **median** when a few extreme values could distort the mean (house prices, incomes, response times).

> `median` and `percentile` are **functions only**: `np.median(a)`, not `a.median()`.

> `.std()` uses the population formula (divide by N). For the sample standard deviation (divide by N−1), use `.std(ddof=1)`.

## 3. Running totals and changes

| Function | Gives | Length |
|----------|-------|--------|
| `np.cumsum(a)` | running total | same as `a` |
| `np.cumprod(a)` | running product (growth) | same as `a` |
| `np.diff(a)` | difference between neighbours `a[1]-a[0], a[2]-a[1], …` | one shorter |

Everyday tools for time-series data: bank balances, stock prices, step counts, visitors.

## 4. Correlation

`np.corrcoef(x, y)[0, 1]` gives the correlation between −1 and 1.

## Exercises

1. Use the best-day index to look up a day name from `["Mon", …, "Sun"]`.
2. How many days were above the mean?
3. Add another salary of 500 and compare mean and median.
4. Grow Rs 1000 by 10% for 5 years with `1000 * np.cumprod(np.full(5, 1.1))`.
5. Which day had the biggest increase in steps?

<details><summary>Solutions</summary>

```python
days[sales.argmax()]                    # 'Thu'
(sales > sales.mean()).sum()            # 4
# mean jumps to ~108.7, median moves only to 35.0
1000 * np.cumprod(np.full(5, 1.1))      # [1100. 1210. 1331. 1464.1 1610.51]
np.diff(daily_steps).argmax() + 1       # day index 3
```
</details>

**Next →** [Lecture 15: The axis argument](../15_axis_argument/)
