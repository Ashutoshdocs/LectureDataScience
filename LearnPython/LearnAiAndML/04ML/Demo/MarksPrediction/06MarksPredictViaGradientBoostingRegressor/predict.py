"""
predict.py - Predict student final marks using the trained Gradient Boosting model.

Usage:
    python predict.py

You will be asked to choose:
    1) Predict from a CSV file   (e.g. predict.csv)
    2) Predict from user input   (type in one student's details and watch the
                                  prediction being built tree by tree)
"""
import os
import sys

import joblib
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
    lr = bundle["learning_rate"]
    n_trees = model.n_estimators_
    while True:
        print("\nEnter the student's details:")
        student = {
            "study_hours": ask_number("Study hours per day", 0, 24),
            "coaching": ask_yes_no("Takes coaching classes?"),
            "live_sessions_attended": ask_number("Live sessions attended (out of 20)", 0, 20, whole=True),
            "recorded_course_completion": ask_number("Recorded course completed (%)", 0, 100),
        }
        row = prepare(pd.DataFrame([student]))[features]
        stages = [p[0] for p in model.staged_predict(row)]
        start = float(model.init_.predict(row)[0])
        first_tree = float(model.estimators_[0][0].predict(row.to_numpy())[0])

        print("\n  How the prediction is built, one tree at a time:")
        print(f"    Start with the average of all students     : {start:.1f}")
        print(f"    Tree 1 says 'add {first_tree:+.1f}', × learning rate {lr}"
              f" = {lr * first_tree:+.2f}  -> {stages[0]:.1f}")
        for k in [5, 10, 25, 50, 100, 200, n_trees]:
            if k <= n_trees:
                print(f"    After {k:>3} trees{'':<29}: {stages[k - 1]:.1f}")
        print(f"\n  >>> Predicted final marks: {stages[-1]:.1f} / 100")

        if input("\nPredict another student? (y/n): ").strip().lower() != "y":
            break


def main():
    bundle = load_bundle()
    model = bundle["model"]

    print("\n==================================================")
    print("   STUDENT MARKS PREDICTION (Gradient Boosting)")
    print("==================================================")
    print(f"  Model: {model.n_estimators_} small trees, added one after another")
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
