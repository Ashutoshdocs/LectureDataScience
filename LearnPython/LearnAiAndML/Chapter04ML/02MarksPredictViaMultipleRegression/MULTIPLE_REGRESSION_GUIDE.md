# 📘 Multiple Linear Regression: A Teaching Guide

A beginner-friendly guide to **what** Multiple Linear Regression is, **how** it works, and **how to implement it in Python**.

---

## 1. What is Multiple Linear Regression?

**Multiple Linear Regression** is a supervised machine learning algorithm used to predict a continuous numerical value using two or more independent input variables (features).

Unlike Simple Linear Regression, which uses only one input variable, Multiple Linear Regression considers multiple factors together to make a prediction.

### Real-World Examples

| Problem | Input Features (X) | Output (Y) |
|---|---|---|
| Student Marks Prediction | Study hours, attendance, previous marks | Final marks |
| House Price Prediction | Area, bedrooms, location score | House price |
| Employee Salary Prediction | Experience, education, job title | Salary |
| Sales Prediction | Advertising spend, price, discounts | Sales revenue |
| Car Price Prediction | Age, mileage, engine capacity | Car price |

It's a **Supervised Learning** algorithm because we train it using historical examples where the actual output is already known.

### Important Terminology

| Term | Meaning | In Our Demo |
|---|---|---|
| Feature (X) | Input variable | Study hours, attendance, etc. |
| Target (Y) | Output to predict | Final marks |
| Training Data | Historical examples | `train.csv` |
| Model | Learned mathematical equation | `model.pkl` |
| Coefficient | Weight assigned to each feature | `b1, b2, b3...` |
| Intercept | Starting value of the equation | `b0` |
| Prediction | Estimated output | Predicted final marks |

---

## 2. The Big Idea: One Input vs Multiple Inputs

Let's understand the difference using school mathematics.

### Simple Linear Regression

Uses ONE independent variable.

Example:

We want to predict student marks based only on study hours.

Mathematical equation:

```text
marks = m × study_hours + c
```

Example:

```text
marks = 3.6 × study_hours + 54.6
```

If a student studies for 6 hours:

```text
marks = 3.6 × 6 + 54.6

marks = 76.2
```

Only study hours are considered.

### Multiple Linear Regression

Now imagine that marks depend on five different factors:

1. Study hours
2. Attendance percentage
3. Previous exam marks
4. Assignments completed
5. Sleep hours

We cannot represent all these inputs using just one X variable.

Therefore, we extend the equation.

```text
marks = b0
      + b1 × study_hours
      + b2 × attendance
      + b3 × previous_marks
      + b4 × assignments
      + b5 × sleep_hours
```

Mathematical representation:

\[
\hat{Y}=b_0+b_1X_1+b_2X_2+b_3X_3+b_4X_4+b_5X_5
\]

Where:

| Symbol | Meaning |
|---|---|
| Y | Predicted final marks |
| b0 | Intercept |
| b1 | Study hours coefficient |
| b2 | Attendance coefficient |
| b3 | Previous marks coefficient |
| b4 | Assignments coefficient |
| b5 | Sleep hours coefficient |
| X1–X5 | Input values |

**Important:** Each coefficient represents the expected change in predicted marks when that particular feature increases by one unit, keeping all other features constant.

---

## 3. Visual Understanding: How Multiple Regression Works

In Simple Linear Regression:

- One input variable
- One output variable
- We find the best-fitting straight line.

In Multiple Linear Regression:

- Multiple input variables
- One output variable
- We find the best-fitting mathematical relationship.

For two input variables, we can visualize a regression plane.

<pre>
          Final Marks (Y)
                |
          100   |          / 
                |       /  Regression Plane
           80   |    /
                |  /
           60   |/
                +---------------- Attendance (X2)
               /
              /
        Study Hours (X1)
</pre>

With five input features, the mathematical relationship exists in a higher-dimensional feature space. We cannot visualize all five dimensions in an ordinary 2D or 3D graph.

---

## 4. How Does It Find the Best Equation?

The model does not know the correct coefficients initially.

