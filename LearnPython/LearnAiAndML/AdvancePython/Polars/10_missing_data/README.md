# Lecture 10: Missing data: `null` (and `NaN`)

Run: `python lecture.py`

## One missing marker for every type

Polars uses **`null`** for missing values in **every** column type: numbers, text, dates, lists.

| | pandas | Polars |
|---|---|---|
| Missing number | `NaN` (turns int columns into float) | `null`. **Int columns stay Int** |
| Missing text | `None` / `NaN` | `null` |
| Missing date | `NaT` | `null` |

## ⚠️ `null` is not `NaN`

`NaN` ("not a number") still exists in Polars, but only as a **floating-point value**, the result of `0 / 0` or `sqrt(-1)`. It's **not** treated as missing:

| | `null` | `NaN` |
|---|---|---|
| Means | value is missing | invalid maths result |
| Types | any | floats only |
| Detect | `.is_null()` | `.is_nan()` |
| Replace | `.fill_null(...)` | `.fill_nan(...)` |
| Skipped by `mean()`/`sum()`? | **yes** | **no**: `mean` becomes `NaN` |

When data comes from pandas or NumPy, convert with `pl.col(pl.Float64).fill_nan(None)`.

## Finding missing values

```python
df.null_count()                                    # per column
df.filter(pl.col("maths").is_null())               # rows where maths is missing
df.filter(pl.any_horizontal(pl.all().is_null()))   # rows with any gap
df.select(pl.col("maths").is_null().mean())        # fraction missing
```

## Dropping

```python
df.drop_nulls()                      # rows with any null
df.drop_nulls(subset=["maths"])      # only if maths is null
```

## Filling

| Code | Fills with |
|------|-----------|
| `pl.col("x").fill_null(0)` | a constant |
| `pl.col("x").fill_null(pl.col("x").mean())` | the column mean (an expression!) |
| `pl.col("x").fill_null(pl.col("x").median())` | median |
| `pl.col("x").fill_null(strategy="forward")` | previous value (time series) |
| `pl.col("x").fill_null(strategy="backward")` | next value |
| `pl.col("x").fill_null(strategy="mean"/"min"/"max"/"zero"/"one")` | built-in strategies |
| `pl.col("x").interpolate()` | straight line between neighbours |
| `pl.col("x").fill_null(pl.col("x").mean().over("class"))` | group mean (Lecture 14) |
| `pl.coalesce("a", "b", pl.lit(0))` | first non-null across columns |
| `df.fill_null(0)` | every column (where the type fits) |

## Exercises

1. Fraction of missing values in each `students` column.
2. Fill every missing mark with that subject's median, in one `with_columns`.
3. Fill missing maths with the **class** average.
4. Show that `mean()` ignores `null` but not `NaN`.

<details><summary>Solutions</summary>

```python
students.select(pl.all().is_null().mean())
students.with_columns(pl.col(marks).fill_null(pl.col(marks).median()))
students.with_columns(pl.col("maths").fill_null(pl.col("maths").mean().over("class")))
pl.Series([1.0, None, 3.0]).mean()          # 2.0
pl.Series([1.0, float("nan"), 3.0]).mean()  # nan
```
</details>

**Next →** [Lecture 11: Data types & casting](../11_data_types_and_casting/)
