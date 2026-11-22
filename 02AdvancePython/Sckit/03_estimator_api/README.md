# Lecture 03: The estimator API, the heart of scikit-learn

Run: `python lecture.py`

Learn this lecture well and every model, preprocessor and tool in the library will feel familiar.

## Three kinds of objects, one design

| Kind | Has | Examples |
|------|-----|----------|
| **Estimator** | `fit(X, y)` | everything below |
| **Predictor** (model) | `fit`, `predict`, `score`; classifiers also `predict_proba` | `LogisticRegression`, `RandomForestRegressor`, `KMeans` |
| **Transformer** | `fit`, `transform`, `fit_transform` | `StandardScaler`, `OneHotEncoder`, `PCA`, `SimpleImputer` |

| Method | Does | Returns |
|--------|------|---------|
| `fit(X, y)` | learn from data | **the estimator itself** (so you can chain: `Model().fit(X, y).predict(X2)`) |
| `predict(X)` | one answer per row | array of shape `(n_samples,)` |
| `predict_proba(X)` | probability of each class | array of shape `(n_samples, n_classes)`; columns follow `classes_` |
| `score(X, y)` | predict and compare with the truth | **accuracy** for classifiers, **R²** for regressors |
| `transform(X)` | apply what was learned | the transformed X |
| `fit_transform(X)` | `fit` then `transform` in one step | the transformed X (**use on training data only**) |

## Hyperparameters vs learned parameters

| | Hyperparameters | Learned parameters |
|--|-----------------|-------------------|
| who sets them | **you**, in the constructor | **the algorithm**, during `fit` |
| examples | `max_depth=3`, `n_neighbors=5`, `C=1.0` | `coef_`, `intercept_`, `classes_`, `mean_`, `feature_importances_` |
| naming | plain names | **end with an underscore `_`** |
| exist when | always | only **after** `fit` |

```python
model = LogisticRegression(C=0.5)     # hyperparameter
model.fit(X, y)
model.coef_                           # learned (trailing underscore)
```

### Inspecting and changing hyperparameters

| Tool | Use |
|------|-----|
| `print(model)` | shows only the hyperparameters you changed from the defaults |
| `model.get_params()` | dict of every hyperparameter |
| `model.set_params(max_depth=5)` | change them (returns the model) |
| `sklearn.base.clone(model)` | a **fresh, unfitted** copy with the same settings (used by cross-validation and grid search internally) |

## Input rules

1. **X must be 2-D**, even with one feature: `[[50], [80]]` or `arr.reshape(-1, 1)`.
2. One sample is also 2-D: `model.predict([[5.1, 3.5, 1.4, 0.2]])`, or `arr.reshape(1, -1)`.
3. Most models need **numbers** (encode text, Lecture 09) and **no NaNs** (impute, Lecture 10). Some, such as `HistGradientBoosting`, accept NaN natively.
4. If you fit with a DataFrame, scikit-learn remembers `feature_names_in_` and **warns** if you later predict with different columns.

| `reshape` call | Shape | Meaning |
|----------------|-------|---------|
| `a.reshape(-1, 1)` | `(n, 1)` | many samples, one feature |
| `a.reshape(1, -1)` | `(1, n)` | one sample, many features |

## Errors you will meet

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: Expected 2D array, got 1D array` | X is a flat list | `reshape(-1, 1)` / double brackets |
| `NotFittedError` | predict/transform before fit | call `fit` first, on the same object |
| `ValueError: X has 3 features, but ... is expecting 4` | different columns at predict time | use the same preprocessing (pipelines, Lecture 20) |
| `ValueError: could not convert string to float` | text in X | encode it |
| `ValueError: Input X contains NaN` | missing values | impute |

## Exercises

1. Print `get_params()` of a `RandomForestClassifier`. How many hyperparameters does it have?
2. Fit a `StandardScaler` and print `mean_` and `scale_`.
3. Use `clone` on a fitted model and show that the clone is unfitted.
4. Call `predict_proba` on two iris flowers and check that each row sums to 1.

**Next →** [Lecture 04: Train/test split & overfitting](../04_train_test_split_overfitting/)
