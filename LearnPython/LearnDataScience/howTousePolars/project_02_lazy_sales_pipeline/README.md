# Project 2 — Lazy Sales Analytics Pipeline

## Goal

Build a small data pipeline using Polars LazyFrames. Scan multiple CSV files, transform and join the data, aggregate revenue, inspect the query plan, and save Parquet and CSV results.

## Folder structure

```text
project_02_lazy_sales_pipeline/
├── README.md
├── main.py
├── pipeline.py
├── data/
│   ├── input/
│   │   ├── sales_2025.csv
│   │   └── sales_2026.csv
│   └── reference/
│       └── products.csv
├── output/
│   ├── reports/
│   └── parquet/
└── logs/
```

## Setup

From repository root:

```bash
pip install -r requirements.txt
```

## Run

```bash
python project_02_lazy_sales_pipeline/main.py
```

## Pipeline steps

1. Lazily scan the sales CSV files using a wildcard path.
2. Select required columns.
3. Cast quantities and prices to numeric types.
4. Join the product reference dataset.
5. Calculate line revenue.
6. Filter invalid or non-positive quantities.
7. Aggregate revenue by region and product.
8. Print the query plan.
9. Collect and save the results as CSV and Parquet.

## Concepts demonstrated

```python
pl.scan_csv("data/input/*.csv")      # Lazy scan of matching CSV files
pl.scan_csv("data/reference/products.csv")
pl.col("quantity").cast(pl.Int64)
lazy_frame.join(other, on="product_id", how="left")
lazy_frame.with_columns(expression)
lazy_frame.group_by("region").agg(...)
lazy_frame.explain()                 # Inspect query plan
lazy_frame.collect()                 # Execute query
dataframe.write_parquet(path)
```

## Student exercises

1. Add a filter for a specific region.
2. Calculate total quantity sold by product.
3. Find the top five products by revenue.
4. Add a monthly revenue aggregation.
5. Add a check for unmatched product IDs after the join.
6. Save the detailed transformed rows as Parquet.
7. Compare the lazy pipeline with an eager `read_csv()` workflow.
8. Print the query plan before and after adding a filter.
9. Add another CSV file and confirm the wildcard scan includes it.
10. Add a data-quality rule for negative unit prices.
