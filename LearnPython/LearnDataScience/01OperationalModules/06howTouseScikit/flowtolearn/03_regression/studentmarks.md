# Simple Linear Regression Using Scikit-learn
## Predicting Student Marks Based on Study Hours

# 1. What Is This Program Doing?

Imagine you are a teacher.

You have observed students studying for different numbers of hours and recorded their examination marks.

You collected the following information:

| Student | Study Hours | Exam Marks |
|---|---:|---:|
| A | 1 | 30 |
| B | 2 | 35 |
| C | 3 | 42 |
| D | 4 | 48 |
| E | 5 | 55 |
| F | 6 | 60 |
| G | 7 | 68 |
| H | 8 | 72 |
| I | 9 | 80 |
| J | 10 | 88 |

Now imagine a new student asks:

**"If I study for 7.5 hours, approximately how many marks might I get?"**

Instead of manually guessing, we can use Machine Learning.

We will train a Linear Regression model using historical data.

The model learns the relationship between:

- Study hours (Input)
- Examination marks (Output)

After learning, we can provide new study hours and ask the model to predict the marks.

This is called **Simple Linear Regression** because we use only one input feature to predict one numerical output.

# 2. What Is Linear Regression?

Linear Regression is a supervised Machine Learning algorithm used to predict numerical values.

Examples:

| Input | Predicted Output |
|---|---|
| Study hours | Exam marks |
| House area | House price |
| Years of experience | Salary |
| Advertising budget | Sales |
| Temperature | Electricity demand |

The algorithm tries to find a mathematical relationship between input and output.

The basic equation is:

\[
y = mx+c
\]

Where:

- \(y\) = Predicted output.
- \(x\) = Input feature.
- \(m\) = Slope (coefficient).
- \(c\) = Intercept.

For our example:

\[
Marks = m \times StudyHours + c
\]

The model learns the values of \(m\) and \(c\) from historical data.

# 3. Complete Python Program

```python
"""Predict marks from one feature: study hours."""

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

X = np.arange(1, 11).reshape(-1, 1)

y = np.array([30,35,42,48,55,60,68,72,80,88])

model = LinearRegression().fit(X, y)

print(
    "Prediction for 7.5 study hours:",
    round(model.predict([[7.5]])[0], 2)
)

print(
    "Training MAE (illustration only):",
    round(mean_absolute_error(y, model.predict(X)), 2)
)
```

Now let's understand every line.

# 4. Step 1: Import Libraries

```python
import numpy as np
```

We import NumPy.

Why?

Because we need to create numerical arrays for our input and output data.

Next:

```python
from sklearn.linear_model import LinearRegression
```

This imports the Linear Regression algorithm from Scikit-learn.

We do not need to implement the regression algorithm mathematically ourselves.

Scikit-learn provides a ready-made implementation.

Next:

```python
from sklearn.metrics import mean_absolute_error
```

This imports Mean Absolute Error (MAE).

We use it to measure the difference between actual and predicted marks.

# 5. Step 2: Create Input Features (X)

```python
X = np.arange(1, 11).reshape(-1, 1)
```

This line is extremely important.

Let's break it down.

### What Does np.arange(1, 11) Do?

NumPy's `arange()` generates a sequence of numbers.

```python
print(np.arange(1, 11))
```

Output:

```text
[ 1  2  3  4  5  6  7  8  9 10]
```

It starts at 1 and stops before 11.

These values represent study hours.

### What Does reshape(-1, 1) Do?

Scikit-learn expects input features in a two-dimensional structure.

Our original array is one-dimensional:

```text
[1 2 3 4 5 6 7 8 9 10]
```

But Linear Regression expects rows and columns.

We use:

```python
.reshape(-1, 1)
```

Output:

```text
[[ 1]
 [ 2]
 [ 3]
 [ 4]
 [ 5]
 [ 6]
 [ 7]
 [ 8]
 [ 9]
 [10]]
```

Now we have:

- 10 rows (students).
- 1 column (study hours).

### Understand reshape(-1, 1)

The two arguments mean:

- `-1`: NumPy automatically calculates the number of rows.
- `1`: Create one column.

For example:

