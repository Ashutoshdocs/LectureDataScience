# Multiple Linear Regression – Student Marks Prediction

## 1. Project Overview

In this practical, we will build a Machine Learning model that predicts a student's marks using three different factors:

1. Study hours
2. Attendance percentage
3. Number of assignments completed

We will use **Multiple Linear Regression** from Scikit-learn.

### What are we trying to achieve?

Imagine a student provides the following information:

| Feature | Value |
|---|---:|
| Study hours | 6 |
| Attendance | 82% |
| Assignments completed | 8 |

Our model will use these three values to estimate the student's marks.

The important concept is that we are not predicting marks using just one factor. We are using multiple independent variables together.

---

## 2. What is Multiple Linear Regression?

Linear Regression is a supervised Machine Learning algorithm used to predict a numerical value.

Examples:

- Predicting student marks.
- Predicting house prices.
- Predicting employee salaries.
- Predicting monthly sales.
- Predicting electricity consumption.

When we use one independent variable, it is called **Simple Linear Regression**.

Example:

```text
Study Hours → Student Marks
```

When we use two or more independent variables, it is called **Multiple Linear Regression**.

Our project uses:

```text
Study Hours ───────┐
                   │
Attendance ────────┼──> Multiple Linear Regression ──> Marks
                   │
Assignments ───────┘
```

The model tries to understand how all three features are related to the target value.

---

## 3. Understanding the Mathematical Formula

Multiple Linear Regression uses the following equation:

\[
y = b_0 + b_1x_1 + b_2x_2 + b_3x_3
\]

Where:

| Symbol | Meaning |
|---|---|
| \(y\) | Predicted marks |
| \(b_0\) | Intercept |
| \(b_1\) | Coefficient for study hours |
| \(b_2\) | Coefficient for attendance |
| \(b_3\) | Coefficient for assignments |
| \(x_1\) | Study hours |
| \(x_2\) | Attendance |
| \(x_3\) | Assignments completed |

The model learns the values of the intercept and coefficients during training.

For example, imagine a trained model learns:

\[
y = 10 + 3x_1 + 0.4x_2 + 2x_3
\]

This is only an illustrative equation, not the actual equation learned by our program.

For a student with:

- Study hours = 6
- Attendance = 82
- Assignments = 8

The prediction would be:

\[
y = 10 + 3(6) + 0.4(82) + 2(8)
\]

\[
y = 10 + 18 + 32.8 + 16
\]

\[
y = 76.8
\]

The estimated marks would be 76.8.

**Important:** The actual model learns its own coefficients from the training data. We do not manually provide these values.

---

## 4. Project Dataset

We create a small dataset using Pandas.

```python
import pandas as pd

df = pd.DataFrame({
    "study_hours": [
        1, 2, 3, 4, 5, 6, 7, 8,
        2, 5, 7, 9, 3, 6, 8
    ],

    "attendance": [
        50, 55, 60, 65, 70, 75, 80, 90,
        58, 72, 85, 95, 62, 78, 88
    ],

    "assignments": [
        2, 3, 4, 5, 6, 7, 8, 10,
        3, 6, 9, 10, 4, 7, 9
    ],

    "marks": [
        28, 35, 42, 48, 57, 65, 73, 91,
        37, 60, 80, 96, 43, 69, 86
    ]
})

print(df)
```

### Understanding the columns

| Column | Description | Type |
|---|---|---|
| study_hours | Hours spent studying | Input |
| attendance | Attendance percentage | Input |
| assignments | Assignments completed | Input |
| marks | Student marks | Output |

We have 15 rows in this dataset.

Each row represents one student's observations.

### What is a feature?

A feature is an input variable used by a Machine Learning model to make predictions.

Our features are:

```python
study_hours
attendance
assignments
```

### What is a target?

The target is the value we want the model to predict.

Our target is:

```python
marks
```

---

## 5. Importing Required Libraries

```python
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_absolute_error, r2_score
```

### Understanding each import

**1. Pandas**

```python
import pandas as pd
```

Pandas is used to create and manipulate tabular data.

We use it to create our student dataset using a DataFrame.

**2. train_test_split**

```python
from sklearn.model_selection import train_test_split
```

This function divides our dataset into two parts:

- Training data
- Testing data

The model learns from training data and is evaluated on testing data.

**3. LinearRegression**

```python
from sklearn.linear_model import LinearRegression
```

