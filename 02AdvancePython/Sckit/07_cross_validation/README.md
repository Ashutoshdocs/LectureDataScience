# Lecture 07: Cross-validation

Run: `python lecture.py`

## The problem with one split

A single train/test split is **one roll of the dice**. A lucky split makes a model look great; an unlucky one makes it look bad. With small datasets, the score can swing by several percent just from changing `random_state`. `lecture.py` shows this.

## K-fold cross-validation

```
 fold 1: [TEST][train][train][train][train]
 fold 2: [train][TEST][train][train][train]
 ...     every row is in the test fold exactly once
 fold 5: [train][train][train][train][TEST]
 → 5 scores → report mean ± std
```

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)          # pass the UNFITTED model
print(scores.mean(), scores.std())
```

- `cross_val_score` **clones** the model for every fold, so you never pass a fitted one.
- **mean** = best estimate of performance; **std** = how stable that estimate is.
- `cv=5` or `cv=10` are common. More folds mean more training data per fold, but more fits.

## Choosing the scoring metric

`scoring="accuracy"`, `"f1"`, `"roc_auc"`, `"recall"`, `"r2"`, `"neg_mean_absolute_error"`, `"neg_root_mean_squared_error"`…

> Error metrics are **negated** (`neg_…`) because scikit-learn always **maximises** scores. Flip the sign back when you report them.

## `cross_validate`: more information

```python
from sklearn.model_selection import cross_validate
res = cross_validate(model, X, y, cv=5, scoring=["accuracy", "f1"], return_train_score=True)
res["test_accuracy"], res["train_accuracy"], res["fit_time"]
```

Train scores much higher than test scores across folds = **overfitting**.

## Splitter objects: control how folds are made

| Splitter | Use when | Notes |
|----------|----------|-------|
| `KFold(n_splits, shuffle=True, random_state)` | regression, plain data | the default for regressors (no shuffle by default!) |
| `StratifiedKFold` | **classification** | keeps class proportions per fold; the **default** when you pass `cv=5` with a classifier |
| `RepeatedStratifiedKFold(n_repeats=3)` | small data, need stable estimates | repeats with different shuffles |
| `GroupKFold(groups=...)` | several rows per patient/customer/user | all rows of one group stay in the same fold, which **prevents leakage** |
| `TimeSeriesSplit` | **time-ordered** data | always trains on the past and tests on the future; never shuffle |
| `LeaveOneOut` | tiny datasets | n fits; slow |

## Leakage warning: grouped data

If the same patient appears in both the training and test folds, the model can recognise the *patient* rather than learn the *disease*, and scores look far too good. `lecture.py` shows plain KFold scoring much higher than GroupKFold on such data.

## Learning curves: do I need more data?

`learning_curve` trains on increasing amounts of data:
- train and validation scores **converge at a low value** → underfitting; more data won't help, so use a better model or features;
- a **big gap** that shrinks as data grows → more data **will** help.

## Cross-validation vs the test set

Cross-validation is for **choosing** (models, hyperparameters) using the training data. The test set is for the **final report, once**. Lecture 21 combines both properly.

## Exercises

1. Compare `cv=3`, `cv=5` and `cv=10` for KNN on iris.
2. Score a regressor with `scoring="neg_mean_absolute_error"` and print the positive MAE.
3. Use `cross_validate` with `return_train_score=True` for an unlimited-depth tree. What does the gap tell you?
4. Use `TimeSeriesSplit(n_splits=4)` on 12 rows and print each fold's train/test indices.

**Next →** [Lecture 08: Scaling](../08_scaling/)
