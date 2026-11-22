# Lecture 06: Regression metrics

Run: `python lecture.py`

Regression predicts **numbers**, so we measure **how far off** the predictions are.

| Metric | Formula (error = y − ŷ) | Units | Better | Notes |
|--------|-------------------------|-------|--------|-------|
| **MAE**: mean absolute error | mean(\|error\|) | same as y | lower | easy to explain: "off by ₹4.2 lakh on average"; robust to outliers |
| **MSE**: mean squared error | mean(error²) | y² | lower | squares make **big errors count much more**; hard to interpret |
| **RMSE** | √MSE (`root_mean_squared_error`) | same as y | lower | like MAE but punishes large mistakes; RMSE ≥ MAE always |
| **R²** (coefficient of determination) | 1 − SSE / SST | none | higher (max 1) | share of variance explained; 0 = as good as predicting the mean; **can be negative** |
| **MAPE** | mean(\|error\| / \|y\|) | % (as a fraction) | lower | "off by 8% on average"; breaks when y is near 0 |
| **median absolute error** | median(\|error\|) | same as y | lower | very robust to outliers |

`model.score(X, y)` for any regressor returns **R²**.

## How to read R²

| R² | Interpretation |
|----|----------------|
| 1.0 | perfect predictions |
| 0.8 | explains 80% of the variation in y |
| 0.0 | no better than always predicting the average (`DummyRegressor`) |
| < 0 | worse than predicting the average! |

A "good" R² depends on the field: physics experiments might expect 0.99, human behaviour 0.3.

## MAE vs RMSE: which one?

- Use **MAE** when all errors cost roughly in proportion to their size, or when there are outliers.
- Use **RMSE** when big errors are **disproportionately bad** (an energy-demand forecast off by 50% causes a blackout).
- A big gap between RMSE and MAE means **a few large errors**. Go and look at them!

## Residuals: look at your errors

**Residual** = actual − predicted. Healthy residuals are centred on 0 with no pattern. If the errors grow with the prediction size or follow a curve, the model is missing something: try transforming the target (log), adding features, or using a non-linear model.

## Always compare with a baseline

`DummyRegressor(strategy="mean")` predicts the training mean for everyone, which gives R² ≈ 0. Your model's MAE should be clearly lower than the dummy's.

## Exercises

1. Show with a tiny example that one huge error increases RMSE far more than MAE.
2. Compute R² by hand (`1 - ((y - p)**2).sum() / ((y - y.mean())**2).sum()`) and compare with `r2_score`.
3. Make a model that gives negative R² (hint: predict a constant far from the mean).
4. Compare MAE of `LinearRegression` with `DummyRegressor` on the diabetes data.

**Next →** [Lecture 07: Cross-validation](../07_cross_validation/)
