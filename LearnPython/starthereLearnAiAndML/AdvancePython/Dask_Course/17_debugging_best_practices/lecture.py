"""Lecture 17: Debugging: reproduce common Dask errors on purpose, then fix them."""
import shutil
import traceback
from pathlib import Path
import dask
import dask.dataframe as dd
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def short(e: Exception, n=120):
    return f"{type(e).__name__}: {str(e).strip().splitlines()[0][:n]}"


print("=== 1. dtype mismatch across files ===")
files = OUT / "mismatch"
shutil.rmtree(files, ignore_errors=True)
files.mkdir(parents=True)
pd.DataFrame({"id": range(1, 2001), "units": [1, 2, 3, 4] * 500}).to_csv(files / "a.csv", index=False)
b = pd.DataFrame({"id": range(2001, 4001), "units": [1, 2, 3, 4] * 500}).astype({"units": "float64"})
b.loc[1500, "units"] = None                                     # a missing value deep in file b
b.to_csv(files / "b.csv", index=False)

ddf = dd.read_csv(files / "*.csv")
print("dtype guessed from a sample of the first file:", ddf.dtypes["units"])
try:
    ddf.units.sum().compute()
except ValueError as e:
    print("compute failed ->", short(e, 70))
print("fix 1, declare dtypes      :", dd.read_csv(files / "*.csv", dtype={"units": "float64"}).units.sum().compute())
print("fix 2, larger sample       :", dd.read_csv(files / "*.csv", sample_rows=5000, assume_missing=True).units.sum().compute())

print("\n=== 2. Errors far from the cause, and the synchronous scheduler ===")
data = dd.from_pandas(pd.DataFrame({"x": range(100), "y": ["a"] * 99 + ["oops"]}), npartitions=4)


def parse(df):
    return df.assign(y_num=df.y.map(lambda v: {"a": 1}[v]))    # KeyError on "oops"


lazy = data.map_partitions(parse, meta=data._meta.assign(y_num=0))
print("building the graph: no error yet")
try:
    lazy.compute()                                              # threads
except KeyError as e:
    print("threaded compute failed ->", short(e))
with dask.config.set(scheduler="synchronous"):
    try:
        lazy.compute()
    except KeyError:
        frames = [f for f in traceback.extract_tb(__import__("sys").exc_info()[2]) if f.filename == __file__]
        print("synchronous compute: the traceback points at YOUR code ->",
              f"line {frames[-1].lineno}: {frames[-1].line}")

print("\n=== 3. Find the bad partition ===")
for i in range(data.npartitions):
    part = data.partitions[i].compute()
    if (part.y != "a").any():
        print(f"partition {i} contains:", part.loc[part.y != "a", "y"].tolist())

print("\n=== 4. meta guessed wrong ===")
def classify(df):
    df = df.copy()
    df["label"] = "small" if len(df) < 5 else 1                 # type depends on partition size!
    return df

guess = data.map_partitions(classify)
print("Dask guessed 'label' dtype from fake data:", guess.dtypes["label"])
print("actual dtype on real partitions:", guess.partitions[0].compute().dtypes["label"])
fixed = data.map_partitions(classify, meta=data._meta.assign(label=pd.Series(dtype="int64")))
print("with explicit meta:", fixed.dtypes["label"], "(and fix the function so it returns one type!)")

print("\n=== 5. Not implemented in Dask ===")
for label, fn in [("ddf.iloc[3]", lambda: data.iloc[3]),
                  ("data.x.values[0]", lambda: data.x.values[0].compute())]:
    try:
        fn()
        print(label, "-> worked")
    except Exception as e:
        print(label, "->", short(e, 80))

print("\n=== 6. Partition sizing sanity check ===")
big = dd.from_pandas(pd.DataFrame({"x": range(1_000_000)}), npartitions=1000)
mb = big.memory_usage_per_partition(deep=True).compute() / 1e6
print(f"{big.npartitions} partitions of ~{mb.mean():.3f} MB -> far too small (overhead dominates)")
fixed = big.repartition(partition_size="100MB")
print(f"after repartition(partition_size='100MB'): {fixed.npartitions} partition(s)")
