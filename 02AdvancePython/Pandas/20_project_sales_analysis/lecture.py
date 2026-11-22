"""Lecture 20: Project: a complete sales analysis, from raw CSV to Excel report."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
pd.set_option("display.width", 140)
pd.set_option("display.float_format", "{:,.1f}".format)


def heading(text):
    print("\n" + text.upper())
    print("-" * len(text))


def load():
    sales = pd.read_csv(DATA / "sales.csv", parse_dates=["date"])
    customers = pd.read_csv(DATA / "customers.csv", parse_dates=["joined"])
    assert sales["order_id"].is_unique, "duplicate order ids!"
    assert sales.isna().sum().sum() == 0, "unexpected missing values"
    full = sales.merge(customers, on="customer_id", how="left", validate="many_to_one")
    assert len(full) == len(sales)
    return full.assign(revenue=lambda d: d["units"] * d["unit_price"],
                       month=lambda d: d["date"].dt.to_period("M"),
                       weekday=lambda d: d["date"].dt.day_name())


def kpis(df):
    return pd.Series({
        "Orders": len(df),
        "Customers": df["customer_id"].nunique(),
        "Units sold": df["units"].sum(),
        "Revenue (Rs)": df["revenue"].sum(),
        "Avg order value (Rs)": df["revenue"].mean(),
        "Median order value (Rs)": df["revenue"].median(),
    }).round().astype(int)


def by_region_category(df):
    return df.pivot_table(index="region", columns="category", values="revenue",
                          aggfunc="sum", margins=True, margins_name="Total")


def products(df):
    out = df.groupby("product").agg(orders=("order_id", "count"), units=("units", "sum"),
                                    revenue=("revenue", "sum"))
    out["revenue_rank"] = out["revenue"].rank(ascending=False, method="min").astype(int)
    out["units_rank"] = out["units"].rank(ascending=False, method="min").astype(int)
    return out.sort_values("revenue", ascending=False)


def monthly(df):
    m = df.groupby("month").agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
    m["growth_%"] = (m["revenue"].pct_change() * 100).round(1)
    m["avg_order"] = (m["revenue"] / m["orders"]).round(0)
    return m


def top_customers(df, n=5):
    return (df.groupby(["customer_id", "name", "city", "segment"], as_index=False)
              .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
              .nlargest(n, "revenue"))


def segments(df):
    return df.groupby("segment").agg(customers=("customer_id", "nunique"),
                                     orders=("order_id", "count"),
                                     avg_order=("revenue", "mean"),
                                     revenue=("revenue", "sum")).round(0)


def concentration(df):
    spend = df.groupby("customer_id")["revenue"].sum().sort_values(ascending=False)
    top = spend.head(round(len(spend) * 0.2))
    return top.sum() / spend.sum() * 100, len(top), len(spend)


full = load()

heading("1. Key figures")
k = kpis(full)
print(k.map("{:,}".format).to_string())

heading("2. Revenue by region and category (Rs lakh)")
rc = by_region_category(full)
print((rc / 1e5).round(1))

heading("3. Products")
prod = products(full)
print(prod)

heading("4. Month by month")
mon = monthly(full)
print(mon)
print("best month:", mon["revenue"].idxmax(), "| weakest:", mon["revenue"].idxmin())

heading("5. Top 5 customers")
top5 = top_customers(full)
print(top5.to_string(index=False))

heading("6. Retail vs Business")
seg = segments(full)
print(seg)

heading("7. Revenue concentration")
share, n_top, n_all = concentration(full)
print(f"The top {n_top} of {n_all} customers (20%) bring in {share:.1f}% of revenue")

heading("8. Busiest weekday")
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = full.groupby("weekday")["revenue"].agg(["count", "sum"]).reindex(days)
print(wd)
print("busiest by revenue:", wd["sum"].idxmax())

heading("9. Saving the report")
with pd.ExcelWriter(OUT / "sales_report.xlsx") as xl:
    k.to_frame("value").to_excel(xl, sheet_name="KPIs")
    rc.to_excel(xl, sheet_name="Region x Category")
    prod.to_excel(xl, sheet_name="Products")
    mon.assign(month=mon.index.astype(str)).set_index("month").to_excel(xl, sheet_name="Monthly")
    top5.to_excel(xl, sheet_name="Top customers", index=False)
    seg.to_excel(xl, sheet_name="Segments")
print("saved output/sales_report.xlsx")

ax = (mon["revenue"] / 1e5).plot(marker="o", figsize=(8, 3.5), color="#2f62c9", grid=True,
                                 title="Monthly revenue (Rs lakh)", xlabel="")
ax.figure.savefig(OUT / "monthly_revenue.png", dpi=150, bbox_inches="tight"); plt.close(ax.figure)
ax = (prod["revenue"].sort_values() / 1e5).plot.barh(figsize=(6, 3.5), color="#2f62c9",
                                                      title="Revenue by product (Rs lakh)", ylabel="")
ax.figure.savefig(OUT / "product_revenue.png", dpi=150, bbox_inches="tight"); plt.close(ax.figure)
print("saved output/monthly_revenue.png and output/product_revenue.png")
