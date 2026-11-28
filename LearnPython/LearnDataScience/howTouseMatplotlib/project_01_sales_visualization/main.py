from pathlib import Path
import logging

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "sales_visualization.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def main():
    # Read transaction data and convert the date column into datetime values.
    df = pd.read_csv(INPUT_DIR / "sales.csv", parse_dates=["date"])

    # Calculate revenue for each transaction.
    df["revenue"] = df["units"] * df["unit_price"]

    # Aggregate revenue by month, region, and product.
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month", as_index=False)["revenue"].sum()
    regional = df.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    product = df.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)

    # Save a compact summary table for later use.
    summary = df.groupby(["region", "product"], as_index=False).agg(
        units_sold=("units", "sum"),
        revenue=("revenue", "sum"),
    )
    summary.to_csv(OUTPUT_DIR / "sales_summary.csv", index=False)

    # Chart 1: revenue trend over time.
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["month"], monthly["revenue"], marker="o", linewidth=2)
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # Chart 2: compare revenue across regions.
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(regional["region"], regional["revenue"])
    ax.bar_label(bars, fmt="%.0f", padding=3)
    ax.set_title("Revenue by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Revenue")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "revenue_by_region.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # Chart 3: compare products using a horizontal bar chart.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(product["product"], product["revenue"])
    ax.set_title("Revenue by Product")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Product")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "revenue_by_product.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    logging.info("Sales visualization completed. Rows processed: %s", len(df))
    print(f"Processed {len(df)} rows. Results saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
