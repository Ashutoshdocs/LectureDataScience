from pathlib import Path
import polars as pl


def build_sales_query(input_dir: Path, products_file: Path) -> pl.LazyFrame:
    """
    Build a lazy sales query.

    Execution is deferred until collect() is called by the caller.
    """
    sales_files = str(input_dir / "sales_*.csv")

    sales = pl.scan_csv(
        sales_files,
        schema_overrides={
            "order_id": pl.Int64,
            "order_date": pl.String,
            "product_id": pl.String,
            "region": pl.String,
            "quantity": pl.Int64,
            "unit_price": pl.Float64,
        },
    )

    products = pl.scan_csv(
        products_file,
        schema_overrides={
            "product_id": pl.String,
            "product_name": pl.String,
            "category": pl.String,
        },
    )

    return (
        sales
        .filter(
            pl.col("quantity").is_not_null()
            & (pl.col("quantity") > 0)
            & pl.col("unit_price").is_not_null()
            & (pl.col("unit_price") >= 0)
        )
        .join(products, on="product_id", how="left")
        .with_columns(
            pl.col("order_date").str.to_date("%Y-%m-%d", strict=False),
            (pl.col("quantity") * pl.col("unit_price")).alias("revenue"),
        )
        .select(
            "order_id",
            "order_date",
            "product_id",
            "product_name",
            "category",
            "region",
            "quantity",
            "unit_price",
            "revenue",
        )
    )


def build_sales_summary(sales_query: pl.LazyFrame) -> pl.LazyFrame:
    return (
        sales_query
        .group_by(["region", "product_name", "category"])
        .agg(
            pl.col("quantity").sum().alias("units_sold"),
            pl.col("revenue").sum().round(2).alias("total_revenue"),
            pl.len().alias("order_line_count"),
        )
        .sort("total_revenue", descending=True)
    )
