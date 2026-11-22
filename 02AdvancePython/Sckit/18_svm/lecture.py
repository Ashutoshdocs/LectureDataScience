"""Lecture 18: SVM: margins & support vectors, C, kernels, gamma, scaling, tuning, LinearSVC, SVR."""
import time

import numpy as np
from sklearn.datasets import load_breast_cancer, make_blobs, make_classification, make_moons
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC, SVR, LinearSVC

print("=== 1. Support vectors and C ===")
Xb, yb = make_blobs(n_samples=100, centers=2, cluster_std=1.8, random_state=4)
for C in [0.01, 1, 100]:
    svm = SVC(kernel="linear", C=C).fit(Xb, yb)
    margin = 2 / np.linalg.norm(svm.coef_)
    print(f"  C={C:<5} support vectors per class {svm.n_support_.tolist()}  margin width {margin:.2f}  train acc {svm.score(Xb, yb):.2f}")
print("  small C: wide street, many support vectors; large C: narrow street, few")

print("\n=== 2. Kernels on curved data (moons) ===")
Xm, ym = make_moons(n_samples=400, noise=0.2, random_state=0)
for kernel in ["linear", "poly", "rbf"]:
    pipe = make_pipeline(StandardScaler(), SVC(kernel=kernel, degree=3))
    print(f"  kernel={kernel:<7} CV {cross_val_score(pipe, Xm, ym, cv=5).mean():.3f}")

print("\n=== 3. gamma: reach of each point (rbf) ===")
Xtr, Xte, ytr, yte = train_test_split(Xm, ym, random_state=0)
for gamma in [0.01, 0.1, 1, 10, 100]:
    svm = make_pipeline(StandardScaler(), SVC(gamma=gamma)).fit(Xtr, ytr)
    print(f"  gamma={gamma:<6} train {svm.score(Xtr, ytr):.3f}  test {svm.score(Xte, yte):.3f}  support vectors {svm[-1].n_support_.sum()}")

print("\n=== 4. Scaling matters ===")
X, y = load_breast_cancer(return_X_y=True)
print(f"  unscaled SVC {cross_val_score(SVC(), X, y, cv=5).mean():.3f} | scaled {cross_val_score(make_pipeline(StandardScaler(), SVC()), X, y, cv=5).mean():.3f}")

print("\n=== 5. Tune C and gamma together ===")
grid = GridSearchCV(make_pipeline(StandardScaler(), SVC()),
                    {"svc__C": [0.1, 1, 10, 100], "svc__gamma": [0.001, 0.01, 0.1, 1]}, cv=5)
grid.fit(X, y)
print("  best:", grid.best_params_, f"CV {grid.best_score_:.3f}")
scores = grid.cv_results_["mean_test_score"].reshape(4, 4)
print("  rows C=0.1..100, cols gamma=0.001..1:")
for C, row in zip([0.1, 1, 10, 100], scores):
    print(f"    C={C:<5}", " ".join(f"{v:.3f}" for v in row))

print("\n=== 6. Probabilities and decision_function ===")
svc = make_pipeline(StandardScaler(), SVC()).fit(X, y)
print("  plain SVC has predict_proba?", hasattr(svc[-1], "predict_proba") and svc[-1].probability)
print("  decision_function (first 3):", svc.decision_function(X[:3]).round(2), "(sign = class, size = confidence)")
calibrated = make_pipeline(StandardScaler(), CalibratedClassifierCV(SVC(), cv=5)).fit(X, y)
print("  CalibratedClassifierCV(SVC()) predict_proba[:, 1]:", calibrated.predict_proba(X[:3])[:, 1].round(3))

print("\n=== 7. Big data: LinearSVC is much faster ===")
Xl, yl = make_classification(n_samples=6_000, n_features=50, random_state=0)
for m in [make_pipeline(StandardScaler(), SVC(kernel="linear")), make_pipeline(StandardScaler(), LinearSVC())]:
    t0 = time.perf_counter()
    m.fit(Xl, yl)
    print(f"  {type(m[-1]).__name__:<10} fit {time.perf_counter() - t0:6.2f} s  train acc {m.score(Xl, yl):.3f}")

print("\n=== 8. SVR: regression with an epsilon tube ===")
rng = np.random.default_rng(0)
xr = np.sort(rng.uniform(0, 6, 80)).reshape(-1, 1)
yr = np.sin(xr).ravel() + rng.normal(0, 0.15, 80)
for eps in [0.01, 0.2, 0.5]:
    svr = SVR(C=10, epsilon=eps).fit(xr, yr)
    print(f"  epsilon={eps:<5} support vectors {len(svr.support_):>2}/80  R2 vs true sin {svr.score(xr, np.sin(xr).ravel()):.3f}")
