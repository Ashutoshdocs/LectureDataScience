"""Lecture 23: Recap. A self-test across the course. Predict each answer, then run."""
from pathlib import Path
import polars as pl
import polars.selectors as cs

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(140)

sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price")))
customers = pl.read_csv(DATA / "customers.csv")
students = pl.read_csv(DATA / "students.csv")
marks = ["maths", "science", "english", "cs"]

questions = [
    ("L04 | Rows and columns in sales (incl. revenue)?",
     lambda: sales.shape),
    ("L04 | Most common product?",
     lambda: sales["product"].value_counts(sort=True).row(0)[0]),
    ("L06 | Numeric columns, excluding ids?",
     lambda: sales.select(cs.numeric() - cs.ends_with("_id")).columns),
    ("L07 | North orders with 5 units?",
     lambda: sales.filter(region="North", units=5).height),
    ("L08 | Share of bulk orders (units >= 4)?",
     lambda: round(sales.select((pl.col("units") >= 4).mean()).item(), 3)),
    ("L09 | Top 3 students by cs?",
     lambda: students.top_k(3, by="cs")["name"].to_list()),
    ("L10 | Students with no missing marks?",
     lambda: students.drop_nulls().height),
    ("L12 | Products ending in 'er'?",
     lambda: sorted(sales.filter(pl.col("product").str.ends_with("er"))["product"].unique().to_list())),
    ("L13 | Revenue by category (Rs lakh)?",
     lambda: dict(sales.group_by("category").agg((pl.col("revenue").sum() / 1e5).round(1)).sort("category").rows())),
    ("L14 | Ravi's rank in his class by total marks?",
     lambda: students.with_columns(total=pl.sum_horizontal(marks))
                     .with_columns(r=pl.col("total").rank("min", descending=True).over("class"))
                     .filter(name="Ravi")["r"].item()),
    ("L15 | Customers who never ordered (anti join)?",
     lambda: customers.join(sales, on="customer_id", how="anti")["name"].to_list()),
    ("L16 | Average mark per subject (unpivot)?",
     lambda: dict(students.unpivot(index="name", on=marks, variable_name="s", value_name="m")
                  .group_by("s").agg(pl.col("m").mean().round(1)).sort("s").rows())),
    ("L17 | Best quarter by revenue?",
     lambda: sales.group_by(q=pl.col("date").dt.quarter()).agg(pl.col("revenue").sum()).sort("revenue").row(-1)[0]),
    ("L17 | Orders on a Sunday (weekday 7)?",
     lambda: sales.filter(pl.col("date").dt.weekday() == 7).height),
    ("L18 | Columns the lazy scan reads for 'units by region'?",
     lambda: [line.strip() for line in pl.scan_csv(DATA / "sales.csv")
              .group_by("region").agg(pl.col("units").sum()).explain().splitlines() if "PROJECT" in line]),
    ("L20 | Same answer in SQL: total units?",
     lambda: sales.sql("SELECT SUM(units) AS u FROM self").item()),
]

for i, (q, answer) in enumerate(questions, start=1):
    print(f"\nQ{i:02}. {q}")
    print(answer())

print("\nIf every answer matched your prediction, you're ready to use Polars on real data. Well done!")
