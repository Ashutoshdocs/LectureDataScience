# Lecture 20: Project: a complete sales analysis

Run: `python lecture.py`. It prints a report and saves `output/sales_report.xlsx` plus two charts.

This project uses the whole workflow on `sales.csv` + `customers.csv`:

```
 load → check → enrich → analyse → report
```

## The business questions

| # | Question | Tools | Lecture |
|---|----------|-------|---------|
| 1 | What are total revenue, orders, average order value? | column maths, `sum`, `mean` | 08 |
| 2 | Which region and category earn most? | `pivot_table`, `margins` | 14 |
| 3 | Which products are best-sellers by revenue *and* units? | `groupby().agg()` | 13 |
| 4 | How does revenue move month to month? | `resample`, `pct_change` | 17 |
| 5 | Who are the top 5 customers and where are they? | `merge`, `groupby`, `nlargest` | 15 |
| 6 | Do Business customers spend more per order than Retail? | merge + groupby | 13, 15 |
| 7 | How concentrated is revenue? (share from the top 20% of customers) | `sort_values`, `cumsum` | 09, 17 |
| 8 | Which weekday is busiest? | `.dt.day_name()` | 17 |
| 9 | Save everything for the boss | `ExcelWriter`, `plot` | 04, 19 |

## Structure of `lecture.py`

The script is split into small functions: `load()`, `kpis()`, `by_region_category()` and so on. That keeps each question readable and lets you reuse the steps on next year's file.

## Good habits shown

- **Check row counts after a merge** (`validate="many_to_one"`)
- **Summarise, then format** (lakhs, rounding) only at the end
- **One function per question**
- **Write results to Excel**, one sheet per table, so non-programmers can use them

## Extension exercises

1. Add a sheet with revenue by **city × category**.
2. Find each region's best-selling product.
3. Which month had the highest *average order value*?
4. Compute repeat-customer rate: customers with 2+ orders ÷ all customers who ordered.

<details><summary>Hints</summary>

```python
full.pivot_table(index="city", columns="category", values="revenue", aggfunc="sum")
full.groupby(["region", "product"])["revenue"].sum().groupby(level=0).idxmax()
full.set_index("date")["revenue"].resample("ME").mean().idxmax()
(full.groupby("customer_id").size() >= 2).mean()
```
</details>

**Next →** [Lecture 21: Project, data cleaning](../21_project_data_cleaning/)
