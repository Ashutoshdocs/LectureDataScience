# Lecture 13: Group by & aggregation

Run: `python lecture.py`

## The pattern

```python
sales.group_by("region").agg(
    pl.col("revenue").sum(),
)
```

Split the rows by `region` → run each expression inside `agg` on each group → combine into one row per group. Groups are processed **in parallel**.

> ⚠️ **Group order is not guaranteed** (that's part of why it's fast). Add `.sort(...)` afterwards, or pass `maintain_order=True` to keep first-seen order.

## Anything inside `agg` is an expression

So you can do far more than `sum` and `mean`:

```python
sales.group_by("region").agg(
    orders=pl.len(),                                        # rows per group
    revenue=pl.col("revenue").sum(),
    avg_order=pl.col("revenue").mean().round(0),
    biggest=pl.col("revenue").max(),
    customers=pl.col("customer_id").n_unique(),
    bulk_orders=(pl.col("units") >= 4).sum(),               # conditional count
    furniture_rev=pl.col("revenue").filter(pl.col("category") == "Furniture").sum(),  # conditional sum
    top_product=pl.col("product").sort_by("revenue").last(),   # product of the biggest order
    products=pl.col("product").unique().sort(),             # a LIST per group
)
```

## Aggregation functions

`sum mean median min max std var count len n_unique first last quantile(0.9)`, plus anything that ends in a single value per group.

Without an aggregation, `agg(pl.col("x"))` returns **a list of all values** in each group. That's handy, and it's a hint you forgot `.sum()`!

## Several keys / expression keys

```python
sales.group_by("region", "category").agg(...)
sales.group_by(pl.col("date").dt.month().alias("month")).agg(...)   # group by a computed key
```

## Quick shortcuts

```python
sales.group_by("region").len()             # counts
sales.group_by("region").sum()             # sum every other column
sales["region"].value_counts()             # same as counting
```

## Filtering groups (like SQL `HAVING`)

```python
(sales.group_by("customer_id").agg(orders=pl.len())
      .filter(pl.col("orders") >= 9))
```

## Iterating over groups (rarely needed)

```python
for (region,), part in sales.group_by("region"):
    print(region, part.height)
```

## Exercises

1. Units sold per product, highest first.
2. Average order revenue per category × region.
3. For each region: orders, revenue, largest order, and the share of bulk orders.
4. Customers who spent more than Rs 3,00,000.
5. For each category, the list of distinct products.

<details><summary>Solutions</summary>

```python
sales.group_by("product").agg(pl.col("units").sum()).sort("units", descending=True)
sales.group_by("category", "region").agg(pl.col("revenue").mean())
sales.group_by("region").agg(pl.len(), pl.col("revenue").sum(), pl.col("revenue").max(), (pl.col("units") >= 4).mean())
sales.group_by("customer_id").agg(pl.col("revenue").sum()).filter(pl.col("revenue") > 300_000)
sales.group_by("category").agg(pl.col("product").unique().sort())
```
</details>

**Next →** [Lecture 14: Window functions with `over`](../14_window_functions_over/)
