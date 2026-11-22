# Lecture 15: Joins & concat

Run: `python lecture.py`

## `join`

```python
sales.join(customers, on="customer_id", how="left")
```

### Join types

| `how=` | Keeps | Columns from right? | Use |
|--------|-------|---------------------|-----|
| `"inner"` (default) | matching rows only | yes | complete records only |
| `"left"` | all left rows | yes (null if no match) | **enrich** a main table |
| `"right"` | all right rows | yes | rare |
| `"full"` | everything from both | yes | find gaps on either side |
| `"semi"` | left rows **that have** a match | **no** | "customers who ordered" (a filter) |
| `"anti"` | left rows **with no** match | **no** | "customers who never ordered" |
| `"cross"` | every combination | yes | build grids (all regions × all months) |

`semi` and `anti` are filters. They never add columns or duplicate rows, which makes them perfect for "who is / isn't in the other table?" questions.

### Options

| Option | Use |
|--------|-----|
| `on="id"` / `on=["a", "b"]` | same key names |
| `left_on="cust", right_on="id"` | different names |
| `suffix="_right"` | rename clashing columns |
| `validate="m:1"` | error if right keys aren't unique (`1:1`, `1:m`, `m:1`, `m:m`) |
| `coalesce=True` | merge the key columns in full joins |
| `nulls_equal=True` | let null keys match each other |

> ⚠️ Duplicate keys multiply rows, exactly as in pandas. Use `validate="m:1"` and check `height` before and after.

## `join_asof`: nearest match in time

Match each row to the **most recent** row on or before it in the other table, e.g. each order gets the price that was valid on that day:

```python
orders.sort("date").join_asof(price_list.sort("date"), on="date", by="product")
```

## `concat`

| `how=` | Does |
|--------|------|
| `"vertical"` (default) | stack rows; columns must match |
| `"vertical_relaxed"` | stack, casting types to a common supertype |
| `"diagonal"` | stack, filling missing columns with null |
| `"horizontal"` | side by side (same height) |
| `"align"` | side by side, aligned on common key columns |

```python
pl.concat([jan, feb, mar])
pl.concat([df_a, df_b], how="diagonal")
```

## Exercises

1. Add each order's customer name, city and segment.
2. Revenue by city.
3. Customers who never ordered (`anti`).
4. Revenue by segment (Retail vs Business).
5. Build a full grid of regions × categories with `cross`, then left-join the revenue so empty combinations show 0.

<details><summary>Solutions</summary>

```python
full = sales.join(customers, on="customer_id", how="left", validate="m:1")
full.group_by("city").agg(pl.col("revenue").sum()).sort("revenue", descending=True)
customers.join(sales, on="customer_id", how="anti")
full.group_by("segment").agg(pl.col("revenue").sum())
regions.join(categories, how="cross").join(rev, on=["region", "category"], how="left").fill_null(0)
```
</details>

**Next →** [Lecture 16: Reshaping](../16_reshaping_pivot_unpivot/)
