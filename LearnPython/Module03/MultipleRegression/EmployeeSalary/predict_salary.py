"""
Predict an employee's annual salary using the saved regression pipeline.

Run:
    python predict_salary.py

Train first:
    python train_model.py
"""

from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "employee_salary_model.joblib"


def main():
    if not MODEL_FILE.exists():
        print("Trained model not found. First run: python train_model.py")
        return

    saved = joblib.load(MODEL_FILE)
    pipeline = saved["pipeline"]
    features = saved["features"]

    education_levels = saved["education_levels"]
    job_titles = saved["job_titles"]

    print("\nAvailable education levels:")
    for value in education_levels:
        print(f" - {value}")

    print("\nAvailable job titles:")
    for value in job_titles:
        print(f" - {value}")

    try:
        experience = float(input("\nEnter experience in years: "))
        education = input("Enter education level exactly as listed: ").strip()
        job_title = input("Enter job title exactly as listed: ").strip()

        if experience < 0:
            raise ValueError("Experience cannot be negative.")
        if education not in education_levels:
            raise ValueError("Education level is not in the training dataset.")
        if job_title not in job_titles:
            raise ValueError("Job title is not in the training dataset.")

        employee = pd.DataFrame(
            [[experience, education, job_title]],
            columns=features,
        )

        predicted_salary = float(pipeline.predict(employee)[0])

        print("\n========== EMPLOYEE SALARY PREDICTION ==========")
        print(f"Experience:       {experience:g} years")
        print(f"Education:        {education}")
        print(f"Job title:        {job_title}")
        print(f"Estimated salary: {predicted_salary:.2f} LPA")
        print("\nTeaching estimate only; not a market salary benchmark.")

    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
