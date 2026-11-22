# Lecture 27: Practice exercises (20, auto-checked)

| File | What it is |
|------|------------|
| `exercises.py` | **Your work.** 20 function stubs. Each docstring says exactly what is tested. |
| `solutions.py` | Reference solutions. Try first! |
| `lecture.py` | The checker. `python lecture.py` tests `solutions.py`; `python lecture.py exercises` tests **your** file. Expected answers are computed independently inside the checker. |

```
python lecture.py exercises
  ✔ 01 iris shapes
  ✘ 08 scale train/test     scaled test (with TRAIN mean/std): got array([[0.]]), expected array([[2.44949]])
  …
  Score: 9 / 20
```

## The exercises

| # | Function | Skill | Lecture |
|---|----------|-------|---------|
| 01 | `iris_shapes()` | loading data, shapes | 02 |
| 02 | `to_column(values)` | `reshape(-1, 1)`: X must be 2-D | 03 |
| 03 | `fit_predict_tree(X, y, X_new)` | create → fit → predict | 01 |
| 04 | `split_data(X, y)` | `train_test_split` with `stratify` | 04 |
| 05 | `accuracy_by_hand(y_true, y_pred)` | what accuracy really is | 05 |
| 06 | `precision_recall(y_true, y_pred)` | precision and recall | 05 |
| 07 | `rmse(y_true, y_pred)` | regression error | 06 |
| 08 | `scale_train_test(X_train, X_test)` | fit on train, transform test (**no leakage**) | 08 |
| 09 | `one_hot(df, column)` | `OneHotEncoder` | 09 |
| 10 | `impute_median(X)` | `SimpleImputer` | 10 |
| 11 | `cv_mean_accuracy(model, X, y)` | `cross_val_score` | 07 |
| 12 | `slope_intercept(x, y)` | `coef_`, `intercept_` | 12 |
| 13 | `make_scaled_knn(k)` | building a `Pipeline` | 20 |
| 14 | `best_k(X, y, ks)` | tuning by CV in a loop | 15, 21 |
| 15 | `count_lasso_zeros(X, y, alpha)` | Lasso sparsity, accessing a pipeline step | 13 |
| 16 | `predict_with_threshold(model, X, t)` | `predict_proba` + custom threshold | 05, 14 |
| 17 | `build_preprocessor(num_cols, cat_cols)` | `ColumnTransformer` with nested pipelines | 20 |
| 18 | `best_C(X, y)` | `GridSearchCV` with `step__param` | 21 |
| 19 | `kmeans_labels(X, k)` | clustering | 22 |
| 20 | `components_for_variance(X, share)` | PCA with a variance fraction | 23 |

## How to practise

1. Do them in order. Each one builds on earlier lectures.
2. Run the checker after each one. Failures show what you returned and what was expected.
3. When you reach 20 / 20, compare with `solutions.py`.
4. Stretch: rewrite 14 using `GridSearchCV`, and 08 using a `Pipeline`.

**Next →** [Lecture 28: Quick revision](../28_quick_revision/)
