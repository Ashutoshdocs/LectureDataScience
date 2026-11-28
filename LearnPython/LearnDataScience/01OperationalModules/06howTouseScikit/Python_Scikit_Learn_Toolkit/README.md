# Scikit-learn (sklearn): Complete Machine Learning Teaching Guide

A structured, practical course for teaching **scikit-learn from beginner to advanced**. It explains the machine-learning workflow, core estimator API, preprocessing, supervised and unsupervised learning, model evaluation, pipelines, hyperparameter tuning, and model persistence.

The toolkit includes two complete projects:
1. Customer churn classification.
2. House price regression.

Both projects use included CSV datasets. No external dataset download is required.

---

# Part 1 — Machine Learning and Scikit-learn Foundations

## Chapter 1 — What is Machine Learning?

Machine Learning (ML) is a way to build computer programs that learn patterns from data and use those patterns to make predictions or discover structure.

Examples:
- Predict whether a customer may leave a service.
- Estimate a house price.
- Identify suspicious transactions.
- Group customers with similar behavior.
- Predict equipment failure from sensor measurements.

A model learns relationships from examples. It does not automatically understand the real-world meaning of the data.

## Chapter 2 — What is Scikit-learn?

Scikit-learn, commonly imported as `sklearn`, is a Python library for classical machine learning. It provides consistent tools for:
- Classification.
- Regression.
- Clustering.
- Dimensionality reduction.
- Data preprocessing.
- Feature selection.
- Model evaluation.
- Model selection and hyperparameter tuning.

It works closely with NumPy, SciPy, and Pandas.

Install the package named `scikit-learn`, but import it using `sklearn`.

```bash
python -m pip install scikit-learn
```

Verify:
```bash
python -c "import sklearn; print(sklearn.__version__)"
```

## Chapter 3 — The end-to-end ML workflow

A typical supervised machine-learning workflow:

1. Define the problem.
2. Collect and understand data.
3. Identify the target column.
4. Separate features (`X`) and target (`y`).
5. Split training and testing data.
6. Preprocess the features.
7. Select an algorithm.
8. Train using `fit()`.
9. Predict using `predict()`.
10. Evaluate using suitable metrics.
11. Improve the model using validation and tuning.
12. Save the trained pipeline.
13. Load it for future predictions.
14. Monitor performance after deployment.

The test set should represent data that the model did not use during training or tuning.

## Chapter 4 — Supervised vs Unsupervised Learning

**Supervised learning** uses examples with known target values.

- Classification predicts categories, such as churn / no churn.
- Regression predicts numerical values, such as a house price.

**Unsupervised learning** uses data without a supplied target label.

- Clustering groups similar observations.
- Dimensionality reduction represents data using fewer variables.

## Chapter 5 — Features and Target

- `X` contains input features used to make a prediction.
- `y` contains the target that the model should learn to predict.

```python
X = df[["age", "monthly_charges", "tenure_months"]]
y = df["churn"]
```

For a single target column, `y` is usually a one-dimensional Pandas Series.

Do not include the answer column in `X`. That would cause target leakage.

## Chapter 6 — Train and Test Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42
)
```

- `test_size=0.20`: reserve 20% for testing.
- `random_state=42`: make the split reproducible.
- `stratify=y`: commonly useful for classification to preserve class proportions.

For classification:
```python
train_test_split(X, y, test_size=0.2,
                 random_state=42, stratify=y)
```

For time-series data, do not randomly shuffle observations if that would let future information leak into training. Split chronologically.

## Chapter 7 — The Estimator API

Scikit-learn estimators follow a consistent API.

- `fit(X, y)`: learn from training data.
- `predict(X)`: produce predictions.
- `transform(X)`: transform input data (transformers).
- `fit_transform(X)`: fit a transformer and transform data.
- `predict_proba(X)`: estimate class probabilities when supported.
- `score(X, y)`: estimator-specific default score; understand what it measures.

Example:
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

---

# Part 2 — Data Preparation and Preprocessing

## Chapter 8 — Understanding your dataset with Pandas

```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
print(df.shape)
print(df.info())
print(df.describe(include="all"))
print(df.isna().sum())
print(df.nunique())
```

Check:
- Number of rows and columns.
- Data types.
- Missing values.
- Duplicate rows.
- Category cardinality.
- Outliers and implausible values.
- Whether the target is balanced.

## Chapter 9 — Missing Values

A model generally cannot accept arbitrary missing values unless the selected estimator and configuration explicitly support them.

Common strategies:
- Remove rows only when justified.
- Impute numerical values with median or mean.
- Impute categorical values with the most frequent value or a constant category.

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median")
X_train_filled = imputer.fit_transform(X_train)
X_test_filled = imputer.transform(X_test)
```

