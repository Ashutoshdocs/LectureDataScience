# Lecture 06: Selecting columns

Run: `python lecture.py`

## `select`: choose (and compute) columns

```python
df.select("name", "maths")                    # by name
df.select(["name", "maths"])                  # a list works too
df.select(pl.col("name"), pl.col("maths") / 10)
df.select(pl.all().exclude("gender"))         # everything except
df.drop("gender")                             # same result
```

`df["maths"]` returns a **Series**. `df.select("maths")` returns a one-column **DataFrame**.

## Selecting by pattern or type

| Code | Selects |
|------|---------|
| `pl.col(pl.Int64)` | all Int64 columns |
| `pl.col(pl.Float64, pl.Int64)` | several types |
| `pl.col("^.*_id$")` | regex: names ending in `_id` (must start with `^` and end with `$`) |
| `pl.all()` | every column |
| `pl.all().exclude("a", "b")` | all except some |

## Selectors: `import polars.selectors as cs`

Selectors are a cleaner way to pick columns by **kind** and can be combined like sets:

| Selector | Picks |
|----------|-------|
| `cs.numeric()` | ints and floats |
| `cs.string()` | text |
| `cs.temporal()` / `cs.date()` | dates/times |
| `cs.boolean()` | true/false |
| `cs.starts_with("m")`, `cs.ends_with("_id")`, `cs.contains("price")` | by name |
| `cs.by_name("a", "b")` | exact names |
| `cs.first()`, `cs.last()` | first / last column |
| `cs.numeric() - cs.by_name("order_id")` | set difference |
| `cs.string() \| cs.date()` | union |
| `~cs.numeric()` | everything *not* numeric |

```python
df.select(cs.numeric().mean())         # mean of every numeric column
df.with_columns(cs.string().str.to_uppercase())
```

## Renaming and reordering

```python
df.rename({"unit_price": "price"})
df.rename(str.upper)                               # function applied to every name
df.select(pl.col("units").alias("qty"))
df.select("date", "product", pl.all().exclude("date", "product"))   # move columns to the front
pl.col("maths", "cs").name.prefix("mark_")         # rename many: prefix / suffix / map
```

## Exercises

1. Select every numeric column of `sales` except `order_id` and `customer_id`.
2. Select all text columns and convert them to upper case.
3. In `students`, compute the max of every column whose name doesn't start with `n`, `c` or `g`.
4. Rename every column to Title Case.

<details><summary>Solutions</summary>

```python
sales.select(cs.numeric() - cs.ends_with("_id"))
sales.select(cs.string().str.to_uppercase())
students.select((cs.numeric()).max())
sales.rename(str.title)
```
</details>

**Next →** [Lecture 07: Filtering rows](../07_filtering_rows/)
