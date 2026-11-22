"""Lecture 11: map_partitions & meta: any pandas code, per partition, and its limits."""
import sys
import warnings
from pathlib import Path
import dask.dataframe as dd
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_parquet       # noqa: E402

pd.set_option("display.width", 140)
ddf = dd.read_parquet(ensure_big_parquet())


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Plain pandas: runs on one partition at a time."""
    df = df.copy()
    df["revenue"] = df["units"] * df["unit_price"]
    df["hour"] = df["timestamp"].dt.hour.astype("int32")
    df["is_night"] = df["hour"].between(0, 5)
    df["price_band"] = pd.cut(df["unit_price"], bins=[0, 2_000, 20_000, np.inf],
                              labels=["low", "mid", "high"]).astype("string")
    return df


print("=== 1. map_partitions with explicit meta ===")
meta = ddf._meta.assign(revenue=pd.Series(dtype="float64"), hour=pd.Series(dtype="int32"),
                        is_night=pd.Series(dtype="bool"), price_band=pd.Series(dtype="string"))
feat = ddf.map_partitions(add_features, meta=meta)
print(feat.dtypes)
print(feat[["timestamp", "unit_price", "revenue", "hour", "is_night", "price_band"]].head(3))
print(feat.groupby("price_band").revenue.sum().compute().sort_index())
print("night-time share of orders:", round(feat.is_night.mean().compute(), 4))

print("\n=== 2. Without meta, Dask runs your function on FAKE data to guess ===")
calls = []
def spy(df):
    calls.append(len(df))
    return add_features(df)
guessed = ddf.map_partitions(spy)          # building the graph triggers the guess
print("rows Dask passed to your function while guessing:", calls)
print("guessed columns match:", list(guessed.columns) == list(meta.columns))
print("If your function fails or behaves differently on tiny fake data, the guess breaks.")
print("Passing meta= skips the guess entirely.")

print("\n=== 3. Series and scalar outputs ===")
print("rows per partition:", ddf.map_partitions(len, meta=("rows", "int64")).compute().tolist())
units_per_part = ddf.map_partitions(lambda df: pd.Series([df.units.sum()]), meta=("units", "f8"))
print("units per partition:", units_per_part.compute().round(0).astype(int).tolist()[:4], "...")

print("\n=== 4. The global-mean trap ===")
tiny = dd.from_pandas(pd.DataFrame({"x": [1, 2, 3, 100, 200, 300]}), npartitions=2)
wrong = tiny.map_partitions(lambda df: df.assign(dev=df.x - df.x.mean()))
m = tiny.x.mean().compute()
right = tiny.map_partitions(lambda df, mean: df.assign(dev=df.x - mean), m)
print("partitions:", [part.x.compute().tolist() for part in tiny.partitions])
print(f"global mean = {m}")
print("deviation using each partition's own mean (WRONG):", wrong.dev.compute().tolist())
print("deviation using the global mean passed in (RIGHT):", right.dev.compute().tolist())

print("\n=== 5. Per-partition rank is NOT a global rank ===")
ranked = ddf.map_partitions(lambda df: df.assign(r=df.order_id.rank(method="first")))
print("highest rank found:", f"{int(ranked.r.max().compute()):,}", "| rows in total:", f"{len(ddf):,}")
print("Each partition ranked only its own 200,000 rows. A global rank needs a sort/shuffle.")

print("\n=== 6. to_delayed / from_delayed ===")
parts = ddf.to_delayed()
print("delayed partitions:", len(parts), type(parts[0]).__name__)
back = dd.from_delayed(parts, meta=ddf._meta)
print("rebuilt rows:", f"{len(back):,}")
