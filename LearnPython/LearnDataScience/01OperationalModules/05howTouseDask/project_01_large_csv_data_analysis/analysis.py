import dask.dataframe as dd


def load_sales(input_pattern: str) -> dd.DataFrame:
    return dd.read_csv(
        input_pattern,
        dtype={
            "order_id": "int64",
            "order_date": "object",
            "region_id": "int64",
            "product": "object",
            "quantity": "int64",
            "unit_price": "float64",
        },
    )


def prepare_sales(sales: dd.DataFrame) -> dd.DataFrame:
    sales = sales[sales["quantity"] > 0]
    sales = sales[sales["unit_price"] >= 0]
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    return sales


def add_region_names(sales: dd.DataFrame, regions: dd.DataFrame) -> dd.DataFrame:
    return sales.merge(regions, on="region_id", how="left")


def summarize_by_region(sales: dd.DataFrame) -> dd.DataFrame:
    return (
        sales.groupby("region_name")["revenue"]
        .agg(["sum", "mean", "count"])
        .reset_index()
    )
