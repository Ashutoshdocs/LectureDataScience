# Lecture 18: Support vector machines (SVM)

Run: `python lecture.py`

## The idea: the widest street

For two classes, many lines can separate them. An SVM picks the one with the **largest margin**: the widest "street" between the classes. The points touching the edges of the street are the **support vectors**. Only they define the boundary.

```
   o   o        |       x   x
     o      o   |   x     x          ← widest gap
   o    [o]  ...|... [x]    x        [ ] = support vectors
```

## `C`: how strict the street is

Real data overlaps, so some points are allowed inside the street or on the wrong side (a **soft margin**).

| `C` | Behaviour |
|-----|-----------|
| small (0.01) | wide street, tolerates mistakes → simpler, may underfit |
| large (100) | narrow street, tries to classify every training point → may overfit |

(Like logistic regression, C is the **inverse** of regularisation strength.)

## Kernels: curved boundaries

The **kernel trick** lets an SVM draw non-linear boundaries by implicitly mapping the data into a higher-dimensional space where it *is* separable, without ever computing that space.

| `kernel` | Boundary | Extra parameters |
|----------|----------|------------------|
| `"linear"` | straight line / plane | `C` |
| `"rbf"` (default) | smooth curved regions | `C`, **`gamma`** |
| `"poly"` | polynomial curves | `C`, `degree`, `gamma` |
| `"sigmoid"` | rarely used | |

### `gamma` (for rbf): how far each training point's influence reaches

| `gamma` | Effect |
|---------|--------|
| small | each point influences a wide area → smooth boundary (may underfit) |
| large | influence is very local → wiggly boundary around single points (overfits) |
| `"scale"` (default) | `1 / (n_features · X.var())`, a sensible start |

Tune `C` and `gamma` **together** with a grid search on a log scale: `C ∈ {0.1, 1, 10, 100}`, `gamma ∈ {0.001, 0.01, 0.1, 1}`.

## Practical rules

1. **Always scale** (SVMs are distance-based): `make_pipeline(StandardScaler(), SVC())`.
2. `SVC` scales roughly with n² to n³ in the number of samples: fine up to ~10–20k rows. For bigger data use `LinearSVC` or `SGDClassifier(loss="hinge")`.
3. For probabilities, wrap the model: `CalibratedClassifierCV(SVC(), cv=5)` gives `predict_proba`. (`SVC(probability=True)` is deprecated since scikit-learn 1.9.) Otherwise use `decision_function` scores.
4. Regression version: `SVR` (`epsilon` = width of the "no-penalty" tube around predictions).

## When to use

✅ Small-to-medium datasets with many features (text, genomics); clear margins; when RBF captures the shape well.

❌ Very large datasets; when you need fast probabilities or easy interpretation.

## Exercises

1. On `make_moons`, compare the linear, poly and rbf kernels.
2. Grid-search `C` and `gamma` on scaled breast-cancer data.
3. Count support vectors (`n_support_`) for C = 0.01 vs 100. Explain the difference.
4. Use `SVR` on noisy `sin(x)` data with different `epsilon` values.

**Next →** [Lecture 19: Naive Bayes & text classification](../19_naive_bayes_text/)
