"""
train.py - Train a DECISION TREE Regressor:  study_hours -> final_marks

The tree learns a set of yes/no questions, e.g.
    "Is study_hours <= 4.95?"  -> yes -> "Is study_hours <= 2.45?" -> ...
Each final box (leaf) predicts the AVERAGE marks of the training students in it.

It also trains a straight line and a tree with NO depth limit, so you can
compare: underfitting vs good fit vs overfitting.

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
from sklearn.tree import DecisionTreeRegressor, export_text

FEATURE = "study_hours"
TARGET = "final_marks"
MAX_DEPTH = 3          # how many questions deep the tree can go (3 -> up to 8 leaves)
MIN_SAMPLES_LEAF = 5   # every leaf must contain at least 5 students
MODEL_FILE = "model.pkl"


def build_model():
    return DecisionTreeRegressor(
        max_depth=MAX_DEPTH, min_samples_leaf=MIN_SAMPLES_LEAF, random_state=42
    )


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

    print(f"[2] Training Decision Tree (max_depth={MAX_DEPTH}, "
          f"min_samples_leaf={MIN_SAMPLES_LEAF}) ...")
    model = build_model().fit(X_train, y_train)

    # Two other models on the same data, for comparison
    others = {
        "Straight line": LinearRegression().fit(X_train, y_train),
        "Tree, no depth limit": DecisionTreeRegressor(random_state=42).fit(X_train, y_train),
    }

    print("[3] Evaluating ...")
    print(f"    {'Model':<24}{'Train R²':>10}{'Test R²':>10}{'Test MAE':>12}")
    rows = [("Straight line", others["Straight line"]),
            (f"Tree, depth {MAX_DEPTH}", model),
            ("Tree, no depth limit", others["Tree, no depth limit"])]
    for name, m in rows:
        tr = r2_score(y_train, m.predict(X_train))
        te = r2_score(y_test, m.predict(X_test))
        mae = mean_absolute_error(y_test, m.predict(X_test))
        print(f"    {name:<24}{tr:>10.3f}{te:>10.3f}{mae:>8.2f} marks")
    print("    Straight line : too simple for the curved pattern -> UNDERFITTING")
    print("    No depth limit: memorises training students (high Train R²) but does")
    print("                    worse on new students (lower Test R²) -> OVERFITTING")

    # Retrain on ALL data so the saved model uses every example
    model = build_model().fit(X, y)

    print(f"\n[4] The tree the model learned ({model.get_n_leaves()} leaves):\n")
    print(export_text(model, feature_names=[FEATURE], decimals=2))
    print("    'value' = predicted marks for students who end up in that leaf")

    joblib.dump(
        {"model": model, "x_min": float(X[FEATURE].min()), "x_max": float(X[FEATURE].max())},
        MODEL_FILE,
    )
    print(f"\n[5] Model saved to '{MODEL_FILE}'. Now run:  python predict.py\n")


if __name__ == "__main__":
    main()
