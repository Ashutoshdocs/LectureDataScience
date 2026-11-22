"""Lecture 26: Project: tumour classifier: model comparison, tuning, threshold choice for recall, final report."""
import warnings

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, make_scorer, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import (GridSearchCV, StratifiedKFold, cross_val_predict, cross_validate,
                                     train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings("ignore", category=ConvergenceWarning)

# ---------------------------------------------------------------- 1. data & problem framing
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(1 - data.target, name="malignant")      # 1 = malignant: the class we must not miss
print("=== 1. Problem ===")
print(f"  {X.shape[0]} tumours, {X.shape[1]} features | malignant {y.sum()} ({y.mean():.0%}), benign {(1 - y).sum()}")
print("  Costly error: a FALSE NEGATIVE (calling a malignant tumour benign).")
print("  Goal: recall(malignant) >= 0.97 while keeping precision as high as possible.")

# ---------------------------------------------------------------- 2. split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print(f"\n=== 2. Stratified split: {len(X_train)} train / {len(X_test)} test, malignant share "
      f"{y_train.mean():.3f} vs {y_test.mean():.3f} ===")

# ---------------------------------------------------------------- 3. compare models
print("\n=== 3. Compare models (5-fold stratified CV on train) ===")
cv = StratifiedKFold(5, shuffle=True, random_state=0)
models = {
    "Dummy": DummyClassifier(strategy="most_frequent"),
    "Logistic": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    "KNN": make_pipeline(StandardScaler(), KNeighborsClassifier()),
    "SVC": make_pipeline(StandardScaler(), SVC()),
    "RandomForest": RandomForestClassifier(n_estimators=300, random_state=0, n_jobs=-1),
    "HistGB": HistGradientBoostingClassifier(random_state=0),
}
rows = []
for name, m in models.items():
    r = cross_validate(m, X_train, y_train, cv=cv, scoring={"accuracy": "accuracy", "recall": "recall",
                                                         "precision": make_scorer(precision_score, zero_division=0), "roc_auc": "roc_auc"})
    rows.append({"model": name, **{k.replace("test_", ""): v.mean() for k, v in r.items() if k.startswith("test_")}})
table = pd.DataFrame(rows).set_index("model").round(3)
print(table.to_string())
print("  Logistic and SVC lead; logistic gives easy probabilities and coefficients, so we tune it.")

# ---------------------------------------------------------------- 4. tune
print("\n=== 4. Tune logistic regression (optimise ROC AUC: threshold-free ranking quality) ===")
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=5000))])
grid = {"clf__C": np.logspace(-3, 2, 11), "clf__class_weight": [None, "balanced"]}
search = GridSearchCV(pipe, grid, cv=cv, scoring="roc_auc", n_jobs=-1).fit(X_train, y_train)
print("  best:", {k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in search.best_params_.items()},
      f"CV ROC AUC {search.best_score_:.4f}")

# ---------------------------------------------------------------- 5. choose the threshold on out-of-fold predictions
print("\n=== 5. Choose the decision threshold with out-of-fold probabilities (train only) ===")
oof = cross_val_predict(search.best_estimator_, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
print(f"  {'threshold':>9} {'recall':>7} {'precision':>9} {'missed':>6} {'false alarms':>12}")
candidates = np.round(np.arange(0.05, 0.75, 0.05), 2)
chosen = None
for t in candidates:
    p = (oof >= t).astype(int)
    rec, prec = recall_score(y_train, p), precision_score(y_train, p)
    _, fp, fn, _ = confusion_matrix(y_train, p).ravel()
    if t in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        print(f"  {t:>9} {rec:>7.3f} {prec:>9.3f} {fn:>6} {fp:>12}")
    if rec >= 0.97:
        chosen = t                                     # highest threshold that still meets the recall goal
print(f"  -> chosen threshold {chosen} (the highest one with recall >= 0.97, so precision stays as high as possible)")

# ---------------------------------------------------------------- 6. final test evaluation
print("\n=== 6. Final evaluation on the untouched test set ===")
proba_test = search.predict_proba(X_test)[:, 1]
for label, t in [("default 0.5", 0.5), (f"chosen {chosen}", chosen)]:
    p = (proba_test >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, p).ravel()
    print(f"  threshold {label:<12} recall {recall_score(y_test, p):.3f}  precision {precision_score(y_test, p):.3f}  "
          f"missed cancers {fn}  false alarms {fp}")
final_pred = (proba_test >= chosen).astype(int)
print(f"  ROC AUC {roc_auc_score(y_test, proba_test):.4f}")
print("  confusion matrix (rows actual benign/malignant, cols predicted):")
print(confusion_matrix(y_test, final_pred))
print(classification_report(y_test, final_pred, target_names=["benign", "malignant"], digits=3))

# ---------------------------------------------------------------- 7. explain
print("=== 7. Which features push towards 'malignant'? (standardised coefficients) ===")
coef = pd.Series(search.best_estimator_[-1].coef_[0], index=data.feature_names).sort_values()
print("  towards malignant:", coef.tail(5)[::-1].round(2).to_dict())
print("  towards benign   :", coef.head(3).round(2).to_dict())

# ---------------------------------------------------------------- 8. a decision function for deployment
print("\n=== 8. Packaging the decision rule ===")


def classify(model, rows, threshold=chosen):
    proba = model.predict_proba(rows)[:, 1]
    return pd.DataFrame({"p_malignant": proba.round(3),
                         "decision": np.where(proba >= threshold, "refer for biopsy", "routine follow-up")})


print(classify(search.best_estimator_, X_test.iloc[:5]).assign(truth=y_test.iloc[:5].map({1: "malignant", 0: "benign"}).values).to_string(index=False))
