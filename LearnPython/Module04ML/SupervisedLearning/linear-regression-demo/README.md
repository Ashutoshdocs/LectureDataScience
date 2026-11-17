# Linear Regression in Python --- Teaching Practical

A beginner-friendly, hands-on lesson that explains **Linear
Regression**, how it learns from data, how to train a model in Python,
and how to make predictions for new values.

------------------------------------------------------------------------

## 1. Learning objectives

By the end of this practical, students should be able to:

1.  Explain what supervised learning means.
2.  Describe Linear Regression in simple terms.
3.  Identify the independent variable (`X`) and dependent variable
    (`y`).
4.  Understand the line of best fit, slope, and intercept.
5.  Train a Linear Regression model using `scikit-learn`.
6.  Make predictions for new data.
7.  Evaluate a model using MAE, MSE, RMSE, and R².
8.  Understand why predictions are not always exactly equal to actual
    values.

------------------------------------------------------------------------

## 2. What is Linear Regression?

Linear Regression is a **supervised machine learning algorithm** used to
predict a numerical value by learning the relationship between input
data and an output.

For example:

-   Input: number of hours a student studies
-   Output: marks scored by the student

The model examines example records where both study hours and marks are
known. It learns a relationship and uses that relationship to estimate
marks for a new number of study hours.

### Simple real-world examples

  Input (X)             Output (y)
  --------------------- ---------------
  Hours studied         Exam marks
  Years of experience   Salary
  House area            House price
  Advertising spend     Sales
  Distance travelled    Fuel consumed

**Important:** Linear Regression predicts a continuous numerical value.
It is a regression task, not a classification task.

------------------------------------------------------------------------

## 3. How does Linear Regression work?

Imagine that we have historical student data. Each student has a known
number of study hours and a known exam score.

The algorithm tries to find a straight line that represents the
relationship between these two values. This is called the **line of best
fit**.

The model uses the line to estimate the output for an input it has not
seen before.

### The equation

For simple Linear Regression:

\[ `\hat{y}`{=tex} = b_0 + b_1x \]

Where:

-   `x` = input feature, such as study hours
-   `ŷ` = predicted output, such as predicted marks
-   `b₀` = intercept; the predicted output when `x = 0`
-   `b₁` = slope or coefficient; how much the prediction changes when
    `x` increases by one unit

The hat on `ŷ` means that this is a **predicted** value, not necessarily
the actual value.

### Example

Suppose a trained model learns:

\[ `\hat{y}`{=tex} = 20 + 5x \]

If a student studies for 6 hours:

\[ `\hat{y}`{=tex} = 20 + (5 `\times 6`{=tex}) = 50 \]

The model predicts **50 marks**.

Here, `20` is the intercept and `5` is the slope. The model predicts an
increase of 5 marks for every additional study hour, within the range
where this linear relationship is reasonable.

> This equation is an illustrative example. The actual coefficient and
> intercept are learned from the training dataset.

------------------------------------------------------------------------

## 4. Understand actual values, predicted values, and errors

A prediction will not always match the actual value.

  -----------------------------------------------------------------------
        Study hours      Actual marks   Predicted marks   Error (actual −
                                                               predicted)
  ----------------- ----------------- ----------------- -----------------
                  2                30                31                -1

                  4                45                41                 4

                  6                50                51                -1

                  8                65                61                 4

                 10                70                71                -1
  -----------------------------------------------------------------------

The difference between an actual value and a predicted value is called a
**residual**.

\[ Residual = Actual - Predicted \]

Linear Regression using ordinary least squares chooses the line that
minimizes the **sum of squared residuals** on the training data.

Why square the residuals?

-   Positive and negative errors should not cancel each other.
-   Larger errors receive a larger penalty.
-   Squared errors are mathematically convenient for fitting a linear
    model.

A model does not need to pass through every observed point. It aims to
fit the overall pattern.

------------------------------------------------------------------------

## 5. Project structure

Create a folder named `linear-regression-demo`:

``` text
linear-regression-demo/
│
├── data/
│   └── student_marks.csv
│
├── train_model.py
├── predict.py
├── requirements.txt
└── README.md
```

The CSV file contains the sample training data. The training program
loads it, trains the model, evaluates it, and displays a graph. The
prediction program uses the trained model to predict marks for new
study-hour values.

------------------------------------------------------------------------

## 6. Step 1 --- Create the dataset

Create `data/student_marks.csv`:

``` csv
hours_studied,marks
1,15
2,20
3,28
4,35
5,42
6,48
7,55
8,60
9,68
10,75
11,80
12,88
```

Explain to students:

-   Each row represents one student's observation.
-   `hours_studied` is the input feature (`X`).
-   `marks` is the target (`y`) that we want to predict.
-   The model learns from these labelled examples.

The dataset is intentionally small and nearly linear so that students
can focus on the algorithm before working with more complex data.

------------------------------------------------------------------------

## 7. Step 2 --- Install the required libraries

Create `requirements.txt`:

