# Lecture 18: Project: a big-data sales pipeline

Run: `python lecture.py`. It writes `output/clean_parquet/`, `output/sales_report.xlsx` and `output/monthly_revenue.png`.

An end-to-end pipeline on the 2.4M-row, 12-file dataset, structured the way real Dask projects are:

```
 data/big/*.csv ──► [1 INGEST] ──► [2 CLEAN] ──► output/clean_parquet/ ──► [3 ANALYSE] ──► [4 REPORT]
  12 raw files      read with      fix types,      typed, compressed,      many summaries    Excel + chart
                    dtypes         derive cols     partitioned by month    in ONE compute    (small, pandas)
```

## Stages

| Stage | Dask techniques | Lecture |
|-------|-----------------|---------|
| Start a `LocalCluster` and print the dashboard link | distributed scheduler | 13 |
| **Ingest** 12 CSVs with declared dtypes | `dd.read_csv(glob, dtype=...)` | 06 |
| **Clean**: fill missing units, add revenue / month / hour, categories | lazy column ops, `fillna`, `astype("category")` | 07, 15 |
| **Store** as Parquet, partitioned by month | `to_parquet(partition_on=...)` | 06 |
| **Analyse**: KPIs, monthly trend, region × category, top products, busiest hours | `groupby`, `dask.compute(...)` once | 08, 15 |
| **Enrich**: top customers with segment/city | broadcast merge with a pandas table | 10 |
| **Report**: Excel workbook + chart | `.compute()` small results → pandas | 15 |

## Design choices to notice

- **CSV is read once.** Everything after stage 2 reads the clean Parquet.
- **All analysis results come from one `dask.compute(...)`**, so the Parquet is scanned once.
- **Only small results are computed into pandas**: dozens of rows, not millions.
- **The customer table stays pandas**, so the join is a broadcast with no shuffle.
- The pipeline is a set of **functions**, so it's easy to rerun on next year's files.

## Extension exercises

1. Add a sheet with revenue by city × segment.
2. Read only Q4 from the Parquet using `filters=[("month", ">=", 10)]` and compare speed with reading everything.
3. Add a data-quality sheet: missing units per month **before** cleaning.
4. Make the pipeline take the input folder as a command-line argument.

**Next →** [Lecture 19: Project: parallel file processing](../19_project_parallel_file_processing/)
