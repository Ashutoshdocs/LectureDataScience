# Lecture 20: SQL, interop with pandas / NumPy / Arrow, and plotting

Run: `python lecture.py` (writes a chart to `output/`)

## SQL on DataFrames

Polars has a built-in SQL engine. Queries compile to the **same optimised lazy plan** as expressions, so they're just as fast.

```python
sales.sql("SELECT region, SUM(units) AS units FROM self GROUP BY region ORDER BY units DESC")

ctx = pl.SQLContext(sales=sales, customers=customers)      # register several tables
ctx.execute("""
    SELECT c.city, SUM(s.units * s.unit_price) AS revenue
    FROM sales s JOIN customers c USING (customer_id)
    GROUP BY c.city ORDER BY revenue DESC
""", eager=True)

pl.sql("SELECT * FROM sales WHERE units = 5").collect()     # finds DataFrames by variable name
```

You can mix freely: start in SQL, continue with expressions, or the other way round. This is useful when a team already knows SQL.

## Converting between libraries

| From → To | Code | Notes |
|-----------|------|-------|
| Polars → pandas | `df.to_pandas()` | needs `pyarrow`; `use_pyarrow_extension_array=True` avoids copies |
| pandas → Polars | `pl.from_pandas(pdf)` | the index is dropped. `reset_index()` first to keep it |
| Polars → NumPy | `df.to_numpy()`, `df["x"].to_numpy()` | numeric columns are zero-copy where possible |
| NumPy → Polars | `pl.DataFrame(arr, schema=[...])`, `pl.Series(arr)` | n/a |
| Polars → Arrow | `df.to_arrow()` | zero-copy |
| Arrow → Polars | `pl.from_arrow(table)` | zero-copy |
| Polars → Python | `df.to_dicts()`, `df.rows()`, `s.to_list()`, `df.item()` | n/a |
| Python → Polars | `pl.DataFrame(list_of_dicts)` | n/a |

**Typical workflow:** do the heavy work in Polars, then `.to_pandas()` the small result for a library that needs pandas (seaborn, statsmodels, some scikit-learn helpers).

> scikit-learn ≥ 1.4 and many plotting libraries accept Polars DataFrames directly. Try before converting.

## Plotting

Options:
1. **Matplotlib with columns**: `plt.bar(df["region"], df["revenue"])`. Polars Series work like arrays.
2. **`df.plot`**: built-in interactive charts via Altair (`pip install altair`): `df.plot.bar(x="region", y="revenue")`.
3. **Convert**: `df.to_pandas().plot(...)` for pandas-style charts.

`lecture.py` uses option 1, which has no extra dependencies.

## Exercises

1. Write a SQL query for revenue by category and month.
2. Convert the result to pandas and check its `dtypes`.
3. Compute a correlation matrix with NumPy from `students` marks via `to_numpy()`.
4. Plot units sold per product as a horizontal bar chart with Matplotlib.

<details><summary>Solutions</summary>

```python
sales.sql("SELECT category, EXTRACT(month FROM date) AS m, SUM(units*unit_price) AS rev FROM self GROUP BY 1, 2 ORDER BY 2")
res.to_pandas().dtypes
np.corrcoef(students.select(marks).drop_nulls().to_numpy(), rowvar=False)
plt.barh(t["product"], t["units"])
```
</details>

**Next →** [Lecture 21: Project: sales analysis](../21_project_sales_analysis/)
