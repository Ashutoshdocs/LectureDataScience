"""Lecture 20: SQL on DataFrames; pandas / NumPy / Arrow interop; plotting."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
customers = pl.read_csv(DATA / "customers.csv", try_parse_dates=True)
students = pl.read_csv(DATA / "students.csv")

print("=== SQL on one DataFrame ===")
print(sales.sql("""
    SELECT region, SUM(units) AS units, COUNT(*) AS orders
    FROM self GROUP BY region ORDER BY units DESC
"""))

print("\n=== SQLContext with a join ===")
ctx = pl.SQLContext(sales=sales, customers=customers)
by_city = ctx.execute("""
    SELECT c.city, SUM(s.units * s.unit_price) AS revenue, COUNT(DISTINCT s.customer_id) AS customers
    FROM sales s JOIN customers c ON s.customer_id = c.customer_id
    GROUP BY c.city ORDER BY revenue DESC
""", eager=True)
print(by_city)

print("\n=== SQL and expressions are the same engine ===")
sql_lf = ctx.execute("SELECT product, units FROM sales WHERE region = 'North'")   # lazy
print(type(sql_lf).__name__)
print(sql_lf.group_by("product").agg(pl.col("units").sum()).sort("units", descending=True)
            .head(3).collect())

print("\n=== Monthly revenue by category in SQL ===")
print(sales.sql("""
    SELECT category, EXTRACT(month FROM date) AS month, SUM(units * unit_price) AS revenue
    FROM self GROUP BY category, month ORDER BY month, category
""").head(6))

print("\n=== Polars <-> pandas ===")
pdf = by_city.to_pandas()
print(type(pdf).__name__, "\n", pdf.dtypes)
back = pl.from_pandas(pdf)
print("round trip equal:", back.equals(by_city))
pdf_indexed = pdf.set_index("city")
print("from_pandas drops the index:", pl.from_pandas(pdf_indexed).columns)
print("reset_index keeps it        :", pl.from_pandas(pdf_indexed.reset_index()).columns)

print("\n=== Polars <-> NumPy ===")
marks = students.select("maths", "science", "english", "cs").drop_nulls()
arr = marks.to_numpy()
print(type(arr).__name__, arr.shape, arr.dtype)
print("correlation (NumPy):\n", np.corrcoef(arr, rowvar=False).round(2))
print(pl.DataFrame(np.eye(3, dtype=int), schema=["a", "b", "c"]))

print("\n=== Polars <-> Arrow ===")
table = sales.to_arrow()
print(type(table).__name__, table.num_rows, "rows")
print("from_arrow shape:", pl.from_arrow(table).shape)

print("\n=== Python objects ===")
print(sales.head(2).to_dicts())
print(sales.select(pl.col("units").sum()).item())

print("\n=== Plotting with matplotlib ===")
units = (sales.group_by("product").agg(pl.col("units").sum()).sort("units"))
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.barh(units["product"].to_list(), units["units"].to_list(), color="#2f62c9")
ax.set_title("Units sold by product")
ax.set_xlabel("Units")
fig.savefig(OUT / "units_by_product.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/units_by_product.png")
