"""Lecture 03: DataFrame basics: creating, anatomy, columns, index, chaining."""
import numpy as np
import pandas as pd

print("=== 1. Four ways to create ===")
by_columns = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "maths": [78, 92, 45],
    "science": [85, 88, 52],
})
print(by_columns, "\n")

by_rows = pd.DataFrame([
    {"name": "Asha", "maths": 78, "science": 85},
    {"name": "Ravi", "maths": 92},                 # missing science -> NaN
    {"name": "Meena", "maths": 45, "science": 52},
])
print(by_rows, "\n")

by_lists = pd.DataFrame([["Asha", 78], ["Ravi", 92]], columns=["name", "maths"])
print(by_lists, "\n")

from_numpy = pd.DataFrame(np.arange(6).reshape(3, 2), columns=["x", "y"])
print(from_numpy)

df = by_columns.copy()   # .copy() so changes below don't touch by_columns (same object otherwise)
print("\n=== 2. Anatomy ===")
print("shape  :", df.shape)
print("columns:", df.columns.tolist())
print("index  :", df.index.tolist())
print("len    :", len(df), "| size:", df.size)
print(df.dtypes)
print(df.to_numpy())

print("\n=== 3. Columns ===")
print(type(df["maths"]), "<- one column is a Series")
print(df[["name", "maths"]])
df["total"] = df["maths"] + df["science"]
df["passed"] = df["maths"] >= 50
print(df)
df = df.drop(columns=["passed"]).rename(columns={"total": "sum"})
print(df)

print("\n=== 4. The index ===")
by_name = df.set_index("name")
print(by_name)
print("Ravi's row:\n", by_name.loc["Ravi"])
print(by_name.reset_index().head(2))

print("\n=== 5. Methods return NEW objects ===")
df.sort_values("maths")
print("after sort_values without reassign:", df["name"].tolist())
df = df.sort_values("maths")
print("after reassign                    :", df["name"].tolist())

print("\n=== 6. Method chaining ===")
result = (
    by_columns
    .rename(columns={"maths": "math"})
    .assign(avg=lambda d: (d["math"] + d["science"]) / 2)
    .sort_values("avg", ascending=False)
    .head(2)
)
print(result)
