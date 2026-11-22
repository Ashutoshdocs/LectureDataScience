# Lecture 13: Relational & regression plots

Run: `python lecture.py`

## Relational plots: how do two numeric variables relate?

| Function | Draws | Use |
|----------|-------|-----|
| `scatterplot` | points | relationships, clusters, outliers |
| `lineplot` | lines, **aggregating** repeated x values | trends over time or ordered x |
| `relplot` | figure-level: `kind="scatter"` or `"line"`, with `col` / `row` facets | the same chart per group |

Semantic mappings from Lecture 10 work in all of them: `hue`, `style`, `size`.

### `lineplot` aggregates automatically

If several rows share the same x (e.g. many days in the same week, or several stores per month), `lineplot` draws the **mean** and a **95% confidence band**:

| Parameter | Effect |
|-----------|--------|
| `estimator="mean"` (default), `"median"`, `"sum"`, `None` | how to combine repeated x values (`None` = draw raw values) |
| `errorbar=("ci", 95)`, `"sd"`, `None` | the shaded band |
| `units="store", estimator=None` | one thin line **per unit** instead of an average |
| `markers=True`, `dashes=False` | marker/line style per hue/style |
| `sort=False` | keep the data order (for paths, not time) |

## Regression plots: add a fitted line

| Function | Notes |
|----------|-------|
| `regplot(x=, y=, data=)` | axes-level: scatter + fitted line + 95% CI band |
| `lmplot(...)` | figure-level `regplot`, with `hue`, `col`, `row` |
| `residplot(x=, y=)` | **residuals** (actual − fitted) vs x. A pattern means a straight line is the wrong model |

| `regplot` / `lmplot` option | Effect |
|-----------------------------|--------|
| `order=2` | polynomial fit |
| `lowess=True` | a flexible, locally weighted smooth curve (no straight-line assumption) |
| `logistic=True` | logistic curve for a 0/1 target (needs `statsmodels`) |
| `robust=True` | down-weights outliers (needs `statsmodels`) |
| `ci=None` | no band |
| `x_bins=5` / `x_estimator=np.mean` | summarise many points into binned means |
| `scatter_kws={"alpha": 0.3}`, `line_kws={"color": "red"}` | style the parts |

⚠️ The fitted line is **descriptive**. For real models, coefficients and predictions, use statsmodels or scikit-learn. And remember that correlation is not causation.

## Exercises

1. Plot weekly visits with `lineplot` (several days per week → mean + band), and with `estimator=None, units=...`.
2. Compare `order=1`, `order=2` and `lowess=True` on the curved practice data.
3. Draw a `residplot` for a straight-line fit on curved data and describe the pattern.
4. Use `lmplot(col="time", hue="smoker")` on the restaurant bills: tip vs total bill.

**Next →** [Lecture 14: Matrix & multi-plot grids](../14_seaborn_matrix_and_multiplot/)