It learns the coefficients by comparing predictions against actual values.

Let's understand this step by step.

### Step 1: Provide Training Data

Example:

| Study Hours | Attendance | Previous Marks | Assignments | Sleep | Actual Final Marks |
|---:|---:|---:|---:|---:|---:|
| 2 | 60 | 45 | 4 | 5 | 48 |
| 4 | 75 | 60 | 7 | 7 | 68 |
| 6 | 85 | 70 | 8 | 7 | 82 |
| 8 | 95 | 85 | 10 | 8 | 94 |

The model receives the input columns (X) and the actual final marks (Y).

### Step 2: Make Predictions

Initially, the model does not know the correct relationship.

It calculates predictions using its learned coefficients.

Example:

```text
Actual marks    = 80
Predicted marks = 75

Error = Predicted - Actual

Error = 75 - 80

Error = -5
```

The model predicted 5 marks less than the actual marks.

### Step 3: Calculate Mean Squared Error (MSE)

The model needs to measure how wrong its predictions are.

\[
MSE=\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i-y_i)^2
\]

Why square the errors?

- Positive and negative errors do not cancel each other.
- Large mistakes receive a bigger penalty.
- It provides a mathematical objective for finding the coefficients.

### Step 4: Find the Best Coefficients

The objective is to find coefficients that minimize the sum of squared prediction errors.

This is called **Ordinary Least Squares (OLS)**.

For Multiple Linear Regression, the matrix representation is:

\[
\mathbf{b}=(X^TX)^{-1}X^Ty
\]

This expression assumes the inverse exists. Practical implementations use numerically stable least-squares methods rather than explicitly calculating the inverse.

Scikit-learn's `LinearRegression()` solves the least-squares problem.

### Step 5: Gradient Descent (Alternative Learning Method)

Another approach is Gradient Descent.

Imagine standing on a hill and trying to reach its lowest point.

You take small steps downhill until you reach a minimum.

For Multiple Linear Regression:

1. Initialize coefficients.
2. Calculate predicted values.
3. Calculate MSE.
4. Calculate gradients for every coefficient.
5. Update coefficients.
6. Repeat until the error converges.

The general update rule:

\[
b_j=b_j-\alpha\frac{\partial MSE}{\partial b_j}
\]

Where:

- b_j = Current coefficient
- α = Learning rate
- Gradient = Direction of error reduction

The intercept is updated similarly.

**Important:** Scikit-learn's ordinary `LinearRegression()` uses least-squares optimization, not iterative Gradient Descent. Gradient Descent is useful for understanding an alternative optimization approach.

---

## 5. Understanding Coefficients with a Practical Example

Suppose the model learns the following hypothetical equation:

```text
marks = 10
      + 2.5 × study_hours
      + 0.2 × attendance
      + 0.4 × previous_marks
      + 1.5 × assignments
      + 0.8 × sleep_hours
```

Let's understand the coefficients.

| Feature | Coefficient | Interpretation |
|---|---:|---|
| Intercept | 10 | Baseline predicted marks |
| Study hours | 2.5 | One extra study hour adds 2.5 predicted marks |
| Attendance | 0.2 | One percentage-point increase adds 0.2 predicted marks |
| Previous marks | 0.4 | One extra previous mark adds 0.4 predicted marks |
| Assignments | 1.5 | One extra assignment adds 1.5 predicted marks |
| Sleep hours | 0.8 | One extra sleep hour adds 0.8 predicted marks |

These interpretations assume all other features remain unchanged.

### Try a Prediction

Student details:

```text
Study hours          = 6
Attendance           = 85
Previous marks       = 70
Assignments          = 8
Sleep hours          = 7
```

Substitute into the equation:

```text
marks = 10
      + 2.5 × 6
      + 0.2 × 85
      + 0.4 × 70
      + 1.5 × 8
      + 0.8 × 7
```

Calculate:

```text
marks = 10 + 15 + 17 + 28 + 12 + 5.6

marks = 87.6
```

Predicted marks = 87.6 / 100.

**Note:** These coefficients are illustrative. Your actual trained model will learn different coefficients from `train.csv`.

