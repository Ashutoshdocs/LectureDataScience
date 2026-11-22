# Lecture 11: Data types (dtypes)

Run: `python lecture.py`

Every column has one dtype. Wrong types cause silent bugs: `"10" + "5"` is `"105"`, text dates don't sort by time, and numbers stored as text can't be summed.

## Common dtypes

| dtype | Holds | Example |
|-------|-------|---------|
| `int64` | whole numbers | units |
| `float64` | decimals, and ints that have `NaN` | marks |
| `str` (pandas 3) / `object` (pandas 2) | text | names |
| `bool` | True/False | passed |
| `datetime64[us]` (pandas 3) / `datetime64[ns]` (pandas 2) | dates & times | order date |
| `timedelta64` | durations | delivery time |
| `category` | repeated labels from a small set | region, grade |
| `Int64`, `Float64`, `boolean`, `string` | **nullable** versions that allow `<NA>` | ints with gaps |

## Converting

| Code | Use |
|------|-----|
| `df["c"].astype(int)` | safe conversion when every value is valid |
| `df["c"].astype("Int64")` | integers **with** missing values |
| `pd.to_numeric(df["c"], errors="coerce")` | text → numbers; bad values become `NaN` |
| `pd.to_datetime(df["c"], errors="coerce")` | text → dates; bad values become `NaT` |
| `df["c"].astype("category")` | repeated labels |
| `df["c"].astype(str)` | anything → text |
| `df.convert_dtypes()` | let pandas pick the best nullable types |

> `errors="coerce"` is your friend for messy data. It turns anything unparseable into a missing value instead of crashing. Then you can **count** how many failed with `.isna().sum()`.

## Cleaning numbers stored as text

```python
s = pd.Series(["12,500", "8,200", "n/a", "15,000"])
pd.to_numeric(s.str.replace(",", ""), errors="coerce")   # [12500, 8200, NaN, 15000]
```

## Why `category`?

A column like `region` repeats 4 values across 240 rows. As `category`, pandas stores each label **once** plus small integer codes:

- **Less memory** (often 5–10× smaller on big data)
- **Faster** groupby and sorting
- **Custom order**: `pd.Categorical(col, categories=["low", "mid", "high"], ordered=True)` lets `"low" < "high"` work, and sorting follows your order instead of A→Z.

## Checking memory

```python
df.info(memory_usage="deep")
df.memory_usage(deep=True)
```

## Exercises

1. Convert `customer_id` in sales to `str`. Why might an ID column be better as text?
2. Convert `region` to `category` and compare memory.
3. Make an ordered category `["small", "medium", "large"]` and sort by it.
4. Convert `["1", "2", "x", None]` to nullable integers.

<details><summary>Solutions</summary>

1. IDs aren't quantities: you never add or average them, and leading zeros (`"007"`) must survive.
3. `pd.Categorical(col, categories=[...], ordered=True)` then `sort_values`.
4. `pd.to_numeric(s, errors="coerce").astype("Int64")` → `[1, 2, <NA>, <NA>]`
</details>

**Next →** [Lecture 12: String methods](../12_string_methods/)
