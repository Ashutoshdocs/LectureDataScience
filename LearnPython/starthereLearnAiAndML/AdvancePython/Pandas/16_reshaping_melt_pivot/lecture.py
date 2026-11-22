"""Lecture 16: Reshaping: melt, pivot, stack/unstack, explode, get_dummies."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 140)

wide = pd.read_csv(DATA / "students.csv")
subjects = ["maths", "science", "english", "cs"]
print("=== Wide ===")
print(wide.head(3))

print("\n=== melt: wide -> long ===")
long = wide.melt(id_vars=["name", "class", "gender"], value_vars=subjects,
                 var_name="subject", value_name="mark")
print(long.head(8))
print("shape wide", wide.shape, "-> long", long.shape)

print("\n=== Long format makes questions easy ===")
print(long.groupby("subject")["mark"].mean().round(1).sort_values(ascending=False))
print(long.groupby(["class", "subject"])["mark"].mean().unstack().round(1))
best = long.loc[long.dropna().groupby("name")["mark"].idxmax(), ["name", "subject", "mark"]]
print("best subject per student:\n", best.reset_index(drop=True))
print("marks under 60:\n", long[long["mark"] < 60].sort_values("mark"))

print("\n=== pivot: long -> wide ===")
back = long.pivot(index="name", columns="subject", values="mark")
print(back.head(3))
original = wide.set_index("name")[subjects].astype(float).sort_index()   # cs was int; melt made it float
same = back[subjects].rename_axis(columns=None).sort_index().equals(original)
print("round trip matches original?", same)

print("\n=== pivot fails on duplicates; pivot_table aggregates ===")
tests = pd.DataFrame({"name": ["Asha", "Asha", "Ravi"], "subject": ["maths"] * 3,
                      "mark": [70, 80, 90]})
try:
    tests.pivot(index="name", columns="subject", values="mark")
except ValueError as e:
    print("pivot ->", e)
print(tests.pivot_table(index="name", columns="subject", values="mark", aggfunc="mean"))

print("\n=== stack / unstack ===")
small = wide.set_index("name")[["maths", "science"]].head(2)
stacked = small.stack()
print(stacked)
print(stacked.unstack())

print("\n=== explode and get_dummies ===")
orders = pd.DataFrame({"order": [1, 2], "items": [["pen", "book"], ["lamp"]]})
print(orders.explode("items"))
print(pd.get_dummies(wide["class"], prefix="class", dtype=int).head(4))

print("\n=== Transpose ===")
print(wide.set_index("name")[subjects].head(3).T)
