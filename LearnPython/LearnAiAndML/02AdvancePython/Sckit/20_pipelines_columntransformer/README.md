# Lecture 20: Pipelines & ColumnTransformer

Run: `python lecture.py`

## Why pipelines?

Without a pipeline you have to remember to fit the imputer, scaler and encoder on training data only, apply them in the same order to test data and to every new prediction, save them all next to the model, and redo them correctly **inside every cross-validation fold**. One slip means data leakage or a crash in production.

A `Pipeline` bundles all the steps into **one estimator**:

```python
from sklearn.pipeline import Pipeline, make_pipeline

pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
    ("model", LogisticRegression()),
])
pipe.fit(X_train, y_train)      # each step: fit_transform → passes result to the next; the last step: fit
pipe.predict(X_test)            # each step: transform → last step: predict
```

| Benefit | Why |
|---------|-----|
| **No leakage** | in `cross_val_score(pipe, ...)` / `GridSearchCV`, preprocessing is re-fit on each training fold only |
| **One object** | fit, predict, score, save and load everything together |
| **Tunable** | grid search can tune any step: `model__C`, `scale__with_mean` |
| **Production-safe** | raw data in, predictions out |

Rules: every step except the last must be a **transformer**. The last can be anything. `make_pipeline(...)` names the steps automatically (lower-case class names).

### Accessing steps

`pipe.named_steps["scale"]`, `pipe["scale"]`, `pipe[-1]` (the last step), `pipe[:-1]` (all preprocessing, as a sub-pipeline). Use `pipe[:-1].transform(X)` to see what the model receives.

## ColumnTransformer: different preprocessing per column

Real tables mix numeric and categorical columns, and each needs different treatment.

```python
from sklearn.compose import ColumnTransformer, make_column_selector

numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore"))])

preprocess = ColumnTransformer([
    ("num", numeric, ["age", "income"]),
    ("cat", categorical, ["city", "plan"]),
], remainder="drop")          # or "passthrough" to keep other columns unchanged

model = Pipeline([("prep", preprocess), ("clf", RandomForestClassifier())])
model.fit(df_train, y_train)  # pass the raw DataFrame!
```

| Feature | Use |
|---------|-----|
| select columns by **name** (DataFrames), index, or boolean mask | `["age", "income"]` |
| `make_column_selector(dtype_include="number")` | pick columns by dtype automatically |
| `remainder="passthrough"` | keep unlisted columns |
| `"drop"` as a transformer | drop specific columns |
| `get_feature_names_out()` | names after transformation: `num__age`, `cat__city_Pune`… |
| `set_output(transform="pandas")` | make transformers return DataFrames (nice for debugging) |

## Other building blocks

| Tool | Does |
|------|------|
| `FeatureUnion` / `make_union` | runs transformers **side by side** on the *same* columns and concatenates the results (e.g. PCA features + selected original features) |
| `TransformedTargetRegressor` | transforms **y** (log) and inverts predictions automatically |
| `FunctionTransformer` | wraps any function as a pipeline step (Lecture 24) |

## Exercises

1. Build the full mixed-data pipeline in `lecture.py` and print `get_feature_names_out()`.
2. Use `make_column_selector` instead of listing column names.
3. Show that the pipeline handles a new row with an unseen city and a missing age.
4. Compare the CV score of scaling outside vs inside the pipeline (Lecture 08's leakage demo).

**Next →** [Lecture 21: Hyperparameter tuning](../21_hyperparameter_tuning/)
