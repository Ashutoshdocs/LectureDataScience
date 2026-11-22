"""Lecture 20: Pipeline, make_pipeline, step access, ColumnTransformer on messy mixed data, column selectors,
set_output, FeatureUnion, robustness to unseen/missing values."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

print("=== 1. A simple pipeline ===")
X, y = load_wine(return_X_y=True)
pipe = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier())])
print("  ", pipe)
print(f"  KNN alone {cross_val_score(KNeighborsClassifier(), X, y, cv=5).mean():.3f} | pipeline {cross_val_score(pipe, X, y, cv=5).mean():.3f}")
auto = make_pipeline(StandardScaler(), KNeighborsClassifier())
print("  make_pipeline step names:", list(auto.named_steps))

print("\n=== 2. Accessing steps ===")
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
pipe.fit(Xtr, ytr)
print("  pipe['scale'].mean_[:3]:", pipe["scale"].mean_[:3].round(2))
print("  pipe[-1]:", pipe[-1], "| pipe[:-1]:", pipe[:-1])
print("  what the model sees (first row, scaled):", pipe[:-1].transform(Xte[:1]).round(2)[0][:5], "...")
print("  test accuracy:", round(pipe.score(Xte, yte), 3))

print("\n=== 3. Messy mixed data ===")
rng = np.random.default_rng(0)
n = 400
df = pd.DataFrame({
    "age": rng.integers(18, 70, n).astype(float),
    "income": rng.lognormal(10.5, 0.5, n).round(-2),
    "visits": rng.poisson(5, n),
    "city": rng.choice(["Pune", "Delhi", "Mumbai", "Chennai"], n),
    "plan": rng.choice(["basic", "pro", "premium"], n, p=[0.6, 0.3, 0.1]),
})
logit = -3 + 0.04 * df["age"] + 0.00002 * df["income"] + 0.2 * df["visits"] + (df["plan"] == "premium") * 1.5
df["bought"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
df.loc[rng.random(n) < 0.1, "age"] = np.nan                  # 10% missing ages
df.loc[rng.random(n) < 0.05, "city"] = np.nan                 # 5% missing cities
print(df.head().to_string())
print("  missing:", df.isna().sum()[df.isna().sum() > 0].to_dict(), "| target balance:", df["bought"].value_counts().to_dict())

X_df = df.drop(columns="bought")
y_df = df["bought"]
Xtr, Xte, ytr, yte = train_test_split(X_df, y_df, stratify=y_df, random_state=0)

numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore"))])
preprocess = ColumnTransformer([
    ("num", numeric, ["age", "income", "visits"]),
    ("cat", categorical, ["city", "plan"]),
])
model = Pipeline([("prep", preprocess), ("clf", LogisticRegression())])
model.fit(Xtr, ytr)
print("\n  features the model sees:", preprocess.get_feature_names_out().tolist())
print(f"  test accuracy {model.score(Xte, yte):.3f} | CV on train {cross_val_score(model, Xtr, ytr, cv=5).mean():.3f}")

print("\n=== 4. Raw, messy new rows just work ===")
new = pd.DataFrame({"age": [np.nan, 45], "income": [30_000, 90_000], "visits": [2, 9],
                    "city": ["Kolkata", "Pune"], "plan": ["basic", "premium"]})
print(new.to_string(index=False))
print("  P(buy):", model.predict_proba(new)[:, 1].round(3), "(missing age imputed, unseen city -> all zeros)")

print("\n=== 5. Select columns by dtype; pandas output for debugging ===")
by_type = ColumnTransformer([
    ("num", numeric, make_column_selector(dtype_include="number")),
    ("cat", categorical, make_column_selector(dtype_include=object)),
])
categorical_dense = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                              ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
by_type_dense = ColumnTransformer([("num", numeric, make_column_selector(dtype_include="number")),
                                   ("cat", categorical_dense, make_column_selector(dtype_exclude="number"))])
by_type_dense.set_output(transform="pandas")
out = by_type_dense.fit_transform(Xtr)
print("  output is a", type(out).__name__, out.shape)
print(out.head(3).round(2).to_string())

print("\n=== 6. Swap the model, keep the preprocessing ===")
for clf in [LogisticRegression(), RandomForestClassifier(n_estimators=200, random_state=0)]:
    m = Pipeline([("prep", preprocess), ("clf", clf)])
    print(f"  {type(clf).__name__:<24} CV {cross_val_score(m, Xtr, ytr, cv=5).mean():.3f}")

print("\n=== 7. FeatureUnion: features side by side ===")
union = FeatureUnion([("pca", PCA(n_components=3)), ("best", SelectKBest(k=3))])
wine_pipe = make_pipeline(StandardScaler(), union, LogisticRegression())
wine_pipe.fit(X, y)
print("  13 wine features -> 3 PCA components + 3 selected originals =", wine_pipe[:-1].transform(X).shape[1], "features")
print(f"  CV accuracy {cross_val_score(wine_pipe, X, y, cv=5).mean():.3f}")
