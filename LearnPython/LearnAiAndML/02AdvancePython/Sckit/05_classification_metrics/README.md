# Lecture 05: Classification metrics

Run: `python lecture.py`

## Why accuracy isn't enough

If 99% of transactions are genuine, a model that **always says "genuine"** is 99% accurate and catches **zero** fraud. You need metrics that look at **which** mistakes happen.

## The confusion matrix

```python
from sklearn.metrics import confusion_matrix
confusion_matrix(y_true, y_pred)
```

For two classes (1 = positive, the class you care about):

|  | **Predicted 0** | **Predicted 1** |
|--|-----------------|-----------------|
| **Actual 0** | TN: true negative | **FP**: false positive (false alarm) |
| **Actual 1** | **FN**: false negative (missed!) | TP: true positive |

> scikit-learn's layout: **rows = actual, columns = predicted**, sorted by label. `confusion_matrix(...).ravel()` gives `tn, fp, fn, tp`.

## The key metrics

| Metric | Formula | Question it answers | Care most when… |
|--------|---------|---------------------|-----------------|
| **Accuracy** | (TP + TN) / all | how often is it right overall? | classes are balanced and errors cost the same |
| **Precision** | TP / (TP + FP) | when it says "positive", how often is that true? | **false alarms are costly** (spam filter deleting real mail) |
| **Recall** (sensitivity) | TP / (TP + FN) | of all real positives, how many did we catch? | **misses are costly** (cancer, fraud) |
| **F1** | 2·P·R / (P + R) | one balance of precision and recall | you need one number on imbalanced data |
| **Specificity** | TN / (TN + FP) | of all real negatives, how many were cleared? | medical tests |

`classification_report(y_true, y_pred)` prints precision, recall, F1 and **support** (the number of true samples) for every class, plus averages:

| Average | Meaning |
|---------|---------|
| **macro** | plain mean over classes: every class counts equally (good for rare classes) |
| **weighted** | mean weighted by support |

## Thresholds: the precision–recall trade-off

Most classifiers output a **probability** (`predict_proba`) or a **score** (`decision_function`). `predict` simply uses **0.5**. Move the threshold to trade metrics:

| Lower threshold (e.g. 0.3) | Higher threshold (e.g. 0.7) |
|----------------------------|-----------------------------|
| more positives flagged | fewer positives flagged |
| ↑ recall, ↓ precision | ↑ precision, ↓ recall |

```python
proba = model.predict_proba(X_test)[:, 1]
pred_custom = (proba >= 0.3).astype(int)
```

Choose the threshold on **validation** data, based on the real cost of each error.

## ROC curve & AUC

The **ROC curve** plots the true-positive rate (recall) against the false-positive rate for **every** threshold. **ROC AUC** (area under it) is a threshold-free summary:

| AUC | Meaning |
|-----|---------|
| 1.0 | perfect ranking |
| 0.5 | random guessing |
| < 0.5 | worse than random (are the labels flipped?) |

AUC answers: "if I pick one random positive and one random negative, how often does the model score the positive higher?" On **heavily imbalanced** data, also look at **average precision** (the area under the precision–recall curve).

## Multiclass

All metrics work with 3+ classes. The confusion matrix becomes n × n. Precision and recall need `average="macro"`, `"weighted"` or `"micro"` (or `None` for per-class values).

## Choosing a metric: cheat sheet

| Situation | Primary metric |
|-----------|----------------|
| balanced classes, equal costs | accuracy |
| rare positive class you must find | recall (+ precision to keep alarms sane), PR AUC |
| false alarms are expensive | precision |
| comparing models independent of threshold | ROC AUC |
| imbalanced, one summary number | F1 (or macro F1 for multiclass) |

## Exercises

1. Compute precision and recall by hand from the confusion matrix in `lecture.py` and check them against scikit-learn.
2. Find the threshold that gives recall ≥ 0.98 for the malignant class.
3. Print the multiclass confusion matrix for iris and find which species get confused.
4. Explain why `DummyClassifier` gets ROC AUC 0.5.

**Next →** [Lecture 06: Regression metrics](../06_regression_metrics/)
