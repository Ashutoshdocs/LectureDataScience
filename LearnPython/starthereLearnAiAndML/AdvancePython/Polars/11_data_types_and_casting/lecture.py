"""Lecture 11: Data types & casting: strict vs non-strict, text -> numbers/dates, Enum, memory."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
print(sales.schema)

print("\n=== cast ===")
cast_demo = sales.select(
    pl.col("units").cast(pl.Int8).alias("units_i8"),
    pl.col("unit_price").cast(pl.Float32).alias("price_f32"),
    pl.col("customer_id").cast(pl.String).alias("cust_str"),
)
print(cast_demo.head(3))

print("\n=== Polars refuses to mix types ===")
try:
    pl.DataFrame({"a": [1, "two", 3]})
except Exception as e:
    print(type(e).__name__, "->", str(e).splitlines()[0][:90])
print(pl.DataFrame({"a": [1, "two", 3]}, strict=False))   # opt-in: everything becomes a supertype

print("\n=== strict=True vs strict=False ===")
raw = pl.DataFrame({"age": ["34", "29", "n/a", "41"]})
try:
    raw.with_columns(pl.col("age").cast(pl.Int64))
except pl.exceptions.InvalidOperationError as e:
    print("strict cast fails ->", str(e).splitlines()[0][:80])
lenient = raw.with_columns(pl.col("age").cast(pl.Int64, strict=False))
print(lenient, "| failed:", lenient["age"].null_count())

print("\n=== Numbers stored as text ===")
money = pl.DataFrame({"spend": ["12,500", "8,200", "n/a", "15,000"]})
print(money.with_columns(
    pl.col("spend").str.replace_all(",", "").cast(pl.Float64, strict=False).alias("spend_num")))

print("\n=== Text to dates ===")
d = pl.DataFrame({"raw": ["2024-01-15", "15/02/2024", "not known"]})
print(d.with_columns(
    iso=pl.col("raw").str.to_date("%Y-%m-%d", strict=False),
    dmy=pl.col("raw").str.to_date("%d/%m/%Y", strict=False),
).with_columns(combined=pl.coalesce("iso", "dmy")))

print("\n=== Categorical vs Enum ===")
sizes = pl.DataFrame({"item": ["A", "B", "C", "D"], "size": ["large", "small", "medium", "small"]})
print("String sort:", sizes.sort("size")["size"].to_list())
size_enum = pl.Enum(["small", "medium", "large"])
sized = sizes.with_columns(pl.col("size").cast(size_enum))
print("Enum sort  :", sized.sort("size")["size"].to_list())
print("bigger than small:", sized.filter(pl.col("size") > "small")["item"].to_list())
try:
    pl.Series(["small", "huge"]).cast(size_enum)
except pl.exceptions.InvalidOperationError as e:
    print("Enum rejects typo/unknown 'huge' ->", type(e).__name__)

print("\n=== Memory ===")
big = sales.sample(100_000, with_replacement=True, seed=1)
as_str = big.select("region").estimated_size("kb")
as_cat = big.select(pl.col("region").cast(pl.Categorical)).estimated_size("kb")
as_enum = big.select(pl.col("region").cast(pl.Enum(["East", "North", "South", "West"]))).estimated_size("kb")
print(f"region String     : {as_str:8.1f} KB")
print(f"region Categorical: {as_cat:8.1f} KB  ({as_str / as_cat:.1f}x smaller)")
print(f"region Enum       : {as_enum:8.1f} KB  ({as_str / as_enum:.1f}x smaller)")

print("\n=== Smallest type that fits (Series.shrink_dtype) ===")
for name in ["units", "unit_price"]:
    print(f"{name:10} {big[name].dtype} -> {big[name].shrink_dtype().dtype}")
print(f"units as Int8: {big.select('units').estimated_size('kb'):.0f} KB -> "
      f"{big.select(pl.col('units').cast(pl.Int8)).estimated_size('kb'):.0f} KB")
