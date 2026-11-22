"""Lecture 21: GridSearchCV, step__param, results table, searching over steps/models, RandomizedSearchCV,
edge-of-grid check, nested CV, final test evaluation."""
import time

import numpy as np
import pandas as pd
from scipy.stats import loguniform, randint
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC

X, y = load_wine(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)

print("=== 1. GridSearchCV on a pipeline ===")
pipe = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier())])
grid = {"knn__n_neighbors": [1, 3, 5, 7, 9, 15, 25], "knn__weights": ["uniform", "distance"], "knn__p": [1, 2]}
search = GridSearchCV(pipe, grid, cv=5, n_jobs=-1)
search.fit(Xtr, ytr)
print(f"  {len(search.cv_results_['params'])} combinations x 5 folds = {len(search.cv_results_['params']) * 5} fits")
print("  best_params_:", search.best_params_)
print(f"  best_score_ (CV on train): {search.best_score_:.3f}")
print("  best_estimator_:", search.best_estimator_)

print("\n=== 2. The full results table ===")
res = pd.DataFrame(search.cv_results_)
cols = ["param_knn__n_neighbors", "param_knn__weights", "param_knn__p", "mean_test_score", "std_test_score", "rank_test_score"]
print(res[cols].sort_values("rank_test_score").head(6).to_string(index=False))

print("\n=== 3. Search over whole steps and over different models ===")
pipe2 = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])
grids = [
    {"scale": [StandardScaler(), MinMaxScaler()], "clf": [LogisticRegression(max_iter=2000)], "clf__C": [0.01, 0.1, 1, 10]},
    {"scale": ["passthrough"], "clf": [RandomForestClassifier(random_state=0)], "clf__max_depth": [3, None]},
    {"scale": [StandardScaler()], "clf": [SVC()], "clf__C": [0.1, 1, 10]},
]
multi = GridSearchCV(pipe2, grids, cv=5, n_jobs=-1).fit(Xtr, ytr)
print("  winner:", multi.best_params_, f"CV {multi.best_score_:.3f}")
top = pd.DataFrame(multi.cv_results_).sort_values("rank_test_score").head(4)
for _, row in top.iterrows():
    print(f"    rank {row['rank_test_score']}: {type(row['param_clf']).__name__:<22} {row['mean_test_score']:.3f}")

print("\n=== 4. RandomizedSearchCV with distributions ===")
Xc, yc = load_breast_cancer(return_X_y=True)
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(Xc, yc, stratify=yc, random_state=0)
rf_pipe = Pipeline([("clf", RandomForestClassifier(random_state=0, n_jobs=-1))])
dists = {"clf__n_estimators": randint(50, 200), "clf__max_depth": randint(2, 20),
         "clf__min_samples_leaf": randint(1, 10), "clf__max_features": ["sqrt", "log2", 0.5]}
t0 = time.perf_counter()
rand = RandomizedSearchCV(rf_pipe, dists, n_iter=10, cv=5, random_state=0, n_jobs=-1).fit(Xc_tr, yc_tr)
print(f"  10 random candidates in {time.perf_counter() - t0:.1f} s -> {rand.best_params_}")
print(f"  best CV {rand.best_score_:.3f}")
log_pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=5000))])
rand_c = RandomizedSearchCV(log_pipe, {"clf__C": loguniform(1e-4, 1e3)}, n_iter=25, cv=5, random_state=0).fit(Xc_tr, yc_tr)
print(f"  logistic C sampled on a log scale: best C = {rand_c.best_params_['clf__C']:.4f}, CV {rand_c.best_score_:.3f}")

print("\n=== 5. Is the best value on the edge of the grid? ===")
narrow = GridSearchCV(log_pipe, {"clf__C": [0.001, 0.003, 0.01]}, cv=5).fit(Xc_tr, yc_tr)
print("  grid [0.001, 0.003, 0.01] -> best", narrow.best_params_["clf__C"], "<- on the edge: extend the grid!")
wide = GridSearchCV(log_pipe, {"clf__C": np.logspace(-3, 2, 11)}, cv=5).fit(Xc_tr, yc_tr)
print(f"  grid 0.001..100 (log) -> best {wide.best_params_['clf__C']:.3g}, CV {wide.best_score_:.3f}")

print("\n=== 6. best_score_ is optimistic: nested cross-validation ===")
inner = GridSearchCV(Pipeline([("scale", StandardScaler()), ("svc", SVC())]),
                     {"svc__C": [0.1, 1, 10, 100], "svc__gamma": [0.001, 0.01, 0.1, 1]}, cv=5)
inner.fit(Xc_tr, yc_tr)
nested = cross_val_score(inner, Xc_tr, yc_tr, cv=5)
print(f"  best_score_ (chosen as the max of 16) : {inner.best_score_:.3f}")
print(f"  nested CV (search inside each fold)    : {nested.mean():.3f} +/- {nested.std():.3f}  <- honest")

print("\n=== 7. Final step: evaluate once on the untouched test set ===")
print(f"  SVC search best params {inner.best_params_} -> test accuracy {inner.score(Xc_te, yc_te):.3f}")
print(f"  wine KNN search -> test accuracy {search.score(Xte, yte):.3f}")
