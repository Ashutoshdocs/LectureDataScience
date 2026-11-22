# Lecture 07: Filtering rows

Run: `python lecture.py`

## `filter` + a boolean expression

```python
sales.filter(pl.col("units") >= 4)
```

## Several conditions

```python
sales.filter((pl.col("region") == "South") & (pl.col("units") > 3))   # and
sales.filter((pl.col("product") == "Desk") | (pl.col("product") == "Chair"))   # or
sales.filter(~(pl.col("category") == "Furniture"))                  # not

# Shortcut: several arguments are AND-ed together
sales.filter(pl.col("region") == "South", pl.col("units") > 3)
```

> ⚠️ Brackets around each condition when you use `&` `|`. Python's `and` / `or` raise an error.

## Handy helpers

| Helper | Example |
|--------|---------|
| `.is_in([...])` | `pl.col("product").is_in(["Desk", "Chair"])` |
| `.is_between(a, b)` | `pl.col("unit_price").is_between(1000, 20000)` (inclusive by default) |
| `.str.contains("x")` | `pl.col("product").str.contains("one")` |
| `.str.starts_with("N")` | prefix |
| `.is_null()` / `.is_not_null()` | missing values |
| `.is_duplicated()` / `.is_unique()` | repeats |
| `.is_first_distinct()` | first occurrence of each value |
| keyword shortcut | `sales.filter(region="North", units=5)` (equality only) |

## Counting and fractions without filtering

```python
sales.select((pl.col("units") >= 4).sum())     # how many
sales.select((pl.col("units") >= 4).mean())    # what fraction
```

## Row slicing (no index, just positions)

| Code | Rows |
|------|------|
| `df.head(5)` / `df.tail(5)` | first / last 5 |
| `df.slice(10, 5)` | 5 rows starting at row 10 |
| `df[10:15]` | same, with Python slicing |
| `df.gather_every(10)` | every 10th row |
| `df.sample(n=5, seed=1)` / `df.sample(fraction=0.1)` | random rows |
| `df.top_k(5, by="x")` | 5 largest by `x` |

## Exercises

1. South orders with more than 3 units (both syntaxes).
2. Laptop or Tablet orders, using `is_in`.
3. Orders in March 2025 (`pl.col("date").dt.month() == 3`).
4. What fraction of orders are **not** Electronics?
5. Students missing a maths mark.

<details><summary>Solutions</summary>

```python
sales.filter((pl.col("region") == "South") & (pl.col("units") > 3))
sales.filter(pl.col("product").is_in(["Laptop", "Tablet"]))
sales.filter(pl.col("date").dt.month() == 3)
sales.select((pl.col("category") != "Electronics").mean())
students.filter(pl.col("maths").is_null())
```
</details>

**Next →** [Lecture 08: Adding columns & when/then](../08_adding_columns_when_then/)
