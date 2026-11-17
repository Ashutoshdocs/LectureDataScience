"""
predict.py - Predict final marks from study hours using the trained
polynomial (degree 3) model.

Usage:
    python predict.py

You will be asked to choose:
    1) Predict from a CSV file   (e.g. predict.csv)
    2) Predict from user input   (type the study hours)
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


def coefficients(model):
    lr = model.named_steps["linearregression"]
    return (lr.intercept_, *lr.coef_)


def clamp(marks):
    """Marks can't go below 0 or above 100."""
    return max(0.0, min(100.0, float(marks)))


def outside_range(hours, bundle):
    return not bundle["x_min"] <= hours <= bundle["x_max"]


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

    df["predicted_marks"] = [round(clamp(p), 1) for p in model.predict(df[[FEATURE]])]

    print("\nPredictions:")
    print(df.to_string(index=False))

    risky = df[df[FEATURE].apply(lambda h: outside_range(h, bundle))]
    if len(risky):
        print(f"\nWARNING: {len(risky)} row(s) are outside the training range "
              f"({bundle['x_min']}-{bundle['x_max']} hours). Those predictions are unreliable.")

    out_path = "predictions_output.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved results to '{out_path}'.")


def predict_from_user(bundle):
    model = bundle["model"]
    b0, b1, b2, b3 = coefficients(model)
    while True:
        raw = input("\nEnter study hours per day (0-24): ").strip()
        try:
            x = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if not 0 <= x <= 24:
            print("  Value must be between 0 and 24.")
            continue

        raw_pred = model.predict(pd.DataFrame({FEATURE: [x]}))[0]
        print(f"  Calculation: {b0:.3f} {b1:+.3f}×{x} {b2:+.3f}×{x}² {b3:+.4f}×{x}³"
              f" = {raw_pred:.1f}")
        print(f"  >>> Predicted final marks: {clamp(raw_pred):.1f} / 100")
        if outside_range(x, bundle):
            print(f"  WARNING: {x} hours is outside the training range "
                  f"({bundle['x_min']}-{bundle['x_max']}). A cubic curve can shoot up or "
                  "down quickly out here, so don't trust this prediction.")

        if input("\nPredict another? (y/n): ").strip().lower() != "y":
            break


def main():
    bundle = load_bundle()
    b0, b1, b2, b3 = coefficients(bundle["model"])

    print("\n==================================================")
    print("   STUDENT MARKS PREDICTION (Polynomial, degree 3)")
    print("==================================================")
    print(f"  Model: marks = {b0:.2f} {b1:+.2f}x {b2:+.2f}x² {b3:+.3f}x³")
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
