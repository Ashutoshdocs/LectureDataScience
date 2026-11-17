"""
predict.py - Predict student final marks using the trained model.

Usage:
    python predict.py

You will be asked to choose:
    1) Predict from a CSV file   (e.g. predict.csv)
    2) Predict from your own input (type the values)
"""
import os
import sys

import joblib
import pandas as pd

MODEL_FILE = "model.pkl"

PROMPTS = {
    "study_hours": ("Study hours per day", 0, 24),
    "attendance_percent": ("Attendance percentage", 0, 100),
    "previous_marks": ("Previous exam marks (out of 100)", 0, 100),
    "assignments_completed": ("Assignments completed (out of 10)", 0, 10),
    "sleep_hours": ("Sleep hours per day", 0, 24),
}


def load_model():
    if not os.path.exists(MODEL_FILE):
        print(f"'{MODEL_FILE}' not found. Training a model first ...")
        import train
        train.main()
    bundle = joblib.load(MODEL_FILE)
    return bundle["model"], bundle["features"]


def clamp(marks):
    """Marks can't go below 0 or above 100."""
    return max(0.0, min(100.0, float(marks)))


def ask_number(label, low, high):
    while True:
        raw = input(f"  {label} [{low}-{high}]: ").strip()
        try:
            value = float(raw)
        except ValueError:
            print("    Please enter a number.")
            continue
        if not low <= value <= high:
            print(f"    Value must be between {low} and {high}.")
            continue
        return value


def predict_from_csv(model, features):
    path = input("\nEnter CSV file path [default: predict.csv]: ").strip() or "predict.csv"
    if not os.path.exists(path):
        print(f"ERROR: file '{path}' not found.")
        return
    df = pd.read_csv(path)
    missing = [c for c in features if c not in df.columns]
    if missing:
        print(f"ERROR: CSV is missing columns: {missing}")
        return

    df["predicted_marks"] = [round(clamp(m), 1) for m in model.predict(df[features])]

    print("\nPredictions:")
    print(df.to_string(index=False))

    out_path = "predictions_output.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved results to '{out_path}'.")


def predict_from_user(model, features):
    while True:
        print("\nEnter the student's details:")
        values = {f: ask_number(*PROMPTS[f]) for f in features}
        row = pd.DataFrame([values])[features]
        marks = clamp(model.predict(row)[0])
        print(f"\n  >>> Predicted final marks: {marks:.1f} / 100\n")

        again = input("Predict another student? (y/n): ").strip().lower()
        if again != "y":
            break


def main():
    model, features = load_model()

    print("\n==========================================")
    print("   STUDENT MARKS PREDICTION (Linear Reg.)")
    print("==========================================")
    print("  1) Predict from a CSV file")
    print("  2) Predict from user input")
    print("  3) Exit")

    choice = input("\nChoose an option (1/2/3): ").strip()
    if choice == "1":
        predict_from_csv(model, features)
    elif choice == "2":
        predict_from_user(model, features)
    elif choice == "3":
        print("Bye!")
    else:
        print("Invalid choice.")
        sys.exit(1)


if __name__ == "__main__":
    main()
