# Student Marks Prediction — Multiple Linear Regression with Python

A step-by-step classroom practical that teaches **Supervised Learning** and **Multiple Linear Regression** by predicting a student's exam marks from two inputs:

- Average study hours per day
- Attendance percentage

The project uses a labelled CSV dataset, trains a model, evaluates it on held-out records, saves the trained model, and then predicts marks for a new student entered through the terminal.

> **Teaching distinction:** This project has two input features (`study_hours` and `attendance`). It is therefore Multiple Linear Regression, not Simple Linear Regression. The target is still one numerical value: `marks`.

---

## 1. Learning objectives

By completing this practical, students will understand:

1. What supervised learning is and why the dataset is labelled.
2. The difference between features (`X`) and target (`y`).
3. What regression means and why marks are a numerical target.
4. The difference between simple and multiple Linear Regression.
5. What the intercept and coefficients mean.
6. Why data is split into training and testing sets.
7. What `fit()` and `predict()` do.
8. How to interpret MAE, RMSE, and R².
9. How a trained model is saved and loaded.
10. Why a model must be retrained after adding new labelled records.

---

## 2. Project folder structure

```text
student_marks_prediction/
│
├── README.md
├── requirements.txt
├── student_marks.csv
├── train_model.py
└── predict_marks.py
```

Files generated after training:

```text
student_marks_prediction/
│
└── student_marks_model.joblib
```

| File | Purpose |
|---|---|
| `student_marks.csv` | Historical student examples used for learning |
| `train_model.py` | Validates data, trains, evaluates, and saves the model |
| `predict_marks.py` | Loads the saved model and predicts for a new student |
| `requirements.txt` | Python libraries required by the project |
| `student_marks_model.joblib` | Generated trained model; created by `train_model.py` |
| `README.md` | Theory, program flow, setup, and teaching guide |

---

## 3. Understand the dataset first

Open `student_marks.csv`. It contains three columns:

```csv
study_hours,attendance,marks
1,55,35
1.5,60,39
2,58,42
```

| Column | Role | Meaning |
|---|---|---|
| `study_hours` | Feature / input | Average hours studied per day |
| `attendance` | Feature / input | Attendance percentage |
| `marks` | Target / label | Known exam marks out of 100 |

### What does one row mean?

For example:

```csv
5,85,76
```

This means a student:

- Studied an average of 5 hours per day.
- Had 85% attendance.
- Scored 76 marks.

The model is given many examples like this. It learns a mathematical relationship between the two input columns and the known marks.

**Why is this supervised learning?**

Because the training dataset contains both the input values and the correct answer (`marks`). The model learns from labelled examples.

---

## 4. What is Linear Regression?

Linear Regression is a supervised machine learning algorithm used to predict a numerical value.

Examples:

| Inputs | Numerical value to predict |
|---|---|
| Study hours and attendance | Exam marks |
| Experience | Salary |
| Area of a house | House price |
| Advertising expenditure | Sales |

Regression predicts a quantity. Classification predicts a category, such as pass/fail or spam/not spam.

### Simple Linear Regression vs Multiple Linear Regression

**Simple Linear Regression** uses one input feature:

$$
\hat{y} = b_0 + b_1x
$$

**Multiple Linear Regression** uses two or more input features:

$$
\hat{y} = b_0 + b_1x_1 + b_2x_2 + \cdots + b_nx_n
$$

This project uses two inputs, so its equation is:

$$
\widehat{marks} =
b_0 +
b_1(study\_hours) +
b_2(attendance)
$$

Where:

- \(\widehat{marks}\) = predicted marks
- \(b_0\) = intercept
- \(b_1\) = coefficient for study hours
- \(b_2\) = coefficient for attendance

The values of the intercept and coefficients are **learned from the training data**. They are not manually entered in the program.

### How to explain a coefficient

Suppose a model learned an illustrative equation:

$$
\widehat{marks} = 10 + 5(study\_hours) + 0.4(attendance)
$$

This is only an example to explain the terms; it is not a promised output from the supplied CSV.

- The intercept is 10.
- The study-hours coefficient is 5.
- The attendance coefficient is 0.4.

In this equation, holding attendance constant, one additional study hour changes the predicted marks by 5. Holding study hours constant, one additional attendance percentage point changes the predicted marks by 0.4.

A coefficient describes the model's learned relationship. It does **not** prove that changing one factor will cause that exact change in a real student's marks.

---

## 5. End-to-end program flow

First, teach the overall flow before opening the Python code.