This imports the Multiple Linear Regression algorithm.

The same `LinearRegression` class supports both simple and multiple linear regression. The number of input columns determines how many features the model uses.

**4. Evaluation metrics**

```python
from sklearn.metrics import mean_absolute_error, r2_score
```

We import two metrics:

- MAE: Measures the average absolute prediction error.
- R²: Measures how well the model explains variation in the target values.

---

## 6. Separating Features and Target

Our next step is to separate input variables from the output variable.

```python
X = df[["study_hours", "attendance", "assignments"]]

y = df["marks"]
```

### What is X?

`X` contains the independent variables or features.

```python
X = df[["study_hours", "attendance", "assignments"]]
```

We select three columns from the DataFrame.

Notice that we use double square brackets:

```python
df[["study_hours", "attendance", "assignments"]]
```

This returns a DataFrame containing multiple columns.

### What is y?

```python
y = df["marks"]
```

This contains the dependent variable or target.

We want our model to learn the relationship:

```text
X = Study Hours + Attendance + Assignments

y = Marks
```

### Visualizing X and y

| X: Study Hours | X: Attendance | X: Assignments | y: Marks |
|---:|---:|---:|---:|
| 1 | 50 | 2 | 28 |
| 2 | 55 | 3 | 35 |
| 3 | 60 | 4 | 42 |
| 4 | 65 | 5 | 48 |
| 5 | 70 | 6 | 57 |

The model uses the first three columns to learn how to predict the fourth column.

---

## 7. Splitting the Dataset into Training and Testing Data

```python
Xtr, Xte, ytr, yte = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=7
)
```

This is one of the most important steps in Machine Learning.

### Why do we split the data?

Suppose we give all 15 records to the model for training.

If we evaluate the model using those same 15 records, we are checking its performance on data it has already seen.

That does not provide a good indication of how well it can predict marks for new students.

Instead, we divide the dataset:

- 75% for training.
- 25% for testing.

### Understanding test_size

```python
test_size=0.25
```

This means 25% of the records will be used for testing.

We have 15 records.

\[
15 \times 0.25 = 3.75
\]

Scikit-learn rounds this up to 4 test records.

Therefore:

| Dataset | Records |
|---|---:|
| Total | 15 |
| Training | 11 |
| Testing | 4 |

### Understanding random_state

```python
random_state=7
```

This controls the randomness of the split.

If we execute the program repeatedly using the same random state, we get the same training and testing records.

This is useful for reproducible experiments.

### Understanding the four variables

```python
Xtr
```
Training input features.

```python
Xte
```
Testing input features.

```python
ytr
```
Actual target values for training records.

```python
yte
```
Actual target values for testing records.

The relationship is:

| Variable | Contains |
|---|---|
| Xtr | Training inputs |
| ytr | Training marks |
| Xte | Testing inputs |
| yte | Actual testing marks |

---

## 8. Creating the Linear Regression Model

```python
model = LinearRegression()
```

This creates a Linear Regression model object.

At this point, the model has not learned anything from our dataset.

It is just an instance of the algorithm.

### What happens internally?

The model will learn:

- An intercept.
- A coefficient for study hours.
- A coefficient for attendance.
- A coefficient for assignments.

It tries to find a linear equation that minimizes the sum of squared errors on the training data.

---

## 9. Training the Model Using fit()

```python
model.fit(Xtr, ytr)
```

This is where Machine Learning actually happens.

The `fit()` method trains the model.

It receives:

```python
Xtr
```

The training input features.

And:

```python
ytr
```

The actual marks corresponding to those features.

### What does the model learn?

It attempts to learn the relationship:

\[
Marks = b_0 + b_1(StudyHours)
+ b_2(Attendance)
+ b_3(Assignments)
\]

The model calculates suitable coefficients and intercept based on the training data.

### Important distinction

```python
model = LinearRegression()
```

Creates the model.

```python
model.fit(Xtr, ytr)
```

Trains the model.

```python
model.predict(Xte)
```

Uses the trained model to make predictions.

---

## 10. Understanding Model Coefficients and Intercept

After training, we can inspect what the model has learned.

```python
print("Intercept:", model.intercept_)

print("Coefficients:", model.coef_)
```

The model has three coefficients because we provided three input features.

To make the output easier to understand:

```python
for feature, coefficient in zip(X.columns, model.coef_):
    print(feature, ":", coefficient)
```