Important: fit the imputer on training data only. Apply the learned transformation to test data.

## Chapter 10 — Encoding Categorical Variables

Many estimators require numerical inputs.

One-hot encoding:
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown="ignore")
```

It creates binary columns representing categories.

Ordinal encoding:
```python
from sklearn.preprocessing import OrdinalEncoder
```

Use ordinal encoding only when the categories have a meaningful order or when the model and encoding choice justify it. Arbitrary integer codes can imply a false ranking.

## Chapter 11 — Feature Scaling

Standardization:
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

StandardScaler transforms values using the training mean and standard deviation.

Other choices:
- `MinMaxScaler`: scales to a specified range.
- `RobustScaler`: uses robust statistics such as median and interquartile range.
- `Normalizer`: scales individual samples to unit norm.

Scaling is important for many distance-based and gradient-based methods. Tree-based models generally do not require feature scaling.

## Chapter 12 — Why fit_transform on Train and transform on Test?

Correct:
```python
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

Incorrect:
```python
X_test_scaled = scaler.fit_transform(X_test)
```

The test data must not influence preprocessing parameters. Learning transformations from test data leaks information about the test distribution.

## Chapter 13 — ColumnTransformer

Different columns may require different preprocessing.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_columns),
    ("categorical", categorical_pipeline, categorical_columns),
])
```

`ColumnTransformer` applies the selected pipeline to the specified columns.

## Chapter 14 — Pipelines

A Pipeline combines preprocessing and a model into one estimator.

```python
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

model_pipeline.fit(X_train, y_train)
predictions = model_pipeline.predict(X_test)
```

Benefits:
- Consistent preprocessing for training and prediction.
- Reduces accidental leakage.
- Makes cross-validation and hyperparameter tuning safer.
- Allows saving the entire workflow as one object.

---

# Part 3 — Classification Algorithms

## Chapter 15 — What is Classification?

Classification predicts a discrete category.

Examples:
- Churn: Yes / No.
- Email: Spam / Not spam.
- Ticket: Low / Medium / High priority.
- Image: Cat / Dog / Bird.

The target is categorical.

## Chapter 16 — Logistic Regression

Despite its name, Logistic Regression is a classification algorithm.

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

It estimates class probabilities and uses a decision rule to assign a class. Scaling is often useful.

## Chapter 17 — K-Nearest Neighbors (KNN)

KNN predicts based on nearby training observations.

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

Important:
- `n_neighbors`: number of neighbors.
- Distance metric and weighting affect predictions.
- Scaling is usually important.
- Prediction can be expensive for large training sets.

## Chapter 18 — Decision Tree Classifier

A decision tree learns rules by splitting feature values.

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
```

Trees are interpretable but can overfit. Control complexity using parameters such as `max_depth`, `min_samples_split`, and `min_samples_leaf`.

## Chapter 19 — Random Forest Classifier

Random Forest combines many decision trees trained with randomness in samples and features.

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
```

It often provides a strong baseline for tabular data. More trees can improve stability but increase computation.

## Chapter 20 — Support Vector Machine (SVM)

SVM finds a decision boundary that separates classes with a large margin.

```python
from sklearn.svm import SVC

model = SVC(kernel="rbf", C=1.0)
```

Scaling is generally important. SVMs can be effective for medium-sized datasets but may become costly on very large datasets.

## Chapter 21 — Naive Bayes

Naive Bayes uses Bayes' theorem with conditional independence assumptions.

```python
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
```

Different variants suit different feature types, such as Gaussian, Multinomial, and Bernoulli Naive Bayes.

## Chapter 22 — Classification Metrics

Accuracy:
```python
from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)
```

Precision, recall, F1:
```python
from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))
```

Confusion matrix:
```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, predictions)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
```

- Precision: among predicted positives, how many were correct?
- Recall: among actual positives, how many were found?
- F1: harmonic mean of precision and recall.
- Accuracy: fraction of all predictions that were correct.

For imbalanced data, accuracy alone can be misleading.

## Chapter 23 — ROC-AUC and Probability Scores

Many classifiers support `predict_proba()` or `decision_function()`.

```python
from sklearn.metrics import roc_auc_score

