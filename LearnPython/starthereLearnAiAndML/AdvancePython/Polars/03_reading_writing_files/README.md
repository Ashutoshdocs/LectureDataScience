# Lecture 03: Reading & writing files

Run: `python lecture.py` (writes into `output/`)

## Eager `read_*` vs lazy `scan_*`

| Format | Eager (load now) | Lazy (plan only) | Write |
|--------|-----------------|------------------|-------|
| CSV | `pl.read_csv` | `pl.scan_csv` | `df.write_csv` |
| **Parquet** | `pl.read_parquet` | `pl.scan_parquet` | `df.write_parquet` |
| JSON | `pl.read_json` | n/a | `df.write_json` |
| NDJSON (one JSON per line) | `pl.read_ndjson` | `pl.scan_ndjson` | `df.write_ndjson` |
| Excel | `pl.read_excel` (needs `fastexcel`) | n/a | `df.write_excel` (needs `xlsxwriter`) |
| Database | `pl.read_database(query, conn)` | n/a | `df.write_database` |
| Many files | `pl.read_csv("data/*.csv")` | `pl.scan_parquet("data/*.parquet")` | n/a |

Use **`scan_*`** for big files: Polars reads only the columns and rows your query needs (Lecture 18).

## Useful `read_csv` options

| Option | Use |
|--------|-----|
| `columns=["a", "b"]` | read only some columns |
| `try_parse_dates=True` | turn `2025-01-03` into a real `Date` |
| `schema_overrides={"id": pl.String}` | force types (keep leading zeros!) |
| `null_values=["n/a", "-", ""]` | extra markers for missing |
| `separator=";"` | non-comma files |
| `n_rows=1000` | preview a huge file |
| `skip_rows=2` | junk lines at the top |
| `infer_schema_length=10000` | look at more rows before guessing types |
| `ignore_errors=True` | bad values become null instead of crashing |

> **No `index=False` needed.** Polars has no index, so `write_csv` never adds a mystery `Unnamed: 0` column.

## Why Parquet?

| | CSV | Parquet |
|---|---|---|
| Format | text | binary, columnar, compressed |
| Size | big | often 3–10× smaller |
| Speed | slow to parse | very fast |
| Types | lost (everything is text) | **kept** (dates stay dates) |
| Read some columns only | no, must parse every line | yes |
| Human-readable | yes | no |

**Rule of thumb:** receive CSV, store Parquet.

## Exercises

1. Read only `date`, `product`, `units` from `sales.csv` with dates parsed.
2. Read `messy_customers.csv` with `Customer ID` as text. Do the leading zeros survive?
3. Save Furniture orders to Parquet and compare the file size with CSV.
4. Write `students.csv` to an Excel file.

<details><summary>Solutions</summary>

```python
pl.read_csv(DATA / "sales.csv", columns=["date", "product", "units"], try_parse_dates=True)
pl.read_csv(DATA / "messy_customers.csv", schema_overrides={"Customer ID": pl.String})
f.write_parquet(OUT / "f.parquet"); (OUT / "f.parquet").stat().st_size
pl.read_csv(DATA / "students.csv").write_excel(OUT / "students.xlsx")
```
</details>

**Next →** [Lecture 04: Exploring data](../04_exploring_data/)
