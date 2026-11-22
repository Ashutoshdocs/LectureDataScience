"""Lecture 02: Built-in and generated datasets; Bunch objects; shapes; DataFrames; exploring a dataset."""
import numpy as np
import pandas as pd
from sklearn.datasets import (load_breast_cancer, load_diabetes, load_digits, load_iris, load_wine,
                              make_blobs, make_classification, make_moons, make_regression)

print("=== 1. Built-in datasets at a glance ===")
for loader in (load_iris, load_wine, load_breast_cancer, load_digits, load_diabetes):
    X, y = loader(return_X_y=True)
    kind = "regression" if loader is load_diabetes else f"{len(np.unique(y))} classes"
    print(f"  {loader.__name__:<20} X {str(X.shape):<11} y {str(y.shape):<7} {kind}")

print("\n=== 2. A Bunch: data + description ===")
iris = load_iris()
print("  keys          :", list(iris.keys()))
print("  feature_names :", iris.feature_names)
print("  target_names  :", [str(n) for n in iris.target_names])
print("  first row     :", iris.data[0], "-> class", iris.target[0], f"({iris.target_names[iris.target[0]]})")
print("  DESCR starts  :", iris.DESCR.splitlines()[2].strip())

print("\n=== 3. as_frame=True gives pandas objects ===")
X_df, y_s = load_wine(return_X_y=True, as_frame=True)
print("  types:", type(X_df).__name__, type(y_s).__name__)
print(X_df.iloc[:3, :4].to_string())
print("  samples per class:", y_s.value_counts().sort_index().to_dict())

print("\n=== 4. Explore before modelling ===")
cancer = load_breast_cancer(as_frame=True)
df = cancer.frame
print("  shape:", df.shape, "| missing values:", int(df.isna().sum().sum()))
print("  class balance:", {str(cancer.target_names[k]): int(v) for k, v in df["target"].value_counts().sort_index().items()})
print(df[["mean radius", "mean texture", "mean area"]].describe().loc[["mean", "std", "min", "max"]].round(1).to_string())

print("\n=== 5. Digits: each row is an 8x8 image ===")
digits = load_digits()
print("  label of first image:", digits.target[0])
for row in digits.images[0]:
    print("   ", "".join("#" if v > 8 else "+" if v > 3 else "." for v in row))

print("\n=== 6. Generated data for experiments ===")
Xc, yc = make_classification(n_samples=1000, n_features=5, n_informative=3, weights=[0.9, 0.1], random_state=0)
print("  make_classification (imbalanced):", Xc.shape, "counts", np.bincount(yc))
Xr, yr = make_regression(n_samples=200, n_features=3, noise=10, random_state=0)
print("  make_regression:", Xr.shape, "y range", yr.min().round(1), "to", yr.max().round(1))
Xb, yb = make_blobs(n_samples=300, centers=3, random_state=0)
print("  make_blobs:", Xb.shape, "cluster sizes", np.bincount(yb))
Xm, ym = make_moons(n_samples=200, noise=0.2, random_state=0)
print("  make_moons first 3 rows:\n", np.round(Xm[:3], 2))

print("\n=== 7. Your own table -> X and y ===")
customers = pd.DataFrame({"age": [23, 45, 31, 52], "plan": ["basic", "pro", "basic", "pro"],
                          "monthly_bill": [299, 999, 349, 1099], "churned": [1, 0, 1, 0]})
X = customers.drop(columns="churned")
y = customers["churned"]
print("  X:", X.shape, list(X.columns), "| y:", y.shape, y.tolist())
try:
    from sklearn.linear_model import LinearRegression
    LinearRegression().fit(X[["age", "monthly_bill"]].iloc[:3], y)
except ValueError as e:
    print("  mismatched rows ->", str(e).splitlines()[0])
