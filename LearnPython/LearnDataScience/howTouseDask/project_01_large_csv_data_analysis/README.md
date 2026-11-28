# Project 1 — Large CSV Data Analysis with Dask

## Goal

Build a sales analytics pipeline using Dask DataFrame. The project reads multiple CSV files, calculates revenue, joins reference data, aggregates results, and writes partitioned outputs.

## Folder structure

```text
project_01_large_csv_data_analysis/
├── README.md
├── main.py
├── analysis.py
├── data/
│   ├── input/
│   │   ├── sales_part_1.csv
│   │   └── sales_part_2.csv
│   └── reference/
│       └── regions.csv
└── output/
```

## Setup

From repository root:

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
```

## Run

```bash
python project_01_large_csv_data_analysis/main.py
```

## What it does

1. Reads multiple CSV files with `dd.read_csv()`.
2. Displays columns, dtypes, and partition count.
3. Adds a revenue column.
4. Filters invalid and high-value rows.
5. Joins region names.
6. Groups sales by region.
7. Computes the relatively small summary result.
8. Writes detailed data and summary outputs.

## Concepts demonstrated

```python
dd.read_csv("data/input/sales_part_*.csv")  # Read multiple CSV files
df.npartitions                              # Count partitions
df[["region", "amount"]]                    # Select columns
df[df["amount"] > 1000]                     # Filter rows
df["revenue"] = df["quantity"] * df["price"]# Add calculated column
df.merge(reference, on="region_id")         # Join data
df.groupby("region")["revenue"].sum()       # Aggregate
result.compute()                            # Execute graph
df.to_parquet("output/parquet/")            # Write Parquet
```

## Student exercises

1. Add a filter for one region.
2. Calculate average revenue by product.
3. Count orders by month.
4. Add a missing-value report.
5. Compare the partition count when reading one file vs multiple files.
6. Export the summary to CSV.
7. Try the same transformation in pandas and compare the code.
8. Increase the sample dataset and observe runtime and partition behavior.
9. Add an unmatched region ID and report it.
10. Start a distributed Client and observe the dashboard while computing.

## Important

The sample data is intentionally small so students can run it on a laptop. Dask's scaling benefit becomes clearer with larger workloads. Do not assume Dask is faster for tiny data.
