"""
train.py - Train a Linear Regression model to predict student final marks.

Usage:
    python train.py                  # uses train.csv
    python train.py my_data.csv      # uses your own training file

Output:
    model.pkl  - the trained model (used by predict.py)
"""
import sys

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

FEATURES = [
    "study_hours",
    "attendance_percent",
    "previous_marks",
    "assignments_completed",
    "sleep_hours",
]
TARGET = "final_marks"
MODEL_FILE = "model.pkl"


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "train.csv"
    print(f"\n[1] Loading training data from '{csv_path}' ...")
    df = pd.read_csv(csv_path)
    print(f"    {len(df)} rows loaded.")

    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: training file is missing columns: {missing}")

    X = df[FEATURES]
    y = df[TARGET]

    # Hold back 20% of the data to check how well the model generalises
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("[2] Training Linear Regression model ...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("[3] Evaluating on unseen test data ...")
    y_pred = model.predict(X_test)
    print(f"    R² score            : {r2_score(y_test, y_pred):.3f}  (1.0 = perfect)")
    print(f"    Mean Absolute Error : {mean_absolute_error(y_test, y_pred):.2f} marks")

    print("\n[4] What the model learned (the equation):")
    print(f"    final_marks = {model.intercept_:.2f}")
    for name, coef in zip(FEATURES, model.coef_):
        print(f"                  {coef:+.3f} × {name}")

    # Retrain on ALL data so the saved model uses every example
    model.fit(X, y)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_FILE)
    print(f"\n[5] Model saved to '{MODEL_FILE}'. Now run:  python predict.py\n")


if __name__ == "__main__":
    main()
