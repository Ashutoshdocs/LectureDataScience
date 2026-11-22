"""Lecture 06: Reading & writing: globs, blocksize, dtypes, CSV vs Parquet, partition_on."""
import shutil
import sys
import time
from pathlib import Path
import dask.dataframe as dd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data          # noqa: E402

BIG = ensure_big_data()
DTYPES = {"units": "float64", "unit_price": "int64", "customer_id": "int64"}


def folder_mb(path: Path) -> float:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 1e6


print("=== 1. Many files, one table ===")
ddf = dd.read_csv(BIG / "sales_2025-*.csv", parse_dates=["timestamp"], dtype=DTYPES,
                  include_path_column=True)
print("partitions:", ddf.npartitions)
per_file = ddf.groupby("path").size().compute()
per_file.index = [Path(p).name for p in per_file.index]
print(per_file.sort_index().head(3), "...")

print("\n=== 2. blocksize controls partitions ===")
for bs in ["64MB", "5MB"]:
    print(f"blocksize={bs:>5} -> {dd.read_csv(BIG / 'sales_2025-*.csv', blocksize=bs).npartitions} partitions")

print("\n=== 3. CSV -> Parquet (do this once) ===")
pq = OUT / "sales_parquet"
shutil.rmtree(pq, ignore_errors=True)
t = time.perf_counter()
ddf.drop(columns="path").to_parquet(pq, write_index=False)
print(f"wrote {len(list(pq.glob('*.parquet')))} Parquet files in {time.perf_counter() - t:.1f} s")
print(f"size: CSV {folder_mb(BIG) - (BIG / 'customers_big.csv').stat().st_size / 1e6:.0f} MB "
      f"-> Parquet {folder_mb(pq):.0f} MB")

print("\n=== 4. Same query, CSV vs Parquet ===")
def query(frame):
    return frame.groupby("region").units.sum().compute()

t = time.perf_counter(); a = query(dd.read_csv(BIG / "sales_2025-*.csv", dtype=DTYPES)); csv_t = time.perf_counter() - t
t = time.perf_counter(); b = query(dd.read_parquet(pq)); pq_t = time.perf_counter() - t
print(f"CSV: {csv_t:.2f} s | Parquet: {pq_t:.2f} s | {csv_t / pq_t:.0f}x faster | same: {a.equals(b)}")
print("Parquet dtypes are stored, not guessed:", dict(dd.read_parquet(pq).dtypes.astype(str)))

print("\n=== 5. partition_on: folders per value ===")
by_region = OUT / "sales_by_region"
shutil.rmtree(by_region, ignore_errors=True)
dd.read_parquet(pq).to_parquet(by_region, partition_on=["region"], write_index=False)
print("folders:", sorted(p.name for p in by_region.iterdir() if p.is_dir()))
north = dd.read_parquet(by_region, filters=[("region", "==", "North")])
print("rows read with filters=[region == North]:", f"{len(north):,}")

print("\n=== 6. Writing CSV ===")
summary = dd.read_parquet(pq).groupby("product")[["units"]].sum()
summary.to_csv(OUT / "product_units.csv", single_file=True)
print((OUT / "product_units.csv").read_text())
dd.read_parquet(pq).head(1000, compute=False).to_csv(OUT / "sample-*.csv", index=False)
print("sample files:", sorted(f.name for f in OUT.glob("sample-*.csv")))
