import polars as pl


REQUIRED_EMPLOYEE_COLUMNS = {
    "employee_id",
    "name",
    "department_id",
    "location",
    "salary",
    "joining_date",
}


def validate_employee_columns(df: pl.DataFrame) -> None:
    missing = REQUIRED_EMPLOYEE_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Employee file is missing columns: {sorted(missing)}")


def clean_employees(df: pl.DataFrame) -> pl.DataFrame:
    validate_employee_columns(df)

    # Convert salary to a numeric type; unparseable values become null.
    df = df.with_columns(
        pl.col("salary").cast(pl.Float64, strict=False)
    )

    # Teaching rule: fill missing salaries with the overall median.
    median_salary = df.select(pl.col("salary").median()).item()
    if median_salary is None:
        raise ValueError("Cannot fill salary: all salary values are missing.")

    df = df.with_columns(
        pl.col("salary").fill_null(median_salary)
    )

    # Parse date strings using the known input format.
    df = df.with_columns(
        pl.col("joining_date").str.to_date("%Y-%m-%d", strict=False)
    )

    return df.with_columns(
        (pl.col("salary") * 12).alias("annual_salary"),
        pl.when(pl.col("salary") >= 75000)
        .then(pl.lit("High"))
        .when(pl.col("salary") >= 65000)
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("Standard"))
        .alias("salary_band"),
    )


def join_departments(employees: pl.DataFrame, departments: pl.DataFrame) -> pl.DataFrame:
    return employees.join(
        departments,
        on="department_id",
        how="left",
    )


def department_summary(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by(["department_id", "department_name"])
        .agg(
            pl.len().alias("employee_count"),
            pl.col("salary").mean().round(2).alias("average_salary"),
            pl.col("salary").max().alias("maximum_salary"),
            pl.col("annual_salary").sum().alias("total_annual_salary"),
        )
        .sort("average_salary", descending=True)
    )
