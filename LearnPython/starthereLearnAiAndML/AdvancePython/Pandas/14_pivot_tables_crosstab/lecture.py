"""Lecture 14: Pivot tables & crosstab."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
pd.set_option("display.width", 140)

sales = pd.read_csv(DATA / "sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
sales["month"] = sales["date"].str[:7]

print("=== pivot_table: revenue by region x category ===")
table = pd.pivot_table(sales, index="region", columns="category", values="revenue",
                       aggfunc="sum", margins=True, fill_value=0)
print(table)
print("\nin lakhs:\n", (table / 1e5).round(1))

print("\n=== Same thing with groupby + unstack ===")
print(sales.groupby(["region", "category"])["revenue"].sum().unstack())

print("\n=== Several aggregations ===")
print(sales.pivot_table(index="category", values=["units", "revenue"],
                        aggfunc={"units": "sum", "revenue": ["sum", "mean"]}).round(0))

print("\n=== Average units by product x region ===")
print(sales.pivot_table(index="product", columns="region", values="units", aggfunc="mean").round(2))

print("\n=== Revenue by month x category ===")
monthly = sales.pivot_table(index="month", columns="category", values="revenue",
                            aggfunc="sum", fill_value=0)
print(monthly)

print("\n=== crosstab: counting combinations ===")
print(pd.crosstab(sales["region"], sales["category"], margins=True))
print("\nrow %:\n", (pd.crosstab(sales["region"], sales["category"], normalize="index") * 100).round(1))

students = pd.read_csv(DATA / "students.csv")
students["result"] = (students["maths"] >= 60).map({True: "pass", False: "fail/absent"})
print("\n", pd.crosstab(students["class"], [students["gender"], students["result"]]))

print("\n=== Export the pivot to Excel ===")
(HERE / "output").mkdir(exist_ok=True)
table.to_excel(HERE / "output" / "region_category.xlsx")
print("saved output/region_category.xlsx")
