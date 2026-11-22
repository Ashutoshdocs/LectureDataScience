"""Lecture 14: Window functions: group values on every row with .over()."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(160)
pl.Config.set_tbl_cols(12)

sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price")))
students = (pl.read_csv(DATA / "students.csv")
              .with_columns(total=pl.sum_horizontal("maths", "science", "english", "cs")))

print("=== agg shrinks, over keeps every row ===")
print(sales.group_by("region").agg(pl.col("revenue").mean().round(0)).sort("region"))
print(sales.with_columns(region_avg=pl.col("revenue").mean().over("region").round(0))
           .select("region", "revenue", "region_avg").head(5))

print("\n=== Common window patterns ===")
print(sales.with_columns(
    vs_region_avg=(pl.col("revenue") - pl.col("revenue").mean().over("region")).round(0),
    pct_of_category=(pl.col("revenue") / pl.col("revenue").sum().over("category") * 100).round(2),
    orders_in_region=pl.len().over("region"),
    rank_in_region=pl.col("revenue").rank("min", descending=True).over("region"),
).select("region", "category", "revenue", "vs_region_avg", "pct_of_category",
         "orders_in_region", "rank_in_region").head(6))

print("\n=== Rank students within class ===")
print(students.with_columns(
    class_rank=pl.col("total").rank("min", descending=True).over("class"),
    class_avg=pl.col("total").mean().over("class").round(1),
).sort("class", "class_rank").select("name", "class", "total", "class_avg", "class_rank"))

print("\n=== Top 2 orders per region ===")
print(sales.filter(pl.col("revenue").rank("ordinal", descending=True).over("region") <= 2)
           .sort("region", "revenue", descending=[False, True])
           .select("region", "order_id", "product", "revenue"))

print("\n=== Running values per customer (ordered by date) ===")
per_customer = sales.with_columns(
    order_no=pl.int_range(1, pl.len() + 1).over("customer_id", order_by="date"),
    running_spend=pl.col("revenue").cum_sum().over("customer_id", order_by="date"),
    days_since_prev=pl.col("date").diff().over("customer_id", order_by="date").dt.total_days(),
)
print(per_customer.filter(pl.col("customer_id") == 1)
                  .select("customer_id", "date", "revenue", "order_no", "running_spend", "days_since_prev"))
print("median days between a customer's orders:", per_customer["days_since_prev"].median())

print("\n=== Several group columns ===")
print(sales.with_columns(n=pl.len().over("region", "category"))
           .select("region", "category", "n").unique().sort("region", "category"))

print("\n=== Fill nulls with the group mean ===")
print(students.with_columns(maths_filled=pl.col("maths").fill_null(pl.col("maths").mean().over("class")).round(1))
              .filter(pl.col("maths").is_null()).select("name", "class", "maths", "maths_filled"))
