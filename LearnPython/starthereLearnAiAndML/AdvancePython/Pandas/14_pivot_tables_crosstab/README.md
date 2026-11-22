# Lecture 14: Pivot tables & crosstab

Run: `python lecture.py`

If you've used Excel pivot tables, this is the same thing, written in one line and repeatable.

## `pivot_table`

```python
pd.pivot_table(sales,
               index="region",        # rows
               columns="category",    # columns
               values="revenue",      # what to summarise
               aggfunc="sum",         # how
               margins=True,          # add an "All" total row and column
               fill_value=0)          # empty cells become 0
```

```
category     Electronics   Furniture       All
region
East           ...           ...           ...
North          ...           ...           ...
...
All            ...           ...           ...
```

| Argument | Meaning |
|----------|---------|
| `index` | the row groups (one or several columns) |
| `columns` | the column groups |
| `values` | the column(s) to aggregate |
| `aggfunc` | `"sum"`, `"mean"`, `"count"`, a list `["sum", "mean"]`, or a dict per column |
| `margins=True` | totals |
| `fill_value=0` | replace empty combinations |

> `pivot_table` = `groupby([index, columns])[values].agg(aggfunc).unstack()`. Same result, friendlier syntax.

## `crosstab`: counting combinations

```python
pd.crosstab(sales["region"], sales["category"])                     # counts
pd.crosstab(sales["region"], sales["category"], normalize="index")  # row percentages
```

| `normalize=` | Each … sums to 1 |
|--------------|------------------|
| `"index"` | row |
| `"columns"` | column |
| `"all"` | whole table |

## `pivot_table` vs `pivot`

- `pivot_table` **aggregates** duplicates (sum, mean…). It's the safe choice.
- `pivot` only **rearranges**. It fails if a row/column combination appears twice (Lecture 16).

## Formatting a pivot for a report

```python
table.style.format("{:,.0f}")          # in Jupyter
(table / 1e5).round(1)                 # in lakhs
table.to_excel("report.xlsx")          # straight to Excel
```

## Exercises

1. Average units per order by product (rows) and region (columns).
2. Count orders by region × category with totals.
3. What % of each region's orders are Furniture?
4. Revenue by month (rows) and category (columns). Hint: make a `month` column first.

<details><summary>Solutions</summary>

```python
sales.pivot_table(index="product", columns="region", values="units", aggfunc="mean").round(2)
pd.crosstab(sales["region"], sales["category"], margins=True)
pd.crosstab(sales["region"], sales["category"], normalize="index")["Furniture"]
sales["month"] = sales["date"].str[:7]
sales.pivot_table(index="month", columns="category", values="revenue", aggfunc="sum")
```
</details>

**Next →** [Lecture 15: Merge, join & concat](../15_merge_join_concat/)
