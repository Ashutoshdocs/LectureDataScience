# Lecture 24: Saving models & writing custom transformers

Run: `python lecture.py`

## Part 1: Saving and loading

Training can take minutes or hours, so you train once, **save** the fitted model, and **load** it wherever predictions are needed: a web API, a batch script, another notebook.

```python
import joblib
joblib.dump(pipeline, "model.joblib")          # save the WHOLE fitted pipeline
model = joblib.load("model.joblib")            # later, elsewhere
model.predict(new_raw_data)
```

| Rule | Why |
|------|-----|
| **Save the whole pipeline**, not just the final model | the imputer, encoder and scaler are part of the model; without them new data can't be prepared the same way |
| Load with the **same scikit-learn version** (and Python, NumPy) | pickled internals can change between versions; record versions next to the file |
| **Only load files you trust** | loading a pickle/joblib file can **execute arbitrary code** |
| Store metadata | training date, data version, feature names, CV score, library versions (a small JSON next to the model) |
| `compress=3` | smaller files |

Alternatives: the `pickle` module (same idea), **skops** (`skops.io`, a safer format that lets you inspect the file before loading), and **ONNX** (`skl2onnx`, to run models outside Python).

## Part 2: Custom transformers

Sometimes you need a preprocessing step scikit-learn doesn't have: domain features, clipping outliers, extracting date parts, ratios. Putting it **inside the pipeline** keeps the benefits: no leakage, one object to save, tunable.

### Option A: `FunctionTransformer` (stateless steps)

When the step **learns nothing** from the data (log, ratio, date parts):

```python
from sklearn.preprocessing import FunctionTransformer

def add_ratio(df):
    df = df.copy()
    df["price_per_m2"] = df["price"] / df["area"]
    return df

pipe = make_pipeline(FunctionTransformer(add_ratio), ...)
```

Use `feature_names_out="one-to-one"` or a callable if you need `get_feature_names_out`. Named module-level functions save fine with joblib; **lambdas don't**.

### Option B: a class (steps that learn something during `fit`)

```python
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, lower=0.01, upper=0.99):     # 1. only store the arguments, unchanged
        self.lower = lower
        self.upper = upper

    def fit(self, X, y=None):                        # 2. learn from training data; set attributes ending in _
        X = np.asarray(X, dtype=float)
        self.low_ = np.quantile(X, self.lower, axis=0)
        self.high_ = np.quantile(X, self.upper, axis=0)
        self.n_features_in_ = X.shape[1]
        return self                                  # 3. always return self

    def transform(self, X):                          # 4. apply what was learned; never re-learn here
        check_is_fitted(self)
        return np.clip(np.asarray(X, dtype=float), self.low_, self.high_)
```

| Piece | What it gives you |
|-------|-------------------|
| `BaseEstimator` | `get_params` / `set_params` (from the `__init__` arguments), a nice `repr`, so the class works with `clone`, `GridSearchCV` and cross-validation |
| `TransformerMixin` | a free `fit_transform` = `fit(...).transform(...)` |
| `ClassifierMixin` / `RegressorMixin` | a free `score` (accuracy / R²) for custom models |

### The rules that keep it compatible

1. `__init__` **only assigns** each argument to an attribute **of the same name**. No validation, no computation there.
2. `fit` learns, sets attributes ending in `_`, and **returns `self`**.
3. `transform` uses only what `fit` learned. It must never look at the test data's statistics.
4. Use `check_is_fitted(self)` to give a clear `NotFittedError`.
5. Implement `get_feature_names_out` if you want names to flow through `ColumnTransformer`.

`sklearn.utils.estimator_checks.check_estimator` runs scikit-learn's full compatibility test suite on your class.

## Exercises

1. Save a tuned pipeline, load it in a fresh script, and predict on a new DataFrame.
2. Write a `FunctionTransformer` that extracts `month` and `dayofweek` from a date column.
3. Write a `TopCategoryKeeper(top_n=3)` transformer that replaces rare categories with `"other"`, learning the top categories in `fit`.
4. Tune your custom transformer's parameter with `GridSearchCV`.

**Next →** [Lecture 25: Project: house prices](../25_project_house_prices/)
