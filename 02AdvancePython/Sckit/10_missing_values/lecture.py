"""Lecture 10: Missing values: inspect, SimpleImputer strategies, add_indicator, KNNImputer, IterativeImputer, NaN-aware models."""
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame({
    "age": [25, np.nan, 40, 35, 52, np.nan],
    "salary": [50, 62, np.nan, 58, 900, 61],          # thousands; 900 is an outlier
    "city": ["Pune", np.nan, "Delhi", "Pune", "Delhi", np.nan],
})

print("=== 1. Inspect ===")
print(df.to_string())
print("  missing count:", df.isna().sum().to_dict())
print("  missing share:", df.isna().mean().round(2).to_dict())

print("\n=== 2. Most models refuse NaN ===")
try:
    LogisticRegression().fit(df[["age", "salary"]], [0, 1, 0, 1, 1, 0])
except ValueError as e:
    print("  LogisticRegression ->", str(e).splitlines()[0])

print("\n=== 3. SimpleImputer strategies (salary has an outlier) ===")
num = df[["age", "salary"]]
for strategy in ["mean", "median", "most_frequent", "constant"]:
    imp = SimpleImputer(strategy=strategy, fill_value=0) if strategy == "constant" else SimpleImputer(strategy=strategy)
    imp.fit(num)
    print(f"  {strategy:<14} fill values (age, salary): {np.round(np.asarray(imp.statistics_, dtype=float), 1)}")
print("  the mean salary is dragged up by the 900 outlier; the median is not")

print("\n=== 4. add_indicator: let the model know a value was missing ===")
imp = SimpleImputer(strategy="median", add_indicator=True)
out = imp.fit_transform(num)
print("  feature names:", list(imp.get_feature_names_out()))
print(np.round(out, 1))

print("\n=== 5. Categorical columns ===")
cat_pipe = make_pipeline(SimpleImputer(strategy="constant", fill_value="missing"),
                         OneHotEncoder(sparse_output=False))
cat_out = cat_pipe.fit_transform(df[["city"]])
print("  columns:", list(cat_pipe.get_feature_names_out()))
print("  ", cat_out.astype(int).tolist())
mf = SimpleImputer(strategy="most_frequent").fit(df[["city"]])
print("  most_frequent would fill with:", mf.statistics_[0])

print("\n=== 6. KNNImputer and IterativeImputer ===")
X_full = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0], [4.0, 8.0, 12.0], [5.0, 10.0, 15.0]])
X_gap = X_full.copy()
X_gap[2, 1] = np.nan                     # true value is 6.0
print("  true missing value: 6.0")
print("  SimpleImputer(mean)  ->", SimpleImputer().fit_transform(X_gap)[2, 1].round(2))
print("  KNNImputer(k=2)      ->", KNNImputer(n_neighbors=2).fit_transform(X_gap)[2, 1].round(2))
print("  IterativeImputer     ->", IterativeImputer(random_state=0).fit_transform(X_gap)[2, 1].round(2),
      "(learns that column 2 = 2 x column 1)")

print("\n=== 7. Impute inside a pipeline vs NaN-aware model ===")
X, y = load_breast_cancer(return_X_y=True)
rng = np.random.default_rng(0)
X_missing = X.copy()
X_missing[rng.random(X.shape) < 0.2] = np.nan              # knock out 20% of all values
print(f"  {np.isnan(X_missing).mean():.0%} of values removed")
models = {
    "mean impute + logistic": make_pipeline(SimpleImputer(), StandardScaler(), LogisticRegression()),
    "median + indicator + logistic": make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                                                   StandardScaler(), LogisticRegression(max_iter=1000)),
    "KNN impute + logistic": make_pipeline(StandardScaler(), KNNImputer(), LogisticRegression()),
    "HistGradientBoosting (raw NaN)": HistGradientBoostingClassifier(random_state=0),
}
for name, model in models.items():
    print(f"  {name:<32} {cross_val_score(model, X_missing, y, cv=5).mean():.3f}")
