# Lecture 14: Logistic regression

Run: `python lecture.py`

## A classifier, despite the name

Logistic regression computes a linear score `z = w·x + b` (like linear regression), then squeezes it through the **sigmoid** curve to get a **probability** between 0 and 1:

```
P(class 1) = 1 / (1 + e^(−z))
z = 0   → 0.5        z = +3 → 0.95        z = −3 → 0.05
```

The **decision boundary** (P = 0.5) is where z = 0: a straight line (or plane) through feature space.

```python
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression().fit(X_train, y_train)
clf.predict(X)            # labels (threshold 0.5)
clf.predict_proba(X)      # [P(class 0), P(class 1)] per row, ordered like clf.classes_
clf.decision_function(X)  # the raw score z
clf.coef_, clf.intercept_
```

## Interpreting coefficients

The coefficients act on the **log-odds**: `exp(coef)` is the **odds ratio**. With `coef = 0.7` for "hours studied", each extra hour multiplies the odds of passing by e^0.7 ≈ 2. Scale the features first if you want to compare coefficients.

## Key hyperparameters

| Parameter | Meaning | Default |
|-----------|---------|---------|
| `C` | **inverse** regularisation strength: small C = strong penalty = simpler model | `1.0` |
| `l1_ratio` | 0 = L2 (Ridge-like), 1 = L1 (Lasso-like, sparse), in between = ElasticNet; needs `solver="saga"` for values above 0 | `0` |
| `solver` | optimisation algorithm: `lbfgs` (default), `liblinear` (small data), `saga` (large data, L1) | `lbfgs` |
| `max_iter` | iteration limit. Raise it if you see `ConvergenceWarning`, **and scale your features** | `100` |
| `class_weight="balanced"` | gives rare classes more weight in the loss | `None` |

> In recent scikit-learn versions the `penalty=` parameter is deprecated. Control the penalty with `C` and `l1_ratio`.

## Multiclass

With 3+ classes, logistic regression uses the **softmax** (multinomial) formulation automatically: one coefficient vector per class, and `predict_proba` returns one probability per class (each row sums to 1).

## Imbalanced classes

On a 95/5 dataset, the model can favour the majority class. Options:
1. `class_weight="balanced"`: up-weights mistakes on the rare class (recall ↑, precision ↓).
2. **Move the threshold** on `predict_proba` (Lecture 05).
3. Judge with recall, F1, PR AUC, **not** accuracy.

## When to use logistic regression

✅ A strong, fast, interpretable **baseline** for any classification task; when you need well-behaved **probabilities**; text classification (with TF-IDF); data where classes are roughly linearly separable.

❌ Strongly non-linear boundaries (add features, or use trees, SVM kernels or boosting).

## Exercises

1. Compute P(pass) by hand with the sigmoid from `coef_` and `intercept_`, and compare it with `predict_proba`.
2. Try `C = 0.001, 1, 1000` on the breast-cancer data. Watch the size of the coefficients and the CV score.
3. Use `class_weight="balanced"` on imbalanced data and compare recall.
4. Fit on iris and print `predict_proba` for one flower of each species.

**Next →** [Lecture 15: K-nearest neighbours](../15_knn/)