Example output format:

```text
Intercept: ...
study_hours : ...
attendance : ...
assignments : ...
```

The actual values are calculated when the program runs.

### What does a coefficient mean?

A coefficient represents the estimated change in predicted marks for a one-unit increase in that feature, while the other features are held constant.

For example, if the coefficient of study hours is 3:

- Increasing study hours by one hour.
- Keeping attendance and assignments unchanged.

Would increase the model's predicted marks by approximately 3.

This is an interpretation of the model's mathematical relationship, not proof that studying one additional hour causes exactly three extra marks.

---

## 11. Making Predictions on Testing Data

```python
pred = model.predict(Xte)
```

The `predict()` method uses the trained model to estimate marks for the testing records.

Remember:

- `Xte` contains input features.
- `yte` contains actual marks.
- `pred` contains predicted marks.

Let's compare them:

```python
comparison = pd.DataFrame({
    "Actual Marks": yte.values,
    "Predicted Marks": pred
})

print(comparison)
```

Example output structure:

| Actual Marks | Predicted Marks |
|---:|---:|
| Actual value | Predicted value |
| Actual value | Predicted value |
| Actual value | Predicted value |
| Actual value | Predicted value |

The actual numerical predictions are generated by running the program.

### Why compare actual and predicted marks?

We want to understand how close the model's predictions are to the actual values.

For example:

| Actual | Predicted | Absolute Error |
|---:|---:|---:|
| 70 | 68 | 2 |
| 80 | 76 | 4 |
| 60 | 64 | 4 |

A smaller difference generally means a more accurate prediction for that record.

---

## 12. Understanding Mean Absolute Error (MAE)

Our code:

```python
mean_absolute_error(yte, pred)
```

MAE measures the average absolute difference between actual and predicted values.

Formula:

\[
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|
\]

Where:

- \(y_i\) = Actual marks.
- \(\hat{y}_i\) = Predicted marks.
- \(n\) = Number of testing records.

### Example

Suppose actual marks are:

```text
70, 80, 60, 90
```

And predicted marks are:

```text
68, 76, 64, 85
```

Absolute errors:

```text
2, 4, 4, 5
```

Therefore:

\[
MAE = \frac{2+4+4+5}{4}
\]

\[
MAE = 3.75
\]

The average absolute prediction error is 3.75 marks.

**How to interpret MAE:**

- Lower MAE is generally better.
- MAE of 0 means perfect predictions on the evaluated records.
- MAE is expressed in the same unit as the target, which is marks in this project.

---

## 13. Understanding R² Score

Our code:

```python
r2_score(yte, pred)
```

R² is also called the coefficient of determination.

It measures how well the model explains the variation in the actual target values.

A simplified interpretation:

| R² value | General interpretation |
|---:|---|
| 1.0 | Perfect predictions |
| 0.8 | Strong fit in many contexts |
| 0.5 | Some variation explained |
| 0.0 | No improvement over predicting the test-set mean |
| Negative | Worse than predicting the test-set mean |

R² formula:

\[
R^2 = 1 -
\frac{\sum (y_i-\hat{y}_i)^2}
{\sum (y_i-\bar{y})^2}
\]

Where:

- \(y_i\) = Actual marks.
- \(\hat{y}_i\) = Predicted marks.
- \(\bar{y}\) = Mean of actual marks.

**Important:** R² is not a percentage accuracy score. A value of 0.8 does not mean the model is 80% accurate.

Also, because our dataset is very small, R² can change significantly depending on which records are selected for testing.

---

## 14. Understanding the Evaluation Code

```python
print(
    "MAE:",
    round(mean_absolute_error(yte, pred), 2),
    "R2:",
    round(r2_score(yte, pred), 3)
)
```

Let's break this down.

### mean_absolute_error()

Calculates the average absolute prediction error.

### round(value, 2)

Rounds the MAE to two decimal places.

Example:

```python
round(3.45678, 2)
```

Output:

```text
3.46
```

### r2_score()

Calculates the R² score.

### round(value, 3)

Rounds the R² score to three decimal places.

Example:

```python
round(0.87654, 3)
```

Output:

```text
0.877
```

---

## 15. Predicting Marks for a New Student

Now comes the interesting part.

We have trained our model and evaluated it.

We want to predict marks for a student who was not included in the original dataset.

Our code:

