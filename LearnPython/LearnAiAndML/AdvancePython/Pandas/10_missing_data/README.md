# Lecture 10: Missing data

Run: `python lecture.py`

Real data always has gaps: a sensor failed, a form field was skipped, a merge found no match.

## How pandas shows "missing"

| Marker | Where you see it |
|--------|------------------|
| `NaN` | numeric columns (from NumPy: "Not a Number") |
| `None` / `NaN` | text columns |
| `NaT` | date columns ("Not a Time") |
| `<NA>` | nullable dtypes like `Int64`, `boolean` (Lecture 11) |

All of them are detected by the same functions.

> ⚠️ An integer column with a missing value becomes **float** (`78` → `78.0`), because plain NumPy ints can't hold `NaN`. Use the nullable `Int64` type to keep integers (Lecture 11).

## Finding missing values

| Code | Gives |
|------|-------|
| `df.isna()` | True/False for every cell |
| `df.isna().sum()` | missing count per column |
| `df.isna().mean()` | missing **fraction** per column |
| `df.isna().any(axis=1)` | rows with at least one gap |
| `df[df["col"].isna()]` | the rows where `col` is missing |
| `df.notna()` | the opposite |

> ⚠️ Don't test with `== np.nan`. `NaN == NaN` is `False`. Always use `isna()`.

## Statistics skip missing values

`mean`, `sum`, `max` and the rest ignore `NaN` by default (`skipna=True`). `count()` counts only non-missing values.

## Three strategies

### 1. Drop
```python
df.dropna()                     # rows with ANY missing value
df.dropna(subset=["maths"])     # only if maths is missing
df.dropna(thresh=6)             # keep rows with at least 6 non-missing values
df.dropna(axis=1)               # drop COLUMNS with missing values
```
Use when the gaps are few and random.

### 2. Fill with a value
```python
df["maths"].fillna(0)                          # a constant
df["maths"].fillna(df["maths"].mean())         # column mean
df["maths"].fillna(df["maths"].median())       # median: robust to outliers
df.fillna({"maths": 0, "english": 50})         # per-column values
df["city"].fillna("Unknown")                   # text
```

### 3. Fill from neighbours / groups
```python
s.ffill()          # carry the last known value forward (time series)
s.bfill()          # pull the next value backward
s.interpolate()    # straight line between known values
df["maths"].fillna(df.groupby("class")["maths"].transform("mean"))   # class average
```

## Choosing a strategy

| Situation | Good choice |
|-----------|-------------|
| A few rows missing, lots of data | `dropna` |
| Numeric, roughly symmetric | `fillna(mean)` |
| Numeric with outliers | `fillna(median)` |
| Category / text | `fillna("Unknown")` or the most common value |
| Time series (prices, sensors) | `ffill` or `interpolate` |
| Values depend on a group | group mean/median with `transform` |
| "Missing" itself means something | keep it, or add a flag column `df["maths_missing"] = df["maths"].isna()` |

## Exercises

1. What fraction of the `students` table is missing overall?
2. Drop students missing **any** mark. How many remain?
3. Fill missing marks with each subject's median.
4. Fill missing maths with the class average.

<details><summary>Solutions</summary>

```python
students.isna().to_numpy().mean()
len(students.dropna())             # 9
marks = ["maths", "science", "english", "cs"]
students[marks].fillna(students[marks].median())
students["maths"].fillna(students.groupby("class")["maths"].transform("mean"))
```
</details>

**Next →** [Lecture 11: Data types](../11_data_types/)
