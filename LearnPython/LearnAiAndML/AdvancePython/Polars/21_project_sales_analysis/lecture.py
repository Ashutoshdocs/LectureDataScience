"""Lecture 21: Project: sales analysis as a lazy Polars pipeline -> Excel + charts."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import polars as pl
import polars.selectors as cs
import xlsxwriter

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
pl.Config.set_tbl_width_chars(140)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_rows(15)
pl.Config.set_thousands_separator(",")


def heading(text):
    print("\n" + text.upper() + "\n" + "-" * len(text))


def base() -> pl.LazyFrame:
    sales = pl.scan_csv(DATA / "sales.csv", try_parse_dates=True)
    customers = pl.scan_csv(DATA / "customers.csv", try_parse_dates=True)
    return (sales.join(customers, on="customer_id", how="left", validate="m:1")
                 .with_columns(revenue=pl.col("units") * pl.col("unit_price"),
                               weekday=pl.col("date").dt.weekday(),
                               day_name=pl.col("date").dt.strftime("%A")))


def kpis(lf):
    return lf.select(
        orders=pl.len(),
        customers=pl.col("customer_id").n_unique(),
        units=pl.col("units").sum(),
        revenue=pl.col("revenue").sum(),
        avg_order=pl.col("revenue").mean().round(0),
        median_order=pl.col("revenue").median(),
    ).cast(pl.Int64)                       # one type, so transposing keeps whole numbers


def products(lf):
    return (lf.group_by("product")
              .agg(orders=pl.len(), units=pl.col("units").sum(), revenue=pl.col("revenue").sum())
              .with_columns(revenue_rank=pl.col("revenue").rank("min", descending=True),
                            units_rank=pl.col("units").rank("min", descending=True))
              .sort("revenue", descending=True))


def monthly(lf):
    return (lf.sort("date")
              .group_by_dynamic("date", every="1mo")
              .agg(orders=pl.len(), revenue=pl.col("revenue").sum())
              .with_columns(month=pl.col("date").dt.strftime("%Y-%m"),
                            growth_pct=(pl.col("revenue").pct_change() * 100).round(1),
                            avg_order=(pl.col("revenue") / pl.col("orders")).round(0),
                            ytd=pl.col("revenue").cum_sum())
              .select("month", "orders", "revenue", "growth_pct", "avg_order", "ytd"))


def top_customers(lf, n=5):
    return (lf.group_by("customer_id", "name", "city", "segment")
              .agg(orders=pl.len(), revenue=pl.col("revenue").sum())
              .top_k(n, by="revenue").sort("revenue", descending=True))


def segments(lf):
    return (lf.group_by("segment")
              .agg(customers=pl.col("customer_id").n_unique(), orders=pl.len(),
                   avg_order=pl.col("revenue").mean().round(0), revenue=pl.col("revenue").sum())
              .sort("segment"))


def customer_spend(lf):
    return lf.group_by("customer_id").agg(spent=pl.col("revenue").sum()).sort("spent", descending=True)


def weekdays(lf):
    return (lf.group_by("weekday", "day_name").agg(orders=pl.len(), revenue=pl.col("revenue").sum())
              .sort("weekday"))


def best_product_per_region(lf):
    return (lf.group_by("region", "product").agg(revenue=pl.col("revenue").sum())
              .filter(pl.col("revenue") == pl.col("revenue").max().over("region"))
              .sort("region"))


lf = base()
k, prod, mon, top5, seg, spend, wd, best = pl.collect_all([
    kpis(lf), products(lf), monthly(lf), top_customers(lf), segments(lf),
    customer_spend(lf), weekdays(lf), best_product_per_region(lf),
])

# The pivot is eager-only, so collect the base once for it
rc = (lf.collect()
        .pivot(on="category", index="region", values="revenue", aggregate_function="sum")
        .sort("region")
        .with_columns(Total=pl.sum_horizontal("Electronics", "Furniture")))
rc = pl.concat([rc, rc.select(pl.lit("Total").alias("region"), cs.numeric().sum())])

heading("1. Key figures")
print(k.transpose(include_header=True, header_name="metric", column_names=["value"]))

heading("2. Revenue by region and category (Rs lakh)")
print(rc.with_columns((cs.numeric() / 1e5).round(1)))

heading("3. Products")
print(prod)

heading("4. Month by month")
print(mon)
print("best month:", mon.sort("revenue").row(-1, named=True)["month"],
      "| weakest:", mon.sort("revenue").row(0, named=True)["month"])

heading("5. Top 5 customers")
print(top5)

heading("6. Retail vs Business")
print(seg)

heading("7. Revenue concentration")
n_top = round(spend.height * 0.2)
share = spend.head(n_top)["spent"].sum() / spend["spent"].sum() * 100
print(f"The top {n_top} of {spend.height} customers (20%) bring in {share:.1f}% of revenue")

heading("8. Busiest weekday")
print(wd)
print("busiest by revenue:", wd.sort("revenue").row(-1, named=True)["day_name"])

heading("9. Best product in each region")
print(best)

heading("Saving")
with xlsxwriter.Workbook(OUT / "sales_report.xlsx") as wb:
    for name, frame in [("KPIs", k), ("Region x Category", rc), ("Products", prod), ("Monthly", mon),
                        ("Top customers", top5), ("Segments", seg), ("Weekdays", wd),
                        ("Best per region", best)]:
        frame.write_excel(workbook=wb, worksheet=name, autofit=True)
print("saved output/sales_report.xlsx with",
      len(pl.read_excel(OUT / "sales_report.xlsx", sheet_id=0)), "sheets")

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(mon["month"].str.slice(5).to_list(), (mon["revenue"] / 1e5).to_list(), marker="o", color="#2f62c9")
ax.set_title("Monthly revenue (Rs lakh)"); ax.grid(True, alpha=0.3)
fig.savefig(OUT / "monthly_revenue.png", dpi=150, bbox_inches="tight"); plt.close(fig)

p = prod.sort("revenue")
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.barh(p["product"].to_list(), (p["revenue"] / 1e5).to_list(), color="#2f62c9")
ax.set_title("Revenue by product (Rs lakh)")
fig.savefig(OUT / "product_revenue.png", dpi=150, bbox_inches="tight"); plt.close(fig)
print("saved output/monthly_revenue.png and output/product_revenue.png")
