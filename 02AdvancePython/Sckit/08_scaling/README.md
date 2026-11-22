# Lecture 08: Feature scaling

Run: `python lecture.py`

## Why scale?

Imagine two features: **age** (20–60) and **salary** (₹20,000–₹2,00,000). For a model that measures **distance** (KNN, SVM, k-means) or takes **gradient steps** (logistic regression, linear models with penalties, neural nets), a salary difference of 1,000 completely drowns an age difference of 30 years. The model is not "learning" that salary matters more. It's a side effect of the **units**.

`lecture.py` shows KNN on the wine data jumping from about **0.69 to about 0.95** accuracy just by scaling.

## The scalers

| Scaler | Formula | Result | Use when |
|--------|---------|--------|----------|
| `StandardScaler` | (x − mean) / std | mean 0, std 1 | **the default** for most models |
| `MinMaxScaler` | (x − min) / (max − min) | range [0, 1] on the training data | you need a bounded range: pixels, neural nets |
| `RobustScaler` | (x − median) / IQR | centred on the median | data with **outliers** |
| `MaxAbsScaler` | x / max(\|x\|) | range [−1, 1], keeps zeros | **sparse** data (text) |
| `Normalizer` | each **row** to unit length | | text / cosine similarity. ⚠️ works on rows, not columns |

## Which models need scaling?

| Need scaling ✅ | Don't care ❌ |
|-----------------|--------------|
| KNN, SVM, k-means, PCA | decision trees |
| logistic regression, Ridge/Lasso (penalties compare coefficient sizes) | random forests, gradient boosting |
| neural networks (MLP) | Naive Bayes (mostly) |

Trees split one feature at a time on thresholds, so multiplying a column by 1,000 changes nothing.

## The golden rule: fit on train, transform test

```python
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)   # LEARN mean/std from training data only
X_test_s  = scaler.transform(X_test)        # APPLY the same numbers to the test data
```

| ❌ Data leakage | Why it's wrong |
|----------------|----------------|
| `scaler.fit(X_all)` before splitting | test-set statistics leak into training, so scores are optimistic |
| `scaler.fit_transform(X_test)` | test data is scaled with *different* numbers than the model was trained on |

New data in production is transformed with the **training** statistics too, which is why you save the scaler with the model. **Pipelines (Lecture 20) make this automatic**, including inside cross-validation.

Test values *can* fall outside the training range (e.g. 2.45 standard deviations, or MinMax above 1). That's normal: the same formula is applied.

## Learned attributes

| Scaler | Attributes |
|--------|------------|
| `StandardScaler` | `mean_`, `scale_` (std), `var_` |
| `MinMaxScaler` | `data_min_`, `data_max_`, `scale_` |
| `RobustScaler` | `center_` (median), `scale_` (IQR) |

`inverse_transform` converts scaled values back to original units.

## Exercises

1. Add an outlier (salary 5,000,000) and compare the three scalers' outputs.
2. Show that a `DecisionTreeClassifier` gets the same accuracy with and without scaling.
3. Use `inverse_transform` to recover the original values.
4. Demonstrate leakage: fit the scaler on all data vs train only, and compare cross-validated scores.

**Next →** [Lecture 09: Encoding categories](../09_encoding_categories/)
