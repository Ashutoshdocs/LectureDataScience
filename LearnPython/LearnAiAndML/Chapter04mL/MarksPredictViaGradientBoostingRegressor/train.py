"""
train.py - Train a GRADIENT BOOSTING Regressor to predict student final marks.

Inputs (4 features):
    study_hours                 - hours studied per day
    coaching                    - takes coaching classes? (Yes / No)
    live_sessions_attended      - live online sessions attended (out of 20)
    recorded_course_completion  - % of the recorded course watched (0-100)
Output:
    final_marks                 - final exam marks (out of 100)

Gradient boosting builds small trees ONE AFTER ANOTHER. Each new tree tries to
fix the mistakes (residuals) left by all the trees before it:
    prediction = average marks + lr × tree1 + lr × tree2 + ... + lr × tree300

Usage:
    python train.py                  # uses train.csv
    python train.py my_data.csv      # uses your own training file

Output:
    model.pkl  - the trained model (used by predict.py)
"""
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

FEATURES = [
    "study_hours",
    "coaching",
    "live_sessions_attended",
    "recorded_course_completion",
]
TARGET = "final_marks"
N_TREES = 300         # how many small trees are added, one after another
LEARNING_RATE = 0.05  # how much of each tree's correction is used (smaller = more careful)
MAX_DEPTH = 2         # each tree is SMALL: only 2 questions deep
SUBSAMPLE = 0.8       # each tree learns from a random 80% of the students
MODEL_FILE = "model.pkl"


def prepare(df):
    """Convert coaching Yes/No into 1/0 so the model can use it."""
    df = df.copy()
    df["coaching"] = (
        df["coaching"].astype(str).str.strip().str.lower()
        .map({"yes": 1, "y": 1, "1": 1, "no": 0, "n": 0, "0": 0})
    )
    if df["coaching"].isna().any():
        raise ValueError("'coaching' column must contain only Yes or No.")
    return df


def build_model(n_trees=N_TREES):
    return GradientBoostingRegressor(
        n_estimators=n_trees,
        learning_rate=LEARNING_RATE,
        max_depth=MAX_DEPTH,
        subsample=SUBSAMPLE,
        random_state=42,
    )


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "train.csv"
    print(f"\n[1] Loading training data from '{csv_path}' ...")
    df = pd.read_csv(csv_path)
    print(f"    {len(df)} rows loaded.")

    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: training file is missing columns: {missing}")
    df = prepare(df)

    X = df[FEATURES]
    y = df[TARGET]

    # Hold back 20% of the data to test on students the model hasn't seen
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"[2] Training Gradient Boosting ({N_TREES} trees, learning_rate={LEARNING_RATE}, "
          f"max_depth={MAX_DEPTH}) ...")
    model = build_model().fit(X_train, y_train)

    print("[3] Evaluating against the other models in this series ...")
    rows = [
        ("Linear regression", LinearRegression().fit(X_train, y_train)),
        ("Single decision tree", DecisionTreeRegressor(random_state=42).fit(X_train, y_train)),
        ("Random forest (200)", RandomForestRegressor(
            n_estimators=200, min_samples_leaf=2, random_state=42).fit(X_train, y_train)),
        (f"Gradient boosting ({N_TREES})", model),
    ]
    print(f"    {'Model':<26}{'Train R²':>10}{'Test R²':>10}{'Test MAE':>12}")
    for name, m in rows:
        tr = r2_score(y_train, m.predict(X_train))
        te = r2_score(y_test, m.predict(X_test))
        mae = mean_absolute_error(y_test, m.predict(X_test))
        print(f"    {name:<26}{tr:>10.3f}{te:>10.3f}{mae:>8.2f} marks")

    # How the error shrinks as trees are added, one at a time
    print("\n    How the error changes as trees are added:")
    print(f"    {'Trees':>7}{'Train RMSE':>13}{'Test RMSE':>12}")
    train_stages = list(model.staged_predict(X_train))
    test_stages = list(model.staged_predict(X_test))
    for k in [1, 10, 50, 100, 200, 300]:
        if k <= N_TREES:
            tr = np.sqrt(mean_squared_error(y_train, train_stages[k - 1]))
            te = np.sqrt(mean_squared_error(y_test, test_stages[k - 1]))
            print(f"    {k:>7}{tr:>11.2f}{te:>12.2f}")
    print("    Each tree fixes part of the remaining error, so the error keeps falling.")

    # Retrain on ALL data so the saved model uses every example
    model = build_model().fit(X, y)

    print("\n[4] Feature importance (which inputs the model relied on most):")
    importance = sorted(zip(FEATURES, model.feature_importances_), key=lambda p: -p[1])
    for name, imp in importance:
        bar = "█" * round(imp * 50)
        print(f"    {name:<28}{imp * 100:5.1f}%  {bar}")

    joblib.dump(
        {"model": model, "features": FEATURES, "learning_rate": LEARNING_RATE},
        MODEL_FILE,
    )
    print(f"\n[5] Model saved to '{MODEL_FILE}'. Now run:  python predict.py\n")


if __name__ == "__main__":
    main()