``` text
pandas
scikit-learn
matplotlib
joblib
```

Create a virtual environment (recommended):

### Windows

``` bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

``` bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Check Python and pip:

``` bash
python --version
pip --version
```

------------------------------------------------------------------------

## 8. Step 3 --- Train the Linear Regression model

Create `train_model.py`:

``` python
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# 1. Load the dataset
data = pd.read_csv("data/student_marks.csv")

print("First five rows:")
print(data.head())

# 2. Separate input feature (X) and target (y)
X = data[["hours_studied"]]
y = data["marks"]

# 3. Split data into training and testing sets
# The model learns from training data and is evaluated on test data.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

# 4. Create the Linear Regression model
model = LinearRegression()

# 5. Train the model
model.fit(X_train, y_train)

# 6. Predict using the test inputs
y_pred = model.predict(X_test)

# 7. Display the learned equation
print("\nModel details")
print("Intercept:", model.intercept_)
print("Slope / Coefficient:", model.coef_[0])

print(
    f"Learned equation: marks = "
    f"{model.intercept_:.2f} + ({model.coef_[0]:.2f} * hours_studied)"
)

# 8. Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("\nModel evaluation")
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# 9. Compare actual and predicted values
comparison = pd.DataFrame({
    "Hours Studied": X_test["hours_studied"].values,
    "Actual Marks": y_test.values,
    "Predicted Marks": y_pred.round(2)
})

comparison["Error"] = (
    comparison["Actual Marks"] - comparison["Predicted Marks"]
).round(2)

print("\nActual vs Predicted")
print(comparison.sort_values("Hours Studied").to_string(index=False))

# 10. Plot the original data and the regression line
plt.scatter(
    X["hours_studied"],
    y,
    label="Actual data"
)

# Draw the fitted line across the observed input range
plt.plot(
    X["hours_studied"],
    model.predict(X),
    label="Regression line"
)

plt.xlabel("Hours Studied")
plt.ylabel("Marks")
plt.title("Student Marks Prediction — Linear Regression")
plt.legend()
plt.grid(True)
plt.show()

# 11. Save the trained model
joblib.dump(model, "student_marks_model.pkl")
print("\nModel saved as student_marks_model.pkl")
```

### Explain the training flow

1.  `pd.read_csv()` loads the dataset.
2.  `X` contains the input feature; `y` contains the value to predict.
3.  `train_test_split()` keeps some records aside for testing.
4.  `LinearRegression()` creates the algorithm object.
5.  `model.fit()` learns the relationship from training data.
6.  `model.predict()` estimates marks for the test inputs.
7.  The metrics help us evaluate how well the model performed.
8.  `joblib.dump()` saves the trained model for later use.

**Teaching point:** `fit()` is the learning/training step. `predict()`
is the inference step. A model should be evaluated on data that was not
used to train it.

------------------------------------------------------------------------

## 9. Step 4 --- Predict marks for new students

Create `predict.py`:

``` python
import joblib
import pandas as pd

# Load the previously trained model
model = joblib.load("student_marks_model.pkl")

# Enter new study-hour values
new_students = pd.DataFrame({
    "hours_studied": [3.5, 5, 7.5, 9, 13]
})

# Generate predictions
predictions = model.predict(new_students)

# Display results
results = new_students.copy()
results["predicted_marks"] = predictions.round(2)

print("Predictions for new students:")
print(results.to_string(index=False))
```

Run it after training:

``` bash
python predict.py
```

Discuss the prediction for 13 study hours. The training data only
contains values from 1 to 12 hours. Predicting outside that range is
called **extrapolation**. The model can produce a number, but the
prediction may be unreliable because the learned relationship may not
continue beyond the observed data.

------------------------------------------------------------------------

## 10. Step 5 --- Run the complete project

From inside the `linear-regression-demo` folder:

``` bash
pip install -r requirements.txt
python train_model.py
python predict.py
```

Expected files after training:

``` text
linear-regression-demo/
├── data/
│   └── student_marks.csv
├── train_model.py
├── predict.py
├── requirements.txt
├── README.md
└── student_marks_model.pkl
```

The exact metric values depend on the train/test split and dataset.
Students should run the code and interpret their own output rather than
memorizing a fixed score.

------------------------------------------------------------------------

## 11. Understand the evaluation metrics

### MAE --- Mean Absolute Error

The average absolute difference between actual and predicted values.

-   Easy to interpret in the target's unit.
-   If MAE is 3, predictions are off by 3 marks on average, in absolute
    terms.

### MSE --- Mean Squared Error

The average of squared prediction errors.

-   Penalizes large errors more strongly.
-   Its unit is the square of the target unit.

### RMSE --- Root Mean Squared Error

The square root of MSE.

-   Expressed in the same unit as the target.
-   More sensitive to large errors than MAE.

### R² --- Coefficient of Determination

Measures how well the model explains variation in the target compared
with a baseline that predicts the test-set mean.

