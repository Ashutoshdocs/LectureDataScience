# Lecture 07: Filtering rows

Run: `python lecture.py`

Filtering works exactly like NumPy boolean masks:

```python
mask = sales["units"] >= 4         # a True/False Series, one per row
big = sales[mask]                  # keep the True rows
big = sales[sales["units"] >= 4]   # same, in one line
```

## Combining conditions

| Operator | Meaning | Example |
|----------|---------|---------|
| `&` | and | `(s["region"] == "North") & (s["units"] > 3)` |
| `\|` | or | `(s["product"] == "Desk") \| (s["product"] == "Chair")` |
| `~` | not | `~(s["category"] == "Furniture")` |

> ⚠️ **Brackets around every condition.** And never `and`/`or`: you'll get `ValueError: The truth value of a Series is ambiguous`.

## Handy filter helpers

| Helper | Instead of | Example |
|--------|-----------|---------|
| `.isin([...])` | many `\|` | `s[s["product"].isin(["Desk", "Chair", "Lamp"])]` |
| `.between(a, b)` | `(x >= a) & (x <= b)` | `s[s["unit_price"].between(1000, 20000)]` |
| `.str.contains("..")` | text search | `s[s["product"].str.contains("one")]` |
| `.str.startswith("..")` | prefix match | `s[s["region"].str.startswith("N")]` |
| `.isna()` / `.notna()` | missing checks | `st[st["maths"].isna()]` |
| `.query("...")` | readable string filter | `s.query("region == 'North' and units > 3")` |
| `.nlargest(n, col)` | sort + head | `s.nlargest(5, "units")` |

## `query`: SQL-like filters

```python
sales.query("units >= 4 and region in ['North', 'East']")
limit = 20000
sales.query("unit_price > @limit")      # @ refers to a Python variable
```

Inside `query` you *can* write `and`, `or`, `not`.

## Counting and fractions

```python
(sales["units"] >= 4).sum()     # how many rows match
(sales["units"] >= 4).mean()    # what fraction
```

## Filter, then select columns

```python
sales.loc[sales["region"] == "West", ["date", "product", "units"]]
```

## Exercises

1. Orders from the South with more than 3 units.
2. All Laptop **or** Tablet orders, using `isin`.
3. Orders in March 2025 (dates are text `"2025-03-..."`, so use `str.startswith`).
4. What fraction of orders are not Electronics?
5. Rewrite exercise 1 with `query`.

<details><summary>Solutions</summary>

```python
sales[(sales["region"] == "South") & (sales["units"] > 3)]
sales[sales["product"].isin(["Laptop", "Tablet"])]
sales[sales["date"].str.startswith("2025-03")]
(~(sales["category"] == "Electronics")).mean()
sales.query("region == 'South' and units > 3")
```
</details>

**Next →** [Lecture 08: Adding & modifying columns](../08_adding_modifying_columns/)
