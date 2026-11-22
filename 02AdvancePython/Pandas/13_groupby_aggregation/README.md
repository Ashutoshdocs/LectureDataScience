# Lecture 13: GroupBy & aggregation

Run: `python lecture.py`

This is the most powerful idea in pandas. You'll use it in almost every analysis.

## Split → Apply → Combine

```
 sales                          SPLIT by region          APPLY sum       COMBINE
 region  revenue                North: 50000, 3600 ...   North: 1.9M     region   revenue
 North   50000          ──►     South: ...         ──►   South: ...  ──► East     ...
 West    6000                   East:  ...               East:  ...      North    1.9M
 East    3500                   West:  6000, 75000 ...   West:  ...      South    ...
 ...                                                                     West     ...
```

```python
sales.groupby("region")["revenue"].sum()
```

Read it aloud: *"group sales by region, take the revenue column, sum it."*

## Aggregation functions

`sum`, `mean`, `median`, `min`, `max`, `count` (non-missing), `size` (all rows), `nunique`, `std`, `first`, `last`.

## Variations

| Code | Gives |
|------|-------|
| `df.groupby("region")["revenue"].sum()` | one column, one stat → Series |
| `df.groupby("region")[["revenue", "units"]].sum()` | several columns |
| `df.groupby(["region", "category"])["revenue"].sum()` | several keys → MultiIndex |
| `.reset_index()` | turn group keys back into columns |
| `df.groupby("region", as_index=False)["revenue"].sum()` | same, directly |
| `.sort_values(ascending=False)` | rank the groups |
| `.unstack()` | move the inner key into columns (a pivot table) |

## `agg`: several statistics at once

```python
sales.groupby("region")["revenue"].agg(["sum", "mean", "count"])

# named aggregation: choose the output column names
sales.groupby("region").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    avg_units=("units", "mean"),
    customers=("customer_id", "nunique"),
)
```

## `transform`: a group result for every row

`agg` shrinks each group to **one row**. `transform` returns a value for **every original row**, which is perfect for comparing a row with its group:

```python
sales["region_avg"] = sales.groupby("region")["revenue"].transform("mean")
sales["share_of_region"] = sales["revenue"] / sales.groupby("region")["revenue"].transform("sum")
```

## `filter`: keep whole groups

```python
sales.groupby("customer_id").filter(lambda g: len(g) >= 8)    # customers with 8+ orders
```

## Looping over groups

```python
for region, part in sales.groupby("region"):
    print(region, len(part))
```

## Other handy tools

- `df.groupby("region").size()`: rows per group
- `df.groupby("region")["revenue"].idxmax()`: index label of the top row per group
- `df.sort_values("revenue").groupby("region").tail(1)`: the top row per group
- `df.groupby(...)["x"].cumsum()`, `.rank()`, `.shift()`: running values within groups

## Exercises

1. Total units sold per product, highest first.
2. Average order revenue per category and region (unstack into a table).
3. For each region: number of orders, total revenue, and largest order.
4. Add a column showing each order's revenue as a % of its category's total.
5. Which customers spent more than Rs 3,00,000 in total?

<details><summary>Solutions</summary>

```python
sales.groupby("product")["units"].sum().sort_values(ascending=False)
sales.groupby(["category", "region"])["revenue"].mean().unstack().round(0)
sales.groupby("region").agg(orders=("order_id", "count"), total=("revenue", "sum"), biggest=("revenue", "max"))
sales["pct_cat"] = sales["revenue"] / sales.groupby("category")["revenue"].transform("sum") * 100
spend = sales.groupby("customer_id")["revenue"].sum(); spend[spend > 300_000]
```
</details>

**Next →** [Lecture 14: Pivot tables & crosstab](../14_pivot_tables_crosstab/)
