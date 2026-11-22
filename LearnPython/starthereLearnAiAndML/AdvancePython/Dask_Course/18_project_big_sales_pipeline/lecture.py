"""Lecture 18: Project: ingest 12 CSVs -> clean Parquet -> analyse in one pass -> Excel report."""
import logging
import shutil
import sys
import time
from pathlib import Path
import dask
import dask.dataframe as dd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from dask.distributed import Client, LocalCluster

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
CLEAN = OUT / "clean_parquet"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data          # noqa: E402

pd.set_option("display.width", 150)
pd.set_option("display.float_format", "{:,.1f}".format)
DTYPES = {"order_id": "int64", "region": "string", "product": "string", "category": "string",
          "units": "float64", "unit_price": "int64", "customer_id": "int64"}


def step(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")
    return time.perf_counter()


def ingest(folder: Path) -> dd.DataFrame:
    return dd.read_csv(folder / "sales_2025-*.csv", dtype=DTYPES, parse_dates=["timestamp"])


def clean(raw: dd.DataFrame) -> dd.DataFrame:
    df = raw.assign(units_missing=raw.units.isna(), units=raw.units.fillna(1))
    df = df.assign(
        revenue=df.units * df.unit_price,
        month=df.timestamp.dt.month,
        hour=df.timestamp.dt.hour,
        weekday=df.timestamp.dt.day_name(),
    )
    return df.astype({"region": "category", "product": "category", "category": "category"})


def analyse(df: dd.DataFrame, customers: pd.DataFrame):
    tasks = dict(
        kpis=df[["revenue", "units"]].sum(),
        orders=df.order_id.count(),
        customers=df.customer_id.nunique(),
        monthly=df.groupby("month").agg(orders=("order_id", "count"), revenue=("revenue", "sum")),
        region_cat=df.groupby(["region", "category"], observed=True).revenue.sum(),
        products=df.groupby("product", observed=True).agg(units=("units", "sum"), revenue=("revenue", "sum")),
        hours=df.groupby("hour").order_id.count(),
        top_customers=df.groupby("customer_id").revenue.sum().nlargest(10),
        missing=df.groupby("month").units_missing.sum(),
    )
    results = dict(zip(tasks, dask.compute(*tasks.values())))      # ONE pass over the data
    results["top_customers"] = (results["top_customers"].rename("revenue").reset_index()
                                .merge(customers, on="customer_id", how="left"))
    return results


def report(r: dict):
    monthly = r["monthly"].sort_index()
    monthly.index = pd.to_datetime(monthly.index, format="%m").strftime("%b")
    monthly["growth_%"] = monthly.revenue.pct_change() * 100
    monthly["revenue"] = monthly.revenue / 1e7
    monthly = monthly.rename(columns={"revenue": "revenue_cr"})
    region_cat = r["region_cat"].unstack() / 1e7
    products = r["products"].sort_values("revenue", ascending=False)
    products = products.assign(revenue_cr=products.revenue / 1e7).drop(columns="revenue")
    kpis = pd.Series({
        "orders": r["orders"], "customers": r["customers"], "units": r["kpis"]["units"],
        "revenue (Rs crore)": r["kpis"]["revenue"] / 1e7,
        "avg order (Rs)": r["kpis"]["revenue"] / r["orders"],
        "rows with missing units (filled)": int(r["missing"].sum()),
    })

    print("KPIs\n", kpis.to_string(float_format="{:,.1f}".format))
    print("\nMonthly\n", monthly)
    print("\nRevenue by region x category (Rs crore)\n", region_cat)
    print("\nProducts\n", products)
    print("\nBusiest hour:", r["hours"].idxmax(), "| quietest:", r["hours"].idxmin())
    print("\nTop 10 customers\n", r["top_customers"].assign(revenue=r["top_customers"].revenue / 1e5)
          .rename(columns={"revenue": "revenue_lakh"}))

    with pd.ExcelWriter(OUT / "sales_report.xlsx") as xl:
        kpis.to_frame("value").to_excel(xl, sheet_name="KPIs")
        monthly.to_excel(xl, sheet_name="Monthly")
        region_cat.to_excel(xl, sheet_name="Region x Category")
        products.to_excel(xl, sheet_name="Products")
        r["hours"].sort_index().to_frame("orders").to_excel(xl, sheet_name="Hours")
        r["top_customers"].to_excel(xl, sheet_name="Top customers", index=False)
        r["missing"].sort_index().to_frame("missing_units").to_excel(xl, sheet_name="Data quality")

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(monthly.index, monthly.revenue_cr, color="#2f62c9")
    ax.set_title("Monthly revenue, 2025 (Rs crore)")
    fig.savefig(OUT / "monthly_revenue.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("\nsaved output/sales_report.xlsx (7 sheets) and output/monthly_revenue.png")


def main():
    big = ensure_big_data()
    OUT.mkdir(exist_ok=True)
    with LocalCluster(n_workers=2, threads_per_worker=1, dashboard_address=":0",
                      silence_logs=logging.ERROR) as cluster, \
         Client(cluster) as client:
        print("dashboard:", client.dashboard_link)

        t = step("1-2. Ingest 12 CSVs, clean, write Parquet partitioned by month")
        shutil.rmtree(CLEAN, ignore_errors=True)
        clean(ingest(big)).to_parquet(CLEAN, partition_on=["month"], write_index=False)
        n_files = len(list(CLEAN.rglob("*.parquet")))
        csv_mb = sum(f.stat().st_size for f in big.glob("sales_*.csv")) / 1e6
        pq_mb = sum(f.stat().st_size for f in CLEAN.rglob("*.parquet")) / 1e6
        print(f"{n_files} Parquet files, {csv_mb:.0f} MB CSV -> {pq_mb:.0f} MB | {time.perf_counter() - t:.1f} s")

        t = step("3. Analyse: one dask.compute over the clean Parquet")
        df = dd.read_parquet(CLEAN)
        customers = pd.read_csv(big / "customers_big.csv")
        results = analyse(df, customers)
        print(f"analysis took {time.perf_counter() - t:.1f} s")

        t = step("4. Report")
        report(results)

        t = step("Bonus: read only Q4 with a partition filter")
        q4 = dd.read_parquet(CLEAN, filters=[("month", ">=", 10)])
        print(f"Q4 revenue Rs {q4.revenue.sum().compute() / 1e7:,.1f} crore "
              f"from {q4.npartitions} of {df.npartitions} partitions | {time.perf_counter() - t:.2f} s")


if __name__ == "__main__":
    main()
