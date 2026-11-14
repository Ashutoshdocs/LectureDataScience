"""
Train a supervised learning regression model for house price prediction.

Run:
    python train_model.py

Input:
    house_prices.csv

Output:
    house_price_model.joblib
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "house_prices.csv"
MODEL_FILE = BASE_DIR / "house_price_model.joblib"

FEATURES = ["area_sqft", "bedrooms"]
TARGET = "price_lakh"


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_FILE}")

    data = pd.read_csv(CSV_FILE)

    required_columns = FEATURES + [TARGET]
    missing = [column for column in required_columns if column not in data.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    data = data[required_columns].apply(pd.to_numeric, errors="coerce").dropna()

    if len(data) < 5:
        raise ValueError("Please provide at least 5 complete labelled rows.")
    if (data[FEATURES] <= 0).any().any():
        raise ValueError("Area and bedroom values must be greater than zero.")
    if (data[TARGET] <= 0).any():
        raise ValueError("House prices must be greater than zero.")

    X = data[FEATURES]
    y = data[TARGET]

    # Keep a fixed random_state so repeated runs use a reproducible split
    # when the dataset row count and ordering are unchanged.
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
    print(f"Rows used: {len(data)}")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows:  {len(X_test)}")

    print("\n======= MODEL PERFORMANCE =======")
    print(f"MAE:  {mae:.2f} lakh")
    print(f"RMSE: {rmse:.2f} lakh")
    print(f"R²:   {r2:.3f}")

    print("\n======= SAMPLE TEST RESULTS =======")
    comparison = pd.DataFrame({
        "Actual price (lakh)": y_test.values,
        "Predicted price (lakh)": predictions.round(2),
    }, index=y_test.index)
    print(comparison.sort_index().to_string())

    # Save both the fitted estimator and the feature order.
    joblib.dump(
        {"model": model, "features": FEATURES, "target": TARGET},
        MODEL_FILE,
    )
    print(f"\nModel saved to: {MODEL_FILE.name}")
    print("If you add labelled rows to the CSV, run this script again to retrain.")


if __name__ == "__main__":
    main()
