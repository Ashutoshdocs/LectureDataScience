"""
train.py - Train a RANDOM FOREST Regressor to predict student final marks.

Inputs (4 features):
    study_hours                 - hours studied per day
    coaching                    - takes coaching classes? (Yes / No)
    live_sessions_attended      - live online sessions attended (out of 20)
    recorded_course_completion  - % of the recorded course watched (0-100)
Output:
    final_marks                 - final exam marks (out of 100)

A random forest = many decision trees, each trained on a random sample of the
students and random features. The forest's prediction is the AVERAGE of all trees.

Usage:
    python train.py                  # uses train.csv
    python train.py my_data.csv      # uses your own training file

Output:
    model.pkl  - the trained model (used by predict.py)
"""
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

FEATURES = [
    "study_hours",
    "coaching",
    "live_sessions_attended",
    "recorded_course_completion",
]
TARGET = "final_marks"
N_TREES = 200          # how many trees in the forest
MIN_SAMPLES_LEAF = 2   # every leaf must contain at least 2 students
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


def build_model():
    return RandomForestRegressor(
        n_estimators=N_TREES,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        oob_score=True,        # test each tree on the students it did NOT see
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

    print(f"[2] Training Random Forest ({N_TREES} trees) ...")
    model = build_model().fit(X_train, y_train)

    print("[3] Evaluating: one model vs. a whole forest ...")
    rows = [
        ("Linear regression", LinearRegression().fit(X_train, y_train)),
        ("Single decision tree", DecisionTreeRegressor(random_state=42).fit(X_train, y_train)),
        (f"Random forest ({N_TREES})", model),
    ]
    print(f"    {'Model':<24}{'Train R²':>10}{'Test R²':>10}{'Test MAE':>12}")
    for name, m in rows:
        tr = r2_score(y_train, m.predict(X_train))
        te = r2_score(y_test, m.predict(X_test))
        mae = mean_absolute_error(y_test, m.predict(X_test))
        print(f"    {name:<24}{tr:>10.3f}{te:>10.3f}{mae:>8.2f} marks")
    print("    Single tree: perfect on training data, poor on new students (overfits).")
    print("    Forest: averaging many different trees cancels out their mistakes.")

    # Retrain on ALL data so the saved model uses every example
    model = build_model().fit(X, y)
    print(f"\n    Out-of-bag R² (all data): {model.oob_score_:.3f}")
    print("    (each tree is scored on the ~37% of students left out of its sample,")
    print("     so this is a free test score without a separate test set)")

    print("\n[4] Feature importance (which inputs the forest relied on most):")
    importance = sorted(zip(FEATURES, model.feature_importances_), key=lambda p: -p[1])
    for name, imp in importance:
        bar = "█" * round(imp * 50)
        print(f"    {name:<28}{imp * 100:5.1f}%  {bar}")

    joblib.dump({"model": model, "features": FEATURES}, MODEL_FILE)
    print(f"\n[5] Model saved to '{MODEL_FILE}'. Now run:  python predict.py\n")


if __name__ == "__main__":
    main()
