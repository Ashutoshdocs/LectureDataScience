"""Lecture 05: Exploring a dataset: head, info, describe, value_counts, missing, duplicates."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

sales = pd.read_csv(DATA / "sales.csv")

print("=== head / tail / sample ===")
print(sales.head())
print(sales.tail(3))
print(sales.sample(3, random_state=1))

print("\n=== shape / columns ===")
print(sales.shape, "->", sales.shape[0], "rows,", sales.shape[1], "columns")
print(sales.columns.tolist())

print("\n=== info() ===")
sales.info()

print("\n=== describe() ===")
print(sales.describe())
print(sales.describe(include="all").T[["count", "unique", "top", "freq"]])

print("\n=== value_counts ===")
print(sales["region"].value_counts())
print(sales["category"].value_counts(normalize=True).round(3))
print("busiest region:", sales["region"].value_counts().idxmax())

print("\n=== unique / nunique ===")
print("products :", sales["product"].unique())
print("customers:", sales["customer_id"].nunique())

print("\n=== missing and duplicates ===")
print("missing per column in sales:\n", sales.isna().sum())
print("duplicate rows:", sales.duplicated().sum())

students = pd.read_csv(DATA / "students.csv")
print("\nmissing per column in students:\n", students.isna().sum())

print("\n=== range checks ===")
print("units range     :", sales["units"].min(), "to", sales["units"].max())
print("unit_price range:", sales["unit_price"].min(), "to", sales["unit_price"].max())
print("date range      :", sales["date"].min(), "to", sales["date"].max())

print("\n=== correlation ===")
print(students.corr(numeric_only=True).round(2))
