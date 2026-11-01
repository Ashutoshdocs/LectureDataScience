"""
Step 2 - Explore the data (EDA) before modelling.

Run:  python src/explore.py
"""
import pandas as pd

from config import CATEGORICAL_FEATURES, DATA_PATH, NUMERIC_FEATURES, TARGET

df = pd.read_csv(DATA_PATH)

print("=== Shape ===")
print(df.shape, "\n")

print("=== Column types ===")
print(df.dtypes, "\n")

print("=== Missing values per column ===")
print(df.isna().sum(), "\n")

print("=== Target balance ===")
print(df[TARGET].value_counts(normalize=True).rename("share").round(3), "\n")

print("=== Numeric summary ===")
print(df[NUMERIC_FEATURES].describe().round(1).T, "\n")

print("=== Mean of numeric features by outcome ===")
print(df.groupby(TARGET)[NUMERIC_FEATURES].mean().round(1).T, "\n")

for col in CATEGORICAL_FEATURES:
    print(f"=== Approval rate by {col} ===")
    print(df.groupby(col)[TARGET].mean().round(3).sort_values(ascending=False), "\n")