probabilities = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, probabilities)
```

ROC-AUC measures ranking discrimination across thresholds. For heavily imbalanced positive classes, also consider precision-recall curves and average precision.

---

# Part 4 — Regression Algorithms

## Chapter 24 — What is Regression?

Regression predicts a numerical value.

Examples:
- House price.
- Monthly revenue.
- Delivery time.
- Energy consumption.

## Chapter 25 — Linear Regression

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Linear regression models a linear relationship between input features and a numerical target.

## Chapter 26 — Ridge and Lasso Regression

Ridge adds L2 regularization:
```python
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)
```

Lasso adds L1 regularization:
```python
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)
```

Regularization can reduce overfitting. Scaling is generally important when comparing coefficient penalties across features.

## Chapter 27 — Decision Tree Regressor

```python
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(max_depth=6, random_state=42)
```

It learns non-linear splits and can capture interactions, but may overfit without complexity controls.

## Chapter 28 — Random Forest Regressor

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
```

It averages predictions from multiple trees and is a useful non-linear baseline.

## Chapter 29 — Regression Metrics

MAE:
```python
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_test, predictions)
```

MSE and RMSE:
```python
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
```

R-squared:
```python
from sklearn.metrics import r2_score
r2 = r2_score(y_test, predictions)
```

- MAE: average absolute prediction error, in target units.
- MSE: average squared error, penalizes large errors more.
- RMSE: square root of MSE, in target units.
- R²: compares the model with a constant-mean baseline; it can be negative.

Always interpret metrics in the context of the target scale and business cost.

---

# Part 5 — Model Validation and Selection

## Chapter 30 — Cross-Validation

Cross-validation evaluates a model across multiple training/validation splits.

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X_train, y_train,
                         cv=cv, scoring="f1")
print(scores.mean(), scores.std())
```

For regression, `KFold` is commonly used. For classification, stratified splitting helps preserve class proportions.

Do not use the final test set repeatedly to choose models. Keep it for final evaluation.

## Chapter 31 — Hyperparameter vs Parameter

- **Model parameters** are learned during fitting, such as coefficients in linear regression.
- **Hyperparameters** are selected before/during model selection, such as tree depth or number of neighbors.

## Chapter 32 — GridSearchCV

Grid Search tries every specified parameter combination.

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "model__max_depth": [3, 5, 8, None],
    "model__min_samples_leaf": [1, 2, 4],
}

search = GridSearchCV(
    pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1
)
search.fit(X_train, y_train)
print(search.best_params_)
best_model = search.best_estimator_
```

The parameter prefix `model__` refers to the step named `model` in a Pipeline.

## Chapter 33 — RandomizedSearchCV

Randomized Search samples a fixed number of hyperparameter combinations.

```python
from sklearn.model_selection import RandomizedSearchCV

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_distributions,
    n_iter=20,
    cv=5,
    scoring="f1",
    random_state=42,
    n_jobs=-1
)
```

It is useful when the search space is large.

## Chapter 34 — Learning Curves

Learning curves help inspect how model performance changes with training-set size.

```python
from sklearn.model_selection import learning_curve
import numpy as np

sizes, train_scores, valid_scores = learning_curve(
    estimator, X, y, cv=5, scoring="accuracy",
    train_sizes=np.linspace(0.1, 1.0, 5)
)
```

A persistent gap between training and validation performance can indicate overfitting. Poor performance on both can indicate underfitting or weak features.

---

# Part 6 — Unsupervised Learning

## Chapter 35 — What is Clustering?

Clustering groups observations based on similarity without using a supplied target label.

Possible uses:
- Customer segmentation.
- Grouping similar products.
- Exploring behavior patterns.
- Finding unusual groups for further investigation.

Clusters are algorithmic groupings, not automatically meaningful business segments.

## Chapter 36 — K-Means Clustering

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
model = KMeans(n_clusters=3, random_state=42, n_init="auto")
labels = model.fit_predict(X_scaled)
```

K-Means:
- Assigns observations to a chosen number of clusters.
- Uses cluster centroids.
- Is sensitive to scaling and outliers.
- Requires choosing `n_clusters`.

## Chapter 37 — Choosing K with the Elbow Method

```python
inertias = []
for k in range(2, 10):
    model = KMeans(n_clusters=k, random_state=42, n_init="auto")
    model.fit(X_scaled)
    inertias.append(model.inertia_)
