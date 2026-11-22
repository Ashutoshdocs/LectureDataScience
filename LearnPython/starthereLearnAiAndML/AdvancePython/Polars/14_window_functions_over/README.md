# Lecture 14: Window functions with `.over()`

Run: `python lecture.py`

## The problem

`group_by().agg()` gives **one row per group**. But often you want the group value **on every original row**:

- each order vs its region's average
- each order's share of its category's revenue
- rank students *within* their class
- running total *per* customer

## `.over()`: group-wise, without losing rows

Add `.over("group_col")` to any expression. It's computed per group, then **broadcast back** to every row of that group:

```python
sales.with_columns(
    region_avg=pl.col("revenue").mean().over("region"),
)
```

```
 region  revenue   region_avg
 North    50000      39143     ← North's average on every North row
 West      6000      44076
 East      3500      36513
 West     75000      44076
```

That's like pandas' `groupby().transform()`, but it fits into any expression.

## Common patterns

| Goal | Expression |
|------|-----------|
| Group mean on every row | `pl.col("x").mean().over("g")` |
| Difference from group mean | `pl.col("x") - pl.col("x").mean().over("g")` |
| Share of group total | `pl.col("x") / pl.col("x").sum().over("g")` |
| Rank within group | `pl.col("x").rank("min", descending=True).over("g")` |
| Running total within group | `pl.col("x").cum_sum().over("g")` |
| Previous value within group | `pl.col("x").shift(1).over("g")` |
| Row number within group | `pl.int_range(pl.len()).over("g")` |
| Rows in group | `pl.len().over("g")` |
| Several group columns | `.over("region", "category")` |
| Fill nulls with group mean | `pl.col("x").fill_null(pl.col("x").mean().over("g"))` |

## Top-N per group (no join needed)

```python
sales.filter(pl.col("revenue").rank("ordinal", descending=True).over("region") <= 2)
```

## Ordering inside a window

Running totals and `shift` depend on row order. Sort first, or use `order_by`:

```python
pl.col("revenue").cum_sum().over("customer_id", order_by="date")
```

## Exercises

1. Add each order's revenue as a % of its category total.
2. Rank students within their class by total marks.
3. Keep only the top 2 orders per region.
4. For each customer, the number of days since their previous order.

<details><summary>Solutions</summary>

```python
(pl.col("revenue") / pl.col("revenue").sum().over("category") * 100)
pl.col("total").rank("min", descending=True).over("class")
sales.filter(pl.col("revenue").rank("ordinal", descending=True).over("region") <= 2)
pl.col("date").diff().over("customer_id", order_by="date").dt.total_days()
```
</details>

**Next →** [Lecture 15: Joins & concat](../15_joins_and_concat/)
