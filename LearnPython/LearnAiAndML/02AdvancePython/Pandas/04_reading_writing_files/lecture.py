"""Lecture 04: Reading & writing CSV, Excel and JSON."""
import io
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

print("=== 1. Read a CSV ===")
sales = pd.read_csv(DATA / "sales.csv")
print(sales.head())
print("shape:", sales.shape)
print(sales.dtypes)

print("\n=== 2. Useful read_csv options ===")
small = pd.read_csv(DATA / "sales.csv", usecols=["date", "product", "units"], nrows=3)
print(small)

indexed = pd.read_csv(DATA / "sales.csv", index_col="order_id", parse_dates=["date"])
print("order 1001:\n", indexed.loc[1001])
print("date dtype after parse_dates:", indexed["date"].dtype)

weird = io.StringIO("item;qty;price\npen;n/a;1,200\nbook;3;-\n")
cleaned = pd.read_csv(weird, sep=";", na_values=["n/a", "-"], thousands=",")
print(cleaned)
print(cleaned.dtypes)

print("\n=== 3. Write CSV ===")
furniture = sales[sales["category"] == "Furniture"]
furniture.to_csv(OUT / "furniture.csv", index=False)
print("wrote", len(furniture), "rows to output/furniture.csv")

furniture.head(3).to_csv(OUT / "with_index.csv")          # index=True by default
print("forgot index=False ->", pd.read_csv(OUT / "with_index.csv").columns.tolist())

print("\n=== 4. Excel with several sheets ===")
students = pd.read_csv(DATA / "students.csv")
with pd.ExcelWriter(OUT / "classes.xlsx") as writer:
    for class_name, part in students.groupby("class"):
        part.to_excel(writer, sheet_name=class_name, index=False)
back = pd.read_excel(OUT / "classes.xlsx", sheet_name=None)   # None = all sheets -> dict
print("sheets:", list(back), "| rows in 10A:", len(back["10A"]))

print("\n=== 5. JSON ===")
students.head(2).to_json(OUT / "students.json", orient="records", indent=2)
print((OUT / "students.json").read_text()[:200], "...")
print(pd.read_json(OUT / "students.json"))
