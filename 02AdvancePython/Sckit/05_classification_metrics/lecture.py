"""Lecture 05: Confusion matrix, precision/recall/F1, report, thresholds, ROC AUC, multiclass, imbalance."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris, make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

print("=== 1. Confusion matrix by hand ===")
y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]           # 1 = spam
y_pred = [1, 0, 0, 1, 0, 1, 1, 0, 1, 1]
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()
print("  rows = actual, cols = predicted\n", cm)
print(f"  TN={tn} FP={fp} FN={fn} TP={tp}")
print(f"  precision by hand {tp / (tp + fp):.3f} | sklearn {precision_score(y_true, y_pred):.3f}")
print(f"  recall    by hand {tp / (tp + fn):.3f} | sklearn {recall_score(y_true, y_pred):.3f}")
print(f"  F1 {f1_score(y_true, y_pred):.3f} | accuracy {accuracy_score(y_true, y_pred):.3f}")
print(classification_report(y_true, y_pred, target_names=["ham", "spam"]))

print("=== 2. Accuracy lies on imbalanced data ===")
X, y = make_classification(n_samples=5000, weights=[0.97, 0.03], class_sep=0.8, random_state=1)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)
for model in [DummyClassifier(strategy="most_frequent"), LogisticRegression(max_iter=1000)]:
    p = model.fit(Xtr, ytr).predict(Xte)
    print(f"  {type(model).__name__:<20} accuracy={accuracy_score(yte, p):.3f} "
          f"recall={recall_score(yte, p, zero_division=0):.3f} precision={precision_score(yte, p, zero_division=0):.3f}")
print("  The dummy is 97% 'accurate' and catches nothing.")

print("\n=== 3. Thresholds on the breast-cancer data (positive = malignant) ===")
data = load_breast_cancer()
yc = 1 - data.target                               # make malignant = 1 (the class we care about)
Xtr, Xte, ytr, yte = train_test_split(data.data, yc, stratify=yc, random_state=0)
clf = make_pipeline(StandardScaler(), LogisticRegression()).fit(Xtr, ytr)
proba = clf.predict_proba(Xte)[:, 1]
print(f"  {'threshold':>9} {'precision':>9} {'recall':>7} {'FP':>3} {'FN':>3}")
for t in [0.1, 0.3, 0.5, 0.7, 0.9]:
    p = (proba >= t).astype(int)
    _, fp, fn, _ = confusion_matrix(yte, p).ravel()
    print(f"  {t:>9} {precision_score(yte, p):>9.3f} {recall_score(yte, p):>7.3f} {fp:>3} {fn:>3}")
print("  lower threshold -> fewer missed cancers (FN), more false alarms (FP)")

print("\n=== 4. ROC curve and AUC ===")
fpr, tpr, thr = roc_curve(yte, proba)
print(f"  ROC AUC            : {roc_auc_score(yte, proba):.4f}")
print(f"  average precision  : {average_precision_score(yte, proba):.4f}")
print(f"  dummy ROC AUC      : {roc_auc_score(yte, np.full_like(proba, 0.5)):.2f} (random guessing)")
print("  a few ROC points (FPR -> TPR):", [(round(float(a), 2), round(float(b), 2)) for a, b in list(zip(fpr, tpr))[::3]])

print("\n=== 5. Multiclass (iris) ===")
Xi, yi = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(Xi, yi, test_size=0.4, stratify=yi, random_state=5)
pi = LogisticRegression(max_iter=500, C=0.05).fit(Xtr, ytr).predict(Xte)
print(confusion_matrix(yte, pi))
for avg in ["macro", "weighted", None]:
    print(f"  recall average={str(avg):<8}:", np.round(recall_score(yte, pi, average=avg), 3))
