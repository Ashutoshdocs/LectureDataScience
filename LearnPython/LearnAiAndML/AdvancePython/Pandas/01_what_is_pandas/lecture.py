"""Lecture 01: What is pandas? Your first DataFrame, and the same questions as Lecture 00."""
import pandas as pd

print("pandas version:", pd.__version__)

table = {
    "name":  ["Asha", "Ravi", "Meena", "John"],
    "class": ["10A", "10A", "10B", "10B"],
    "maths": [78, 92, 45, 83],
}
df = pd.DataFrame(table)
print(df)

print("\n--- A DataFrame is made of Series ---")
print(type(df))
print(type(df["maths"]))
print(type(df["maths"].to_numpy()), "<- the NumPy array underneath")

print("\n--- Each column has its own type ---")
print(df.dtypes)

print("\n--- Lecture 00's questions, one line each ---")
print("average maths     :", df["maths"].mean())
print("scored above 60   :", df.loc[df["maths"] > 60, "name"].tolist())
print("sorted by maths   :", df.sort_values("maths", ascending=False)["name"].tolist())
print("top student       :", df.loc[df["maths"].idxmax(), "name"])
print("average per class :", df.groupby("class")["maths"].mean().to_dict())

print("\n--- Reading a CSV with a missing value ---")
import io
csv_text = "name,maths\nAsha,78\nRavi,92\nMeena,\n"
marks = pd.read_csv(io.StringIO(csv_text))
print(marks)
print("mean ignoring missing:", marks["maths"].mean())   # NaN is skipped automatically
