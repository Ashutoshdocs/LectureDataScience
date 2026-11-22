"""Lecture 20: Recap. A self-test across the course. Predict each answer, then run."""
import sys
from pathlib import Path
import dask
import dask.array as da
import dask.bag as db
import dask.dataframe as dd
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_parquet       # noqa: E402

small = dd.from_pandas(pd.read_csv(DATA / "sales.csv"), npartitions=4)
big = dd.read_parquet(ensure_big_parquet())
big = big.assign(revenue=big.units * big.unit_price)


@dask.delayed
def double(x):
    return 2 * x


questions = [
    ("L01 | Type of small.units.sum() BEFORE compute?",
     lambda: type(small.units.sum()).__name__),
    ("L01 | ...and its value?",
     lambda: int(small.units.sum().compute())),
    ("L03 | dask.compute(*[double(i) for i in range(4)])?",
     lambda: dask.compute(*[double(i) for i in range(4)])),
    ("L04 | Number of chunks in da.ones((1000, 1000), chunks=250)?",
     lambda: da.ones((1000, 1000), chunks=250).npartitions),
    ("L05 | Rows per partition in `small`?",
     lambda: small.map_partitions(len).compute().tolist()),
    ("L05 | Partitions in the big Parquet dataset?",
     lambda: big.npartitions),
    ("L07 | Orders in the big data with units == 5?",
     lambda: f"{len(big[big.units == 5]):,}"),
    ("L08 | Region with the most revenue (big data)?",
     lambda: big.groupby("region").revenue.sum().compute().idxmax()),
    ("L09 | known_divisions after set_index('timestamp', sorted=True)?",
     lambda: big.set_index("timestamp", sorted=True).known_divisions),
    ("L11 | Does map_partitions(lambda d: d.order_id.rank()) give a GLOBAL rank? Max rank found (2.4M rows):",
     lambda: int(big.map_partitions(lambda d: d.order_id.rank(), meta=("r", "f8")).max().compute())),
    ("L12 | Busiest hour of the day (big data)?",
     lambda: big.groupby(big.timestamp.dt.hour).order_id.count().compute().idxmax()),
    ("L14 | Bag: frequencies of ['a', 'b', 'a']?",
     lambda: sorted(db.from_sequence(["a", "b", "a"], npartitions=1).frequencies().compute(scheduler="sync"))),
    ("L15 | Total revenue and mean units in ONE pass?",
     lambda: tuple(round(float(v), 3) for v in dask.compute(big.revenue.sum(), big.units.mean()))),
]

for i, (q, answer) in enumerate(questions, start=1):
    print(f"\nQ{i:02}. {q}")
    print(answer())

print("\nIf every answer matched your prediction, you're ready to scale real work with Dask. Well done!")
