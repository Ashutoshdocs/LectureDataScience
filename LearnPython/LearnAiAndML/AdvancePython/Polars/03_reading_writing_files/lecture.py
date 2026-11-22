"""Lecture 03: Reading & writing CSV, Parquet, JSON and Excel. read_* vs scan_*."""
import io
from pathlib import Path
import polars as pl

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

print("=== read_csv ===")
sales = pl.read_csv(DATA / "sales.csv")
print(sales.head(3))
print("date is:", sales.schema["date"])

sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
print("with try_parse_dates:", sales.schema["date"])

print("\n=== Options ===")
print(pl.read_csv(DATA / "sales.csv", columns=["date", "product", "units"], n_rows=3))

default = pl.read_csv(DATA / "messy_customers.csv")
as_text = pl.read_csv(DATA / "messy_customers.csv", schema_overrides={"Customer ID": pl.String})
print("Customer ID default :", default["Customer ID"].head(3).to_list(), default.schema["Customer ID"])
print("Customer ID as text :", as_text["Customer ID"].head(3).to_list())

weird = io.StringIO("item;qty;price\npen;n/a;12\nbook;3;-\n")
print(pl.read_csv(weird, separator=";", null_values=["n/a", "-"]))

print("\n=== Write CSV and Parquet ===")
furniture = sales.filter(pl.col("category") == "Furniture")
furniture.write_csv(OUT / "furniture.csv")
furniture.write_parquet(OUT / "furniture.parquet")
# 48,000 rows resampled at random with unique ids, so the comparison is realistic
big = (sales.sample(48_000, with_replacement=True, shuffle=True, seed=1)
            .drop("order_id").with_row_index("order_id", offset=1))
big.write_csv(OUT / "big.csv")
big.write_parquet(OUT / "big.parquet")
csv_kb = (OUT / "big.csv").stat().st_size / 1024
pq_kb = (OUT / "big.parquet").stat().st_size / 1024
print(f"48,000 rows -> CSV {csv_kb:,.0f} KB | Parquet {pq_kb:,.0f} KB ({csv_kb / pq_kb:.0f}x smaller)")
print("types kept by Parquet:", pl.read_parquet(OUT / "furniture.parquet").schema["date"])
print("types lost by CSV    :", pl.read_csv(OUT / "furniture.csv").schema["date"])

print("\n=== scan_*: lazy reading ===")
lf = pl.scan_parquet(OUT / "big.parquet")
answer = lf.filter(pl.col("region") == "West").select(pl.col("units").sum()).collect()
print("West units (from 48k rows, reading only 2 columns):", answer.item())

print("\n=== JSON / NDJSON ===")
students = pl.read_csv(DATA / "students.csv")
students.head(2).write_json(OUT / "students.json")
students.head(2).write_ndjson(OUT / "students.ndjson")
print((OUT / "students.ndjson").read_text())
print(pl.read_ndjson(OUT / "students.ndjson"))

print("\n=== Excel ===")
students.write_excel(OUT / "students.xlsx", worksheet="marks")
print(pl.read_excel(OUT / "students.xlsx", sheet_name="marks").head(3))

print("\n=== Many files at once ===")
for region in ["North", "South"]:
    sales.filter(pl.col("region") == region).write_csv(OUT / f"part_{region}.csv")
print("rows across part_*.csv:", pl.read_csv(OUT / "part_*.csv").height)
