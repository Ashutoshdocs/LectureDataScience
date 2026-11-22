# Lecture 11: Feature engineering & feature selection

Run: `python lecture.py`

> "Better features beat better algorithms." Good features often matter more than the choice of model.

## Feature engineering: create useful inputs

| Technique | Tool | Example |
|-----------|------|---------|
| **Polynomial / interaction terms** | `PolynomialFeatures(degree=2)` | `[a, b]` → `[a, b, a², ab, b²]`, so linear models can fit curves and interactions |
| **Binning** (discretising) | `KBinsDiscretizer(n_bins, encode, strategy)` | age → age groups |
| **Custom functions** | `FunctionTransformer(np.log1p)` | log of skewed amounts; ratios |
| **Splines** | `SplineTransformer` | smooth curves without wild polynomials |
| **Domain features** | pandas, before modelling | `price_per_m2 = price / area`, `day_of_week`, `is_weekend` |
| **Date parts** | pandas `.dt.month`, `.dt.dayofweek` | seasonality |

### `PolynomialFeatures`

```python
PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
```
- `include_bias=False` drops the column of 1s (linear models already have an intercept).
- `interaction_only=True` keeps only products like `ab`, not squares.
- The number of features **explodes**: 10 features at degree 3 gives 285 columns. Combine with regularisation (Ridge, Lecture 13).

### Skewed targets or features

Prices and incomes are usually right-skewed. `np.log1p` makes them more symmetric, which helps linear models. For the **target**, use `TransformedTargetRegressor(regressor=..., func=np.log1p, inverse_func=np.expm1)` so predictions come back in original units automatically.

## Feature selection: keep what matters

Why remove features? **Less overfitting**, **faster** models, **simpler** explanations, and lower data-collection costs.

| Method | Tool | How it decides |
|--------|------|----------------|
| **Variance threshold** | `VarianceThreshold(threshold=0)` | drops constant / near-constant columns |
| **Univariate statistics** | `SelectKBest(score_func=f_classif, k=10)` | tests each feature alone: `f_classif`, `chi2`, `mutual_info_classif`, `f_regression` |
| **Model-based** | `SelectFromModel(Lasso / RandomForest)` | keeps features with large coefficients or importances |
| **Recursive elimination** | `RFE(estimator, n_features_to_select)`, `RFECV` | repeatedly fits and drops the weakest feature |
| **Permutation importance** | `sklearn.inspection.permutation_importance` | how much the score drops when a feature is shuffled; model-agnostic and computed on **test** data |

> Honest result from `lecture.py`: on the breast-cancer data, keeping **all 30** features scores best (0.981) and 5 features score 0.949. Selection trades a little accuracy for a much simpler model. Always measure; don't assume fewer features is better.

All selectors have `get_support()` (a boolean mask) and `get_feature_names_out()`.

> ⚠️ **Selection must happen inside cross-validation / a pipeline.** Selecting features using all the labels and *then* cross-validating leaks information. Lecture 08 showed pure noise scoring well that way.

## Exercises

1. Fit `LinearRegression` on `y = x²` data with and without `PolynomialFeatures`.
2. Bin ages into 4 equal-width groups with `KBinsDiscretizer(encode="ordinal", strategy="uniform")`.
3. Use `SelectKBest(k=5)` on the breast-cancer data and print the chosen feature names.
4. Compare the top-5 features by `RandomForest.feature_importances_` and by `permutation_importance`.

**Next →** [Lecture 12: Linear regression](../12_linear_regression/)
