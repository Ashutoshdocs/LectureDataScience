from pathlib import Path
import dask.dataframe as dd

from analysis import load_sales, prepare_sales, add_region_names, summarize_by_region

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
REGIONS_FILE = BASE_DIR / "data" / "reference" / "regions.csv"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sales_pattern = str(INPUT_DIR / "sales_part_*.csv")
    sales = load_sales(sales_pattern)
    regions = dd.read_csv(REGIONS_FILE, dtype={"region_id": "int64", "region_name": "object"})

    print("Dask DataFrame:", sales)
    print("Columns:", list(sales.columns))
    print("Dtypes:")
    print(sales.dtypes)
    print("Partitions:", sales.npartitions)

    prepared = prepare_sales(sales)
    enriched = add_region_names(prepared, regions)
    summary_query = summarize_by_region(enriched)

    print("\nHigh-value sales preview:")
    print(enriched[enriched["revenue"] > 10000].head())

    # Compute the small summary, not the full detailed dataset.
    summary = summary_query.compute()
    print("\nRegion summary:")
    print(summary)

    # Dask writes partitioned output.
    enriched.to_parquet(
        str(OUTPUT_DIR / "sales_parquet"),
        write_index=False,
        overwrite=True,
    )
    summary.to_csv(str(OUTPUT_DIR / "region_summary-*.csv"), index=False)

    print("\nOutputs saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