```python
import numpy as np

data = np.array([10, 20, 30, 40])

print(data.reshape(-1, 1))
```

Output:

```text
[[10]
 [20]
 [30]
 [40]]
```

Why is this important?

Scikit-learn expects a two-dimensional feature matrix.

Generally:

\[
X = (NumberOfRecords, NumberOfFeatures)
\]

# 6. Step 3: Create Target Values (y)

```python
y = np.array([30,35,42,48,55,60,68,72,80,88])
```

This contains the actual examination marks.

| Study Hours (X) | Exam Marks (y) |
|---:|---:|
| 1 | 30 |
| 2 | 35 |
| 3 | 42 |
| 4 | 48 |
| 5 | 55 |
| 6 | 60 |
| 7 | 68 |
| 8 | 72 |
| 9 | 80 |
| 10 | 88 |

Notice:

- X contains the input.
- y contains the corresponding actual output.

In Machine Learning:

**X = Features**

**y = Target**

The algorithm learns the relationship between them.

Let's inspect their shapes:

```python
print("X shape:", X.shape)
print("y shape:", y.shape)
```

Output:

```text
X shape: (10, 1)
y shape: (10,)
```

This means:

- 10 records.
- 1 input feature.
- 10 target values.

# 7. Step 4: Create and Train the Model

```python
model = LinearRegression().fit(X, y)
```

Let's understand this line.

First:

```python
model = LinearRegression()
```

This creates a Linear Regression model.

At this point, the model has not learned from our data.

Next:

```python
model.fit(X, y)
```

This is where learning happens.

The model receives:

- X = Study hours.
- y = Actual marks.

It tries to find the best-fitting straight line through the training data.

### What Does the Model Learn?

It learns two important values:

1. Slope (Coefficient).
2. Intercept.

The mathematical equation is:

\[
y = mx+c
\]

The model tries to find the values of \(m\) and \(c\) that minimize the sum of squared prediction errors.

We can inspect them:

```python
print("Coefficient:", model.coef_)
print("Intercept:", model.intercept_)
```

### What Is the Coefficient?

The coefficient represents the estimated change in predicted marks for one additional study hour.

For example, if:

\[
m = 6.5
\]

Then the model estimates that each additional study hour is associated with approximately 6.5 additional marks.

This is an illustrative interpretation; the actual coefficient is calculated from our dataset.

### What Is the Intercept?

The intercept is the predicted output when the input is zero.

For example, if:

\[
c = 24
\]

Then the equation becomes:

\[
y = 6.5x+24
\]

Again, these values are illustrative.

The actual model learns its own coefficient and intercept.

# 8. Step 5: Make a Prediction

Now comes the interesting part.

Imagine a new student studies for 7.5 hours.

We want to predict their marks.

```python
model.predict([[7.5]])
```

Why are we using double square brackets?

Because Scikit-learn expects a two-dimensional feature matrix.

Our new input has:

- One student.
- One feature.

Therefore:

```python
[[7.5]]
```

represents one row and one column.

The model applies the learned equation:

\[
y = mx+c
\]

It calculates the predicted marks.

### Understand the Complete Prediction

```python
prediction = model.predict([[7.5]])

print(prediction)
```

The output is a NumPy array containing one predicted value.

To retrieve the first prediction:

```python
prediction[0]
```

To round it to two decimal places:

```python
round(prediction[0], 2)
```

The complete statement:

```python
print(
    "Prediction for 7.5 study hours:",
    round(model.predict([[7.5]])[0], 2)
)
```

This prints the estimated marks for the new student.

# 9. Step 6: Understand Mean Absolute Error (MAE)

Now we want to understand how close the model's predictions are to the actual marks.

Our program contains:

```python
mean_absolute_error(y, model.predict(X))
```

Let's break it down.

First:

```python
model.predict(X)
```

This predicts marks for all ten original students.

Next:

```python
mean_absolute_error(y, predictions)
```

This compares:

- Actual marks: `y`
- Predicted marks: `predictions`

### What Is MAE?

MAE means Mean Absolute Error.

It calculates the average absolute difference between actual and predicted values.

Formula:

\[
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat y_i|
\]

Where:

