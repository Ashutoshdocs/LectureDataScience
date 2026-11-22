"""Lecture 11: PolynomialFeatures, binning, FunctionTransformer, log targets, feature selection, permutation importance."""
import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, SelectFromModel, SelectKBest, VarianceThreshold, f_classif
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, KBinsDiscretizer, PolynomialFeatures, StandardScaler

print("=== 1. PolynomialFeatures ===")
poly = PolynomialFeatures(degree=2, include_bias=False)
print("  [a, b] = [2, 3] ->", poly.fit_transform([[2, 3]])[0], list(poly.get_feature_names_out(["a", "b"])))
x = np.linspace(-3, 3, 30).reshape(-1, 1)
y = x.ravel() ** 2 + np.random.default_rng(0).normal(0, 0.3, 30)
print(f"  y = x^2: plain linear R2 {LinearRegression().fit(x, y).score(x, y):.3f} | "
      f"with x^2 R2 {make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(x, y).score(x, y):.3f}")
for n_feat in (5, 10, 20):
    print(f"  {n_feat} features at degree 3 -> {PolynomialFeatures(3).fit(np.zeros((1, n_feat))).n_output_features_} columns")

print("\n=== 2. Binning ===")
ages = np.array([[5], [17], [23], [35], [48], [61], [79]])
for strategy in ["uniform", "quantile"]:
    kb = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy=strategy, quantile_method="averaged_inverted_cdf")
    print(f"  {strategy:<8} bins {kb.fit_transform(ages).ravel().astype(int)}  edges {np.round(kb.bin_edges_[0], 1)}")

print("\n=== 3. FunctionTransformer and domain features ===")
amounts = np.array([[10], [100], [1_000], [10_000], [100_000]])
log_tf = FunctionTransformer(np.log1p, inverse_func=np.expm1)
print("  log1p:", log_tf.fit_transform(amounts).ravel().round(2))
flats = pd.DataFrame({"price": [60, 90, 150], "area": [50, 80, 100], "sold": pd.to_datetime(["2026-01-03", "2026-03-15", "2026-07-06"])})
flats["price_per_m2"] = flats["price"] / flats["area"]
flats["month"] = flats["sold"].dt.month
flats["is_weekend"] = (flats["sold"].dt.dayofweek >= 5).astype(int)
print(flats.to_string(index=False))

print("\n=== 4. Log-transforming a skewed target ===")
rng = np.random.default_rng(1)
Xs = rng.uniform(0, 3, size=(300, 1))
ys = np.exp(1 + Xs.ravel() + rng.normal(0, 0.3, 300))       # exponential (skewed) target
for name, model in [("plain", LinearRegression()),
                    ("log target", TransformedTargetRegressor(regressor=LinearRegression(), func=np.log1p, inverse_func=np.expm1))]:
    print(f"  {name:<11} CV R2 {cross_val_score(model, Xs, ys, cv=5).mean():.3f}")

print("\n=== 5. Feature selection ===")
data = load_breast_cancer()
X, y, names = data.data, data.target, data.feature_names
X_const = np.hstack([X, np.ones((len(X), 1))])
print("  VarianceThreshold removes the constant column:", X_const.shape[1], "->", VarianceThreshold().fit_transform(X_const).shape[1])
kbest = SelectKBest(f_classif, k=5).fit(X, y)
print("  SelectKBest(k=5):", names[kbest.get_support()].tolist())
sfm = SelectFromModel(RandomForestClassifier(n_estimators=200, random_state=0), max_features=5).fit(X, y)
print("  SelectFromModel(forest):", names[sfm.get_support()].tolist())
rfe = RFE(LogisticRegression(), n_features_to_select=5)
rfe.fit(StandardScaler().fit_transform(X), y)
print("  RFE(logistic):", names[rfe.get_support()].tolist())

print("\n=== 6. Does selection help? (inside a pipeline = honest) ===")
for k in [2, 5, 10, 30]:
    pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif, k=k), LogisticRegression())
    print(f"  k={k:<3} CV accuracy {cross_val_score(pipe, X, y, cv=5).mean():.3f}")

print("\n=== 7. Impurity importance vs permutation importance ===")
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0, stratify=y)
forest = RandomForestClassifier(n_estimators=200, random_state=0).fit(Xtr, ytr)
imp_top = np.argsort(forest.feature_importances_)[::-1][:5]
perm = permutation_importance(forest, Xte, yte, n_repeats=10, random_state=0)
perm_top = np.argsort(perm.importances_mean)[::-1][:5]
print("  feature_importances_ top 5 :", names[imp_top].tolist())
print("  permutation (test) top 5   :", names[perm_top].tolist())
print("  correlated features share credit, so the two rankings can differ")