---

## 6. How Good Is the Model?

After training, we need to evaluate how well the model predicts unseen data.

| Metric | Meaning | Good Value |
|---|---|---|
| R² Score | How much variation in marks the model explains | Closer to 1 |
| MAE | Average absolute prediction error | Lower is better |
| MSE | Average squared prediction error | Lower is better |
| RMSE | Square root of MSE, in marks | Lower is better |

### R² Score

Suppose:

```text
R² = 0.95
```

This means the model explains approximately 95% of the variation in the target values on the evaluated dataset.

It does not mean that every prediction is 95% accurate.

### MAE

Suppose:

```text
MAE = 2.3
```

This means the average absolute prediction error is 2.3 marks.

### Why Train/Test Split?

We should not evaluate the model only on data it has already seen.

We divide the dataset:

```text
             train.csv
                 |
          Train/Test Split
                 |
          ----------------
          |              |
       80% Data       20% Data
          |              |
       Training        Testing
          |              |
       Learn the       Evaluate
        Model           Model
```

The model learns from training data and is evaluated using unseen test data.

---

## 7. Assumptions of Multiple Linear Regression

Multiple Linear Regression works best when the following assumptions are reasonably satisfied.

### 1. Linearity

The expected relationship between the features and target should be approximately linear.

### 2. Independence

Observations should be independent of each other.

### 3. Constant Variance (Homoscedasticity)

The variance of prediction errors should remain approximately constant across different predicted values.

### 4. Normally Distributed Errors

For traditional statistical inference, residuals should be approximately normally distributed.

### 5. No Severe Multicollinearity

Independent variables should not be excessively correlated with each other.

Example:

```text
Study hours
        |
        | Strong relationship
        |
Hours spent studying
```

If two features represent nearly the same information, coefficient estimates can become unstable.

---

## 8. Limitations of Multiple Linear Regression

1. **Linear relationship:** It cannot naturally capture complex nonlinear relationships.
2. **Outliers:** Extreme values can significantly influence coefficients.
3. **Multicollinearity:** Strong relationships between features can make coefficients unstable.
4. **Overfitting:** Too many features relative to the available training data can reduce generalization.
5. **Extrapolation:** Predictions outside the training-data range can be unrealistic.
6. **Correlation is not causation:** A positive coefficient does not prove that a feature causes the target to increase.

### Can Multiple Linear Regression Handle Curved Relationships?

Yes, by introducing transformed features such as:

```text
study_hours
study_hours²
study_hours³
```

This leads to Polynomial Regression, which can still be implemented using a linear regression estimator because it is linear in its coefficients.

---

## 9. Multiple Linear Regression in Python

We will use Scikit-learn.

### Step 1: Install Libraries

```bash
pip install pandas numpy scikit-learn joblib
```

### Step 2: Load Dataset

```python
import pandas as pd

df = pd.read_csv("train.csv")

print(df.head())
```

### Step 3: Define Input Features (X)

```python
X = df[
    [
        "study_hours",
        "attendance_percent",
        "previous_marks",
        "assignments_completed",
        "sleep_hours"
    ]
]
```

We have five independent variables.

### Step 4: Define Target (Y)

```python
y = df["final_marks"]
```

We have one dependent variable.

### Step 5: Split the Dataset

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
```

### Step 6: Create and Train the Model

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train, y_train)
```

What happens here?

- The model receives five input features.
- It compares them against actual final marks.
- It calculates the coefficients and intercept.
- It learns the best-fitting linear relationship.

### Step 7: Make Predictions

```python
y_pred = model.predict(X_test)

print(y_pred)
```

### Step 8: Evaluate the Model

```python
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

print("R2 Score:", r2_score(y_test, y_pred))

print("MAE:", mean_absolute_error(y_test, y_pred))

print("MSE:", mean_squared_error(y_test, y_pred))

print("RMSE:", mean_squared_error(y_test, y_pred) ** 0.5)
```

### Step 9: Understand the Learned Equation

```python
print("Intercept:", model.intercept_)

for feature, coefficient in zip(X.columns, model.coef_):
    print(feature, ":", coefficient)
```

