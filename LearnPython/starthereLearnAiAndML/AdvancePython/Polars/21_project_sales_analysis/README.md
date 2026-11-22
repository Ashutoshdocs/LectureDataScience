# Lecture 21: Project: sales analysis as a lazy pipeline

Run: `python lecture.py`. It prints a report and saves `output/sales_report.xlsx` (one sheet per table) and two charts.

This is the same analysis as the pandas course project, written the Polars way:

```
 scan_csv ─► clean & enrich (LazyFrame) ─► many small queries ─► collect_all ─► Excel + charts
```

## The business questions

| # | Question | Polars tools | Lecture |
|---|----------|-------------|---------|
| 1 | Total revenue, orders, average order value? | `select` with aggregations | 05 |
| 2 | Revenue by region × category with totals | `pivot`, `sum_horizontal` | 16 |
| 3 | Product ranking by revenue *and* units | `group_by().agg()`, `rank` | 09, 13 |
| 4 | Month-by-month trend and growth | `group_by_dynamic`, `pct_change`, `cum_sum` | 17 |
| 5 | Top 5 customers with city & segment | `join`, `top_k` | 15 |
| 6 | Retail vs Business | `join` + `group_by` | 13, 15 |
| 7 | Share of revenue from the top 20% of customers | `sort`, `head`, sums | 09 |
| 8 | Busiest weekday | `.dt.weekday()` | 17 |
| 9 | Each region's best product | `.over()` + `filter` | 14 |

## Design of `lecture.py`

- `base()` returns one **LazyFrame** with the join and new columns. Every question builds on it.
- Each question is a small function returning a **LazyFrame**.
- `pl.collect_all([...])` runs them **together**, so shared work (scanning, joining) happens once.
- `write_excel(workbook=..., worksheet=...)` puts every table in one workbook.

## Extension exercises

1. Add a sheet with revenue by city × category.
2. Which month had the highest average order value?
3. Repeat-customer rate: customers with 2+ orders ÷ customers who ordered.
4. Rewrite question 2 in SQL with `pl.SQLContext`.

<details><summary>Hints</summary>

```python
df.pivot(on="category", index="city", values="revenue", aggregate_function="sum")
base().group_by_dynamic("date", every="1mo").agg(pl.col("revenue").mean()).sort("revenue").tail(1)
base().group_by("customer_id").len().select((pl.col("len") >= 2).mean())
```
</details>

**Next →** [Lecture 22: Project: data cleaning](../22_project_data_cleaning/)
