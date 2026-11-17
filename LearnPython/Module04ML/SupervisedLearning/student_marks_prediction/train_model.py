"""
TRAINING PROGRAM — Student Marks Prediction with Multiple Linear Regression

Run this file first:
    python train_model.py

Input:
    student_marks.csv

Output:
    student_marks_model.joblib

Teaching note:
    This project uses TWO input features (study_hours and attendance)
    to predict ONE numeric target (marks). This is Multiple Linear
    Regression, because there is more than one input feature.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# ------------------------------------------------------------
# STEP 1: Locate the files
# ------------------------------------------------------------
# __file__ is the path of this Python script.
# resolve() converts it to an absolute path.
# parent gives the folder containing this script.
# This means the program can find the CSV/model even if it is
# launched from a different working directory.
BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "student_marks.csv"
MODEL_FILE = BASE_DIR / "student_marks_model.joblib"


# ------------------------------------------------------------
# STEP 2: Tell the program which columns have which roles
# ------------------------------------------------------------
# FEATURES are the input columns (capital X convention).
# The model uses both study hours and attendance to make a prediction.
FEATURES = ["study_hours", "attendance"]

# TARGET is the answer/label the model should learn to predict (y).
TARGET = "marks"


def main():
    # --------------------------------------------------------
    # STEP 3: Check that the CSV file exists
    # --------------------------------------------------------
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_FILE}")

    # Read the CSV into a pandas DataFrame (a table in Python).
    data = pd.read_csv(CSV_FILE)

    print("\n========== FIRST FIVE RECORDS ==========")
    print(data.head())

    # --------------------------------------------------------
    # STEP 4: Validate the CSV structure and values
    # --------------------------------------------------------
    # A valid dataset must contain both input columns and the target.
    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in data.columns]

    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")

    # Keep only the columns used by this model.
    # Convert values to numbers; invalid text becomes NaN.
    # dropna() removes rows that have missing/invalid values.
    data = data[required].apply(pd.to_numeric, errors="coerce").dropna()

    # A very small dataset is not suitable for this train/test exercise.
    if len(data) < 5:
        raise ValueError("Add at least 5 complete student records.")

    # Check that the input values are within the expected teaching ranges.
    if (data["study_hours"] <= 0).any():
        raise ValueError("Study hours must be greater than zero.")

    if not data["attendance"].between(0, 100).all():
        raise ValueError("Attendance must be between 0 and 100.")

    if not data["marks"].between(0, 100).all():
        raise ValueError("Marks must be between 0 and 100.")

    # --------------------------------------------------------
    # STEP 5: Separate FEATURES (X) from TARGET (y)
    # --------------------------------------------------------
    # X is a table with two columns:
    #   study_hours | attendance
    #
    # y is a single series containing the known exam marks.
    #
    # During training, the algorithm sees X and the correct y values
    # and learns a relationship between them.
    X = data[FEATURES]
    y = data[TARGET]

    # --------------------------------------------------------
    # STEP 6: Split records into training and testing sets
    # --------------------------------------------------------
    # 75% of records are used to train the model.
    # 25% are held back to test how the model performs on unseen records.
    #
    # random_state=42 makes the split repeatable for classroom demos.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
    )

    # --------------------------------------------------------
    # STEP 7: Create the Linear Regression model
    # --------------------------------------------------------
    # LinearRegression is the algorithm implementation from scikit-learn.
    # At this point, the model object exists, but it has not learned yet.
    model = LinearRegression()

    # --------------------------------------------------------
    # STEP 8: TRAIN / FIT the model
    # --------------------------------------------------------
    # fit() is the learning step.
    # It uses the training inputs and their known marks to calculate
    # the best-fitting coefficients and intercept.
    #
    # With two input features, the learned relationship is:
    # predicted_marks = intercept
    #                 + (coefficient_1 * study_hours)
    #                 + (coefficient_2 * attendance)
    model.fit(X_train, y_train)

    # Show the values learned by the model.
    print("\n========== LEARNED MODEL ==========")
    print(f"Intercept: {model.intercept_:.4f}")

    for feature, coefficient in zip(FEATURES, model.coef_):
        print(f"Coefficient for {feature}: {coefficient:.4f}")

    print(
        "\nLearned equation:\n"
        f"marks = {model.intercept_:.4f}"
        f" + ({model.coef_[0]:.4f} * study_hours)"
        f" + ({model.coef_[1]:.4f} * attendance)"
    )

    # --------------------------------------------------------
    # STEP 9: TEST / PREDICT using inputs the model did not train on
    # --------------------------------------------------------
    # predict() uses the learned equation.
    # X_test contains held-out student input records.
    predictions = model.predict(X_test)

    # --------------------------------------------------------
    # STEP 10: Evaluate the model
    # --------------------------------------------------------
    # Compare predicted marks with the actual marks (y_test).
    # MAE: average absolute error, measured in marks.
    # RMSE: root mean squared error, also measured in marks.
    # R²: comparison with a baseline that predicts the test-set mean.
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions) if len(y_test) >= 2 else float("nan")

    print("\n========== DATASET SUMMARY ==========")
    print(f"Student records used: {len(data)}")
    print(f"Training records:      {len(X_train)}")
    print(f"Testing records:       {len(X_test)}")

    print("\n========== MODEL PERFORMANCE ==========")
    print(f"MAE:  {mae:.2f} marks")
    print(f"RMSE: {rmse:.2f} marks")
    print(f"R²:   {r2:.3f}")

    # Put actual and predicted values side by side for classroom discussion.
    result = X_test.copy()
    result["Actual marks"] = y_test
    result["Predicted marks"] = predictions.round(2)
    result["Residual (actual - predicted)"] = (
        result["Actual marks"] - result["Predicted marks"]
    ).round(2)

    print("\n========== TEST SET COMPARISON ==========")
    print(result.sort_index().to_string())

    # --------------------------------------------------------
    # STEP 11: SAVE the trained model
    # --------------------------------------------------------
    # Save a dictionary containing:
    #   model    -> the trained LinearRegression object
    #   features -> exact feature order expected during prediction
    #   target   -> target column name for reference
    #
    # predict_marks.py loads this file. We do not need to train again
    # every time a new student asks for a prediction.
    joblib.dump(
        {"model": model, "features": FEATURES, "target": TARGET},
        MODEL_FILE,
    )

    print(f"\nTrained model saved as: {MODEL_FILE.name}")
    print("Training complete. You can now run: python predict_marks.py")
    print("After adding labelled rows to the CSV, run this training script again.")


# This condition means main() runs only when this file is executed directly.
# It will not automatically run if another Python file imports this file.
if __name__ == "__main__":
    main()