```text
             student_marks.csv
        (study_hours, attendance, marks)
                     |
                     v
             train_model.py
                     |
                     v
             Read CSV using pandas
                     |
                     v
             Validate columns/data
                     |
                     v
              Separate X and y
          X = study_hours, attendance
                 y = marks
                     |
                     v
              Split the dataset
                 /       \
                /         \
               v           v
         Training data   Testing data
               |           |
               v           |
         LinearRegression |
               |           |
               v           |
           model.fit()     |
         Model learns      |
         coefficients      |
               |           |
               v           v
           model.predict(X_test)
                     |
                     v
             Evaluate predictions
              MAE, RMSE, R²
                     |
                     v
        Save model to .joblib file
                     |
                     v
             predict_marks.py
                     |
                     v
          Load saved model from disk
                     |
                     v
          Ask for new student's inputs
          study_hours + attendance
                     |
                     v
             model.predict()
                     |
                     v
           Display predicted marks
```

### Explain the two programs

**Program 1 — `train_model.py`**

This is the learning phase. It reads historical examples, trains the algorithm, checks its performance, and saves the trained model.

**Program 2 — `predict_marks.py`**

This is the prediction phase. It loads the model that was already trained. It asks for a new student's inputs and uses the learned relationship to estimate marks.

The prediction program does not train the model again.

---

## 6. Step-by-step explanation of `train_model.py`

### Step 1 — Import libraries

```python
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
```

| Library / function | Purpose |
|---|---|
| `Path` | Builds reliable paths to project files |
| `pandas` | Reads and manipulates CSV data |
| `joblib` | Saves and loads the trained model |
| `LinearRegression` | Provides the Linear Regression algorithm |
| `train_test_split` | Divides data into training and testing sets |
| `mean_absolute_error` | Calculates MAE |
| `mean_squared_error` | Used to calculate RMSE |
| `r2_score` | Calculates R² |

### Step 2 — Define file paths and column names

```python
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "student_marks.csv"
MODEL_FILE = BASE_DIR / "student_marks_model.joblib"

FEATURES = ["study_hours", "attendance"]
TARGET = "marks"
```

- `BASE_DIR` identifies the folder where the script is located.
- `CSV_FILE` points to the input CSV.
- `MODEL_FILE` is where the trained model will be saved.
- `FEATURES` tells the algorithm which columns are inputs.
- `TARGET` identifies the answer the algorithm must learn to predict.

### Step 3 — Read and validate the data

```python
data = pd.read_csv(CSV_FILE)
```

Pandas reads the CSV into a DataFrame, which is like a table in Python.

The program checks that all required columns exist, converts their values to numbers, and removes rows with missing or invalid numeric values. It also checks that study hours are positive and attendance and marks are between 0 and 100.

**Why validate?** Incorrect data can lead to misleading predictions or runtime errors.

### Step 4 — Separate X and y

```python
X = data[FEATURES]
y = data[TARGET]
```

`X` contains the two input columns:

```text
study_hours | attendance
```

`y` contains the known marks:

```text
marks
```

Ask students: Which column is the answer the model is trying to predict? The answer is `marks`.

### Step 5 — Split training and testing data

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
```

- 75% of the records are used for training.
- 25% are kept aside for testing.
- `random_state=42` makes the split repeatable.

**Why do we test separately?**

If we evaluate a model only on the records it has already learned from, we do not get a fair indication of how it handles unseen records. The held-out test set gives us a basic check of performance on data not used in fitting.

### Step 6 — Create the model

```python
model = LinearRegression()
```

This creates the algorithm object. It has not learned from the dataset yet.

### Step 7 — Train the model using `fit()`

```python
model.fit(X_train, y_train)
```

This is the most important learning step.

- `X_train` supplies study hours and attendance.
- `y_train` supplies the corresponding known marks.
- `fit()` calculates the coefficients and intercept that best fit the training examples under the ordinary least-squares objective.

The model learns a relationship with this general form:

$$
\widehat{marks} =
b_0 + b_1(study\_hours) + b_2(attendance)
$$

### Step 8 — Make predictions for test records

```python
predictions = model.predict(X_test)
```

The model receives the test students' study hours and attendance. It returns predicted marks.

The actual marks are already available in `y_test`, so the program can compare actual and predicted results.

### Step 9 — Evaluate the model

```python
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)
```

The program calculates three metrics:

- **MAE:** average absolute prediction error, in marks.
- **RMSE:** square root of average squared error, in marks; larger errors receive more weight.
- **R²:** compares model performance with a baseline that predicts the test-set mean.

General interpretation:

| Metric | Better direction | Meaning |
|---|---|---|
| MAE | Lower | Smaller average absolute error |
| RMSE | Lower | Smaller error, with extra penalty for large misses |
| R² | Usually closer to 1 | Better than the mean baseline |

An R² of 0 means the model is no better than the mean baseline on that test set. A negative R² means it is worse than that baseline.

Do not judge a model from one metric alone. This is a small classroom dataset, so results can vary with the records and test split.

### Step 10 — Save the model

```python
joblib.dump(
    {"model": model, "features": FEATURES, "target": TARGET},
    MODEL_FILE,
)
```

The program saves a dictionary containing:

- The trained model object.
- The feature names and their expected order.
- The target column name.

This creates `student_marks_model.joblib`. The prediction script uses this file later.

---

## 7. Step-by-step explanation of `predict_marks.py`

### Step 1 — Check whether a trained model exists

```python
if not MODEL_FILE.exists():
    print("Trained model not found. First run: python train_model.py")
    return
