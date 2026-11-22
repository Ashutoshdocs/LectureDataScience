# Polars: From Zero to Confident

A hands-on Polars course in 24 short lectures (00–23). It builds on the NumPy and pandas courses. Knowing pandas helps, but isn't required.

Every lecture folder has:

| File | What it is |
|------|------------|
| `README.md` | The lesson: concepts, diagrams, tables, common mistakes, exercises (with solutions) |
| `lecture.py` | Runnable code for the lesson. Read it, run it, change it |

The `data/` folder holds the CSV files the lectures read (the same datasets as the pandas course):

| File | Rows | What's in it |
|------|------|--------------|
| `sales.csv` | 240 | Orders across 2025: date, region, product, category, units, unit price, customer |
| `customers.csv` | 41 | Customer id, name, city, join date, segment |
| `students.csv` | 12 | Marks in 4 subjects, with a few missing values |
| `messy_customers.csv` | 10 | Deliberately dirty data for the cleaning project |

## How to use this course

1. **Install Python 3.10+**.
2. **Install the libraries** from your terminal:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Work through the folders **in order**: read `README.md`, run `python lecture.py` from inside the folder, then do the exercises.

## Course map

| # | Lecture | Big idea |
|---|---------|----------|
| 00 | [Prerequisites](00_prerequisites/) | Python, method chaining, columnar thinking |
| 01 | [What is Polars?](01_what_is_polars/) | Rust + Arrow + multi-threading + lazy queries. Why it's fast |
| 02 | [Series & DataFrame](02_series_and_dataframe/) | Tables with a schema and **no index** |
| 03 | [Reading & writing files](03_reading_writing_files/) | CSV, Parquet, JSON, Excel; `read_*` vs `scan_*` |
| 04 | [Exploring data](04_exploring_data/) | `glimpse`, `describe`, `null_count`, `value_counts` |
| 05 | [Expressions: the core idea](05_expressions_the_core_idea/) | `pl.col(...)` recipes inside `select` / `with_columns` / `filter` |
| 06 | [Selecting columns](06_selecting_columns/) | `select`, selectors, regex, `exclude` |
| 07 | [Filtering rows](07_filtering_rows/) | `filter`, `is_in`, `is_between`, row slicing |
| 08 | [Adding columns & when/then](08_adding_columns_when_then/) | `with_columns`, conditional logic, `replace` |
| 09 | [Sorting & ranking](09_sorting_and_ranking/) | `sort`, `top_k`, `rank` |
| 10 | [Missing data](10_missing_data/) | `null` vs `NaN`, `fill_null`, `drop_nulls` |
| 11 | [Data types & casting](11_data_types_and_casting/) | Strict schema, `cast`, `Categorical` / `Enum` |
| 12 | [String methods](12_string_methods/) | The `.str` namespace |
| 13 | [Group by & aggregation](13_group_by_aggregation/) | `group_by().agg()` with expressions |
| 14 | [Window functions: `over`](14_window_functions_over/) | Group values on every row, without a join |
| 15 | [Joins & concat](15_joins_and_concat/) | inner/left/full/semi/anti, `join_asof`, `concat` |
| 16 | [Reshaping: pivot & unpivot](16_reshaping_pivot_unpivot/) | Wide ↔ long |
| 17 | [Dates & time series](17_dates_and_time_series/) | `.dt`, `group_by_dynamic`, rolling windows |
| 18 | [Lazy API & query optimisation](18_lazy_api_query_optimization/) | `LazyFrame`, `explain()`, pushdown, streaming |
| 19 | [Performance: Polars vs pandas](19_performance_polars_vs_pandas/) | A head-to-head race on millions of rows |
| 20 | [SQL & interop](20_sql_and_interop/) | `df.sql(...)`, pandas / NumPy / Arrow conversion, plotting |
| 21 | [Project: sales analysis](21_project_sales_analysis/) | A full lazy pipeline to an Excel report |
| 22 | [Project: data cleaning](22_project_data_cleaning/) | Messy → tidy, all with expressions |
| 23 | [Recap & cheat sheet](23_recap_cheatsheet/) | pandas → Polars translation table |

## Run everything at once

```bash
python run_all.py
```

## Version notes

Tested with **Polars 2.1**. Polars changes faster than pandas, so if something errors on your version, check the [Polars docs](https://docs.pola.rs/). Changes worth knowing:

- `Expr.cut` / `Expr.qcut` are **deprecated** in Polars 2. The replacements are `bin_intervals` / `bin_quantiles` (still experimental). This course uses `when/then` for binning, which is stable across versions.
- Older tutorials use `groupby`, `melt`, `apply`, `with_row_count`, `str.lengths`. These became `group_by`, `unpivot`, `map_elements`, `with_row_index`, `str.len_chars` in Polars 1.0.
