"""Lecture 11: Data types: astype, to_numeric, to_datetime, category, nullable ints."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pd.read_csv(DATA / "sales.csv")

print("=== dtypes after read_csv ===")
print(sales.dtypes)

print("\n=== The bugs wrong types cause ===")
as_text = pd.Series(["10", "5", "20"])
print("text 'sum'      :", as_text.sum(), "<- joined, not added!")
print("numeric sum     :", as_text.astype(int).sum())
dates_text = pd.Series(["2025-12-01", "2025-02-15", "2025-11-30"])
print("max of text date:", dates_text.max(), "(works only because of YYYY-MM-DD)")
print("days between    :", (pd.to_datetime(dates_text).max() - pd.to_datetime(dates_text).min()).days)

print("\n=== astype ===")
sales["customer_id"] = sales["customer_id"].astype(str)
sales["date"] = pd.to_datetime(sales["date"])
print(sales.dtypes)

print("\n=== to_numeric with errors='coerce' ===")
raw = pd.Series(["12,500", "8,200", "n/a", "15,000", ""])
try:
    raw.astype(float)
except ValueError as e:
    print("astype(float) fails ->", e)
clean = pd.to_numeric(raw.str.replace(",", ""), errors="coerce")
print(clean.tolist(), "| failed:", clean.isna().sum())

print("\n=== to_datetime with errors='coerce' ===")
messy_dates = pd.Series(["2024-01-15", "2024-03-01", "not known"])
print(pd.to_datetime(messy_dates, errors="coerce"))

print("\n=== Nullable integers ===")
s = pd.Series(["1", "2", "x", None])
as_float = pd.to_numeric(s, errors="coerce")
print("plain  :", as_float.tolist(), as_float.dtype)
print("Int64  :", as_float.astype("Int64").tolist(), as_float.astype("Int64").dtype)

print("\n=== category: memory ===")
big = pd.concat([sales] * 50, ignore_index=True)       # 12,000 rows
before = big["region"].memory_usage(deep=True)
after = big["region"].astype("category").memory_usage(deep=True)
print(f"region as text    : {before:>8,} bytes")
print(f"region as category: {after:>8,} bytes  ({before / after:.0f}x smaller)")
cat = big["region"].astype("category")
print("categories:", cat.cat.categories.tolist())
print("codes     :", cat.cat.codes.head().tolist())

print("\n=== Ordered category ===")
sizes = pd.DataFrame({"item": ["A", "B", "C", "D"], "size": ["large", "small", "medium", "small"]})
print("A->Z sort  :", sizes.sort_values("size")["size"].tolist())
sizes["size"] = pd.Categorical(sizes["size"], categories=["small", "medium", "large"], ordered=True)
print("ordered    :", sizes.sort_values("size")["size"].tolist())
print("bigger than small:", sizes.loc[sizes["size"] > "small", "item"].tolist())

print("\n=== convert_dtypes ===")
print(pd.read_csv(DATA / "students.csv").convert_dtypes().dtypes)
