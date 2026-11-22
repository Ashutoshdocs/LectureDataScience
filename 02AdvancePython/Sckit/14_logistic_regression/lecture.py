"""Lecture 14: Logistic regression: sigmoid, probabilities, coefficients/odds, C, convergence, multiclass, class_weight."""
import warnings

import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris, make_classification
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

np.set_printoptions(suppress=True)

print("=== 1. Probabilities from the sigmoid ===")
X = np.array([[0.5], [1], [1.5], [2], [3], [3.5], [4], [5]])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
clf = LogisticRegression().fit(X, y)
w, b = clf.coef_[0, 0], clf.intercept_[0]
print(f"  z = {w:.3f} x hours + ({b:.3f})")
for h in [1, 2.5, 4]:
    z = w * h + b
    p_hand = 1 / (1 + np.exp(-z))
    p_sk = clf.predict_proba([[h]])[0, 1]
    print(f"  {h} h: z={z:+.2f}  sigmoid {p_hand:.3f}  predict_proba {p_sk:.3f}  label {clf.predict([[h]])[0]}")
print(f"  decision boundary (P=0.5) at {-b / w:.2f} hours")
print(f"  odds ratio per extra hour: exp({w:.2f}) = {np.exp(w):.2f}x")

print("\n=== 2. C: inverse regularisation strength (breast cancer) ===")
Xc, yc = load_breast_cancer(return_X_y=True)
for C in [0.001, 0.01, 0.1, 1, 100]:
    pipe = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=5000))
    score = cross_val_score(pipe, Xc, yc, cv=5).mean()
    size = np.abs(pipe.fit(Xc, yc)[-1].coef_).sum()
    print(f"  C={C:<6} CV accuracy {score:.3f}   sum |coef| {size:7.2f}")

print("\n=== 3. L1 (sparse) logistic regression ===")
for C in [0.05, 0.2, 1]:
    l1 = make_pipeline(StandardScaler(), LogisticRegression(C=C, l1_ratio=1, solver="saga", max_iter=5000)).fit(Xc, yc)
    print(f"  C={C:<5} features used {np.sum(l1[-1].coef_ != 0):>2}/30   train accuracy {l1.score(Xc, yc):.3f}")

print("\n=== 4. ConvergenceWarning: scale your data ===")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    LogisticRegression(max_iter=100).fit(Xc, yc)
print("  unscaled, max_iter=100 ->", "ConvergenceWarning" if any(issubclass(c.category, ConvergenceWarning) for c in caught) else "no warning")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    make_pipeline(StandardScaler(), LogisticRegression(max_iter=100)).fit(Xc, yc)
print("  scaled,   max_iter=100 ->", "ConvergenceWarning" if caught else "no warning")

print("\n=== 5. Multiclass (softmax) on iris ===")
iris = load_iris()
m = LogisticRegression(max_iter=1000).fit(iris.data, iris.target)
print("  coef_ shape:", m.coef_.shape, "(one row per class)")
for idx in [0, 60, 120]:
    p = m.predict_proba(iris.data[idx:idx + 1])[0]
    print(f"  flower {idx:>3} true={iris.target_names[iris.target[idx]]:<10} proba {p.round(3)} sum {p.sum():.1f}")

print("\n=== 6. Imbalanced data: class_weight='balanced' ===")
Xi, yi = make_classification(n_samples=4000, weights=[0.95, 0.05], class_sep=0.7, random_state=3)
Xtr, Xte, ytr, yte = train_test_split(Xi, yi, stratify=yi, random_state=0)
for cw in [None, "balanced"]:
    p = LogisticRegression(class_weight=cw).fit(Xtr, ytr).predict(Xte)
    print(f"  class_weight={str(cw):<9} recall {recall_score(yte, p):.3f}  precision {precision_score(yte, p):.3f}  "
          f"flagged {p.sum():>3} of {len(p)}")
