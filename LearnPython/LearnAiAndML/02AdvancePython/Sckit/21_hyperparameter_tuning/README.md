# Lecture 21: Hyperparameter tuning

Run: `python lecture.py`

## What we're tuning

**Hyperparameters** are the settings you choose before training (`max_depth`, `C`, `n_neighbors`, `learning_rate`…). Good values depend on the data, so we **search** for them and judge each candidate with **cross-validation on the training set**. The test set stays untouched until the end.

## `GridSearchCV`: try every combination

```python
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([("scale", StandardScaler()), ("svc", SVC())])
param_grid = {
    "svc__C": [0.1, 1, 10, 100],
    "svc__gamma": [0.001, 0.01, 0.1],
}
search = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
search.fit(X_train, y_train)          # 4 × 3 = 12 combinations × 5 folds = 60 fits
```

### The double-underscore rule

`stepname__parameter` reaches inside a pipeline: `svc__C` = "parameter `C` of the step called `svc`". It also goes deeper: `prep__num__impute__strategy`.

You can even search over **whole steps**: `{"scale": [StandardScaler(), MinMaxScaler(), "passthrough"]}`, or over a **list of grids** for different models.

### What you get back

| Attribute | Contains |
|-----------|----------|
| `best_params_` | the winning combination |
| `best_score_` | its mean CV score |
| `best_estimator_` | a pipeline **re-fitted on the whole training set** with the best settings (`refit=True`, the default) |
| `cv_results_` | every candidate's scores. Load it with `pd.DataFrame(search.cv_results_)` |
| `search.predict(X)` / `search.score(X, y)` | use the best estimator directly |

## `RandomizedSearchCV`: sample instead of trying everything

Grids explode: 5 parameters × 10 values = 100,000 combinations. Random search tries `n_iter` random combinations from **distributions**:

```python
from scipy.stats import loguniform, randint
params = {"clf__C": loguniform(1e-3, 1e3), "clf__max_depth": randint(2, 20)}
RandomizedSearchCV(pipe, params, n_iter=40, cv=5, random_state=0)
```

It's usually **as good as a grid in far fewer fits**, because typically only a few hyperparameters really matter, and random sampling explores each of them at many values.

| Distribution | For |
|--------------|-----|
| `loguniform(a, b)` | scale-type parameters spanning orders of magnitude: `C`, `alpha`, `learning_rate`, `gamma` |
| `randint(a, b)` | integers: `max_depth`, `n_neighbors` |
| a plain list | categorical choices: `["uniform", "distance"]` |

`HalvingGridSearchCV` / `HalvingRandomSearchCV` (experimental) give all candidates a little data, then keep only the best for more rounds, which is faster on big searches.

## Avoiding fooling yourself

- `best_score_` is **slightly optimistic**: you chose the maximum of many noisy scores.
- For an honest estimate, either (a) evaluate `best_estimator_` **once** on a held-out test set, or (b) use **nested cross-validation**: an outer CV loop around the whole search (`cross_val_score(GridSearchCV(...), X, y)`).
- If the best value sits at the **edge** of your grid (e.g. the largest C), extend the grid in that direction.
- Search on a **log scale** for C, alpha, gamma and learning rates: `[0.001, 0.01, 0.1, 1, 10]`.

## A sensible tuning workflow

1. Start with defaults and a baseline.
2. Coarse random search over wide ranges.
3. Narrower grid around the best region.
4. Check that the best params aren't on the edge.
5. Final evaluation on the test set, once.

## Exercises

1. Grid-search `n_neighbors` (1–30) and `weights` for scaled KNN on wine.
2. Use `RandomizedSearchCV` with `loguniform` for logistic regression's `C`.
3. Put the result of `cv_results_` in a DataFrame and show the top 5 candidates.
4. Run nested CV and compare it with `best_score_`.

**Next →** [Lecture 22: Clustering](../22_clustering/)
