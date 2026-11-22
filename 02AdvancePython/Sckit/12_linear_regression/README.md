# Lecture 12: Linear regression

Run: `python lecture.py`

## The model

Linear regression predicts a number as a **weighted sum** of the features plus a constant:

```
ŷ = w₁·x₁ + w₂·x₂ + … + wₙ·xₙ + b
```

| Symbol | scikit-learn attribute | Meaning |
|--------|------------------------|---------|
| w (weights) | `coef_` (one per feature) | how much ŷ changes when that feature rises by 1, **holding the others fixed** |
| b (bias) | `intercept_` | the prediction when every feature is 0 |

## How it learns: least squares

`fit` finds the weights that make the **sum of squared errors** as small as possible:

```
minimise  Σ (yᵢ − ŷᵢ)²
```

There's an exact formula (no iterations, no hyperparameters to tune). Squaring means big errors are punished heavily, and it makes the maths neat.

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train, y_train)
model.coef_, model.intercept_, model.predict(X_new), model.score(X_test, y_test)  # score = R²
```

## Interpreting coefficients

- A coefficient is in **"units of y per unit of x"**: `+5.9` marks per extra hour studied.
- Coefficients of features on **different scales can't be compared** directly. Scale the features first (`StandardScaler`), and the coefficients then mean "change in y per one standard deviation".
- **Correlated features** (area in m² *and* in ft²) make coefficients unstable and hard to read. Ridge regression fixes the instability (Lecture 13).
- Correlation ≠ causation: a coefficient describes the data, not a guaranteed effect of changing x.

## Assumptions (what can go wrong)

| Assumption | If violated | What to do |
|------------|-------------|------------|
| the relationship is (roughly) linear | curved residual pattern, poor R² | `PolynomialFeatures`, splines, log transforms, or a tree model |
| errors have similar spread everywhere | residuals fan out | log-transform y |
| no extreme outliers | the line gets dragged towards them | `HuberRegressor`, `RANSACRegressor`, or clean the data |
| features not near-duplicates | wild, unstable coefficients | Ridge, or drop duplicates |

## Fitting curves while staying "linear"

`PolynomialFeatures` adds `x²`, `x³`… The model is still linear **in its weights**, so least squares still works, but it can now draw curves. High degrees overfit wildly: in `lecture.py` the train R² keeps creeping up with the degree (0.65 → 0.94) while the test R² peaks at degree 5 (0.99) and collapses at degree 15 (0.19).

## When to use linear regression

✅ A fast, interpretable **first baseline** for any regression problem; when relationships are roughly linear; when you must explain the effect of each feature.

❌ Strongly non-linear patterns with many interactions. Try random forests or gradient boosting (Lecture 17).

## Related models

`Ridge`, `Lasso`, `ElasticNet` (penalised, Lecture 13) · `HuberRegressor` (robust to outliers) · `SGDRegressor` (huge datasets) · `TransformedTargetRegressor` (log target, Lecture 11).

## Exercises

1. Fit on two features (hours studied, hours slept) and interpret both coefficients.
2. Add an outlier and compare `LinearRegression` with `HuberRegressor`.
3. Find the polynomial degree with the best **test** R² in the overfitting demo.
4. Standardise the diabetes features and rank them by the absolute size of their coefficients.

**Next →** [Lecture 13: Ridge, Lasso & ElasticNet](../13_regularization_ridge_lasso/)