```python
new_student = pd.DataFrame({
    "study_hours": [6],
    "attendance": [82],
    "assignments": [8]
})

prediction = model.predict(new_student)

print("Predicted Marks:", prediction[0])
```

### Why are we using a DataFrame?

During training, our model received a Pandas DataFrame with these feature names:

```python
study_hours
attendance
assignments
```

When predicting, we provide a DataFrame with the same feature names and column order.

This makes it clear which value belongs to which feature.

### Why are values inside square brackets?

```python
"study_hours": [6]
```

We are providing one row of input data.

The model expects multiple features for each sample.

The DataFrame has this structure:

| study_hours | attendance | assignments |
|---:|---:|---:|
| 6 | 82 | 8 |

### Understanding prediction[0]

```python
model.predict(new_student)
```

Returns an array of predictions.

For one student, it might look like:

```python
[75.42]
```

To retrieve the first prediction:

```python
prediction[0]
```

We then round it:

```python
round(prediction[0], 2)
```

The predicted value is an estimate, not a guaranteed exam result.

---

## 16. Complete Program with Detailed Comments

Create a file named:

`multiple_linear_regression.py`

```python
# Import Pandas to create and manage tabular data
import pandas as pd

# Import function to split the dataset into training and testing sets
from sklearn.model_selection import train_test_split

# Import Multiple Linear Regression algorithm
from sklearn.linear_model import LinearRegression

# Import metrics to evaluate model performance
from sklearn.metrics import mean_absolute_error, r2_score


# --------------------------------------------------
# STEP 1: CREATE THE DATASET
# --------------------------------------------------

# Create a DataFrame containing student information
df = pd.DataFrame({

    # Number of hours spent studying
    "study_hours": [
        1, 2, 3, 4, 5, 6, 7, 8,
        2, 5, 7, 9, 3, 6, 8
    ],

    # Student attendance percentage
    "attendance": [
        50, 55, 60, 65, 70, 75, 80, 90,
        58, 72, 85, 95, 62, 78, 88
    ],

    # Number of assignments completed
    "assignments": [
        2, 3, 4, 5, 6, 7, 8, 10,
        3, 6, 9, 10, 4, 7, 9
    ],

    # Actual marks obtained by students
    "marks": [
        28, 35, 42, 48, 57, 65, 73, 91,
        37, 60, 80, 96, 43, 69, 86
    ]
})


# Display the complete dataset
print("Student Dataset:")
print(df)


# --------------------------------------------------
# STEP 2: SEPARATE FEATURES AND TARGET
# --------------------------------------------------

# X contains all input columns used for prediction
X = df[["study_hours", "attendance", "assignments"]]

# y contains the target column we want to predict
y = df["marks"]


# --------------------------------------------------
# STEP 3: SPLIT DATA INTO TRAINING AND TESTING
# --------------------------------------------------

# 75% of the records are used for training
# 25% of the records are used for testing
# random_state makes the split reproducible
Xtr, Xte, ytr, yte = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=7
)


# Display the number of records in each dataset
print("\nTraining records:", len(Xtr))
print("Testing records:", len(Xte))


# --------------------------------------------------
# STEP 4: CREATE THE MODEL
# --------------------------------------------------

# Create a Linear Regression model
model = LinearRegression()


# --------------------------------------------------
# STEP 5: TRAIN THE MODEL
# --------------------------------------------------

# The model learns relationships between input features and marks
model.fit(Xtr, ytr)


# --------------------------------------------------
# STEP 6: DISPLAY LEARNED COEFFICIENTS
# --------------------------------------------------

# Display the intercept learned by the model
print("\nIntercept:", model.intercept_)

# Display the coefficient for each feature
for feature, coefficient in zip(X.columns, model.coef_):

    print(feature, "coefficient:", coefficient)


# --------------------------------------------------
# STEP 7: PREDICT MARKS FOR TESTING DATA
# --------------------------------------------------

# Predict marks using the testing input features
pred = model.predict(Xte)


# --------------------------------------------------
# STEP 8: COMPARE ACTUAL AND PREDICTED VALUES
# --------------------------------------------------

# Create a DataFrame to compare actual marks with predictions
comparison = pd.DataFrame({

    "Actual Marks": yte.values,

    "Predicted Marks": pred

})

print("\nActual vs Predicted Marks:")
print(comparison)


# --------------------------------------------------
# STEP 9: EVALUATE MODEL PERFORMANCE
# --------------------------------------------------

# MAE measures average absolute prediction error
mae = mean_absolute_error(yte, pred)

# R2 measures how well the model explains target variation
r2 = r2_score(yte, pred)

print("\nModel Evaluation:")

print("MAE:", round(mae, 2))

print("R2 Score:", round(r2, 3))


# --------------------------------------------------
# STEP 10: PREDICT MARKS FOR A NEW STUDENT
# --------------------------------------------------

# Create a new student's input data
new_student = pd.DataFrame({

    "study_hours": [6],

    "attendance": [82],

    "assignments": [8]

})


# Use the trained model to estimate marks
new_prediction = model.predict(new_student)


# Display the estimated marks
print("\nNew Student Estimate:", round(new_prediction[0], 2))
```

