# Lecture 15: Merge, join & concat

Run: `python lecture.py`

Real data lives in **several tables**: orders in one, customers in another, products in a third. Combining them is a core skill, and it works the same way as SQL joins.

## `merge`: match rows on a key column

```python
orders_with_names = sales.merge(customers, on="customer_id", how="left")
```

### The four join types

```
 left (sales)        right (customers)
 customer_id 1..40   customer_id 1..41  (41 has no orders)

 how="inner"  →  only ids in BOTH                  (like a VLOOKUP, dropping misses)
 how="left"   →  every left row, matched if possible  ← most common
 how="right"  →  every right row
 how="outer"  →  everything from both, NaN where no match
```

| `how=` | Keeps | Use when |
|--------|-------|----------|
| `"inner"` (default) | matches only | you only want complete records |
| `"left"` | all left rows | **enriching** a main table with extra info |
| `"right"` | all right rows | rarely; swap the tables and use left |
| `"outer"` | all rows from both | finding what's missing on either side |

### Key options

| Option | Use |
|--------|-----|
| `on="id"` | same column name on both sides |
| `left_on="cust", right_on="id"` | different names |
| `on=["a", "b"]` | match on several columns |
| `suffixes=("_order", "_cust")` | rename clashing column names |
| `indicator=True` | adds `_merge` column: `both` / `left_only` / `right_only` |
| `validate="many_to_one"` | **error** if the right key isn't unique (catches duplicated rows) |

> ⚠️ **Duplicate keys multiply rows.** If a customer appears twice in `customers`, each of their orders appears twice after the merge, and revenue totals double. Check `len()` before and after, or use `validate=`.

## `concat`: stack tables

```python
pd.concat([jan, feb, mar], ignore_index=True)        # one under another (same columns)
pd.concat([left, right], axis=1)                     # side by side (aligned on index)
```

Typical use: combining monthly files with the same columns:

```python
files = sorted(Path("data").glob("sales_*.csv"))
all_sales = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
```

## `join`: merge on the index

```python
sales.set_index("customer_id").join(customers.set_index("customer_id"))
```
A shortcut for index-to-index merges. `merge` can do everything `join` does.

## `map` for a simple lookup

To pull a single column from another table, `map` is lighter than a merge:

```python
city_of = customers.set_index("customer_id")["city"]
sales["city"] = sales["customer_id"].map(city_of)
```

## Exercises

1. Add each order's customer name and city to `sales`.
2. Revenue by city.
3. Which customers have never ordered? (`indicator=True`)
4. Revenue by customer segment (Retail vs Business).

<details><summary>Solutions</summary>

```python
full = sales.merge(customers, on="customer_id", how="left")
full.groupby("city")["revenue"].sum().sort_values(ascending=False)
m = customers.merge(sales, on="customer_id", how="left", indicator=True)
m.loc[m["_merge"] == "left_only", "name"]
full.groupby("segment")["revenue"].sum()
```
</details>

**Next →** [Lecture 16: Reshaping with melt & pivot](../16_reshaping_melt_pivot/)
