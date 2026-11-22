"""Lecture 03: Estimators, predictors, transformers; hyperparameters vs learned_; get/set_params; clone; input rules."""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

print("=== 1. Predictor methods ===")
clf = LogisticRegression(max_iter=500)
returned = clf.fit(X, y)
print("  fit() returns the model itself:", returned is clf)
two = X[[0, 100]]
print("  predict       :", clf.predict(two))
print("  predict_proba :\n", clf.predict_proba(two).round(3))
print("  rows sum to 1 :", clf.predict_proba(two).sum(axis=1))
print("  classes_      :", clf.classes_, "(column order of predict_proba)")
print("  score (accuracy on training data):", round(clf.score(X, y), 3))

print("\n=== 2. Transformer methods ===")
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
print("  learned mean_ :", scaler.mean_.round(2))
print("  learned scale_:", scaler.scale_.round(2))
print("  transformed column means ~0:", Xs.mean(axis=0).round(6), "| std ~1:", Xs.std(axis=0).round(3))

print("\n=== 3. Hyperparameters vs learned attributes ===")
tree = DecisionTreeClassifier(max_depth=2, random_state=0)
print("  print(tree)   :", tree, "<- only non-default settings shown")
print("  n params      :", len(tree.get_params()), "->", {k: tree.get_params()[k] for k in ["max_depth", "criterion", "min_samples_leaf"]})
print("  has feature_importances_ before fit?", hasattr(tree, "feature_importances_"))
tree.fit(X, y)
print("  after fit     :", tree.feature_importances_.round(3))
learned = [a for a in vars(tree) if a.endswith("_") and not a.startswith("_")]
print("  learned attrs :", learned)
tree.set_params(max_depth=4)
print("  set_params    :", tree, "(must re-fit for it to take effect)")

print("\n=== 4. clone(): fresh unfitted copy with the same settings ===")
copy = clone(tree)
print("  clone:", copy, "| fitted?", hasattr(copy, "tree_"), "| original fitted?", hasattr(tree, "tree_"))

print("\n=== 5. Chaining ===")
print("  LinearRegression().fit(...).predict(...) ->",
      LinearRegression().fit([[1], [2], [3]], [2, 4, 6]).predict([[10]]))

print("\n=== 6. Input rules and the errors you will meet ===")
sizes = np.array([50, 80, 100, 120])
prices = np.array([30, 48, 60, 72])
print("  reshape(-1, 1):", sizes.shape, "->", sizes.reshape(-1, 1).shape,
      "| reshape(1, -1):", sizes.reshape(1, -1).shape)
lin = LinearRegression().fit(sizes.reshape(-1, 1), prices)
print("  price for 90 m2:", lin.predict([[90]])[0].round(1))

df = pd.DataFrame(X[:, :2], columns=["sepal_len", "sepal_wid"])
named = LogisticRegression().fit(df, y)
print("  feature_names_in_ remembered from DataFrame:", list(named.feature_names_in_))

cases = {
    "1-D X": lambda: LinearRegression().fit(sizes, prices),
    "predict before fit": lambda: LogisticRegression().predict(X[:1]),
    "wrong number of features": lambda: clf.predict(X[:1, :3]),
    "text in X": lambda: LinearRegression().fit([["a"], ["b"]], [1, 2]),
    "NaN in X": lambda: LinearRegression().fit([[1.0], [np.nan]], [1, 2]),
}
for label, action in cases.items():
    try:
        action()
    except (ValueError, NotFittedError) as e:
        print(f"  {label:<25} -> {type(e).__name__}: {str(e).splitlines()[0][:80]}")
