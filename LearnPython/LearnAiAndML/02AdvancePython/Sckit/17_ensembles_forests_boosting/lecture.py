"""Lecture 17: Ensembles: bagging vs single tree, random forest (n_estimators, OOB), boosting (learning rate, early stopping),
HistGradientBoosting (speed, NaN), voting and stacking."""
import time

import numpy as np
from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.ensemble import (BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier,
                              HistGradientBoostingClassifier, RandomForestClassifier, StackingClassifier,
                              VotingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)

print("=== 1. One tree vs many ===")
models = {
    "single tree": DecisionTreeClassifier(random_state=0),
    "bagging (100 trees)": BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=0),
    "random forest": RandomForestClassifier(n_estimators=200, random_state=0),
    "extra trees": ExtraTreesClassifier(n_estimators=200, random_state=0),
}
for name, m in models.items():
    s = cross_val_score(m, X, y, cv=5)
    print(f"  {name:<20} CV {s.mean():.3f} +/- {s.std():.3f}")

print("\n=== 2. More trees: the score rises, then settles (no overfitting from adding trees) ===")
for n in [1, 5, 20, 100, 300]:
    s = cross_val_score(RandomForestClassifier(n_estimators=n, random_state=0, n_jobs=-1), X, y, cv=5)
    print(f"  n_estimators={n:<4} CV {s.mean():.3f} +/- {s.std():.3f}")

print("\n=== 3. Out-of-bag score: free validation ===")
rf = RandomForestClassifier(n_estimators=300, oob_score=True, random_state=0, n_jobs=-1).fit(Xtr, ytr)
print(f"  OOB score {rf.oob_score_:.3f} | CV on train {cross_val_score(RandomForestClassifier(n_estimators=300, random_state=0, n_jobs=-1), Xtr, ytr, cv=5).mean():.3f} | test {rf.score(Xte, yte):.3f}")
top = np.argsort(rf.feature_importances_)[::-1][:3]
print("  top features:", load_breast_cancer().feature_names[top].tolist())

print("\n=== 4. Gradient boosting: learning rate x number of trees ===")
for lr in [1.0, 0.1, 0.01]:
    gb = GradientBoostingClassifier(n_estimators=300, learning_rate=lr, max_depth=3, random_state=0).fit(Xtr, ytr)
    staged = [np.mean(p == yte) for p in gb.staged_predict(Xte)]
    best_round = int(np.argmax(staged)) + 1
    print(f"  learning_rate={lr:<5} test after 10 rounds {staged[9]:.3f}, after 300 {staged[-1]:.3f}, best {max(staged):.3f} at round {best_round}")

print("\n=== 5. Early stopping ===")
gb_es = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.1, validation_fraction=0.2,
                                   n_iter_no_change=10, random_state=0).fit(Xtr, ytr)
print(f"  asked for 1000 rounds, stopped after {gb_es.n_estimators_}; test {gb_es.score(Xte, yte):.3f}")

print("\n=== 6. HistGradientBoosting: fast on big data, handles NaN ===")
Xb, yb = make_classification(n_samples=20_000, n_features=20, n_informative=10, random_state=0)
Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(Xb, yb, random_state=0)
for m in [GradientBoostingClassifier(n_estimators=100, random_state=0), HistGradientBoostingClassifier(max_iter=100, random_state=0)]:
    t0 = time.perf_counter()
    m.fit(Xb_tr, yb_tr)
    print(f"  {type(m).__name__:<32} {time.perf_counter() - t0:5.2f} s  test {m.score(Xb_te, yb_te):.3f}")
X_nan = Xtr.copy()
X_nan[np.random.default_rng(0).random(X_nan.shape) < 0.1] = np.nan
hgb = HistGradientBoostingClassifier(random_state=0).fit(X_nan, ytr)
print(f"  trained on data with 10% NaN, no imputation: test {hgb.score(Xte, yte):.3f}")

print("\n=== 7. Voting and stacking different models ===")
base = [("logistic", make_pipeline(StandardScaler(), LogisticRegression())),
        ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier())),
        ("forest", RandomForestClassifier(n_estimators=200, random_state=0))]
for name, m in base:
    print(f"  {name:<9} CV {cross_val_score(m, X, y, cv=5).mean():.3f}")
vote = VotingClassifier(base, voting="soft")
stack = StackingClassifier(base, final_estimator=LogisticRegression())
print(f"  soft vote CV {cross_val_score(vote, X, y, cv=5).mean():.3f}")
print(f"  stacking  CV {cross_val_score(stack, X, y, cv=5).mean():.3f}")
