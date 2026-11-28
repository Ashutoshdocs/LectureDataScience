# Data Preprocessing Using Scikit-learn
## Understanding SimpleImputer and StandardScaler

# 1. What Is This Program Doing?

Imagine you are working on a Machine Learning project.

You have collected information about five customers:

- Age
- Salary

Your dataset looks like this:

| Customer | Age | Salary |
|---|---:|---:|
| A | 22 | 25000 |
| B | 25 | 30000 |
| C | Missing | 35000 |
| D | 32 | Missing |
| E | 40 | 60000 |

But there are two problems.

**Problem 1: Missing Values**

Customer C's age is missing.

Customer D's salary is missing.

Many Machine Learning algorithms cannot directly work with missing numerical values.

**Problem 2: Different Numerical Scales**

Age values are between 22 and 40.

Salary values are between 25000 and 60000.

The scales are very different.

Some Machine Learning algorithms perform better when numerical features are scaled.

To solve these problems, Scikit-learn provides:

1. `SimpleImputer`
2. `StandardScaler`

# 2. Complete Python Program

```python
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

X = np.array([
    [22, 25000],
    [25, 30000],
    [np.nan, 35000],
    [32, np.nan],
    [40, 60000]
])

print("Raw data:\n", X)

filled = SimpleImputer(
    strategy="mean"
).fit_transform(X)

print("After filling missing values:\n", filled)

scaled = StandardScaler().fit_transform(filled)

print("After scaling (rounded):\n", np.round(scaled, 2))
```

Now let's understand every line.

# 3. Step 1: Import Libraries

```python
import numpy as np
```

We import NumPy to create and manipulate numerical arrays.

Next:

```python
from sklearn.impute import SimpleImputer
```

SimpleImputer is used to handle missing values.

Next:

```python
from sklearn.preprocessing import StandardScaler
```

StandardScaler is used to standardize numerical features.

# 4. Step 2: Create the Dataset

```python
X = np.array([
    [22, 25000],
    [25, 30000],
    [np.nan, 35000],
    [32, np.nan],
    [40, 60000]
])
```

We create a NumPy array.

Our dataset contains two columns:

- Column 1: Age
- Column 2: Salary

Let's understand the values:

| Row | Age | Salary |
|---|---:|---:|
| 1 | 22 | 25000 |
| 2 | 25 | 30000 |
| 3 | NaN | 35000 |
| 4 | 32 | NaN |
| 5 | 40 | 60000 |

### What is np.nan?

`np.nan` means Not a Number.

It is commonly used to represent missing numerical values.

For example:

```python
age = np.nan

print(age)
```

Output:

```text
nan
```

Why do we use NaN instead of 0?

Because zero can be a valid value.

For example:

- Age = 0 could be valid for a newborn.
- Salary = 0 could mean no income.

A missing value and an actual zero are not necessarily the same thing.

# 5. Step 3: Print the Original Dataset

```python
print("Raw data:\n", X)
```

Output:

```text
Raw data:

[[2.2e+01 2.5e+04]
 [2.5e+01 3.0e+04]
 [    nan 3.5e+04]
 [3.2e+01     nan]
 [4.0e+01 6.0e+04]]
```

The output shows our original data.

Notice that two values are missing.

Before training many Machine Learning algorithms, we need to handle these missing values.

# 6. Step 4: What Is SimpleImputer?

```python
filled = SimpleImputer(
    strategy="mean"
).fit_transform(X)
```

This is one of the most important lines.

Let's break it down.

### What is SimpleImputer?

SimpleImputer is a Scikit-learn tool that replaces missing values using a selected strategy.

Available strategies include:

| Strategy | Meaning |
|---|---|
| mean | Replace with column average |
| median | Replace with column median |
| most_frequent | Replace with most common value |
| constant | Replace with a specified value |

### What Does strategy="mean" Mean?

It means:

If a value is missing, calculate the average of the available values in that column and use it to replace the missing value.

**Important:** Mean is calculated separately for each column.

### Let's Calculate the Mean Manually

Our Age column:

```text
22, 25, NaN, 32, 40
```

Ignore the missing value.

