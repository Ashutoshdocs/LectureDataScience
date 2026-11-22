"""
predict.py - Predict final marks from study hours using the trained model.

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


def load_model():
    if not os.path.exists(MODEL_FILE):
        print(f"'{MODEL_FILE}' not found. Training a model first ...")
        import train
        train.main()
    return joblib.load(MODEL_FILE)


def clamp(marks):
    """Marks can't go below 0 or above 100."""
    return max(0.0, min(100.0, float(marks)))


def predict_from_csv(model):
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

    out_path = "predictions_output.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved results to '{out_path}'.")


def predict_from_user(model):
    m, c = model.coef_[0], model.intercept_
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

        marks = clamp(model.predict(pd.DataFrame({FEATURE: [hours]}))[0])
        print(f"  Calculation: {m:.2f} × {hours} + {c:.2f}")
        print(f"  >>> Predicted final marks: {marks:.1f} / 100")

        if input("\nPredict another? (y/n): ").strip().lower() != "y":
            break


def main():
    model = load_model()

    print("\n==========================================")
    print("   STUDENT MARKS PREDICTION (Linear Reg.)")
    print("==========================================")
    print(f"  Model: final_marks = {model.coef_[0]:.2f} × study_hours + {model.intercept_:.2f}")
    print("\n  1) Predict from a CSV file")
    print("  2) Predict from user input")
    print("  3) Exit")

    choice = input("\nChoose an option (1/2/3): ").strip()
    if choice == "1":
        predict_from_csv(model)
    elif choice == "2":
        predict_from_user(model)
    elif choice == "3":
        print("Bye!")
    else:
        print("Invalid choice.")
        sys.exit(1)


if __name__ == "__main__":
    main()
