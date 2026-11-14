"""
Train an employee salary prediction model using multiple linear regression.

Run:
    python train_model.py

Input:
    employee_salary.csv

Output:
    employee_salary_model.joblib
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "employee_salary.csv"
MODEL_FILE = BASE_DIR / "employee_salary_model.joblib"

NUMERIC_FEATURES = ["experience_years"]
CATEGORICAL_FEATURES = ["education_level", "job_title"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "salary_lpa"


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_FILE}")

    data = pd.read_csv(CSV_FILE)

    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    data = data[required].copy()
    data["experience_years"] = pd.to_numeric(
        data["experience_years"], errors="coerce"
    )
    data[TARGET] = pd.to_numeric(data[TARGET], errors="coerce")
    data = data.dropna()

    for column in CATEGORICAL_FEATURES:
        data[column] = data[column].astype(str).str.strip()

    if len(data) < 8:
        raise ValueError("Please provide at least 8 complete employee records.")
    if (data["experience_years"] < 0).any():
        raise ValueError("Experience years cannot be negative.")
    if (data[TARGET] <= 0).any():
        raise ValueError("Salary must be greater than zero.")
    if any((data[column] == "").any() for column in CATEGORICAL_FEATURES):
        raise ValueError("Education level and job title cannot be blank.")

    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("regression", LinearRegression()),
        ]
    )

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions) if len(y_test) >= 2 else float("nan")

    print("\n========== DATASET ==========")
    print(f"Employee records used: {len(data)}")
    print(f"Training records:       {len(X_train)}")
    print(f"Testing records:        {len(X_test)}")
    print(f"Education levels:       {', '.join(sorted(data['education_level'].unique()))}")
    print(f"Job titles:             {', '.join(sorted(data['job_title'].unique()))}")

    print("\n======= MODEL PERFORMANCE =======")
    print(f"MAE:  {mae:.2f} LPA")
    print(f"RMSE: {rmse:.2f} LPA")
    print(f"R²:   {r2:.3f}")

    print("\n======= TEST SET COMPARISON =======")
    comparison = pd.DataFrame(
        {
            "Actual salary (LPA)": y_test.values,
            "Predicted salary (LPA)": predictions.round(2),
        },
        index=y_test.index,
    )
    print(comparison.sort_index().to_string())

    joblib.dump(
        {
            "pipeline": pipeline,
            "features": FEATURES,
            "numeric_features": NUMERIC_FEATURES,
            "categorical_features": CATEGORICAL_FEATURES,
            "education_levels": sorted(data["education_level"].unique().tolist()),
            "job_titles": sorted(data["job_title"].unique().tolist()),
        },
        MODEL_FILE,
    )
    print(f"\nTrained pipeline saved as: {MODEL_FILE.name}")
    print("Add labelled records to the CSV and run this script again to retrain.")


if __name__ == "__main__":
    main()
