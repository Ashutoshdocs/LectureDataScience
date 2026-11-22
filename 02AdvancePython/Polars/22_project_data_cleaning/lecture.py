"""Lecture 22: Project: cleaning a messy customer file with Polars expressions."""
import re
from pathlib import Path
import polars as pl

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
pl.Config.set_tbl_width_chars(170)
pl.Config.set_tbl_cols(12)
SRC = DATA / "messy_customers.csv"

raw = pl.read_csv(SRC, schema_overrides={"Customer ID": pl.String})
print("=== RAW ===")
print(raw)
raw.glimpse()

print("\n=== Look at every text column ===")
for col in ["City", "Age"]:
    print(col, "->", raw[col].unique(maintain_order=True).to_list())


def snake(name: str) -> str:
    """' Spend (Rs) ' -> 'spend_rs'"""
    return re.sub(r"\W+", "_", name.strip().lower()).strip("_")


print("\n=== 1. Column names ===")
df = raw.rename(snake).rename({"spend_rs": "spend"})
print(df.columns)

print("\n=== 2. Duplicates ===")
print("duplicate rows:", df.is_duplicated().sum() // 2)
df = df.unique(maintain_order=True)
print("rows now:", df.height)

print("\n=== 3. Strict casting tells you what's wrong ===")
try:
    df.with_columns(pl.col("age").cast(pl.Int64))
except pl.exceptions.InvalidOperationError as e:
    print("strict cast failed:", str(e).splitlines()[0][:110])

print("\n=== 4. Clean every column in ONE parallel with_columns ===")
EMAIL = r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$"
age = pl.col("age").cast(pl.Int64, strict=False)
df = df.with_columns(
    full_name=pl.col("full_name").str.strip_chars().str.replace_all(r"\s+", " ").str.to_titlecase(),
    email=pl.col("email").str.strip_chars().str.to_lowercase(),
    age=pl.when(age.is_between(0, 120)).then(age),                  # impossible -> null
    city=pl.col("city").str.strip_chars().str.to_titlecase().replace({"Bangalore": "Bengaluru"}),
    signup_date=pl.coalesce(pl.col("signup_date").str.to_date("%Y-%m-%d", strict=False),
                            pl.col("signup_date").str.to_date("%d/%m/%Y", strict=False)),
    spend=pl.col("spend").str.replace_all(",", "").cast(pl.Float64, strict=False),
).with_columns(
    email=pl.when(pl.col("email") == "").then(None).otherwise(pl.col("email")),
).with_columns(
    email_valid=pl.col("email").str.contains(EMAIL).fill_null(False),
)
print(df)
print(df.schema)

print("\n=== 5. What changed ===")
print("cities:", raw["City"].n_unique(), "spellings ->", df["city"].n_unique(), df["city"].unique().sort().to_list())
print("impossible ages removed:", raw["Age"].filter(raw["Age"].is_in(["-5", "250"])).to_list())

print("\n=== 6. Report ===")
print(f"rows: {raw.height} -> {df.height}")
nulls = df.null_count().transpose(include_header=True, header_name="column", column_names=["nulls"])
print(nulls.filter(pl.col("nulls") > 0))
review = df.filter(~pl.col("email_valid") | pl.any_horizontal(pl.all().is_null()))
print(f"{review.height} rows need human review:", review["customer_id"].to_list())

df.write_parquet(OUT / "customers_clean.parquet")
df.write_csv(OUT / "customers_clean.csv")
review.write_csv(OUT / "needs_review.csv")
print("types survive in Parquet:", pl.read_parquet(OUT / "customers_clean.parquet").schema["signup_date"],
      "| CSV:", pl.read_csv(OUT / "customers_clean.csv").schema["signup_date"])


# ---- The same steps as one reusable, lazy function ----
def clean(lf: pl.LazyFrame) -> pl.LazyFrame:
    age = pl.col("age").cast(pl.Int64, strict=False)
    return (lf.rename(snake).rename({"spend_rs": "spend"})
              .unique(maintain_order=True)
              .with_columns(
                  full_name=pl.col("full_name").str.strip_chars().str.replace_all(r"\s+", " ").str.to_titlecase(),
                  email=pl.col("email").str.strip_chars().str.to_lowercase(),
                  age=pl.when(age.is_between(0, 120)).then(age),
                  city=pl.col("city").str.strip_chars().str.to_titlecase().replace({"Bangalore": "Bengaluru"}),
                  signup_date=pl.coalesce(pl.col("signup_date").str.to_date("%Y-%m-%d", strict=False),
                                          pl.col("signup_date").str.to_date("%d/%m/%Y", strict=False)),
                  spend=pl.col("spend").str.replace_all(",", "").cast(pl.Float64, strict=False))
              .with_columns(email=pl.when(pl.col("email") == "").then(None).otherwise(pl.col("email")))
              .with_columns(email_valid=pl.col("email").str.contains(EMAIL).fill_null(False)))


lazy_result = clean(pl.scan_csv(SRC, schema_overrides={"Customer ID": pl.String})).collect()
print("\nclean() on a LazyFrame gives the same result?", lazy_result.equals(df))
