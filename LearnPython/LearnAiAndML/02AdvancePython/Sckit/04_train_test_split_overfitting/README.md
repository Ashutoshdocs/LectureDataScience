# Lecture 04: Train/test split, overfitting & baselines

Run: `python lecture.py`

## Why you must hold data back

A model's real job is predicting **new** data. Scoring it on the rows it learned from is like giving students the exam questions in advance: the score says nothing about real understanding.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
```

| Argument | Meaning | Default |
|----------|---------|---------|
| `test_size` | fraction (0.2) or count (50) of rows for testing | 0.25 |
| `random_state` | fixes the shuffle so results are repeatable | random each run |
| `stratify=y` | keep the **same class proportions** in train and test, which is vital for imbalanced data | off |
| `shuffle` | shuffle before splitting (set `False` for time series) | `True` |

The **order** of the four outputs is fixed: `X_train, X_test, y_train, y_test`. Mixing them up is a silent bug.

## Under-, good and overfitting

| | Train score | Test score | Meaning | Fix |
|--|-------------|------------|---------|-----|
| **Underfitting** | low | low | model too simple; misses the pattern | more complex model, better features |
| **Good fit** | high | high, close to train | learned the real pattern | ✅ |
| **Overfitting** | very high (often 1.0) | clearly lower | memorised noise | simpler model, regularisation, more data |

**Model complexity** is controlled by hyperparameters: `max_depth` for trees, `n_neighbors` for KNN (small k = complex), polynomial degree, `C`/`alpha` for regularisation. `lecture.py` sweeps `max_depth` and prints the classic U-shape: the test score rises, peaks, then falls while the training score keeps climbing.

## Bias–variance in one sentence

A too-simple model is **consistently wrong** (high bias). A too-complex model is **wrong in a different way for every training sample** (high variance). The sweet spot balances both.

## Always compare with a baseline

`DummyClassifier(strategy="most_frequent")` always predicts the majority class, and `DummyRegressor(strategy="mean")` always predicts the average. If your model can't clearly beat them, it hasn't learned anything useful. On 90/10 imbalanced data, the dummy already scores **90% accuracy**!

## Train / validation / test

When you tune hyperparameters by looking at a score, that score becomes optimistic. The professional setup:

```
 all data ─▶ train (fit models) | validation (choose settings) | test (final report, once)
```

In practice, **cross-validation on the training set** replaces a fixed validation set (Lectures 07, 21).

## Exercises

1. Remove `random_state` and run the split twice. Do the test labels change?
2. Use `test_size=0.2` on iris. How many rows end up in each part?
3. Extend the depth sweep to 1–20 for the breast-cancer data. Which depth is best on the test set?
4. Compute the `DummyClassifier` accuracy for the breast-cancer data.

**Next →** [Lecture 05: Classification metrics](../05_classification_metrics/)
