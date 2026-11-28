# Project 1 — Customer Churn Classification

## Run
From the toolkit root:
```bash
pip install -r requirements.txt
python project_01_customer_churn_classification/main.py
```

## Dataset
`data/input/customers.csv` is a synthetic teaching dataset. The target column is `churn` (1 = churn, 0 = retained). It includes numeric and categorical features plus a small number of missing values to demonstrate preprocessing.

## What the script demonstrates
- Train/test split with stratification.
- Numeric and categorical preprocessing.
- SimpleImputer, StandardScaler, OneHotEncoder.
- ColumnTransformer and Pipeline.
- LogisticRegression.
- Classification metrics and confusion matrix.
- Saving the full fitted pipeline with joblib.

## Student tasks
- Compare Logistic Regression with RandomForestClassifier.
- Try `class_weight="balanced"`.
- Tune the probability threshold.
- Add cross-validation and GridSearchCV.
