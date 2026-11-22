"""Lecture 06: Selecting columns: names, types, regex, selectors, renaming."""
from pathlib import Path
import polars as pl
import polars.selectors as cs

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
students = pl.read_csv(DATA / "students.csv")

print("=== By name ===")
print(students.select("name", "maths").head(3))
print("df['maths'] is a", type(students["maths"]).__name__,
      "| df.select('maths') is a", type(students.select("maths")).__name__)
print(students.select(pl.all().exclude("gender", "class")).head(2))
print(students.drop("gender", "class").columns)

print("\n=== By type and regex ===")
print("Float64 cols:", students.select(pl.col(pl.Float64)).columns)
print("Int64 cols  :", sales.select(pl.col(pl.Int64)).columns)
print("*_id cols   :", sales.select(pl.col("^.*_id$")).columns)

print("\n=== Selectors ===")
print("numeric          :", sales.select(cs.numeric()).columns)
print("numeric - ids    :", sales.select(cs.numeric() - cs.ends_with("_id")).columns)
print("string           :", sales.select(cs.string()).columns)
print("date             :", sales.select(cs.date()).columns)
print("string | date    :", sales.select(cs.string() | cs.date()).columns)
print("not numeric      :", sales.select(~cs.numeric()).columns)
print("starts with 'u'  :", sales.select(cs.starts_with("u")).columns)
print("contains 'price' :", sales.select(cs.contains("price")).columns)

print("\n=== Selectors with expressions ===")
print(students.select(cs.numeric().mean().round(1)))
print(sales.select(cs.string().str.to_uppercase()).head(3))

print("\n=== Renaming ===")
print(sales.rename({"unit_price": "price", "customer_id": "cust"}).columns)
print(sales.rename(str.title).columns)
print(students.select("name", pl.col("maths", "cs").name.prefix("mark_")).head(2))

print("\n=== Reordering ===")
front = ["product", "units"]
print(sales.select(*front, pl.all().exclude(front)).head(2))
