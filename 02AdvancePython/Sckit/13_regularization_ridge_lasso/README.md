# Lecture 13: Regularisation: Ridge, Lasso & ElasticNet

Run: `python lecture.py`

## The problem

With many features, polynomial terms, or correlated columns, plain least squares happily uses **huge, wild coefficients** to fit noise. The result is overfitting and coefficients that change completely when the data changes slightly (Lecture 12, sections 5 and 6).

## The idea: penalise big coefficients

Add a cost for large weights to the error being minimised:

| Model | Minimises | Penalty | Effect |
|-------|-----------|---------|--------|
| `LinearRegression` | squared error | none | uses every feature freely |
| `Ridge` | squared error + **α·Σw²** | L2 | shrinks **all** coefficients smoothly towards 0 (never exactly 0); stabilises correlated features |
| `Lasso` | squared error + **α·Σ\|w\|** | L1 | pushes some coefficients to **exactly 0**, which is **automatic feature selection** |
| `ElasticNet` | both, mixed by `l1_ratio` | L1 + L2 | selection like Lasso, stability like Ridge for correlated groups |

## `alpha`: the strength knob

| `alpha` | Behaviour |
|---------|-----------|
| 0 | same as `LinearRegression` |
| small | mild shrinking |
| large | strong shrinking → underfitting (all coefficients near 0 → predicts roughly the mean) |

`lecture.py` prints a table of coefficients as alpha grows, and counts how many Lasso sets to zero.

> In `LogisticRegression` and `SVC`, the knob is **`C = 1/strength`**: a *small* C means a *strong* penalty, the opposite direction to alpha.

## Scaling is required

The penalty compares coefficient **sizes**. A feature measured in rupees gets a tiny coefficient and one in lakhs a large one, so the penalty would treat them unfairly. **Always put a `StandardScaler` before Ridge, Lasso or ElasticNet.**

## Choosing alpha automatically

`RidgeCV(alphas=[...])`, `LassoCV(cv=5)` and `ElasticNetCV(l1_ratio=[...])` try many alphas with built-in cross-validation and store the winner in `alpha_`. You can also use `GridSearchCV` (Lecture 21).

## When to use which

| Situation | Choose |
|-----------|--------|
| many useful, correlated features | **Ridge** |
| you suspect only a few features matter, or you want a sparse, explainable model | **Lasso** |
| many correlated features **and** you want selection | **ElasticNet** |
| more features than samples (genetics, text) | Ridge / Lasso / ElasticNet, never plain least squares |

## Exercises

1. Plot (print) Ridge coefficients for alphas 0.01 → 1000 and describe what happens.
2. Use `LassoCV` on the diabetes data. Which features survive?
3. Fit a degree-12 polynomial with and without Ridge and compare the test R².
4. Show that Lasso without scaling selects different features than with scaling.

**Next →** [Lecture 14: Logistic regression](../14_logistic_regression/)
