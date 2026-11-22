"""Lecture 06: Selecting with [], loc (labels) and iloc (positions)."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
df = pd.read_csv(DATA / "students.csv", index_col="name").drop(columns="gender")
print(df, "\n")

print("=== [] for columns ===")
print(df["maths"].head(3))
print(df[["maths", "cs"]].head(3))

print("\n=== loc: by label ===")
print(df.loc["Ravi"])
print("Ravi maths:", df.loc["Ravi", "maths"])
print(df.loc[["Asha", "Meena"]])
print(df.loc["Asha":"Meena"])                     # end label INCLUDED
print(df.loc[:, "maths":"english"].head(3))
print(df.loc[df["maths"] > 80, ["class", "maths"]])

print("\n=== iloc: by position ===")
print(df.iloc[0])
print(df.iloc[-1].name, "<- name of the last row")
print(df.iloc[:3])                                # rows 0,1,2 (3 excluded)
print(df.iloc[:, 0].head(3))
print("row 2, col 1:", df.iloc[2, 1])
print(df.iloc[[0, 2], [1, 3]])
print(df.iloc[-3:, :2])

print("\n=== at / iat ===")
print("at['Zara','science']:", df.at["Zara", "science"], "| iat[4, 2]:", df.iat[4, 2])

print("\n=== Changing values with loc ===")
df.loc["Meena", "maths"] = 50
df.loc[df["cs"] < 50, "cs"] = 50
print(df.loc[["Meena"], ["maths", "cs"]])

print("\n=== The chained-assignment trap ===")
before = df["science"].copy()
import warnings
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df[df["science"] < 60]["science"] = 60        # does NOT change df
if caught:
    print("pandas warned:", type(caught[0].message).__name__)
print("chained assignment changed df?", not df["science"].equals(before))
df.loc[df["science"] < 60, "science"] = 60        # correct way
print("loc assignment changed df?    ", not df["science"].equals(before))
