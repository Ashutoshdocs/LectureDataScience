"""
predict.py - Predict student final marks using the trained Random Forest.

Usage:
    python predict.py

You will be asked to choose:
    1) Predict from a CSV file   (e.g. predict.csv)
    2) Predict from user input   (type in one student's details)
"""
import os
import sys

import joblib
import numpy as np
import pandas as pd

from train import prepare

MODEL_FILE = "model.pkl"


def load_bundle():
    if not os.path.exists(MODEL_FILE):
        print(f"'{MODEL_FILE}' not found. Training a model first ...")
        import train
        train.main()
    return joblib.load(MODEL_FILE)


def ask_number(label, low, high, whole=False):
    while True:
        raw = input(f"  {label} [{low}-{high}]: ").strip()
        try:
            value = int(raw) if whole else float(raw)
        except ValueError:
            print("    Please enter a whole number." if whole else "    Please enter a number.")
            continue
        if not low <= value <= high:
            print(f"    Value must be between {low} and {high}.")
            continue
        return value


def ask_yes_no(label):
    while True:
        raw = input(f"  {label} (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return "Yes"
        if raw in ("n", "no"):
            return "No"
        print("    Please type y or n.")


def tree_predictions(model, row):
    """Ask every tree in the forest for its own prediction."""
    values = row.to_numpy()
    return np.array([tree.predict(values)[0] for tree in model.estimators_])


def predict_from_csv(bundle):
    model, features = bundle["model"], bundle["features"]
    path = input("\nEnter CSV file path [default: predict.csv]: ").strip() or "predict.csv"
    if not os.path.exists(path):
        print(f"ERROR: file '{path}' not found.")
        return
    df = pd.read_csv(path)
    missing = [c for c in features if c not in df.columns]
    if missing:
        print(f"ERROR: CSV is missing columns: {missing}")
        return
    try:
        X = prepare(df)[features]
    except ValueError as err:
        print(f"ERROR: {err}")
        return

    df["predicted_marks"] = [round(float(p), 1) for p in model.predict(X)]

    print("\nPredictions:")
    print(df.to_string(index=False))

    out_path = "predictions_output.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved results to '{out_path}'.")


def predict_from_user(bundle):
    model, features = bundle["model"], bundle["features"]
    while True:
        print("\nEnter the student's details:")
        student = {
            "study_hours": ask_number("Study hours per day", 0, 24),
            "coaching": ask_yes_no("Takes coaching classes?"),
            "live_sessions_attended": ask_number("Live sessions attended (out of 20)", 0, 20, whole=True),
            "recorded_course_completion": ask_number("Recorded course completed (%)", 0, 100),
        }
        row = prepare(pd.DataFrame([student]))[features]
        preds = tree_predictions(model, row)
        forest = model.predict(row)[0]

        print(f"\n  The forest has {len(preds)} trees. Each one made its own prediction:")
        print(f"    Lowest tree   : {preds.min():.1f}")
        print(f"    Highest tree  : {preds.max():.1f}")
        print(f"    First 5 trees : {', '.join(f'{p:.1f}' for p in preds[:5])} ...")
        print(f"  Average of all {len(preds)} trees = forest prediction")
        print(f"\n  >>> Predicted final marks: {forest:.1f} / 100")

        if input("\nPredict another student? (y/n): ").strip().lower() != "y":
            break


def main():
    bundle = load_bundle()
    model = bundle["model"]

    print("\n==================================================")
    print("   STUDENT MARKS PREDICTION (Random Forest)")
    print("==================================================")
    print(f"  Model: forest of {len(model.estimators_)} decision trees")
    print("  Inputs: study hours, coaching, live sessions, recorded course")
    print("\n  1) Predict from a CSV file")
    print("  2) Predict from user input")
    print("  3) Exit")

    choice = input("\nChoose an option (1/2/3): ").strip()
    if choice == "1":
        predict_from_csv(bundle)
    elif choice == "2":
        predict_from_user(bundle)
    elif choice == "3":
        print("Bye!")
    else:
        print("Invalid choice.")
        sys.exit(1)


if __name__ == "__main__":
    main()
