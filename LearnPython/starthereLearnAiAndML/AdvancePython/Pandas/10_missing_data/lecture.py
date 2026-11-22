"""Lecture 10: Missing data: find, drop, fill, interpolate."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
students = pd.read_csv(DATA / "students.csv")
marks = ["maths", "science", "english", "cs"]
print(students, "\n")

print("=== Finding missing values ===")
print(students.isna().sum())
print("fraction missing per column:\n", students.isna().mean().round(3))
print("overall fraction missing:", round(students.isna().to_numpy().mean(), 3))
print("rows with any gap:\n", students[students.isna().any(axis=1)][["name"] + marks])
print("NaN == NaN ?", np.nan == np.nan, "-> always use isna()")

print("\n=== Ints become floats when a value is missing ===")
print(students[["maths", "cs"]].dtypes)

print("\n=== Stats skip NaN ===")
print("maths mean :", round(students["maths"].mean(), 2))
print("maths count:", students["maths"].count(), "of", len(students))

print("\n=== 1. Drop ===")
print("dropna()               :", len(students.dropna()), "rows left")
print("dropna(subset=[maths]) :", len(students.dropna(subset=["maths"])), "rows left")
print("dropna(thresh=7)       :", len(students.dropna(thresh=7)), "rows left")
print("dropna(axis=1) columns :", students.dropna(axis=1).columns.tolist())

print("\n=== 2. Fill with a value ===")
filled = students.copy()
filled[marks] = filled[marks].fillna(filled[marks].median())
print(filled.loc[students.isna().any(axis=1), ["name"] + marks])
print(students.fillna({"maths": 0, "english": 50}).loc[[7, 9, 10], ["name"] + marks])

print("\n=== 3. Fill from the group ===")
class_mean = students.groupby("class")["maths"].transform("mean")
print(pd.DataFrame({"name": students["name"], "class": students["class"],
                    "maths": students["maths"], "class_mean": class_mean.round(1),
                    "filled": students["maths"].fillna(class_mean).round(1)}).iloc[8:11])

print("\n=== 4. Time series: ffill / bfill / interpolate ===")
temps = pd.Series([31.0, np.nan, np.nan, 34.0, np.nan, 30.0],
                  index=pd.date_range("2025-06-01", periods=6))
print(pd.DataFrame({"raw": temps, "ffill": temps.ffill(),
                    "bfill": temps.bfill(), "interpolate": temps.interpolate()}))

print("\n=== 5. Flag before filling ===")
flagged = students.assign(maths_missing=students["maths"].isna(),
                          maths=students["maths"].fillna(students["maths"].median()))
print(flagged.loc[flagged["maths_missing"], ["name", "maths", "maths_missing"]])
