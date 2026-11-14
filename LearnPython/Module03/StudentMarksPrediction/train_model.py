"""
Train a supervised learning model to predict student exam marks.

Run:
    python train_model.py

Input:
    student_marks.csv

Output:
    student_marks_model.joblib
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "student_marks.csv"
MODEL_FILE = BASE_DIR / "student_marks_model.joblib"

FEATURES = ["study_hours", "attendance"]
TARGET = "marks"


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_FILE}")

    data = pd.read_csv(CSV_FILE)

    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")

    data = data[required].apply(pd.to_numeric, errors="coerce").dropna()

    if len(data) < 5:
        raise ValueError("Add at least 5 complete student records.")

    if (data["study_hours"] <= 0).any():
        raise ValueError("Study hours must be greater than zero.")
    if not data["attendance"].between(0, 100).all():
        raise ValueError("Attendance must be between 0 and 100.")
    if not data["marks"].between(0, 100).all():
        raise ValueError("Marks must be between 0 and 100.")

    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions) if len(y_test) >= 2 else float("nan")

    print("\n========== DATASET ==========")
    print(f"Student records used: {len(data)}")
    print(f"Training records:      {len(X_train)}")
    print(f"Testing records:       {len(X_test)}")

    print("\n======= MODEL PERFORMANCE =======")
    print(f"MAE:  {mae:.2f} marks")
    print(f"RMSE: {rmse:.2f} marks")
    print(f"R²:   {r2:.3f}")

    print("\n======= TEST SET COMPARISON =======")
    result = pd.DataFrame({
        "Actual marks": y_test.values,
        "Predicted marks": predictions.round(2),
    }, index=y_test.index)
    print(result.sort_index().to_string())

    joblib.dump(
        {"model": model, "features": FEATURES, "target": TARGET},
        MODEL_FILE,
    )
    print(f"\nTrained model saved as: {MODEL_FILE.name}")
    print("Add labelled records to the CSV and run this script again to retrain.")


if __name__ == "__main__":
    main()
