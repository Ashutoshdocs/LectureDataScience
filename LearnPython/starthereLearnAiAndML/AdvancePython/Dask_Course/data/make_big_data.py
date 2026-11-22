"""Create a 'big' multi-file sales dataset for the Dask lectures.

12 monthly CSV files (data/big/sales_2025-01.csv ... sales_2025-12.csv),
200,000 rows each = 2.4 million rows, about 160 MB in total.

Lectures call ensure_big_data(), which builds the files only if they're missing.
Run directly to (re)build:  python make_big_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BIG = HERE / "big"
ROWS_PER_MONTH = 200_000

PRODUCTS = ["Laptop", "Phone", "Tablet", "Headphones", "Charger", "Desk", "Chair", "Lamp"]
CATEGORY = ["Electronics"] * 5 + ["Furniture"] * 3
PRICE = [55000, 25000, 18000, 3500, 900, 12000, 7500, 1500]
WEIGHTS = [.10, .18, .10, .17, .20, .07, .08, .10]
REGIONS = ["North", "South", "East", "West"]


def build_month(month: int, rng: np.random.Generator) -> pd.DataFrame:
    n = ROWS_PER_MONTH
    start = pd.Timestamp(2025, month, 1)
    days = start.days_in_month
    idx = rng.choice(len(PRODUCTS), size=n, p=WEIGHTS)
    df = pd.DataFrame({
        "order_id": (month * 1_000_000) + np.arange(n),
        "timestamp": start + pd.to_timedelta(rng.integers(0, days * 86_400, n), unit="s"),
        "region": rng.choice(REGIONS, n, p=[.3, .25, .25, .2]),
        "product": np.array(PRODUCTS)[idx],
        "category": np.array(CATEGORY)[idx],
        "units": rng.integers(1, 6, n),
        "unit_price": np.array(PRICE)[idx],
        "customer_id": rng.integers(1, 20_001, n),
    }).sort_values("timestamp")
    # a few messy values, so cleaning steps have something to do
    bad = rng.choice(n, size=n // 1000, replace=False)
    df.loc[df.index[bad], "units"] = np.nan
    return df


def ensure_big_data(verbose: bool = True) -> Path:
    BIG.mkdir(exist_ok=True)
    files = [BIG / f"sales_2025-{m:02d}.csv" for m in range(1, 13)]
    if all(f.exists() for f in files):
        return BIG
    if verbose:
        print("Building data/big/ (12 CSV files, 2.4M rows), one-time, ~10 seconds...")
    rng = np.random.default_rng(2025)
    for m, f in enumerate(files, start=1):
        if not f.exists():
            build_month(m, rng).to_csv(f, index=False)
    customers = pd.DataFrame({
        "customer_id": np.arange(1, 20_001),
        "segment": rng.choice(["Retail", "Business"], 20_000, p=[.7, .3]),
        "city": rng.choice(["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru", "Pune"], 20_000),
    })
    customers.to_csv(BIG / "customers_big.csv", index=False)
    return BIG


def ensure_big_parquet(verbose: bool = True) -> Path:
    """The same 2.4M rows as Parquet (data/big_parquet/), built once from the CSVs."""
    out = HERE / "big_parquet"
    if out.exists() and any(out.glob("*.parquet")):
        return out
    import dask.dataframe as dd
    ensure_big_data(verbose)
    if verbose:
        print("Converting data/big/*.csv to Parquet (one-time, ~5 seconds)...")
    (dd.read_csv(BIG / "sales_2025-*.csv", parse_dates=["timestamp"],
                 dtype={"units": "float64", "unit_price": "int64", "customer_id": "int64"})
       .to_parquet(out, write_index=False))
    return out


if __name__ == "__main__":
    import shutil
    shutil.rmtree(BIG, ignore_errors=True)
    path = ensure_big_data()
    size = sum(f.stat().st_size for f in path.glob("*.csv")) / 1e6
    print(f"Wrote {len(list(path.glob('*.csv')))} files, {size:.0f} MB, to {path}")
