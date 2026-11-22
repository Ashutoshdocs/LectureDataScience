# Lecture 10: Missing values

Run: `python lecture.py`

## Why it matters

Real data has gaps: unanswered survey questions, broken sensors, optional form fields. Most scikit-learn models raise `ValueError: Input X contains NaN`. Exceptions such as `HistGradientBoosting*` and decision trees (since 1.3) handle NaN natively.

## First, look

```python
df.isna().sum()                 # count per column
df.isna().mean()                # share per column
```

Ask **why** values are missing. "Income not given" can itself be informative: wealthy people skip that question more often. That's what **missing indicators** capture.

## Options

| Approach | How | When |
|----------|-----|------|
| drop rows | `df.dropna()` | very few rows affected, missing at random. ⚠️ you can't drop rows at prediction time! |
| drop columns | `df.drop(columns=...)` | a column is mostly empty (> 50–70%) |
| **impute** (fill) | `SimpleImputer`, `KNNImputer`, `IterativeImputer` | the usual choice |
| use a NaN-aware model | `HistGradientBoostingClassifier` | tabular data, quick strong baseline |

## `SimpleImputer`

```python
SimpleImputer(strategy="median", add_indicator=True)
```

| `strategy` | Fills with | Good for |
|------------|------------|----------|
| `"mean"` | column average | numbers without big outliers |
| `"median"` | middle value | numbers **with** outliers (incomes, prices) |
| `"most_frequent"` | the most common value | categories, small integers |
| `"constant"` (+ `fill_value`) | a value you choose | categories → `"missing"`; counts → 0 |

- `statistics_` stores the learned fill value per column.
- `add_indicator=True` appends a 0/1 column "was missing" for every column that had gaps, so the model can learn from missingness itself.
- Like scalers, imputers must be **fit on training data only**, so put them in a pipeline.
- `missing_values` can be set to `-1`, `""` or `"?"` if your data uses a placeholder instead of NaN.

## `KNNImputer`

Fills a gap using the average of the **k most similar rows** (similarity measured on the non-missing features). It's often more accurate than a single column mean, but slower, and it needs scaled numeric data.

## `IterativeImputer` (experimental)

Models each feature with missing values as a function of the others, round after round. It needs `from sklearn.experimental import enable_iterative_imputer`. It's powerful but slower, and it can overfit.

## Categorical columns

Use `SimpleImputer(strategy="most_frequent")` or `strategy="constant", fill_value="missing"`, then one-hot encode. The "missing" category becomes its own column.

## Exercises

1. Compare `mean` and `median` imputation on a salary column with one huge outlier.
2. Use `add_indicator=True` and print the new feature names.
3. Fill a categorical column with `"missing"` and one-hot encode it.
4. Compare cross-validated scores of mean imputation vs `HistGradientBoostingClassifier` with raw NaNs.

**Next →** [Lecture 11: Feature engineering & selection](../11_feature_engineering_selection/)
