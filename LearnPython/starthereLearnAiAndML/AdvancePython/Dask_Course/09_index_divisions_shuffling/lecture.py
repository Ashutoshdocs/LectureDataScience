"""Lecture 09: Index, divisions & shuffling: why set_index is expensive and when it pays off."""
import sys
import time
from pathlib import Path
import dask.dataframe as dd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_parquet       # noqa: E402

PQ = ensure_big_parquet()
ddf = dd.read_parquet(PQ)

print("=== 1. Fresh from Parquet: default index, no useful divisions ===")
print("index name:", ddf.index.name, "| known_divisions:", ddf.known_divisions)

print("\n=== 2. set_index with sorted=True (data is already in time order) ===")
t = time.perf_counter()
by_time = ddf.set_index("timestamp", sorted=True)
by_time = by_time.persist()                     # keep it in memory for the comparisons below
sorted_t = time.perf_counter() - t
print(f"took {sorted_t:.2f} s | known_divisions: {by_time.known_divisions}")
print("first 3 divisions:", [str(d) for d in by_time.divisions[:3]])

print("\n=== 3. set_index on unsorted data needs a shuffle ===")
t = time.perf_counter()
by_customer = ddf.set_index("customer_id").persist()
shuffle_t = time.perf_counter() - t
print(f"set_index('customer_id'): {shuffle_t:.2f} s (vs {sorted_t:.2f} s for the already-sorted column)")
print("divisions:", [int(d) for d in by_customer.divisions[:4]], "...")

print("\n=== 4. Known divisions make lookups cheap ===")
plain = ddf.persist()
t = time.perf_counter()
day_scan = plain[(plain.timestamp >= "2025-06-15") & (plain.timestamp < "2025-06-16")].compute()
scan_t = time.perf_counter() - t
t = time.perf_counter()
day_loc = by_time.loc["2025-06-15"].compute()
loc_t = time.perf_counter() - t
print(f"filter on a column: {scan_t * 1000:6.0f} ms | .loc on a sorted index: {loc_t * 1000:6.0f} ms | rows: "
      f"{len(day_scan):,} = {len(day_loc):,}")
print("partitions touched by .loc:", by_time.loc["2025-06-15"].npartitions, "of", by_time.npartitions)

t = time.perf_counter()
cust = by_customer.loc[777].compute()
print(f"all orders of customer 777: {len(cust)} rows in {(time.perf_counter() - t) * 1000:.0f} ms "
      f"(1 partition of {by_customer.npartitions})")

print("\n=== 5. shuffle: put equal keys together without sorting ===")
shuffled = ddf.shuffle(on="customer_id").persist()
parts_per_customer = (shuffled.map_partitions(lambda df: df[["customer_id"]].drop_duplicates())
                              .customer_id.value_counts().max().compute())
print("max partitions any customer appears in after shuffle:", parts_per_customer)
before = ddf.map_partitions(lambda df: df[["customer_id"]].drop_duplicates()).customer_id.value_counts().max().compute()
print("...and before the shuffle:", before)

print("\n=== 6. Save the indexed version so you never shuffle again ===")
out = Path(__file__).resolve().parent / "output" / "by_time"
by_time.to_parquet(out, overwrite=True)
back = dd.read_parquet(out, index="timestamp", calculate_divisions=True)
print("re-read with calculate_divisions=True -> known_divisions:", back.known_divisions)
