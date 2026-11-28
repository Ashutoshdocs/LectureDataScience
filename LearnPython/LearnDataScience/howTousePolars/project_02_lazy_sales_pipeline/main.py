from pathlib import Path
import polars as pl

from pipeline import build_sales_query, build_sales_summary

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
PRODUCTS_FILE = BASE_DIR / "data" / "reference" / "products.csv"
REPORTS_DIR = BASE_DIR / "output" / "reports"
PARQUET_DIR = BASE_DIR / "output" / "parquet"
LOGS_DIR = BASE_DIR / "logs"


def main():
    for folder in [REPORTS_DIR, PARQUET_DIR, LOGS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

    sales_query = build_sales_query(INPUT_DIR, PRODUCTS_FILE)
    summary_query = build_sales_summary(sales_query)

    print("Lazy query plan:")
    print(summary_query.explain())

    # collect() triggers execution and returns an eager DataFrame.
    detailed_sales = sales_query.collect()
    summary = summary_query.collect()

    print("\nDetailed sales:")
    print(detailed_sales)

    print("\nSales summary:")
    print(summary)

    detailed_sales.write_parquet(PARQUET_DIR / "detailed_sales.parquet")
    summary.write_parquet(PARQUET_DIR / "sales_summary.parquet")
    summary.write_csv(REPORTS_DIR / "sales_summary.csv")

    print("\nOutputs saved under:", BASE_DIR / "output")


if __name__ == "__main__":
    main()
