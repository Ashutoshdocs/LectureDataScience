"""
Predict exam marks for a new student using the saved model.

Run:
    python predict_marks.py

Train first:
    python train_model.py
"""

from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "student_marks_model.joblib"


def main():
    if not MODEL_FILE.exists():
        print("Trained model not found. First run: python train_model.py")
        return

    saved = joblib.load(MODEL_FILE)
    model = saved["model"]
    features = saved["features"]

    try:
        study_hours = float(input("Enter average study hours per day: "))
        attendance = float(input("Enter attendance percentage (0-100): "))

        if study_hours <= 0:
            raise ValueError("Study hours must be greater than zero.")
        if not 0 <= attendance <= 100:
            raise ValueError("Attendance must be between 0 and 100.")

        student = pd.DataFrame(
            [[study_hours, attendance]],
            columns=features,
        )

        predicted_marks = float(model.predict(student)[0])
        predicted_marks = max(0.0, min(100.0, predicted_marks))

        print("\n========== STUDENT RESULT PREDICTION ==========")
        print(f"Study hours per day: {study_hours:g}")
        print(f"Attendance:          {attendance:g}%")
        print(f"Predicted marks:     {predicted_marks:.2f} / 100")
        print("\nNote: This is an educational model estimate, not a guaranteed result.")

    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
