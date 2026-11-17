"""
predict.py - Predict final marks from study hours using the trained
Decision Tree Regressor.

Usage:
    python predict.py

You will be asked to choose:
    1) Predict from a CSV file   (e.g. predict.csv)
    2) Predict from user input   (type the study hours, see the questions the tree asks)
"""
import os
import sys

import joblib
import pandas as pd

FEATURE = "study_hours"
MODEL_FILE = "model.pkl"


def load_bundle():
    if not os.path.exists(MODEL_FILE):
        print(f"'{MODEL_FILE}' not found. Training a model first ...")
        import train
        train.main()
    return joblib.load(MODEL_FILE)


def decision_path(model, hours):
    """Walk down the tree and return the questions asked + the leaf value."""
    tree = model.tree_
    node = 0
    steps = []
    while tree.children_left[node] != -1:          # -1 means "this is a leaf"
        threshold = tree.threshold[node]
        if hours <= threshold:
            steps.append(f"Is {FEATURE} <= {threshold:.2f}?  YES")
            node = tree.children_left[node]
        else:
            steps.append(f"Is {FEATURE} <= {threshold:.2f}?  NO")
            node = tree.children_right[node]
    leaf_value = tree.value[node][0][0]
    n_students = int(tree.n_node_samples[node])
    return steps, leaf_value, n_students


def predict_from_csv(bundle):
    model = bundle["model"]
    path = input("\nEnter CSV file path [default: predict.csv]: ").strip() or "predict.csv"
    if not os.path.exists(path):
        print(f"ERROR: file '{path}' not found.")
        return
    df = pd.read_csv(path)
    if FEATURE not in df.columns:
        print(f"ERROR: CSV must have a '{FEATURE}' column.")
        return

    df["predicted_marks"] = [round(float(p), 1) for p in model.predict(df[[FEATURE]])]

    print("\nPredictions:")
    print(df.to_string(index=False))
    print("\nNote: students who land in the same leaf get exactly the same prediction.")

    out_path = "predictions_output.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved results to '{out_path}'.")


def predict_from_user(bundle):
    model = bundle["model"]
    while True:
        raw = input("\nEnter study hours per day (0-24): ").strip()
        try:
            hours = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if not 0 <= hours <= 24:
            print("  Value must be between 0 and 24.")
            continue

        steps, value, n = decision_path(model, hours)
        print("  The tree asks:")
        for i, step in enumerate(steps, 1):
            print(f"    {i}. {step}")
        print(f"  -> Reached a leaf with {n} training students, average marks {value:.1f}")
        print(f"  >>> Predicted final marks: {value:.1f} / 100")

        if not bundle["x_min"] <= hours <= bundle["x_max"]:
            print(f"  NOTE: {hours} hours is outside the training range "
                  f"({bundle['x_min']}-{bundle['x_max']}). A tree can't extrapolate: "
                  "it just uses the nearest leaf.")

        if input("\nPredict another? (y/n): ").strip().lower() != "y":
            break


def main():
    bundle = load_bundle()
    model = bundle["model"]

    print("\n==================================================")
    print("   STUDENT MARKS PREDICTION (Decision Tree)")
    print("==================================================")
    print(f"  Model: tree with depth {model.get_depth()} and {model.get_n_leaves()} leaves")
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