```

Plot `inertias` against `k`. An elbow can suggest a useful value, but it is not a guaranteed optimum.

## Chapter 38 — Silhouette Score

```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X_scaled, labels)
```

The score ranges from -1 to 1 for valid cluster assignments:
- Higher values generally indicate better separation.
- Near zero suggests overlapping clusters.
- Negative values can indicate questionable assignments.

Use domain understanding as well as metrics.

## Chapter 39 — DBSCAN

DBSCAN groups dense regions and can label isolated points as noise.

```python
from sklearn.cluster import DBSCAN

model = DBSCAN(eps=0.5, min_samples=5)
labels = model.fit_predict(X_scaled)
```

`eps` and `min_samples` strongly affect results. Scaling and parameter selection matter.

## Chapter 40 — Hierarchical Clustering

Agglomerative clustering repeatedly merges groups.

```python
from sklearn.cluster import AgglomerativeClustering

model = AgglomerativeClustering(n_clusters=3)
labels = model.fit_predict(X_scaled)
```

It can be useful for understanding nested group structures on appropriately sized datasets.

---

# Part 7 — Dimensionality Reduction and Feature Engineering

## Chapter 41 — Principal Component Analysis (PCA)

PCA projects numerical features into a lower-dimensional representation.

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)
```

PCA:
- Finds directions that capture variance.
- Can help visualize high-dimensional data.
- May reduce redundant dimensions.
- Can make original features less directly interpretable.

Fit PCA on training data only in a predictive workflow, preferably inside a Pipeline.

## Chapter 42 — Explained Variance

```python
print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_.sum())
```

The ratio indicates the fraction of variance captured by each component.

## Chapter 43 — Feature Selection

Feature selection chooses a subset of input variables.

Examples:
- `SelectKBest`
- `RFE`
- `SelectFromModel`

```python
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X_train, y_train)
```

Feature selection must be fitted within cross-validation folds to avoid leakage. Put it inside a Pipeline.

## Chapter 44 — Feature Engineering

Feature engineering creates or transforms inputs to make useful patterns easier for a model to learn.

Examples:
- `house_age = current_year - year_built`
- `total_spend = quantity * unit_price`
- Extract month, weekday, or hour from timestamps.
- Group rare categories when justified.
- Create ratios with safe handling of zero denominators.

Feature engineering should use only information available at prediction time.

---

# Part 8 — Model Persistence and Deployment Basics

## Chapter 45 — Save a Trained Model

```python
import joblib
joblib.dump(pipeline, "model.joblib")
```

Save the complete Pipeline rather than only the final estimator when preprocessing is required.

## Chapter 46 — Load a Model and Predict

```python
loaded_model = joblib.load("model.joblib")
new_predictions = loaded_model.predict(new_data)
```

New input data must have the same feature columns and compatible types expected by the pipeline.

Only load model files from trusted sources. Pickle/joblib-based formats can execute code during loading.

## Chapter 47 — Reproducibility

For reproducible experiments:
- Set `random_state` where supported.
- Record package versions.
- Keep data and code versions.
- Store training configuration and evaluation metrics.
- Preserve the test set policy.
- Document feature definitions.

## Chapter 48 — Data Leakage

Data leakage happens when training or model selection receives information that would not legitimately be available at prediction time.

Examples:
- Scaling the full dataset before splitting.
- Imputing using train and test together.
- Including a post-outcome field as a feature.
- Tuning repeatedly against the final test set.
- Using future observations to predict the past.

Use train/test separation and Pipelines to reduce leakage risk.

## Chapter 49 — Imbalanced Classification

When one class is much rarer than another:
- Inspect class counts.
- Use precision, recall, F1, ROC-AUC, and average precision as appropriate.
- Consider `class_weight="balanced"` when supported.
- Tune the decision threshold based on business costs.
- Use stratified splitting.
- Resampling must happen inside each training fold, not before splitting.

Do not judge a rare-event classifier by accuracy alone.

## Chapter 50 — A Practical Model Review Checklist

Before accepting a model:
- Is the target clearly defined?
- Are features available at prediction time?
- Is the split appropriate for the real use case?
- Is preprocessing inside the Pipeline?
- Are metrics appropriate for the problem?
- Is performance compared with a simple baseline?
- Has cross-validation been used appropriately?
- Has the test set remained untouched during tuning?
- Are errors inspected by segment?
- Is the model artifact and environment documented?
- Is there a plan to monitor data and performance drift?

---

# Part 9 — Practical Projects

## Project 1 — Customer Churn Classification

**Goal:** Predict whether a customer will churn based on tenure, service usage, monthly charges, contract type, and support interactions.

