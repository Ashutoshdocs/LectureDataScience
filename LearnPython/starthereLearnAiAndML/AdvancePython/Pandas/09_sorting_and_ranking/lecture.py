"""Lecture 09: Sorting & ranking."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pd.read_csv(DATA / "sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
students = pd.read_csv(DATA / "students.csv")
students["total"] = students[["maths", "science", "english", "cs"]].sum(axis=1)

cols = ["order_id", "region", "product", "revenue"]

print("=== sort_values ===")
print(sales.sort_values("revenue")[cols].head(3))
print(sales.sort_values("revenue", ascending=False)[cols].head(3))
print(sales.sort_values(["region", "revenue"], ascending=[True, False])[cols].head(6))

print("\n=== missing values in sorting ===")
print(students.sort_values("maths", na_position="first")[["name", "maths"]].head(3))

print("\n=== reset_index after sorting ===")
top = sales.sort_values("revenue", ascending=False).head(3)
print("index before:", top.index.tolist())
print("index after :", top.reset_index(drop=True).index.tolist())

print("\n=== sort_index and custom key ===")
names = pd.DataFrame({"name": ["bob", "Alice", "carol", "Dave"]})
print("default (capitals first):", names.sort_values("name")["name"].tolist())
print("case-insensitive        :", names.sort_values("name", key=lambda s: s.str.lower())["name"].tolist())
print(sales.sample(4, random_state=0).sort_index()[cols])

print("\n=== nlargest / nsmallest ===")
print(sales.nlargest(5, "revenue")[cols])
print(students.nsmallest(3, "cs")[["name", "cs"]])

print("\n=== rank methods on ties ===")
s = pd.Series([90, 85, 85, 70], index=["A", "B", "C", "D"])
print(pd.DataFrame({
    "score": s,
    "average": s.rank(ascending=False),
    "min": s.rank(ascending=False, method="min"),
    "dense": s.rank(ascending=False, method="dense"),
    "first": s.rank(ascending=False, method="first"),
}))

print("\n=== ranking students ===")
students["rank"] = students["total"].rank(ascending=False, method="min").astype(int)
students["class_rank"] = (students.groupby("class")["total"]
                          .rank(ascending=False, method="min").astype(int))
students["maths_pct"] = students["maths"].rank(pct=True).round(2)
print(students.sort_values("rank")[["name", "class", "total", "rank", "class_rank", "maths_pct"]])