\[
Mean = \frac{22+25+32+40}{4}
\]

\[
Mean = \frac{119}{4}
\]

\[
\boxed{Mean = 29.75}
\]

So the missing age becomes 29.75.

Now calculate the Salary mean:

```text
25000, 30000, 35000, NaN, 60000
```

\[
Mean = \frac{25000+30000+35000+60000}{4}
\]

\[
Mean = \frac{150000}{4}
\]

\[
\boxed{Mean = 37500}
\]

So the missing salary becomes 37500.

### Dataset After Imputation

| Customer | Age | Salary |
|---|---:|---:|
| A | 22 | 25000 |
| B | 25 | 30000 |
| C | 29.75 | 35000 |
| D | 32 | 37500 |
| E | 40 | 60000 |

The missing values have been replaced.

### What Does fit_transform() Mean?

This is another important concept.

```python
SimpleImputer(strategy="mean").fit_transform(X)
```

It performs two operations.

**fit():**

Calculates the mean of each column from the available values.

**transform():**

Uses the calculated means to replace missing values.

So:

```python
imputer = SimpleImputer(strategy="mean")

imputer.fit(X)

filled = imputer.transform(X)
```

The above three lines are equivalent to:

```python
filled = SimpleImputer(strategy="mean").fit_transform(X)
```

Let's inspect the calculated statistics:

```python
imputer = SimpleImputer(strategy="mean")

imputer.fit(X)

print("Calculated means:", imputer.statistics_)
```

Expected output:

```text
Calculated means: [   29.75 37500.  ]
```

This proves that Scikit-learn calculates a separate mean for every column.

# 7. Step 5: What Is StandardScaler?

Now our dataset has no missing values.

But look at the numerical scales:

| Age | Salary |
|---:|---:|
| 22 | 25000 |
| 25 | 30000 |
| 29.75 | 35000 |
| 32 | 37500 |
| 40 | 60000 |

Age values are small.

Salary values are much larger.

Some Machine Learning algorithms can be sensitive to these differences.

For example:

- Logistic Regression
- K-Nearest Neighbors
- Support Vector Machines
- Neural Networks

To handle this, we use StandardScaler.

```python
from sklearn.preprocessing import StandardScaler
```

### What Does StandardScaler Do?

It transforms numerical data so that each feature has:

- Mean approximately equal to 0.
- Standard deviation approximately equal to 1.

Formula:

\[
z = \frac{x-\mu}{\sigma}
\]

Where:

- \(x\) = Original value.
- \(\mu\) = Mean of the column.
- \(\sigma\) = Standard deviation of the column.
- \(z\) = Scaled value.

### Understand With an Example

Suppose we have:

```text
Age = [20, 30, 40, 50, 60]
```

Mean:

\[
\mu = \frac{20+30+40+50+60}{5}
\]

\[
\mu = 40
\]

Standard deviation:

\[
\sigma = \sqrt{\frac{\sum(x-\mu)^2}{n}}
\]

\[
\sigma = \sqrt{200}
\]

\[
\sigma \approx 14.14
\]

Now scale the first value:

\[
z = \frac{20-40}{14.14}
\]

\[
z \approx -1.41
\]

The value 20 becomes approximately -1.41.

Similarly, the other values become:

| Original Age | Scaled Age |
|---:|---:|
| 20 | -1.41 |
| 30 | -0.71 |
| 40 | 0.00 |
| 50 | 0.71 |
| 60 | 1.41 |

Notice that the values are now on a standardized scale.

# 8. Step 6: Apply StandardScaler to Our Dataset

```python
scaled = StandardScaler().fit_transform(filled)
```

Let's break this down.

**fit():**

Calculates the mean and standard deviation of each column.

**transform():**

Uses those statistics to scale each value.

We can also write it separately:

```python
scaler = StandardScaler()

scaler.fit(filled)

scaled = scaler.transform(filled)
```

Inspect the learned values:

```python
print("Means:", scaler.mean_)

print("Standard deviations:", scaler.scale_)
```

Remember:

StandardScaler calculates separate statistics for Age and Salary.

# 9. Step 7: Print the Scaled Dataset

```python
print("After scaling (rounded):", np.round(scaled, 2))
```

