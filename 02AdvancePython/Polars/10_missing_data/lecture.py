"""Lecture 10: Missing data: null vs NaN, find, drop, fill, interpolate."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
students = pl.read_csv(DATA / "students.csv")
marks = ["maths", "science", "english", "cs"]
print(students)

print("\n=== Finding ===")
print(students.null_count())
print(students.select(pl.all().is_null().mean().round(3)))
print(students.filter(pl.any_horizontal(pl.col(marks).is_null())).select("name", *marks))

print("\n=== Ints stay ints with nulls ===")
s = pl.Series("x", [1, None, 3])
print(s, "| dtype:", s.dtype)

print("\n=== null vs NaN ===")
nan_vs_null = pl.DataFrame({"with_null": [1.0, None, 3.0], "with_nan": [1.0, float("nan"), 3.0]})
print(nan_vs_null)
print(nan_vs_null.select(
    pl.col("with_null").mean().alias("mean_null"),
    pl.col("with_nan").mean().alias("mean_nan"),
    pl.col("with_null").is_null().sum().alias("nulls_in_null_col"),
    pl.col("with_nan").is_null().sum().alias("nulls_in_nan_col"),
    pl.col("with_nan").is_nan().sum().alias("nans_in_nan_col"),
))
print("fix:", nan_vs_null.with_columns(pl.col("with_nan").fill_nan(None)).null_count())

print("\n=== Dropping ===")
print("drop_nulls()               :", students.drop_nulls().height, "rows left")
print("drop_nulls(subset=['maths']):", students.drop_nulls(subset=["maths"]).height, "rows left")

print("\n=== Filling ===")
print(students.with_columns(pl.col(marks).fill_null(pl.col(marks).median()))
      .filter(pl.col("name").is_in(["Karan", "Omar", "Sara"])).select("name", *marks))
print(students.with_columns(
    maths_zero=pl.col("maths").fill_null(0),
    maths_class_avg=pl.col("maths").fill_null(pl.col("maths").mean().over("class")).round(1),
).filter(pl.col("maths").is_null()).select("name", "class", "maths", "maths_zero", "maths_class_avg"))

print("\n=== Time series: forward / backward / interpolate ===")
temps = pl.DataFrame({
    "day": pl.date_range(pl.date(2025, 6, 1), pl.date(2025, 6, 6), "1d", eager=True),
    "temp": [31.0, None, None, 34.0, None, 30.0],
})
print(temps.with_columns(
    forward=pl.col("temp").fill_null(strategy="forward"),
    backward=pl.col("temp").fill_null(strategy="backward"),
    interpolated=pl.col("temp").interpolate(),
))

print("\n=== coalesce: first non-null across columns ===")
contacts = pl.DataFrame({"mobile": [None, "98765", None], "office": ["2222", None, None]})
print(contacts.with_columns(best=pl.coalesce("mobile", "office", pl.lit("none"))))

print("\n=== Flag, then fill ===")
print(students.with_columns(
    maths_missing=pl.col("maths").is_null(),
    maths=pl.col("maths").fill_null(pl.col("maths").median()),
).filter(pl.col("maths_missing")).select("name", "maths", "maths_missing"))