---

## 17. Complete Machine Learning Workflow

Remember this workflow because it applies to many supervised Machine Learning projects.

```text
                Student Dataset
                       |
                       v
              Separate X and y
                       |
                       v
             Train/Test Split
                       |
              +--------+--------+
              |                 |
              v                 v
         Training Data      Testing Data
              |
              v
        Create Model
              |
              v
        model.fit()
              |
              v
        Trained Model
              |
              v
        model.predict()
              |
              v
       Compare Predictions
              |
              v
        Evaluate MAE / R²
              |
              v
       Predict New Student
```

The most important methods are:

| Method | Purpose |
|---|---|
| `train_test_split()` | Divides the dataset |
| `LinearRegression()` | Creates the algorithm |
| `fit()` | Trains the model |
| `predict()` | Makes predictions |
| `mean_absolute_error()` | Measures average absolute error |
| `r2_score()` | Measures explained variation |

---

## 18. Simple Linear Regression vs Multiple Linear Regression

| Simple Linear Regression | Multiple Linear Regression |
|---|---|
| Uses one input feature | Uses two or more input features |
| Predicts using one variable | Predicts using multiple variables |
| Example: Study hours → Marks | Study hours + Attendance + Assignments → Marks |
| One coefficient | Multiple coefficients |
| Easier to visualize in 2D | More difficult to visualize |

Both algorithms use the same Scikit-learn class:

```python
LinearRegression()
```

The difference is the number of input columns passed to the model.

---

## 19. Important Limitations of This Project

This is a teaching dataset with only 15 records.

It is useful for understanding how Multiple Linear Regression works, but it is not sufficient to build a reliable real-world student performance prediction system.

Remember:

1. A very small dataset can produce unstable evaluation results.
2. The relationships in this artificial dataset are simplified.
3. Attendance, study hours, and assignments cannot explain every factor affecting marks.
4. A model can produce predictions outside the expected marks range.
5. A prediction is an estimate, not a guaranteed result.

For a real project, collect a larger, representative dataset and evaluate the model on data it has never seen.

---

## 20. Student Practice Exercises

### Beginner Level

1. Add a new column called `sleep_hours` to the dataset.
2. Display the first five records using `head()`.
3. Display the dataset dimensions using `shape`.
4. Print only the input features.
5. Print only the target column.

### Intermediate Level

6. Change `test_size` from 0.25 to 0.20. What changes?
7. Change `random_state` from 7 to 42. Do the predictions change?
8. Display the coefficients for all three features.
9. Print actual marks and predicted marks side by side.
10. Calculate MAE manually using the actual and predicted values.

### Advanced Level

11. Add `sleep_hours` as a fourth feature.
12. Compare the model with and without the new feature.
13. Try a larger dataset.
14. Compare training MAE with testing MAE.
15. Explain why a negative R² score can occur.

---

## 21. Key Takeaways

By completing this practical, you should understand:

- What Multiple Linear Regression is.
- How multiple features are used to predict one numerical target.
- The difference between independent variables and dependent variables.
- How to separate X and y using Pandas.
- Why we split data into training and testing sets.
- How `LinearRegression()` creates a model.
- How `fit()` trains a model.
- How `predict()` estimates new values.
- What coefficients and intercept represent.
- How MAE and R² evaluate model performance.
- How to predict marks for a completely new student.

**Final concept to remember:**

Simple Linear Regression uses one input variable to predict an output.

Multiple Linear Regression uses multiple input variables together to predict an output.

In this project:

\[
\boxed{
Marks = f(StudyHours, Attendance, Assignments)
}
\]

This is the foundation of many real-world regression problems.