`np.round(scaled, 2)` rounds the results to two decimal places.

The output will be approximately:

```text
[[-1.42 -1.08]
 [-0.98 -0.72]
 [-0.28 -0.36]
 [ 0.06 -0.18]
 [ 1.61  2.34]]
```

Now both columns have:

- Mean approximately 0.
- Standard deviation approximately 1.

The original age and salary values have been transformed.

**Important:** StandardScaler does not delete the original information. It changes the numerical representation of the features.

# 10. Complete Data Transformation Flow

```text
             ORIGINAL DATA
                   |
                   |
          -------------------
          |                 |
          v                 v
         AGE              SALARY
          |                 |
          |                 |
       Missing            Missing
          |                 |
          -------+---------
                 |
                 v
            SIMPLE IMPUTER
                 |
                 v
          MISSING VALUES FILLED
                 |
                 v
           STANDARD SCALER
                 |
                 v
           SCALED DATASET
                 |
                 v
          READY FOR ML MODEL
```

# 11. Why Not Do This Manually?

Imagine you have:

- 100,000 customer records.
- 20 numerical columns.
- Missing values in multiple columns.
- Different numerical scales.

You could manually calculate the averages and replace missing values.

You could also calculate the mean and standard deviation and scale each column yourself.

But this would require significant code and repeated calculations.

Scikit-learn makes it much simpler:

```python
filled = SimpleImputer(strategy="mean").fit_transform(X)

scaled = StandardScaler().fit_transform(filled)
```

Two operations prepare the data.

# 12. Important Concept: fit() vs transform()

Students should understand this difference.

| Method | What it does |
|---|---|
| fit() | Learns statistics or parameters from data |
| transform() | Applies the learned transformation |
| fit_transform() | Learns and transforms in one operation |

For SimpleImputer:

- `fit()` learns the column means.
- `transform()` fills missing values.

For StandardScaler:

- `fit()` learns the column means and standard deviations.
- `transform()` scales the values.

# 13. Very Important: Avoid Data Leakage

In real Machine Learning projects, we should not calculate preprocessing statistics using both training and testing data.

Why?

Because the test data should remain unseen during training.

Correct approach:

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

preprocessing = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

model = Pipeline([
    ("preprocessing", preprocessing),
    ("classifier", LogisticRegression())
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)
```

The pipeline learns the imputation and scaling statistics from training data only.

The same learned transformations are then applied to test data.

This helps prevent data leakage.

# 14. Practice Exercises for Students

### Beginner

1. Replace `strategy="mean"` with `strategy="median"`.
2. Print the imputed dataset.
3. Print the means calculated by SimpleImputer.
4. Print the means calculated by StandardScaler.
5. Print the standard deviations calculated by StandardScaler.

### Intermediate

6. Add another numerical column called Experience.
7. Add two missing values in that column.
8. Apply SimpleImputer to all three columns.
9. Compare the original and scaled datasets.
10. Explain why we use separate statistics for each column.

### Challenge

11. Create a dataset containing 100 customer records.
12. Introduce missing values in Age and Salary.
13. Split the dataset into training and testing data.
14. Create a preprocessing Pipeline.
15. Train a Logistic Regression model using the prepared data.

# 15. Important Concepts to Remember

| Component | Responsibility |
|---|---|
| NumPy | Creates and handles numerical arrays |
| `np.nan` | Represents a missing numerical value |
| SimpleImputer | Replaces missing values |
| `strategy="mean"` | Uses column averages |
| `strategy="median"` | Uses column medians |
| StandardScaler | Standardizes numerical features |
| `fit()` | Learns statistics |
| `transform()` | Applies transformations |
| `fit_transform()` | Learns and applies transformations |

# Final Teaching Summary

Think about preparing a dataset like preparing ingredients before cooking.

- SimpleImputer: Fills missing ingredients.
- StandardScaler: Standardizes ingredient measurements.
- Pipeline: Connects preparation operations into one workflow.

**The main lesson:**

Before training a Machine Learning model, we often need to clean and prepare our data. Scikit-learn provides reusable preprocessing tools that make this process easier, consistent, and less error-prone.