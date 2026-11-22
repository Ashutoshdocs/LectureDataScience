"""Lecture 18: Vectorization vs apply vs iterrows: a speed race."""
import time
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
n = 1_000_000
df = pd.DataFrame({
    "units": rng.integers(1, 6, n),
    "unit_price": rng.choice([900, 1500, 3500, 25000, 55000], n),
    "product": rng.choice(["phone", "lamp", "desk", "chair"], n),
})
print(f"Table: {n:,} rows\n")


def timed(label, func, rows=n):
    t = time.perf_counter()
    result = func()
    ms = (time.perf_counter() - t) * 1000
    per_million = ms * n / rows
    print(f"{label:<34} {ms:9.1f} ms   (~{per_million:9.0f} ms per 1M rows)")
    return result, per_million


print("=== Task 1: revenue = units * unit_price ===")
small = df.head(20_000)                       # slow methods get a smaller slice
_, fast = timed("vectorized  df.a * df.b", lambda: df["units"] * df["unit_price"])
_, ap = timed("df.apply(axis=1)   [20k rows]",
              lambda: small.apply(lambda r: r["units"] * r["unit_price"], axis=1), 20_000)


def loop():
    out = []
    for _, row in small.iterrows():
        out.append(row["units"] * row["unit_price"])
    return out


_, it = timed("iterrows loop      [20k rows]", loop, 20_000)
print(f"-> vectorized is ~{ap / fast:,.0f}x faster than apply and ~{it / fast:,.0f}x faster than iterrows")

print("\n=== Task 2: label 'bulk' / 'single' ===")
_, a = timed("Series.apply(lambda)", lambda: df["units"].apply(lambda u: "bulk" if u >= 4 else "single"))
_, b = timed("np.where", lambda: np.where(df["units"] >= 4, "bulk", "single"))
print(f"-> np.where ~{a / b:,.0f}x faster")

print("\n=== Task 3: three tiers ===")
rev = df["units"] * df["unit_price"]


def tier(v):
    if v >= 100_000:
        return "gold"
    elif v >= 20_000:
        return "silver"
    return "bronze"


_, a = timed("Series.apply(tier)", lambda: rev.apply(tier))
_, b = timed("np.select", lambda: np.select([rev >= 100_000, rev >= 20_000], ["gold", "silver"], "bronze"))
print(f"-> np.select ~{a / b:,.0f}x faster")
print("same answer?", (rev.apply(tier).to_numpy() == np.select([rev >= 100_000, rev >= 20_000],
                                                               ["gold", "silver"], "bronze")).all())

print("\n=== Task 4: text and lookups ===")
lookup = {"phone": "Electronics", "lamp": "Furniture", "desk": "Furniture", "chair": "Furniture"}
_, a = timed("apply(lambda: lookup[p])", lambda: df["product"].apply(lambda p: lookup[p]))
_, b = timed("map(dict)", lambda: df["product"].map(lookup))
_, c = timed("apply(str.upper)", lambda: df["product"].apply(str.upper))
_, d = timed(".str.upper()", lambda: df["product"].str.upper())
print("-> text: .str is about the same speed as apply. Use it for missing-value safety and clarity.")

print("\n=== Building a DataFrame: append in a loop vs list of dicts ===")


def grow():
    out = pd.DataFrame(columns=["i", "sq"])
    for i in range(300):
        out = pd.concat([out, pd.DataFrame([{"i": i, "sq": i * i}])], ignore_index=True)
    return out


def collect():
    rows = [{"i": i, "sq": i * i} for i in range(300)]
    return pd.DataFrame(rows)


t = time.perf_counter(); grow(); g = time.perf_counter() - t
t = time.perf_counter(); collect(); c = time.perf_counter() - t
print(f"concat in loop: {g*1000:7.1f} ms | list then DataFrame: {c*1000:5.2f} ms  (~{g / c:,.0f}x)")
