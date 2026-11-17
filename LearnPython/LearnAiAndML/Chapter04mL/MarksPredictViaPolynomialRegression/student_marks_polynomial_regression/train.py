"""
train.py - Train a POLYNOMIAL Regression model (degree 3):  study_hours -> final_marks

The model learns one curve:
    final_marks = b0 + b1·x + b2·x² + b3·x³        (x = study_hours)

It also trains a plain straight line on the same data, so you can see
why a curve fits this data better.

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
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

FEATURE = "study_hours"
TARGET = "final_marks"
DEGREE = 3
MODEL_FILE = "model.pkl"


def build_model():
    # Step 1: turn x into [x, x², x³]   Step 2: fit linear regression on those columns
    return make_pipeline(
        PolynomialFeatures(degree=DEGREE, include_bias=False),
        LinearRegression(),
    )


def equation(model):
    lr = model.named_steps["linearregression"]
    b0 = lr.intercept_
    b1, b2, b3 = lr.coef_
    return b0, b1, b2, b3


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "train.csv"
    print(f"\n[1] Loading training data from '{csv_path}' ...")
    df = pd.read_csv(csv_path)
    print(f"    {len(df)} rows loaded.")

    for col in (FEATURE, TARGET):
        if col not in df.columns:
            sys.exit(f"ERROR: training file must have a '{col}' column.")

    X = df[[FEATURE]]
    y = df[TARGET]

    # Hold back 20% of the data to test on students the model hasn't seen
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"[2] Training Polynomial Regression model (degree {DEGREE}) ...")
    model = build_model()
    model.fit(X_train, y_train)

    # A straight line on the same data, for comparison
    line = LinearRegression().fit(X_train, y_train)

    print("[3] Evaluating on unseen test data ...")
    poly_pred = model.predict(X_test)
    line_pred = line.predict(X_test)
    print(f"    {'Model':<22}{'R² score':>10}{'Avg error (MAE)':>18}")
    print(f"    {'Straight line':<22}{r2_score(y_test, line_pred):>10.3f}"
          f"{mean_absolute_error(y_test, line_pred):>12.2f} marks")
    print(f"    {'Polynomial (degree 3)':<22}{r2_score(y_test, poly_pred):>10.3f}"
          f"{mean_absolute_error(y_test, poly_pred):>12.2f} marks")

    # Retrain on ALL data so the saved model uses every example
    model.fit(X, y)
    b0, b1, b2, b3 = equation(model)

    print("\n[4] The curve the model learned:")
    print(f"    final_marks = {b0:.3f} {b1:+.3f}·x {b2:+.3f}·x² {b3:+.4f}·x³")
    print("    (x = study_hours)")

    joblib.dump(
        {"model": model, "x_min": float(X[FEATURE].min()), "x_max": float(X[FEATURE].max())},
        MODEL_FILE,
    )
    print(f"\n[5] Model saved to '{MODEL_FILE}'. Now run:  python predict.py\n")


if __name__ == "__main__":
    main()