Folder: `project_01_customer_churn_classification/`

Run from the repository root:
```bash
pip install -r requirements.txt
python project_01_customer_churn_classification/main.py
```

The project:
- Loads a local CSV dataset.
- Splits features and target.
- Separates numeric and categorical columns.
- Imputes missing values.
- Scales numerical columns and one-hot encodes categorical columns.
- Builds a Pipeline with Logistic Regression.
- Evaluates accuracy, precision, recall, F1, ROC-AUC, and confusion matrix.
- Saves the full pipeline with joblib.
- Writes a metrics report and prediction CSV.

Expected outputs:
- `churn_model.joblib`
- `classification_report.txt`
- `confusion_matrix.png`
- `predictions.csv`
- `metrics.json`

Teaching questions:
1. Which features appear useful for predicting churn?
2. Why can accuracy be misleading if churn is rare?
3. What is the difference between precision and recall?
4. Why is preprocessing placed inside the Pipeline?
5. How would you tune the classification threshold?

## Project 2 — House Price Regression

**Goal:** Predict a property's sale price using area, bedrooms, bathrooms, age, distance to city center, and location category.

Folder: `project_02_house_price_regression/`

Run:
```bash
python project_02_house_price_regression/main.py
```

The project:
- Loads a local CSV dataset.
- Splits training and testing data.
- Imputes missing values.
- Scales numerical columns and one-hot encodes categorical columns.
- Trains Linear Regression and Random Forest Regression pipelines.
- Compares MAE, RMSE, and R².
- Saves the best pipeline and prediction results.
- Creates an actual-versus-predicted plot.

Expected outputs:
- `best_house_price_model.joblib`
- `model_comparison.csv`
- `actual_vs_predicted.png`
- `predictions.csv`

Teaching questions:
1. Which model achieves lower MAE?
2. What does a negative R² mean?
3. Why should location be encoded?
4. Why is the same test set used for comparing both models?
5. What additional features might improve price predictions?

---

# Part 10 — Practice and Assessment

## Beginner exercises
1. Load a CSV using Pandas.
2. Separate `X` and `y`.
3. Split data into train and test.
4. Train Logistic Regression.
5. Train Linear Regression.
6. Calculate accuracy and MAE.

## Intermediate exercises
1. Impute missing numerical values.
2. One-hot encode categorical columns.
3. Build a Pipeline.
4. Build a ColumnTransformer.
5. Evaluate a classifier with a confusion matrix.
6. Compare a Decision Tree and Random Forest.
7. Use cross-validation.

## Advanced exercises
1. Tune a Pipeline with GridSearchCV.
2. Compare ROC-AUC and average precision on imbalanced data.
3. Build a clustering workflow with K-Means.
4. Use PCA to reduce dimensions.
5. Put feature selection inside a Pipeline.
6. Save and reload a complete preprocessing/model Pipeline.
7. Explain and demonstrate data leakage.

## Suggested teaching sequence

| Session | Topics | Practical |
|---|---|---|
| 1 | ML workflow, features, target, train/test | First model |
| 2 | Missing values, encoding, scaling | Preprocessing |
| 3 | Pipelines and ColumnTransformer | End-to-end estimator |
| 4 | Classification algorithms and metrics | Churn baseline |
| 5 | Regression algorithms and metrics | House price baseline |
| 6 | Cross-validation and hyperparameter tuning | GridSearchCV |
| 7 | Clustering, PCA, feature selection | Unsupervised lab |
| 8 | Persistence, leakage, model review | Save/load model |
| 9 | Project 1 | Churn classification |
| 10 | Project 2 | House price regression |

---

# Repository Structure

```text
Python_Scikit_Learn_Toolkit/
├── README.md
├── requirements.txt
├── project_01_customer_churn_classification/
│   ├── README.md
│   ├── main.py
│   ├── data/
│   │   ├── input/customers.csv
│   │   └── reference/feature_dictionary.csv
│   ├── output/
│   └── logs/
└── project_02_house_price_regression/
    ├── README.md
    ├── main.py
    ├── data/
    │   ├── input/houses.csv
    │   └── reference/feature_dictionary.csv
    ├── output/
    └── logs/
```

## Run both projects

From the repository root:
```bash
pip install -r requirements.txt
python project_01_customer_churn_classification/main.py
python project_02_house_price_regression/main.py
```

The scripts resolve input and output paths relative to their own locations, so they do not depend on the terminal's current working directory.
