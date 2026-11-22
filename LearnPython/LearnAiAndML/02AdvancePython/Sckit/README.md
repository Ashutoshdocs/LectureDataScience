# scikit-learn: a complete, detailed course

From "what is machine learning?" to tuned, saved, end-to-end pipelines, with two projects, auto-checked exercises and a revision sheet.

Each folder is one lecture:

- `README.md` teaches the lecture: what you need first, **why** the tool exists, **when** to use it, **how** to use it (parameters, attributes, pitfalls), and exercises with solutions.
- `lecture.py` is a runnable demo. Run it with `python lecture.py` and compare the output with the README. Errors that are part of the lesson are caught and printed, so every file runs to the end.

```bash
pip install scikit-learn pandas      # numpy, scipy and joblib come with scikit-learn
python run_all.py                    # runs every lecture; expects "29 of 29 scripts ran successfully"
```

Tested with Python 3.13, scikit-learn 1.9, NumPy 2.5 and pandas 3.0. Everything works offline: only built-in datasets and generated data are used. Every lecture fixes `random_state`, so your numbers should match the READMEs (tiny differences can appear with other library versions).

## Course map

| # | Lecture | You will learn |
|---|---------|----------------|
| **Part 1: Foundations** | | |
| 00 | [Prerequisites & what ML is](00_prerequisites_what_is_ml/) | NumPy/pandas you need, rules vs learning, supervised/unsupervised, the ML workflow |
| 01 | [Your first model](01_first_model/) | create → `fit` → `predict`, samples, features, labels |
| 02 | [Datasets, X and y](02_datasets_X_and_y/) | built-in and generated datasets, shapes, DataFrames, `as_frame` |
| 03 | [The estimator API](03_estimator_api/) | `fit`/`predict`/`score`/`transform`, hyperparameters vs learned `_` attributes, `get_params`, `clone`, the 2-D gotcha |
| **Part 2: Evaluating honestly** | | |
| 04 | [Train/test split & overfitting](04_train_test_split_overfitting/) | `train_test_split`, `stratify`, under- vs overfitting, baselines |
| 05 | [Classification metrics](05_classification_metrics/) | confusion matrix, precision/recall/F1, ROC AUC, thresholds, imbalance |
| 06 | [Regression metrics](06_regression_metrics/) | MAE, MSE, RMSE, R², residuals, MAPE |
| 07 | [Cross-validation](07_cross_validation/) | `KFold`, `StratifiedKFold`, `cross_validate`, `GroupKFold`, `TimeSeriesSplit`, learning curves |
| **Part 3: Preparing data** | | |
| 08 | [Scaling](08_scaling/) | `StandardScaler`, `MinMaxScaler`, `RobustScaler`, data leakage |
| 09 | [Encoding categories](09_encoding_categories/) | `OneHotEncoder`, `OrdinalEncoder`, `LabelEncoder`, unknown and rare categories |
| 10 | [Missing values](10_missing_values/) | `SimpleImputer`, `KNNImputer`, missing indicators |
| 11 | [Feature engineering & selection](11_feature_engineering_selection/) | polynomials, binning, `FunctionTransformer`, `SelectKBest`, `RFE` |
| **Part 4: Models** | | |
| 12 | [Linear regression](12_linear_regression/) | least squares, coefficients, multiple features, polynomial curves |
| 13 | [Ridge, Lasso & ElasticNet](13_regularization_ridge_lasso/) | L1/L2 penalties, `alpha`, feature selection, `RidgeCV` |
| 14 | [Logistic regression](14_logistic_regression/) | probabilities, decision thresholds, `C`, multiclass, `class_weight` |
| 15 | [K-nearest neighbours](15_knn/) | distance, choosing k, weights, the need for scaling |
| 16 | [Decision trees](16_decision_trees/) | splits, Gini, `export_text`, depth control, importances |
| 17 | [Ensembles: forests & boosting](17_ensembles_forests_boosting/) | bagging, random forests, gradient boosting, `HistGradientBoosting`, voting |
| 18 | [Support vector machines](18_svm/) | margins, kernels, `C` and `gamma`, `SVR` |
| 19 | [Naive Bayes & text](19_naive_bayes_text/) | `CountVectorizer`, `TfidfVectorizer`, `MultinomialNB`, spam filter |
| **Part 5: Workflow** | | |
| 20 | [Pipelines & ColumnTransformer](20_pipelines_columntransformer/) | chaining steps, mixed column types, no leakage |
| 21 | [Hyperparameter tuning](21_hyperparameter_tuning/) | `GridSearchCV`, `RandomizedSearchCV`, `step__param`, nested CV |
| 22 | [Clustering](22_clustering/) | `KMeans`, elbow, silhouette, `DBSCAN`, `AgglomerativeClustering` |
| 23 | [PCA](23_pca_dimensionality_reduction/) | components, explained variance, PCA in pipelines |
| 24 | [Saving models & custom transformers](24_saving_and_custom_transformers/) | `joblib`, `BaseEstimator` + `TransformerMixin`, `FunctionTransformer` |
| **Part 6: Putting it together** | | |
| 25 | [Project: house prices (regression)](25_project_house_prices/) | messy mixed data → pipeline → tuning → error analysis |
| 26 | [Project: tumour classifier](26_project_tumour_classifier/) | model comparison → tuning → threshold choice → final report |
| 27 | [Practice exercises](27_practice_exercises/) | 20 auto-checked exercises with solutions |
| 28 | [Quick revision](28_quick_revision/) | cheat sheet, "which model when", and a self-test |

## The one picture to remember

```
 data ─▶ X (2-D features), y (1-D target)
        │
        ├─ train_test_split ─▶ train ───────────────▶ Pipeline(preprocess → model).fit
        │                                                     │  tune with cross-validation
        └──────────────────▶ test (touch ONCE, at the end) ──▶ .predict / .score ─▶ metrics
```