-   `1.0`: perfect predictions on the evaluated data.
-   `0.0`: no better than the mean baseline.
-   Negative: worse than that baseline.

**Important:** A high R² does not automatically mean a model is useful
or reliable. Check the test data, errors, data quality, and whether the
relationship makes sense.

------------------------------------------------------------------------

## 12. What happens if we add new data?

Ask students to add another row to `data/student_marks.csv`, for
example:

``` csv
13,92
```

Then run:

``` bash
python train_model.py
python predict.py
```

Discuss:

1.  Did the slope change?
2.  Did the intercept change?
3.  Did the evaluation metrics change?
4.  Did predictions for the same input values change?

The model is not automatically updated when the CSV changes. It must be
trained again by running `train_model.py`. The new row can affect the
fitted line because the model learns from the available training
records.

For a fair evaluation, use enough representative data and keep a
separate test set. With a very small dataset, evaluation scores can
change substantially depending on which rows are selected for testing.

------------------------------------------------------------------------

## 13. Common student questions

### Q1. Why is it called Linear Regression?

Because the model represents the relationship using a linear equation.
In simple Linear Regression, this appears as a straight line in a
two-dimensional graph.

### Q2. Does the line pass through every data point?

No. It is the line that best fits the observations according to the
least-squares objective. Individual observations can be above or below
the line.

### Q3. Why are predictions different from actual values?

The data may contain noise, missing factors, measurement errors, or a
relationship that is not perfectly linear. The model only uses the
features supplied to it.

### Q4. What is the difference between `fit()` and `predict()`?

-   `fit(X, y)` learns model parameters from labelled training data.
-   `predict(X)` uses the learned model to estimate outputs for input
    data.

### Q5. What is the difference between slope and intercept?

-   Slope tells us how much the predicted output changes for a one-unit
    increase in the input.
-   Intercept is the model's predicted output when the input is zero.

### Q6. Can Linear Regression use more than one input feature?

Yes. That is called **Multiple Linear Regression**. For example, marks
could be predicted using study hours, attendance, and assignment score.

### Q7. Can Linear Regression predict values outside the dataset range?

It can calculate them, but this is extrapolation and may be unreliable.
Do not assume the same relationship continues indefinitely.

### Q8. Is Linear Regression used for classification?

Normally, no. It is designed to predict numerical values. Classification
algorithms predict categories or classes.

------------------------------------------------------------------------

## 14. Classroom activities

### Activity 1 --- Change the input

Change the values in `new_students` inside `predict.py`. Predict marks
for 2, 4, 6, and 10 hours. Compare the outputs.

### Activity 2 --- Add a new observation

Add a row to the CSV, retrain the model, and compare the learned slope
and intercept.

### Activity 3 --- Introduce an unusual observation

Add an observation such as:

``` csv
6,10
```

Retrain and observe how an unusual point can influence the fitted line
and evaluation metrics. Discuss why data validation matters.

### Activity 4 --- Predict outside the training range

Try 15 or 20 study hours. Discuss extrapolation and why a numerical
answer is not necessarily a trustworthy answer.

### Activity 5 --- Build a different prediction problem

Create a new CSV with:

-   `experience_years`
-   `salary_lakh`

Train a new Linear Regression model to predict salary from experience.
Keep the input and target columns clear.

------------------------------------------------------------------------

## 15. Important limitations

-   Linear Regression assumes the relationship can be reasonably
    represented by a linear function.
-   Outliers can strongly influence the fitted line.
-   Missing, incorrect, or biased data can lead to poor predictions.
-   A relationship in the data does not prove that one variable causes
    another.
-   Extrapolation beyond the training range can be unreliable.
-   Real-world models often need more data, more relevant features,
    validation, and monitoring.

------------------------------------------------------------------------

## 16. Quick revision

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Supervised learning                 Learning from examples that include
                                      known answers

  Feature (`X`)                       Input used by the model

  Target (`y`)                        Output the model learns to predict

  Training                            Learning patterns and parameters
                                      from data

  Testing                             Evaluating performance on held-out
                                      data

  Slope / coefficient                 Change in predicted output for one
                                      unit of input

  Intercept                           Predicted output when input is zero

  Residual                            Actual value minus predicted value

  MAE                                 Average absolute error

  MSE                                 Average squared error

  RMSE                                Square root of MSE

  R²                                  Performance relative to a
                                      mean-prediction baseline
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 17. Final teaching flow

Teach the practical in this order:

1.  Explain supervised learning and numerical prediction.
2.  Show the CSV and identify `X` and `y`.
3.  Explain the straight line, slope, and intercept.
4.  Explain actual values, predictions, and residuals.
5.  Install libraries and run the training program.
6.  Read the learned equation and evaluation metrics.
7.  Examine the scatter plot and regression line.
8.  Run predictions for new students.
9.  Add new data, retrain, and compare results.
10. Discuss limitations and real-world use cases.

**Final takeaway:** Linear Regression learns a relationship from
historical labelled data and uses that relationship to predict a
numerical output for new inputs.
