# Lecture 15: K-nearest neighbours (KNN)

Run: `python lecture.py`

## The idea: "you are like your neighbours"

To predict a new point:
1. Measure its **distance** to every training point.
2. Take the **k closest**.
3. **Classification:** majority vote of their labels. **Regression:** average of their values.

There's no real "training": `fit` just **stores** the data (a "lazy learner"). The work happens at prediction time.

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
knn = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
knn.predict(X_new)
knn.kneighbors(X_new)     # distances and indices of the neighbours, useful for explaining predictions
```

## Hyperparameters

| Parameter | Effect | Typical |
|-----------|--------|---------|
| `n_neighbors` (k) | small k → follows noise (overfits); large k → over-smooths (underfits) | 3–15; tune with CV; odd numbers avoid ties for two classes |
| `weights` | `"uniform"`: every neighbour votes equally; `"distance"`: closer neighbours count more | try both |
| `metric` / `p` | `p=2` Euclidean (default), `p=1` Manhattan; also `"cosine"` | Euclidean |
| `algorithm` | `auto`, `kd_tree`, `ball_tree`, `brute`: speed only, not results | `auto` |

## Scaling is essential

KNN is **all about distances**, so unscaled features with big units dominate completely (Lecture 08: wine accuracy 0.69 → 0.95). **Always use `StandardScaler` in a pipeline.**

## The curse of dimensionality

In many dimensions, **all points become roughly equally far apart**, so "nearest" stops meaning much. KNN works best with a **moderate number of meaningful features**. `lecture.py` adds pure-noise features and shows the accuracy dropping. Remedies: feature selection or PCA (Lecture 23).

## Strengths and weaknesses

| ✅ | ❌ |
|----|----|
| simple and intuitive; easy to explain ("these 5 similar customers bought it") | slow predictions on big data (compares with every stored point) |
| naturally multiclass; non-linear boundaries | needs scaling; hurt by irrelevant features |
| no training time; easy to add new data | memory: stores the entire training set |

## When to use

✅ Small-to-medium datasets with a few meaningful numeric features; recommendation-style "find similar items"; quick baselines.

❌ Millions of rows, hundreds of features, or when fast predictions are required.

## Exercises

1. Find the best k (1–30) for scaled wine with cross-validation.
2. Compare `weights="uniform"` and `"distance"` for k = 15.
3. Use `kneighbors` to explain one prediction: which training samples were the neighbours?
4. Use `KNeighborsRegressor` on `y = sin(x)` data with k = 1, 5 and 25.

**Next →** [Lecture 16: Decision trees](../16_decision_trees/)
