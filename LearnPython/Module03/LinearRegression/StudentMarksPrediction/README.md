# Student Marks Prediction – Supervised Learning with Python

A beginner-friendly machine learning practical that predicts a student's exam marks using labelled study and attendance data.

## 1. Project structure

```text
student_marks_prediction/
├── README.md
├── student_marks.csv
├── train_model.py
└── predict_marks.py
```

## 2. What will the model learn?

The model uses these input features:

- `study_hours` – average hours studied per day
- `attendance` – attendance percentage

It learns to predict:

- `marks` – exam marks out of 100 (target/label)

This is a **supervised learning regression** example because the target is a numeric value.

## 3. How supervised learning works

```text
        student_marks.csv
      (study hours, attendance,
           known marks)
                |
                v
          Load the data
                |
                v
        Split into train/test
           /          \
          v            v
       Train         Test
       model         model
          \            /
           v          v
          Evaluate results
                |
                v
          Save trained model
                |
                v
      Predict marks for a new student
```

## 4. Requirements

Python 3.9 or later is recommended.

Install dependencies:

```bash
python -m pip install pandas scikit-learn joblib
```

On Linux, use `python3` if `python` is not configured.

## 5. Run the practical

Open a terminal in the project folder.

### Step 1 – Train the model

```bash
python train_model.py
```

The script:
1. Reads `student_marks.csv`.
2. Checks that the required columns and numeric values are present.
3. Splits the data into training and testing sets.
4. Trains a Linear Regression model.
5. Displays MAE, RMSE, and R².
6. Saves the model to `student_marks_model.joblib`.

### Step 2 – Predict marks

```bash
python predict_marks.py
```

Example:

```text
Enter average study hours per day: 5
Enter attendance percentage (0-100): 85
```

The script displays the predicted marks out of 100.

Train the model before running predictions.

## 6. Add new student records

Open `student_marks.csv` in Excel or a text editor.

The header must remain:

```csv
study_hours,attendance,marks
```

Add a new row with a known exam result. Example:

```csv
6,90,88
```

This means the student studied 6 hours per day, had 90% attendance, and scored 88 marks.

Save the CSV, then retrain:

```bash
python train_model.py
```

Run prediction again:

```bash
python predict_marks.py
```

Use the same study hours and attendance values before and after retraining to compare the predictions fairly.

### Observe the impact

Record the following before adding data:
- MAE, RMSE and R² from the training script
- Prediction for one fixed student input

Then:
1. Add a labelled student record.
2. Save the CSV.
3. Run `python train_model.py` again.
4. Predict the exact same student input.
5. Compare the prediction and evaluation metrics.

The model can produce a different prediction because it has learned from the updated dataset. Metrics may improve or worsen; adding data does not guarantee better performance.

## 7. Classroom experiments

| Experiment | Add or change | Discuss |
|---|---|---|
| A | Add a student who studies 2 hours and has 60% attendance, with a realistic known mark | Does the prediction for similar students change? |
| B | Add a student who studies 8 hours and has 95% attendance, with a known mark | How does the model learn from this example? |
| C | Add an unrealistic record, such as 2 study hours, 40% attendance, and 100 marks | How can inaccurate data mislead a model? |
| D | Add several realistic student records | Does the model's evaluation become more stable? |

Use genuine or clearly labelled teaching examples. The model learns patterns from the records; it does not prove that study hours or attendance alone determine a student's result.

## 8. Understand the metrics

- **MAE:** average absolute prediction error in marks. Lower is generally better.
- **RMSE:** prediction error in marks that penalizes large errors more strongly. Lower is generally better.
- **R²:** compares the model with a simple mean-value baseline. Closer to 1 is generally better; a negative score means it performs worse than that baseline on the test set.

This is a small educational dataset, not a validated student assessment system. Predictions are estimates, not guaranteed exam results.

## 9. Troubleshooting

**Missing Python packages**
```bash
python -m pip install pandas scikit-learn joblib
```

**Model not found**

Run training first:
```bash
python train_model.py
```

**CSV validation error**

Check:
- The header is exactly `study_hours,attendance,marks`.
- All values are numeric.
- No required field is blank.
- Attendance is between 0 and 100.
- Marks are between 0 and 100.
- Study hours are greater than zero.

## 10. Learning outcomes

After completing this lab, students should understand:

- Supervised learning and labelled datasets
- Features versus target/label
- Regression in machine learning
- Training and testing datasets
- Linear Regression
- Model evaluation using MAE, RMSE and R²
- Making predictions for unseen inputs
- Retraining after adding new labelled data
- How inaccurate or biased data can affect predictions
