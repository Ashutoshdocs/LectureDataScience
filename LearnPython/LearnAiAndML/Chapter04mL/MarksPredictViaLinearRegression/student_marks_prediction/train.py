"""
train.py - Train a SIMPLE Linear Regression model:  study_hours -> final_marks

The model learns one straight line:   final_marks = m × study_hours + c

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

FEATURE = "study_hours"
TARGET = "final_marks"
MODEL_FILE = "model.pkl"


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "train.csv"
    print(f"\n[1] Loading training data from '{csv_path}' ...")
    df = pd.read_csv(csv_path)
    print(f"    {len(df)} rows loaded.")

    for col in (FEATURE, TARGET):
        if col not in df.columns:
            sys.exit(f"ERROR: training file must have a '{col}' column.")

    X = df[[FEATURE]]   # one input column
    y = df[TARGET]      # output column

    # Hold back 20% of the data to test the model on students it hasn't seen
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

    # Retrain on ALL data so the saved model uses every example
    model.fit(X, y)
    m = model.coef_[0]
    c = model.intercept_

    print("\n[4] The line the model learned:")
    print(f"    final_marks = {m:.2f} × study_hours + {c:.2f}")
    print(f"    Slope (m)     = {m:.2f}  -> each extra study hour adds ~{m:.1f} marks")
    print(f"    Intercept (c) = {c:.2f}  -> predicted marks with 0 study hours")

    joblib.dump(model, MODEL_FILE)
    print(f"\n[5] Model saved to '{MODEL_FILE}'. Now run:  python predict.py\n")


if __name__ == "__main__":
    main()
