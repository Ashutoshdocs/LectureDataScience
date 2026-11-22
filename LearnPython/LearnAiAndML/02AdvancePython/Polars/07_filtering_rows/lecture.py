"""Lecture 07: Filtering rows with boolean expressions; row slicing."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
students = pl.read_csv(DATA / "students.csv")
cols = ["order_id", "date", "region", "product", "units"]

print("=== Basic filter ===")
big = sales.filter(pl.col("units") >= 4)
print(f"{big.height} of {sales.height} orders have 4+ units")
print(big.select(cols).head(3))

print("\n=== & | ~ and the comma shortcut ===")
a = sales.filter((pl.col("region") == "South") & (pl.col("units") > 3))
b = sales.filter(pl.col("region") == "South", pl.col("units") > 3)
c = sales.filter(region="South").filter(pl.col("units") > 3)
print("South & units>3:", a.height, "| comma form:", b.height, "| keyword form:", c.height)
print("Desk | Chair   :", sales.filter((pl.col("product") == "Desk") | (pl.col("product") == "Chair")).height)
print("not Furniture  :", sales.filter(~(pl.col("category") == "Furniture")).height)

try:
    sales.filter((pl.col("units") > 3) and (pl.col("region") == "North"))
except TypeError as e:
    print("using 'and' ->", str(e).splitlines()[0])

print("\n=== Helpers ===")
print("is_in        :", sales.filter(pl.col("product").is_in(["Laptop", "Tablet"])).height)
print("is_between   :", sales.filter(pl.col("unit_price").is_between(1000, 20000)).height)
print("str.contains :", sales.filter(pl.col("product").str.contains("one"))["product"].unique().to_list())
print("March        :", sales.filter(pl.col("date").dt.month() == 3).height)
print("Q1 dates     :", sales.filter(pl.col("date").is_between(pl.date(2025, 1, 1), pl.date(2025, 3, 31))).height)
print(students.filter(pl.col("maths").is_null()).select("name", "maths"))
print("any mark missing:", students.filter(pl.any_horizontal(pl.col("maths", "science", "english").is_null()))["name"].to_list())

print("\n=== Counting without filtering ===")
print(sales.select(
    (pl.col("units") >= 4).sum().alias("bulk_orders"),
    (pl.col("category") != "Electronics").mean().round(3).alias("share_not_electronics"),
))

print("\n=== First order of each customer ===")
print(sales.filter(pl.col("customer_id").is_first_distinct()).height, "customers")

print("\n=== Row slicing ===")
print(sales.slice(10, 3).select(cols))
print(sales[100:102].select(cols))
print("every 60th row:", sales.gather_every(60)["order_id"].to_list())
print(sales.sample(n=3, seed=7).select(cols))
print(sales.top_k(3, by="unit_price").select("order_id", "product", "unit_price"))
