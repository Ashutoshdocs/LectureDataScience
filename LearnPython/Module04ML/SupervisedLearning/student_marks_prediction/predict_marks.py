"""
PREDICTION PROGRAM — Estimate marks for a new student.

Run this only AFTER training:
    python train_model.py
    python predict_marks.py

Input from user:
    study hours per day
    attendance percentage

Output:
    estimated exam marks out of 100
"""

from pathlib import Path

import joblib
import pandas as pd


# Find the saved model in the same folder as this Python file.
BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "student_marks_model.joblib"


def main():
    # --------------------------------------------------------
    # STEP 1: Check whether training has already created the model
    # --------------------------------------------------------
    if not MODEL_FILE.exists():
        print("Trained model not found. First run: python train_model.py")
        return

    # --------------------------------------------------------
    # STEP 2: Load the saved training result
    # --------------------------------------------------------
    # joblib.load() restores the saved Python objects.
    # The training script saved a dictionary, not just the model.
    saved = joblib.load(MODEL_FILE)

    model = saved["model"]       # The trained LinearRegression object
    features = saved["features"] # Required input column names and order

    # --------------------------------------------------------
    # STEP 3: Collect input for a new student
    # --------------------------------------------------------
    try:
        # input() receives text from the keyboard.
        # float() converts that text into a numeric value.
        study_hours = float(input("Enter average study hours per day: "))
        attendance = float(input("Enter attendance percentage (0-100): "))

        # ----------------------------------------------------
        # STEP 4: Validate the user's input
        # ----------------------------------------------------
        if study_hours <= 0:
            raise ValueError("Study hours must be greater than zero.")

        if not 0 <= attendance <= 100:
            raise ValueError("Attendance must be between 0 and 100.")

        # ----------------------------------------------------
        # STEP 5: Arrange input in the same structure used in training
        # ----------------------------------------------------
        # scikit-learn expects a 2D table:
        # one row = one student
        # columns = features in the same order as training
        #
        # Example:
        # study_hours | attendance
        #      5      |     85
        student = pd.DataFrame(
            [[study_hours, attendance]],
            columns=features,
        )

        # ----------------------------------------------------
        # STEP 6: Ask the trained model to predict
        # ----------------------------------------------------
        # predict() returns an array. [0] selects the first (only) result.
        predicted_marks = float(model.predict(student)[0])

        # Keep the displayed estimate within the expected 0–100 mark range.
        # This is a display/business-rule clamp; it does not change the
        # underlying Linear Regression model or make the estimate guaranteed.
        predicted_marks = max(0.0, min(100.0, predicted_marks))

        # ----------------------------------------------------
        # STEP 7: Display the result
        # ----------------------------------------------------
        print("\n========== STUDENT RESULT PREDICTION ==========")
        print(f"Study hours per day: {study_hours:g}")
        print(f"Attendance:          {attendance:g}%")
        print(f"Predicted marks:     {predicted_marks:.2f} / 100")
        print("\nNote: This is an educational model estimate, not a guaranteed result.")

    # Handle invalid numeric text and our validation errors cleanly.
    except ValueError as error:
        print(f"Invalid input: {error}")


# Start the program when this file is run directly.
if __name__ == "__main__":
    main()
