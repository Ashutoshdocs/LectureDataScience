"""Lecture 02: Series, a labelled 1D array."""
import pandas as pd

print("=== Creating ===")
print(pd.Series([4200, 6100, 5300]))                       # automatic index 0,1,2
steps = pd.Series([4200, 6100, 5300, 8800, 7600],
                  index=["Mon", "Tue", "Wed", "Thu", "Fri"], name="steps")
print(steps)
print(pd.Series({"Delhi": 39, "Mumbai": 32, "Chennai": 36}))   # from a dict

print("\n=== Parts of a Series ===")
print("values:", steps.to_numpy())
print("index :", steps.index.tolist())
print("name  :", steps.name, "| dtype:", steps.dtype, "| size:", steps.size)

print("\n=== Accessing ===")
print("by label    steps['Tue']   :", steps["Tue"])
print("by position steps.iloc[1]  :", steps.iloc[1])
print("several labels:\n", steps[["Mon", "Wed"]])
print("label slice (end INCLUDED):\n", steps["Tue":"Thu"])
print("mask > 6000:\n", steps[steps > 6000])

print("\n=== Vectorized maths and stats ===")
print((steps / 1000).round(1))
print("mean:", steps.mean(), "| max:", steps.max(), "on", steps.idxmax())
print("days above mean:", steps[steps > steps.mean()].index.tolist())
print(steps.describe())

print("\n=== Alignment by label ===")
a = pd.Series({"Mon": 1, "Tue": 2})
b = pd.Series({"Tue": 10, "Wed": 20})
print(a + b)
print(a.add(b, fill_value=0))

print("\n=== value_counts / unique ===")
drinks = pd.Series(["tea", "coffee", "tea", "juice", "tea", "coffee"])
print(drinks.value_counts())
print("unique:", drinks.unique(), "| how many:", drinks.nunique())

print("\n=== Converting out ===")
print(steps.to_list())
print(steps.to_dict())
