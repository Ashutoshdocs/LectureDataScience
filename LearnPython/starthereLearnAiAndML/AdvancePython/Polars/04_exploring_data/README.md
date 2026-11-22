# Lecture 04: Exploring data

Run: `python lecture.py`

## The exploration toolkit

| Command | Answers |
|---------|---------|
| `df.head(n)` / `df.tail(n)` / `df.sample(n)` | What do rows look like? |
| `df.shape`, `df.columns`, `df.schema` | Size, names, types |
| **`df.glimpse()`** | Every column on one line: type + first values. Great for wide tables |
| `df.describe()` | count, null_count, mean, std, min, quartiles, max (all columns) |
| `df.null_count()` | Missing values per column |
| `df["c"].value_counts(sort=True)` | Frequency of each value |
| `df["c"].unique()` / `df["c"].n_unique()` | Distinct values / how many |
| `df.n_unique()` / `df.is_duplicated().sum()` | Unique rows / duplicate rows |
| `df.estimated_size("kb")` | Memory used |
| `df.select(pl.corr("a", "b"))` | Correlation |

## Display settings

```python
pl.Config.set_tbl_rows(20)        # rows shown
pl.Config.set_tbl_cols(12)        # columns shown
pl.Config.set_fmt_str_lengths(50) # long text
with pl.Config(tbl_rows=-1):      # temporarily show everything
    print(df)
```

## The new-dataset checklist

1. `shape` and `glimpse()`: size and types right? Dates parsed?
2. `null_count()`: where are the gaps?
3. `describe()`: impossible min/max values?
4. `value_counts()` on each text column: typos, inconsistent case?
5. `is_duplicated().sum()`: repeated rows?

## Exercises

1. Which region has the most orders?
2. What fraction of orders are Electronics? (`value_counts(normalize=True)`)
3. How many different customers ordered?
4. Which `students` columns have missing values?

<details><summary>Solutions</summary>

```python
sales["region"].value_counts(sort=True).row(0)
sales["category"].value_counts(normalize=True)
sales["customer_id"].n_unique()
students.null_count()
```
</details>

**Next →** [Lecture 05: Expressions, the core idea](../05_expressions_the_core_idea/)
