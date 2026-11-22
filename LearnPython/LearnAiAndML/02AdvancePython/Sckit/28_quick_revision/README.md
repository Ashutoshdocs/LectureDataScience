# Lecture 28: Quick revision: scikit-learn on one page

Run: `python lecture.py` for a 25-question self-test. Every answer is produced by running real code.

## 1. The API (every object)

```python
model = SomeModel(hyper=...)        # hyperparameters only
model.fit(X_train, y_train)         # learns → attributes ending in _ (coef_, classes_, mean_)
model.predict(X_new)                # labels / numbers
model.predict_proba(X_new)          # classifiers: probabilities, columns follow classes_
model.score(X_test, y_test)         # accuracy (classifiers) or R² (regressors)
transformer.fit_transform(X_train)  # transformers: learn + apply
transformer.transform(X_test)       # apply only, NEVER re-fit on test data
```

X is **2-D** `(n_samples, n_features)`; y is **1-D**. `reshape(-1, 1)` for one feature. `get_params`, `set_params`, `clone`.

## 2. Honest evaluation

```python
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
cross_val_score(pipe, X_tr, y_tr, cv=5, scoring="f1")
```

| Overfitting | train ≫ test → simplify / regularise / more data |
|---|---|
| **Underfitting** | both low → more complex model, better features |
| **Baseline** | `DummyClassifier` / `DummyRegressor`: you must beat it |
| **Leakage** | anything fitted on data that includes the test fold. **Use pipelines** |
| **Splitters** | `StratifiedKFold` (classes), `GroupKFold` (repeated entities), `TimeSeriesSplit` (time) |

## 3. Metrics

| Classification | Regression |
|----------------|------------|
| confusion matrix (rows = truth) | MAE (robust, in units) |
| precision = TP/(TP+FP): false alarms | RMSE (punishes big errors) |
| recall = TP/(TP+FN): misses | R² (1 = perfect, 0 = the mean, can be < 0) |
| F1, ROC AUC (threshold-free), PR AUC (imbalance) | MAPE (% error) |

Move the **threshold** on `predict_proba` to trade precision against recall. Choose it on training/validation data.

## 4. Preprocessing

| Problem | Tool |
|---------|------|
| different units | `StandardScaler` (default), `MinMaxScaler`, `RobustScaler` (outliers) |
| nominal categories | `OneHotEncoder(handle_unknown="ignore")` |
| ordered categories | `OrdinalEncoder(categories=[[...]])` |
| missing values | `SimpleImputer(strategy="median", add_indicator=True)`, `KNNImputer` |
| curves, interactions | `PolynomialFeatures`, `SplineTransformer` |
| skewed target | `TransformedTargetRegressor(func=np.log1p, inverse_func=np.expm1)` |
| too many features | `SelectKBest`, `SelectFromModel`, `RFE`, `PCA` |
| text | `TfidfVectorizer(ngram_range=(1, 2))` |
| mixed column types | `ColumnTransformer` |

## 5. Models: which one when?

| Model | Task | Scale? | Key hyperparameters | Use when |
|-------|------|--------|---------------------|----------|
| `LinearRegression` | reg | no* | none | baseline, interpretable |
| `Ridge` / `Lasso` / `ElasticNet` | reg | **yes** | `alpha`, `l1_ratio` | many/correlated features; Lasso = selection |
| `LogisticRegression` | clf | **yes** | `C`, `class_weight` | baseline classifier, probabilities, text |
| `KNeighbors*` | both | **yes** | `n_neighbors`, `weights` | small data, few features |
| `DecisionTree*` | both | no | `max_depth`, `min_samples_leaf`, `ccp_alpha` | explainable rules |
| `RandomForest*` | both | no | `n_estimators`, `max_features`, `min_samples_leaf` | strong default for tables |
| `HistGradientBoosting*` | both | no | `learning_rate`, `max_iter`, `max_leaf_nodes` | often the best on tables; handles NaN |
| `SVC` / `SVR` | both | **yes** | `C`, `gamma`, `kernel` | small/medium data, clear margins |
| `MultinomialNB` | clf | no | `alpha` | text, very fast baseline |
| `KMeans` | cluster | **yes** | `n_clusters` | round groups |
| `DBSCAN` | cluster | **yes** | `eps`, `min_samples` | any shape, outliers |
| `PCA` | reduce | **yes** | `n_components` | visualise, compress |

\* scaling doesn't change LinearRegression's predictions, but it makes the coefficients comparable.

**Strategy:** baseline → logistic/ridge → random forest → gradient boosting → tune the winner.

## 6. Pipelines & tuning

```python
pre = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), num_cols),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)])
pipe = Pipeline([("prep", pre), ("clf", RandomForestClassifier(random_state=0))])
search = RandomizedSearchCV(pipe, {"clf__max_depth": randint(2, 20)}, n_iter=20, cv=5)
search.fit(X_train, y_train); search.best_params_; search.score(X_test, y_test)
joblib.dump(search.best_estimator_, "model.joblib")
```

- `step__param` with a **double underscore**; search on log scales; check that the best value isn't on the grid's edge.
- `best_score_` is optimistic, so confirm with nested CV or the test set (once).

## 7. The ten commandments

1. Split before you look at the test set.
2. Fit every learned step on training data only, using pipelines.
3. Beat a dummy baseline.
4. Pick metrics that match the real cost of errors.
5. Use cross-validation, not one lucky split.
6. Scale for distance-, gradient- and penalty-based models.
7. Encode categories with encoders, not `get_dummies`, inside models.
8. Start simple; add complexity only when it clearly helps.
9. Use the test set once, at the very end.
10. Save the whole pipeline, plus versions and metadata.

← [Back to course map](../README.md)