- \(y_i\) = Actual marks.
- \(\hat y_i\) = Predicted marks.
- \(n\) = Number of records.

### Example

Imagine we have:

| Student | Actual Marks | Predicted Marks | Absolute Error |
|---|---:|---:|---:|
| A | 50 | 55 | 5 |
| B | 60 | 55 | 5 |
| C | 70 | 65 | 5 |

Then:

\[
MAE = \frac{5+5+5}{3}
\]

\[
\boxed{MAE=5}
\]

This means the average absolute prediction error is 5 marks.

Generally:

- Lower MAE is better.
- Higher MAE means larger prediction errors.

### Important: Training MAE vs Testing MAE

Our current program calculates:

```python
mean_absolute_error(y, model.predict(X))
```

This evaluates the model on the same data it was trained on.

Therefore, this is **training MAE**, not an unbiased estimate of performance on new data.

To evaluate generalization, we should use a separate test dataset.

# 10. Visualize the Regression Concept

Imagine plotting the dataset on a graph.

- X-axis = Study hours.
- Y-axis = Exam marks.
- Each student is represented by a point.
- Linear Regression draws a straight line that best fits the observations.

The model tries to minimize the squared vertical distances between the observed points and the fitted line.

This is called the Least Squares method.

# 11. Complete Improved Program: Training and Testing

The earlier program is useful for introducing Linear Regression.

Now let's improve it by dividing our data into training and testing sets.

```python
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Step 1: Create input features
X = np.arange(1, 11).reshape(-1, 1)

# Step 2: Create target values
y = np.array([30,35,42,48,55,60,68,72,80,88])

# Step 3: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Step 4: Create model
model = LinearRegression()

# Step 5: Train model
model.fit(X_train, y_train)

# Step 6: Predict using test data
predictions = model.predict(X_test)

# Step 7: Evaluate
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

print("Test MAE:",
      round(mean_absolute_error(y_test, predictions), 2))

print("Test R2:",
      round(r2_score(y_test, predictions), 3))

# Step 8: Predict for a new student
print("New student prediction:",
      round(model.predict([[7.5]])[0], 2))
```

Why is this better?

Because the model is trained on one portion of the dataset and evaluated on records it has not seen during training.

With only ten records, however, this is a very small demonstration dataset. Its evaluation score can vary substantially depending on the split.

# 12. Important Concepts to Remember

| Concept | Explanation |
|---|---|
| Linear Regression | Predicts continuous numerical values |
| X | Input features |
| y | Target values |
| `np.arange()` | Generates a sequence of numbers |
| `reshape(-1, 1)` | Converts a one-dimensional array into a column |
| `LinearRegression()` | Creates a regression model |
| `fit()` | Trains the model |
| `coef_` | Learned slope/coefficient |
| `intercept_` | Learned intercept |
| `predict()` | Generates predictions |
| MAE | Measures average absolute prediction error |
| R² | Measures explained variation in the target |

# 13. Practice Exercises for Students

### Beginner

1. Change the study hours from 1–10 to 1–20.
2. Add more students.
3. Change the actual marks.
4. Predict marks for 5 hours.
5. Predict marks for 12 hours.
6. Print the model coefficient.
7. Print the model intercept.

### Intermediate

8. Create a dataset with attendance percentage and marks.
9. Train a Linear Regression model.
10. Predict marks for a student with 85% attendance.
11. Calculate MAE.
12. Compare the predicted and actual marks.

### Challenge

13. Use two features: study hours and attendance.
14. Predict marks using Multiple Linear Regression.
15. Compare Simple and Multiple Linear Regression.
16. Split the data into training and testing sets.
17. Compare training MAE with testing MAE.

# Final Teaching Summary

Think of Linear Regression as a teacher learning from previous student records.

- X = Study hours.
- y = Actual examination marks.
- `fit()` = Learn the relationship.
- `coef_` = How much predicted marks change per additional study hour.
- `intercept_` = Predicted marks when study hours are zero.
- `predict()` = Estimate marks for a new student.
- MAE = Measure the average prediction error.

**The main lesson:**

Linear Regression allows us to learn a mathematical relationship from historical numerical data and use that relationship to predict values for new inputs.