This shows how much weight the model has assigned to each input feature.

### Step 10: Predict Marks for a New Student

```python
new_student = pd.DataFrame(
    [[6, 85, 70, 8, 7]],
    columns=X.columns
)

prediction = model.predict(new_student)

print("Predicted Final Marks:", prediction[0])
```

---

## 10. Save and Reuse the Trained Model

Instead of training the model every time, we can save it.

```python
import joblib

joblib.dump(
    {
        "model": model,
        "features": list(X.columns)
    },
    "model.pkl"
)
```

Later, load it:

```python
bundle = joblib.load("model.pkl")

model = bundle["model"]

features = bundle["features"]
```

We can now make predictions without retraining, provided the saved model and its dependencies are compatible.

Our practical also includes `predict.py`, which provides two ways to predict:

1. Read student data from a CSV file.
2. Enter student details manually.

---

## 11. Summary: Simple vs Multiple Linear Regression

| Comparison | Simple Linear Regression | Multiple Linear Regression |
|---|---|---|
| Input variables | One | Two or more |
| Output variables | One | One |
| Equation | Y = b0 + b1X1 | Y = b0 + b1X1 + b2X2 + ... |
| Example | Marks from study hours | Marks from five factors |
| Visualization | Straight line | Plane or higher-dimensional relationship |
| Complexity | Lower | Higher |
| Interpretation | One coefficient | Multiple coefficients |

### Remember

```text
SIMPLE LINEAR REGRESSION

One Input
    |
    v
Study Hours
    |
    v
Linear Regression
    |
    v
Predicted Marks


MULTIPLE LINEAR REGRESSION

Study Hours ---------|
Attendance ----------|
Previous Marks ------| 
Assignments ---------|----> Multiple Linear Regression
Sleep Hours ---------|               |
                                      v
                                Predicted Marks
```

---

## 12. Practice Exercises ✏️

Complete these exercises using the student marks prediction project.

### Exercise 1: Remove One Feature

Train the model using only:

```python
X = df[["study_hours"]]
```

Compare its R² score against the original five-feature model.

Question: Does using more features always improve the model's performance on unseen data?

### Exercise 2: Remove Previous Marks

Remove `previous_marks` from the feature list.

Compare:

- Original R²
- New R²
- Original MAE
- New MAE

Question: How does removing a feature impact the model?

### Exercise 3: Understand Coefficients

Print all coefficients:

```python
print(model.coef_)
```

Questions:

- Which coefficient is positive?
- Which coefficient is negative?
- Which coefficient has the largest absolute value?
- Why does coefficient magnitude alone not always indicate feature importance?

### Exercise 4: Add More Features

Add a new feature called:

```text
class_participation
```

Update your CSV and retrain the model.

Observe how the coefficients change.

### Exercise 5: Test Unusual Values

Predict marks for:

```text
Study hours = 0
Attendance = 0
Previous marks = 0
Assignments = 0
Sleep hours = 0
```

Does the predicted result make sense?

### Exercise 6: Compare Simple and Multiple Regression

Train two models:

- Model 1: Only study hours.
- Model 2: All five features.

Compare their performance on the same test split.

### Exercise 7: Polynomial Regression

Try adding:

```python
study_hours_squared = df["study_hours"] ** 2
```

Train another model and compare its performance.

Question: Can adding a squared feature help the model learn a curved relationship?

---

## 13. Final Takeaway

Multiple Linear Regression predicts one numerical output using multiple independent variables.

The algorithm:

1. Receives multiple input features.
2. Learns a coefficient for every feature.
3. Learns an intercept.
4. Minimizes the squared prediction errors using least squares.
5. Produces a mathematical equation.
6. Uses that equation to predict new values.

**Golden Rule:**

Simple Linear Regression = One independent variable.

Multiple Linear Regression = Two or more independent variables.

Both belong to the Linear Regression family because the model is linear in its coefficients.

**Our Student Marks Prediction project is an example of Multiple Linear Regression because it uses five independent variables to predict final marks.**
