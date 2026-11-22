"""Lecture 07: Cross-validation: one-split luck, cross_val_score, scoring, cross_validate, splitters, groups, time, learning curves."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import (GroupKFold, KFold, StratifiedKFold, TimeSeriesSplit, cross_val_score,
                                     cross_validate, learning_curve, train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)
knn = KNeighborsClassifier(n_neighbors=5)

print("=== 1. One split = one roll of the dice ===")
scores = []
for seed in range(10):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=seed)
    scores.append(knn.fit(Xtr, ytr).score(Xte, yte))
print("  test accuracy for 10 different splits:", np.round(scores, 3))
print(f"  range {min(scores):.3f} - {max(scores):.3f}: which one would you report?")

print("\n=== 2. cross_val_score ===")
for cv in (3, 5, 10):
    s = cross_val_score(knn, X, y, cv=cv)
    print(f"  cv={cv:<2} mean {s.mean():.3f} +/- {s.std():.3f}   folds {np.round(s, 3)}")

print("\n=== 3. Choosing the metric (error metrics are negated) ===")
Xd, yd = load_diabetes(return_X_y=True)
neg_mae = cross_val_score(LinearRegression(), Xd, yd, cv=5, scoring="neg_mean_absolute_error")
r2 = cross_val_score(LinearRegression(), Xd, yd, cv=5, scoring="r2")
print(f"  neg MAE {neg_mae.mean():.1f} -> report MAE {-neg_mae.mean():.1f} | R2 {r2.mean():.3f}")
Xc, yc = load_breast_cancer(return_X_y=True)
logit = make_pipeline(StandardScaler(), LogisticRegression())
for metric in ["accuracy", "f1", "roc_auc", "recall"]:
    print(f"  breast cancer {metric:<8}: {cross_val_score(logit, Xc, yc, cv=5, scoring=metric).mean():.3f}")

print("\n=== 4. cross_validate: train vs test, several metrics, timings ===")
for depth in (3, None):
    res = cross_validate(DecisionTreeClassifier(max_depth=depth, random_state=0), Xc, yc, cv=5,
                         scoring=["accuracy", "f1"], return_train_score=True)
    print(f"  max_depth={str(depth):<4} train acc {res['train_accuracy'].mean():.3f} | test acc {res['test_accuracy'].mean():.3f}"
          f" | test f1 {res['test_f1'].mean():.3f} | fit {res['fit_time'].mean() * 1000:.1f} ms")

print("\n=== 5. Splitters ===")
y_sorted = np.array([0] * 6 + [1] * 6)
X_small = np.arange(12).reshape(-1, 1)
print("  KFold (no shuffle) on sorted labels -> test-fold labels:")
for _, te in KFold(n_splits=3).split(X_small):
    print("    ", y_sorted[te])
print("  StratifiedKFold keeps the mix:")
for _, te in StratifiedKFold(n_splits=3).split(X_small, y_sorted):
    print("    ", y_sorted[te])
print("  TimeSeriesSplit: train on the past, test on the future")
for tr, te in TimeSeriesSplit(n_splits=3).split(X_small):
    print(f"     train {tr.min()}-{tr.max()}  test {te.tolist()}")

print("\n=== 6. Grouped data: KFold leaks, GroupKFold doesn't ===")
rng = np.random.default_rng(0)
n_patients, visits = 40, 10
patient = np.repeat(np.arange(n_patients), visits)
patient_signature = rng.normal(size=(n_patients, 5))[patient]       # each patient has a unique "fingerprint"
Xg = patient_signature + rng.normal(scale=0.1, size=patient_signature.shape)
yg = rng.integers(0, 2, n_patients)[patient]                        # label depends only on the patient (random!)
model = KNeighborsClassifier(n_neighbors=1)
plain = cross_val_score(model, Xg, yg, cv=KFold(5, shuffle=True, random_state=0)).mean()
grouped = cross_val_score(model, Xg, yg, cv=GroupKFold(5), groups=patient).mean()
print(f"  KFold accuracy {plain:.3f}  <- model recognises patients it already saw (leakage)")
print(f"  GroupKFold     {grouped:.3f}  <- honest: labels are random, so ~0.5 is the truth")

print("\n=== 7. Learning curve: would more data help? ===")
sizes, train_s, val_s = learning_curve(make_pipeline(StandardScaler(), LogisticRegression()), Xc, yc,
                                       train_sizes=[0.1, 0.3, 0.6, 1.0], cv=5)
for n, tr, va in zip(sizes, train_s.mean(axis=1), val_s.mean(axis=1)):
    print(f"  {n:>4} samples  train {tr:.3f}  validation {va:.3f}  gap {tr - va:.3f}")
