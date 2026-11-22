"""Lecture 02: Series & DataFrame: creating, schema, anatomy, no index."""
import numpy as np
import polars as pl

print("=== Series ===")
steps = pl.Series("steps", [4200, 6100, 5300, 8800, 7600])
print(steps)
print("name:", steps.name, "| dtype:", steps.dtype, "| len:", len(steps))
print("mean:", steps.mean(), "| max:", steps.max(), "| doubled:", (steps * 2).to_list())
print("mask > 6000:", steps.filter(steps > 6000).to_list())
print("position of max:", steps.arg_max())

days = pl.Series("day", ["Mon", "Tue", "Wed", "Thu", "Fri"])
week = pl.DataFrame([days, steps])                   # labels live in their own column
print(week)

print("\n=== Creating DataFrames ===")
by_cols = pl.DataFrame({"name": ["Asha", "Ravi", "Meena"], "maths": [78, 92, 45]})
by_rows = pl.DataFrame([{"name": "Asha", "maths": 78}, {"name": "Ravi"}])   # missing -> null
by_list = pl.DataFrame([["Asha", 78], ["Ravi", 92]], schema=["name", "maths"], orient="row")
typed = pl.DataFrame({"name": ["Asha"], "maths": [78]},
                     schema={"name": pl.String, "maths": pl.Int16})
from_np = pl.DataFrame(np.arange(6).reshape(3, 2), schema=["x", "y"])
for label, frame in [("dict of lists", by_cols), ("list of dicts", by_rows),
                     ("rows", by_list), ("typed", typed), ("numpy", from_np)]:
    print(f"\n{label}:", frame.schema)
print(by_rows)

print("\n=== schema_overrides ===")
products = pl.DataFrame(
    [{"product": "Pen", "price": 10, "stock": 300},
     {"product": "Book", "price": 250, "stock": 40},
     {"product": "Lamp", "price": 1500, "stock": 12},
     {"product": "Desk", "price": 12000, "stock": 3}],
    schema_overrides={"price": pl.Float32})
print(products)

print("\n=== Anatomy ===")
print("shape:", products.shape, "| height:", products.height, "| width:", products.width)
print("columns:", products.columns)
print("dtypes :", products.dtypes)
print("column :", products["price"].to_list())
print("row 2 as tuple:", products.row(2))
print("row 2 as dict :", products.row(2, named=True))
print("as dicts:", products.to_dicts()[:2])

print("\n=== No index: use a filter or a row number ===")
print(products.filter(pl.col("product") == "Lamp"))
print(products.with_row_index("row_nr"))

print("\n=== Methods return new frames ===")
products.sort("price", descending=True)
print("unchanged:", products["product"].to_list())
products = products.sort("price", descending=True)
print("reassigned:", products["product"].to_list())

print("\n=== Nested types ===")
nested = pl.DataFrame({"order": [1, 2], "items": [["pen", "book"], ["lamp"]],
                       "ship": [{"city": "Delhi", "days": 2}, {"city": "Pune", "days": 4}]})
print(nested)
print(nested.schema)
