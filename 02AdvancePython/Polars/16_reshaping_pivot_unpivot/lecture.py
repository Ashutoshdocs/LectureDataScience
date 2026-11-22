"""Lecture 16: Reshaping: unpivot, pivot, transpose, explode, unnest, dummies."""
from pathlib import Path
import polars as pl
import polars.selectors as cs

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(140)

wide = pl.read_csv(DATA / "students.csv")
subjects = ["maths", "science", "english", "cs"]
# cs is Int64 and the others Float64 (they contain nulls). Unify before stacking.
wide = wide.with_columns(pl.col(subjects).cast(pl.Float64))
print("=== Wide ===")
print(wide.head(3))

print("\n=== unpivot: wide -> long ===")
long = wide.unpivot(index=["name", "class", "gender"], on=subjects,
                    variable_name="subject", value_name="mark")
print(long.head(8))
print("shape wide", wide.shape, "-> long", long.shape)
print("selectors work too:", wide.unpivot(index=cs.string(), on=cs.float()).shape)

print("\n=== Long format makes questions easy ===")
print(long.group_by("subject").agg(pl.col("mark").mean().round(1)).sort("mark", descending=True))
print(long.drop_nulls().group_by("name", maintain_order=True)
          .agg(best_subject=pl.col("subject").sort_by("mark").last(), best_mark=pl.col("mark").max()))
print(long.filter(pl.col("mark") < 60).sort("mark"))

print("\n=== pivot: long -> wide ===")
back = long.pivot(on="subject", index=["name", "class", "gender"], values="mark")
print(back.head(3))
print("round trip matches?", back.equals(wide))

print("\n=== pivot with aggregation (a pivot table) ===")
sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price")))
table = (sales.pivot(on="category", index="region", values="revenue", aggregate_function="sum")
              .sort("region")
              .with_columns(Total=pl.sum_horizontal("Electronics", "Furniture")))
totals = table.select(pl.lit("Total").alias("region"), cs.numeric().sum())
print(pl.concat([table, totals]))
print(sales.pivot(on="category", index="region", values="order_id", aggregate_function="len").sort("region"))

print("\n=== Monthly revenue by category ===")
print(sales.with_columns(month=pl.col("date").dt.strftime("%m-%b"))
           .pivot(on="category", index="month", values="revenue", aggregate_function="sum",
                  sort_columns=True)
           .sort("month").fill_null(0).head(6))

print("\n=== transpose ===")
print(wide.select("name", *subjects).head(3).transpose(include_header=True, header_name="field",
                                                       column_names="name"))

print("\n=== explode / back to lists ===")
orders = pl.DataFrame({"order": [1, 2], "items": [["pen", "book"], ["lamp"]]})
exploded = orders.explode("items")
print(exploded)
print(exploded.group_by("order", maintain_order=True).agg(pl.col("items")))

print("\n=== unnest a struct, one-hot dummies ===")
ship = pl.DataFrame({"order": [1, 2], "ship": [{"city": "Delhi", "days": 2}, {"city": "Pune", "days": 4}]})
print(ship.unnest("ship"))
print(wide.select("name", "class").to_dummies(columns=["class"]).head(4))
