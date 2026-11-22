"""Lecture 04: train_test_split, stratify, overfitting sweep, baselines, train/val/test."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris, make_classification
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

print("=== 1. train_test_split ===")
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print("  all:", X.shape, "| train:", X_train.shape, "| test:", X_test.shape)
print("  first 10 test labels (shuffled):", y_test[:10])
_, _, _, again = train_test_split(X, y, test_size=0.25, random_state=42)
print("  same random_state -> identical split:", np.array_equal(y_test, again))

print("\n=== 2. stratify keeps class balance ===")
y_imb = np.array([0] * 90 + [1] * 10)
X_imb = np.arange(100).reshape(-1, 1)
for strat in (None, y_imb):
    _, _, _, yt = train_test_split(X_imb, y_imb, test_size=0.2, random_state=3, stratify=strat)
    print(f"  stratify={'y' if strat is not None else 'None':<4} test counts [0s, 1s] = {np.bincount(yt)}")

print("\n=== 3. Why not score on training data? Complexity sweep ===")
Xc, yc = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, random_state=0, stratify=yc)
print(f"  {'max_depth':>9}  {'train':>6}  {'test':>6}  {'gap':>5}")
best = (0, None)
for depth in [1, 2, 3, 4, 5, 7, 10, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(Xtr, ytr)
    tr, te = tree.score(Xtr, ytr), tree.score(Xte, yte)
    best = max(best, (te, depth), key=lambda t: t[0])
    print(f"  {str(depth):>9}  {tr:6.3f}  {te:6.3f}  {tr - te:5.3f}  {'#' * int((te - 0.85) * 200)}")
print(f"  best test score {best[0]:.3f} at max_depth={best[1]}; unlimited depth hits train=1.000 (memorised)")

print("\n=== 4. Same idea with KNN: small k = complex ===")
for k in [1, 5, 15, 50, 150]:
    knn = KNeighborsClassifier(n_neighbors=k).fit(Xtr, ytr)
    print(f"  k={k:<4} train={knn.score(Xtr, ytr):.3f} test={knn.score(Xte, yte):.3f}")

print("\n=== 5. Baselines ===")
Xi, yi = make_classification(n_samples=2000, weights=[0.9, 0.1], random_state=0)
Xi_tr, Xi_te, yi_tr, yi_te = train_test_split(Xi, yi, stratify=yi, random_state=0)
dummy = DummyClassifier(strategy="most_frequent").fit(Xi_tr, yi_tr)
tree = DecisionTreeClassifier(max_depth=5, random_state=0).fit(Xi_tr, yi_tr)
print(f"  imbalanced data (90/10): dummy accuracy {dummy.score(Xi_te, yi_te):.3f} vs tree {tree.score(Xi_te, yi_te):.3f}")
print("  the dummy never predicts the rare class:", np.unique(dummy.predict(Xi_te)))
print(f"  breast cancer dummy: {DummyClassifier().fit(Xtr, ytr).score(Xte, yte):.3f} (any real model must beat this)")

print("\n=== 6. Train / validation / test ===")
X_tmp, X_final_test, y_tmp, y_final_test = train_test_split(Xc, yc, test_size=0.2, random_state=0, stratify=yc)
X_tr2, X_val, y_tr2, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
print("  train", X_tr2.shape[0], "| validation", X_val.shape[0], "| test", X_final_test.shape[0])
scores = {d: DecisionTreeClassifier(max_depth=d, random_state=0).fit(X_tr2, y_tr2).score(X_val, y_val) for d in [2, 3, 4, 6]}
chosen = max(scores, key=scores.get)
final = DecisionTreeClassifier(max_depth=chosen, random_state=0).fit(X_tmp, y_tmp)
print("  validation scores:", {k: round(v, 3) for k, v in scores.items()}, "-> chose depth", chosen)
print(f"  final, honest test score (used once): {final.score(X_final_test, y_final_test):.3f}")