```

If training has not been run, there is no saved model to load. The program asks the user to train first.

### Step 2 — Load the model

```python
saved = joblib.load(MODEL_FILE)
model = saved["model"]
features = saved["features"]
```

`joblib.load()` reads the saved dictionary.

- `model` is the trained Linear Regression object.
- `features` contains the expected input columns in the training order.

### Step 3 — Collect new student input

```python
study_hours = float(input("Enter average study hours per day: "))
attendance = float(input("Enter attendance percentage (0-100): "))
```

`input()` receives text. `float()` converts the entered values to numbers so they can be passed to the model.

### Step 4 — Validate input

The program checks that study hours are greater than zero and attendance is between 0 and 100.

If the user enters invalid numeric data or a value outside these checks, the program displays an error instead of making a prediction.

### Step 5 — Create a DataFrame for the new student

```python
student = pd.DataFrame(
    [[study_hours, attendance]],
    columns=features,
)
```

The model was trained with a two-column table. The new input must have the same feature names and order.

For example, if the user enters 5 hours and 85% attendance, the DataFrame represents:

| study_hours | attendance |
|---:|---:|
| 5 | 85 |

### Step 6 — Predict

```python
predicted_marks = float(model.predict(student)[0])
```

- `model.predict(student)` runs the learned equation.
- It returns an array of predictions.
- `[0]` selects the first result because we supplied one student.
- `float()` converts the result to a regular Python number.

The script then limits the displayed result to the 0–100 range. This is a display safeguard; it does not make the prediction guaranteed or improve the underlying model.

### Step 7 — Display the result

The program prints the input values and the estimated marks out of 100.

The result is an estimate from a small educational dataset, not a guaranteed exam result.

---

## 8. Install Python dependencies

Python 3.9 or later is recommended.

Create `requirements.txt` with:

```text
pandas
scikit-learn
joblib
```

Install the dependencies from the project directory:

```bash
python -m pip install -r requirements.txt
```

On Linux, use `python3` if `python` is not configured:

```bash
python3 -m pip install -r requirements.txt
```

Optional: create and activate a virtual environment.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install the requirements.

---

## 9. Run the complete practical

Open a terminal inside the `student_marks_prediction` folder.

### First: train the model

```bash
python train_model.py
```

The program reads and validates the CSV, splits the data, trains the model, prints metrics and actual-versus-predicted results, and saves:

```text
student_marks_model.joblib
```

### Second: predict marks for a new student

```bash
python predict_marks.py
```

Example input:

```text
Enter average study hours per day: 5
Enter attendance percentage (0-100): 85
```

The program displays an estimated mark. The exact prediction depends on the dataset and fitted model; do not memorize a fixed output.

---

## 10. Add new student records and observe the impact

Open `student_marks.csv` in Excel or a text editor.

**Keep the header exactly as follows:**

```csv
study_hours,attendance,marks
```

Add a new row with a known result. For example:

```csv
6,90,88
```

This represents a student who studied 6 hours per day, had 90% attendance, and scored 88 marks.

Now retrain:

```bash
python train_model.py
```

Then predict again:

```bash
python predict_marks.py
```

### Classroom experiment

To observe the effect of new data fairly:

1. Before editing the CSV, record MAE, RMSE, and R².
2. Run `predict_marks.py` with a fixed input, for example 5 hours and 85% attendance. Record the estimate.
3. Add one new labelled student row to the CSV.
4. Run `python train_model.py` again.
5. Enter the exact same 5 hours and 85% attendance in `predict_marks.py`.
6. Compare the new prediction and metrics with the earlier results.

The model may produce a different prediction because its coefficients are recalculated from the updated training data. Metrics may improve or worsen; adding a row does not guarantee better performance.

**Important:** Editing the CSV alone does not update the saved model. You must run `train_model.py` again. The prediction program uses the last model saved by the training program.

---

## 11. Classroom experiments

| Experiment | Change | Discuss |
|---|---|---|
| A | Add a realistic student with 2 study hours and 60% attendance | Does the prediction for similar inputs change? |
| B | Add a realistic student with 8 study hours and 95% attendance | How does the model use this labelled example? |
| C | Add an unrealistic record, such as 2 hours, 40% attendance, and 100 marks | How can incorrect data mislead a model? |
| D | Add several realistic student records | Do the metrics and predictions change? |
| E | Keep study hours fixed and change attendance | How does the predicted value respond? |
| F | Keep attendance fixed and change study hours | How does the predicted value respond? |

Use genuine or clearly labelled teaching examples. The model learns patterns from the records; it does not prove that study hours or attendance alone determine a student's result.

---

## 12. Common questions students may ask

### Q1. Why do we call this supervised learning?

Because the CSV contains input features and the known correct output (`marks`). The model learns from labelled examples.

### Q2. Why are there two input columns?

The project assumes both study hours and attendance may help estimate marks. The model uses both as features.

### Q3. Is this Simple or Multiple Linear Regression?

Multiple Linear Regression, because it uses two independent input features.

### Q4. What is `X`?

`X` is the input data: `study_hours` and `attendance`.

### Q5. What is `y`?

`y` is the target value: `marks`.

### Q6. What does `fit()` do?

It learns the coefficients and intercept from the training data.

### Q7. What does `predict()` do?

It uses the learned model to estimate marks for input records.

### Q8. Why do we split the dataset?

To keep some examples separate from training and use them to evaluate how the model performs on unseen records.

### Q9. Why save the model?

So a separate program can load and use the trained model without repeating training every time.

### Q10. Does adding a CSV row automatically change predictions?

No. Run `train_model.py` again to retrain and overwrite the saved model.

### Q11. Why can the prediction be different from the actual marks?

The dataset may be small or noisy, and the two features may not explain every factor that affects exam performance. A regression model estimates a relationship; it does not know every student's circumstances.

---

## 13. Troubleshooting

### Missing Python package

```bash
python -m pip install -r requirements.txt
```

### Model file not found

Run training first:

```bash
python train_model.py
```

### Dataset not found

Check that `student_marks.csv` is in the same folder as `train_model.py`.

### CSV validation error

Check:

- Header is exactly `study_hours,attendance,marks`.
- All required values are numeric.
- Required values are not blank.
- Study hours are greater than zero.
- Attendance is between 0 and 100.
- Marks are between 0 and 100.
- At least five complete records are present.

### Prediction input error

Enter numeric values. Study hours must be greater than zero and attendance must be from 0 to 100.

---

## 14. Important limitations to teach

- This is a small educational dataset, not a validated student assessment system.
- Linear Regression assumes a relationship that can be reasonably represented by a linear equation.
- Outliers and inaccurate records can affect the fitted coefficients.
- The model only knows the features supplied to it; other factors are not included.
- A relationship in the data does not prove cause and effect.
- Predictions outside the range of training examples may be unreliable.
- A good training result does not guarantee good performance on future students.
- The model's output is an estimate, not a guaranteed exam result.

---

## 15. Final revision table

| Concept | Meaning in this project |
|---|---|
| Supervised learning | Learns from student records with known marks |
| Features (`X`) | Study hours and attendance |
| Target (`y`) | Exam marks |
| Regression | Predicting a numerical value |
| Multiple Linear Regression | Using two or more input features |
| `fit()` | Learns model coefficients from training data |
| `predict()` | Estimates marks for new inputs |
| Training set | Records used to learn |
| Test set | Held-out records used for evaluation |
| MAE | Average absolute prediction error |
| RMSE | Error metric that penalizes larger misses more |
| R² | Compares model with a mean-prediction baseline |
| Joblib | Saves and loads the trained model |
| Retraining | Fitting the model again after updating labelled data |

---

## 16. Recommended teaching sequence

1. Open the CSV and explain each column.
2. Introduce supervised learning and labelled data.
3. Explain regression and numerical prediction.
4. Compare Simple and Multiple Linear Regression.
5. Introduce the equation, intercept, and coefficients.
6. Walk through `train_model.py` from imports to model saving.
7. Explain `X`, `y`, train/test split, `fit()`, and `predict()`.
8. Interpret MAE, RMSE, and R².
9. Walk through `predict_marks.py` and enter a new student's values.
10. Add a labelled row, retrain, and compare the result.

**Final takeaway:** The training program learns a relationship from historical student records. The prediction program reuses that learned relationship to estimate marks for a new student based on study hours and attendance.
