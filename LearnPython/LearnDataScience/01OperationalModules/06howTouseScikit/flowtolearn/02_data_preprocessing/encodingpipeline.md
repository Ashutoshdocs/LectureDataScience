# Data Preprocessing Using Scikit-learn
## Understanding OneHotEncoder, StandardScaler, SimpleImputer, ColumnTransformer and Pipeline

# 1. What Is This Program Doing?

Imagine you own an online shopping company.

You have historical customer information, and you want to build a Machine Learning model that predicts whether a customer will purchase a product.

You have information about customers such as:

| Age | Salary | City | Purchased |
|---:|---:|---|---:|
| 22 | 25000 | Pune | 0 |
| 25 | 30000 | Mumbai | 0 |
| 31 | 42000 | Pune | 1 |
| 35 | 50000 | Delhi | 1 |
| 45 | 65000 | Mumbai | 1 |
| 52 | 72000 | Delhi | 1 |
| 28 | 38000 | Pune | 0 |
| 41 | 58000 | Mumbai | 1 |

Our objective is to train a Machine Learning model that learns from this information.

Later, when a new customer visits our website, we provide their:

- Age
- Salary
- City

The model predicts whether they are likely to purchase.

**But there is a problem!**

Machine Learning algorithms generally work with numerical data.

Our dataset contains:

- Age: Numerical
- Salary: Numerical
- City: Text (Pune, Mumbai, Delhi)

We also need to handle missing values and prepare the numerical columns appropriately.

This is where Scikit-learn preprocessing tools become useful.

# 2. Understand the Complete Program

First, let's look at the complete code.

```python
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

df = pd.DataFrame({
    "age":[22,25,31,35,45,52,28,41],
    "salary":[25000,30000,42000,50000,65000,72000,38000,58000],
    "city":["Pune","Mumbai","Pune","Delhi","Mumbai","Delhi","Pune","Mumbai"],
    "purchased":[0,0,1,1,1,1,0,1]
})

X = df[["age","salary","city"]]
y = df["purchased"]

numeric = Pipeline([
    ("fill", SimpleImputer(strategy="median")),
    ("scale", StandardScaler())
])

categorical = Pipeline([
    ("fill", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore"))
])

prep = ColumnTransformer([
    ("numbers", numeric, ["age","salary"]),
    ("categories", categorical, ["city"])
])

model = Pipeline([
    ("prep", prep),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X, y)

new_customer = pd.DataFrame({
    "age":[29],
    "salary":[90000],
    "city":["Pune"]
})

print("Purchase prediction (1=yes, 0=no):",
      model.predict(new_customer)[0])
```

Now let's understand every component.

# 3. Create the Dataset Using Pandas

```python
import pandas as pd
```

We import Pandas because it allows us to create and manipulate tabular data.

Next:

```python
df = pd.DataFrame({
    "age":[22,25,31,35,45,52,28,41],
    "salary":[25000,30000,42000,50000,65000,72000,38000,58000],
    "city":["Pune","Mumbai","Pune","Delhi","Mumbai","Delhi","Pune","Mumbai"],
    "purchased":[0,0,1,1,1,1,0,1]
})
```

We create a DataFrame.

Our columns represent:

| Column | Meaning | Data Type |
|---|---|---|
| age | Customer age | Numerical |
| salary | Customer salary | Numerical |
| city | Customer location | Categorical |
| purchased | Purchase outcome | Target |

### What does 0 and 1 mean?

For this demonstration:

- 0 = Customer did not purchase.
- 1 = Customer purchased.

Our objective is to predict this column.

# 4. Separate Features (X) and Target (y)

```python
X = df[["age","salary","city"]]

y = df["purchased"]
```

This is an important Machine Learning concept.

**X = Input Features**

These are the columns given to the model.

```text
age
salary
city
```

**y = Target**

This is the answer the model needs to learn.

```text
purchased
```

Think about it like an examination:

- X = Questions given to the student.
- y = Correct answers.
- Model = Student learning from examples.

# 5. Why Do We Need SimpleImputer?

Before understanding the code, imagine this dataset:

| Age | Salary |
|---:|---:|
| 22 | 25000 |
| 25 | 30000 |
| Missing | 42000 |
| 35 | Missing |
| 45 | 65000 |

What happens if a value is missing?

Many Machine Learning algorithms cannot directly process missing numerical values.

We need to fill those missing values.

Scikit-learn provides:

```python
from sklearn.impute import SimpleImputer
```

### What is SimpleImputer?

It automatically replaces missing values using a strategy we choose.

Common strategies:

| Strategy | What it does |
|---|---|
| mean | Replaces missing values with the average |
| median | Replaces missing values with the middle value |
| most_frequent | Replaces missing values with the most common value |
| constant | Replaces missing values with a value we specify |

Example:

```python
from sklearn.impute import SimpleImputer
import numpy as np

data = np.array([
    [20],
    [30],
    [np.nan],
    [40],
    [50]
])

imputer = SimpleImputer(strategy="median")

result = imputer.fit_transform(data)

print(result)
```

Output:

```text
[[20.]
 [30.]
 [35.]
 [40.]
 [50.]]
```

Why 35?

Because the median of 20, 30, 40 and 50 is:

\[
Median = \frac{30+40}{2}=35
\]

The missing value is replaced with 35.

# 6. Why Do We Need StandardScaler?

Look at our numerical columns:

| Age | Salary |
|---:|---:|
| 22 | 25000 |
| 25 | 30000 |
| 31 | 42000 |
| 35 | 50000 |

Notice something?

Age values are around 20–50.

Salary values are around 25,000–72,000.

The scales are very different.

Some Machine Learning algorithms can be affected by differences in feature scales.

For example, Logistic Regression often benefits from numerical scaling.

Scikit-learn provides:

```python
from sklearn.preprocessing import StandardScaler
```

### What does StandardScaler do?

It transforms values so that the resulting column has:

- Mean approximately 0.
- Standard deviation approximately 1.

Formula:

\[
z = \frac{x-\mu}{\sigma}
\]

Where:

- \(x\) = Original value.
- \(\mu\) = Mean.
- \(\sigma\) = Standard deviation.
- \(z\) = Scaled value.

Example:

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

data = np.array([
    [20],
    [30],
    [40],
    [50],
    [60]
])

scaler = StandardScaler()

result = scaler.fit_transform(data)

print(result)
```

Output:

```text
[[-1.414]
 [-0.707]
 [ 0.   ]
 [ 0.707]
 [ 1.414]]
```

The original values have been converted into scaled values.

**Important:** StandardScaler does not make all values lie between 0 and 1. That is the purpose of MinMaxScaler.

# 7. Why Do We Need OneHotEncoder?

Now comes one of the most important concepts.

Our dataset contains:

```text
city

Pune
Mumbai
Delhi
Pune
Mumbai
Delhi
```

These are text values.

Our Machine Learning model needs numerical inputs.

How do we convert them?

We use OneHotEncoder.

```python
from sklearn.preprocessing import OneHotEncoder
```

### What does OneHotEncoder do?

It converts categorical values into separate numerical columns.

Before encoding:

| City |
|---|
| Pune |
| Mumbai |
| Delhi |

After encoding:

| City_Delhi | City_Mumbai | City_Pune |
|---:|---:|---:|
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |

Each city gets its own column.

This is called One-Hot Encoding.

### Why not simply assign numbers?

Suppose we encode:

```text
Delhi = 1
Mumbai = 2
Pune = 3
```

The algorithm might incorrectly interpret these numbers as having an ordered or numerical relationship.

For example, it might interpret Pune as greater than Mumbai.

But cities have no such numerical relationship.

OneHotEncoder avoids introducing that artificial ordering.

### Practical Example

```python
from sklearn.preprocessing import OneHotEncoder

cities = [["Pune"], ["Mumbai"], ["Delhi"], ["Pune"]]

encoder = OneHotEncoder(sparse_output=False)

result = encoder.fit_transform(cities)

print(encoder.get_feature_names_out())
print(result)
```

Output:

```text
['x0_Delhi' 'x0_Mumbai' 'x0_Pune']

[[0. 0. 1.]
 [0. 1. 0.]
 [1. 0. 0.]
 [0. 0. 1.]]
```

Note: `sparse_output=False` is supported in modern scikit-learn versions.

# 8. What Is Pipeline?

Now we understand three important preprocessing tools:

1. SimpleImputer
2. StandardScaler
3. OneHotEncoder

But imagine we have 20 preprocessing steps.

We would have to execute each one manually.

For example:

```python
data = imputer.fit_transform(data)

data = scaler.fit_transform(data)

data = encoder.fit_transform(data)
```

This becomes difficult when we have different columns and different preprocessing requirements.

Scikit-learn provides Pipeline.

```python
from sklearn.pipeline import Pipeline
```

### What does Pipeline do?

Pipeline connects multiple processing steps into a single workflow.

Think of a manufacturing factory.

```text
Raw Material
     |
     v
Machine 1
     |
     v
Machine 2
     |
     v
Machine 3
     |
     v
Finished Product
```

Similarly:

```text
Raw Data
   |
   v
SimpleImputer
   |
   v
StandardScaler
   |
   v
Prepared Data
```

### Pipeline Syntax

```python
numeric = Pipeline([
    ("fill", SimpleImputer(strategy="median")),
    ("scale", StandardScaler())
])
```

Let's understand:

```python
("fill", SimpleImputer(strategy="median"))
```

- `fill` is the name of the pipeline step.
- `SimpleImputer` is the actual transformer.
- `strategy="median"` specifies how missing values are replaced.

Next:

```python
("scale", StandardScaler())
```

- `scale` is the name of the next step.
- `StandardScaler()` performs scaling.

The order matters:

1. Fill missing values.
2. Scale the completed numerical data.

This Pipeline is specifically for numerical columns.

# 9. Why Do We Need Two Different Pipelines?

Look at our dataset again.

| Column | Type | Required Processing |
|---|---|---|
| age | Numerical | Imputation + Scaling |
| salary | Numerical | Imputation + Scaling |
| city | Categorical | Imputation + Encoding |

Can we apply StandardScaler directly to city?

No.

Can we apply OneHotEncoder directly to salary?

We could, but it would not be the appropriate processing for a continuous numerical feature.

Therefore, we create two pipelines.

### A. Numerical Pipeline

```python
numeric = Pipeline([
    ("fill", SimpleImputer(strategy="median")),
    ("scale", StandardScaler())
])
```

This pipeline handles:

```text
age
salary
```

Its workflow:

```text
Age, Salary
     |
     v
SimpleImputer
     |
     v
StandardScaler
     |
     v
Processed Numerical Data
```

### B. Categorical Pipeline

```python
categorical = Pipeline([
    ("fill", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore"))
])
```

This pipeline handles:

```text
city
```

Its workflow:

```text
City
  |
  v
SimpleImputer
  |
  v
OneHotEncoder
  |
  v
Processed Categorical Data
```

Why `most_frequent`?

If a city value is missing, we replace it with the most frequently occurring city.

Why `handle_unknown="ignore"`?

Imagine our training dataset contains:

```text
Pune
Mumbai
Delhi
```

But a new customer comes from:

```text
Hyderabad
```

Hyderabad was not present during training.

Without appropriate handling, the encoder can raise an error.

With:

```python
OneHotEncoder(handle_unknown="ignore")
```

The encoder handles the unknown category without failing. Its encoded representation for that unknown category is all zeros across the learned city columns.

# 10. What Is ColumnTransformer?

Now we have two pipelines:

- Numeric pipeline.
- Categorical pipeline.

But how do we tell Scikit-learn which pipeline should process which columns?

This is where ColumnTransformer comes in.

```python
from sklearn.compose import ColumnTransformer
```

Example:

```python
prep = ColumnTransformer([
    ("numbers", numeric, ["age","salary"]),
    ("categories", categorical, ["city"])
])
```

Understand its structure:

```python
("numbers", numeric, ["age","salary"])
```

It means:

- `numbers`: Name of this transformation.
- `numeric`: Pipeline to execute.
- `["age","salary"]`: Columns to process.

Similarly:

```python
("categories", categorical, ["city"])
```

It means:

- `categories`: Name of this transformation.
- `categorical`: Pipeline to execute.
- `["city"]`: Column to process.

### Complete ColumnTransformer Flow

```text
                  ORIGINAL DATA
                       |
          ---------------------------
          |                         |
          v                         v
      AGE, SALARY                  CITY
          |                         |
          v                         v
    NUMERIC PIPELINE          CATEGORICAL PIPELINE
          |                         |
          v                         v
    SimpleImputer              SimpleImputer
          |                         |
          v                         v
    StandardScaler             OneHotEncoder
          |                         |
          v                         v
    Numerical Data             Encoded Data
          |                         |
          -----------+--------------
                     |
                     v
              TRANSFORMED DATA
```

**ColumnTransformer allows different preprocessing operations on different columns of the same dataset.**

# 11. Now Combine Everything Into One Pipeline

We have prepared our data-processing workflow.

But we still need to train a Machine Learning model.

Let's import:

```python
from sklearn.linear_model import LogisticRegression
```

What is Logistic Regression?

It is a classification algorithm.

It predicts a category rather than a continuous numerical value.

In our example:

```text
0 = Not purchased
1 = Purchased
```

Now look at this code:

```python
model = Pipeline([
    ("prep", prep),
    ("classifier", LogisticRegression(max_iter=1000))
])
```

We create one final pipeline.

It contains two steps:

### Step 1: prep

```python
("prep", prep)
```

This executes our ColumnTransformer.

It:

1. Handles missing numerical values.
2. Scales numerical columns.
3. Handles missing categorical values.
4. Encodes categorical columns.

### Step 2: classifier

```python
("classifier", LogisticRegression(max_iter=1000))
```

After preprocessing, the transformed data is passed to Logistic Regression.

The classifier learns the relationship between customer information and purchase outcomes.

### Complete Model Architecture

```text
                RAW CUSTOMER DATA
                         |
                         v
                 COLUMN TRANSFORMER
                         |
              -----------------------
              |                     |
              v                     v
        NUMERIC DATA          CATEGORICAL DATA
              |                     |
         SimpleImputer         SimpleImputer
              |                     |
         StandardScaler        OneHotEncoder
              |                     |
              -----------+---------
                         |
                         v
                 PREPROCESSED DATA
                         |
                         v
                LOGISTIC REGRESSION
                         |
                         v
                   TRAINED MODEL
```

# 12. Train the Complete Pipeline

```python
model.fit(X, y)
```

This is the most interesting part.

We are not manually executing:

- SimpleImputer
- StandardScaler
- OneHotEncoder
- ColumnTransformer
- Logistic Regression

Instead, one command executes the complete workflow.

```python
model.fit(X, y)
```

What happens internally?

1. The original DataFrame is provided.
2. The ColumnTransformer identifies the appropriate columns.
3. Numerical columns are imputed and scaled.
4. Categorical columns are imputed and encoded.
5. The transformed dataset is passed to Logistic Regression.
6. Logistic Regression learns from the features and target.

**One fit() call trains the entire pipeline.**

An important advantage is that preprocessing parameters are learned during fitting and reused consistently during prediction.

# 13. Predict for a New Customer

Now imagine a new customer visits our website.

Their details are:

| Feature | Value |
|---|---|
| Age | 29 |
| Salary | 90000 |
| City | Pune |

We create a new DataFrame:

```python
new_customer = pd.DataFrame({
    "age":[29],
    "salary":[90000],
    "city":["Pune"]
})
```

Why use a DataFrame?

Because our pipeline was trained with named columns. Providing a DataFrame with matching column names makes the input structure clear.

Now predict:

```python
prediction = model.predict(new_customer)

print(prediction[0])
```

The output will be:

```text
0
```

or:

```text
1
```

The meaning:

- 0 = Model predicts no purchase.
- 1 = Model predicts purchase.

The exact result depends on the fitted model.

**Important:** This is a tiny illustrative dataset with only eight records. The prediction is not reliable evidence of real customer purchasing behaviour. A real project needs much more representative data and proper train/test evaluation.

# 14. Why Is Pipeline Better Than Doing Everything Manually?

| Without Pipeline | With Pipeline |
|---|---|
| Execute each preprocessing step separately | One workflow |
| More code to maintain | Cleaner code |
| Easy to forget a transformation | Consistent transformations |
| Risk of different training and prediction processing | Reuses learned transformations |
| More opportunity for data leakage | Helps prevent leakage when used correctly |

### Very Important: Data Leakage

Imagine we calculate the average salary using the complete dataset, including test data.

Then we split the dataset.

The training process has indirectly used information from the test data.

This is called data leakage.

A proper approach is:

1. Split training and test data.
2. Fit the pipeline using training data only.
3. Predict using the test data.
4. Evaluate using actual test labels.

Example:

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
```

The preprocessing steps are fitted using training data and then reused on test data.

# 15. Practice Exercises for Students

### Beginner

1. Add a new customer record.
2. Change the customer's city.
3. Change the salary to 100000.
4. Replace one salary with a missing value.
5. Experiment with `strategy="mean"` instead of median.

### Intermediate

6. Add a new categorical column called `education`.
7. Add another numerical column called `experience`.
8. Modify ColumnTransformer to process these new columns.
9. Try `handle_unknown="ignore"` by predicting for Hyderabad.
10. Print the transformed data using:

```python
model.named_steps["prep"].transform(X)
```

### Challenge

11. Split the dataset into training and testing data.
12. Train the pipeline using training data.
13. Evaluate the model using accuracy, precision and recall.
14. Compare Logistic Regression with Decision Tree.
15. Use cross-validation to evaluate the pipeline.

# 16. Important Concepts to Remember

| Component | Responsibility |
|---|---|
| SimpleImputer | Handles missing values |
| StandardScaler | Scales numerical features |
| OneHotEncoder | Converts categories into numerical columns |
| Pipeline | Connects multiple processing/model steps |
| ColumnTransformer | Applies different processing to different columns |
| LogisticRegression | Performs classification |
| fit() | Learns preprocessing parameters and trains the model |
| predict() | Generates predictions using the fitted workflow |

# Final Teaching Summary

Think of building a Machine Learning model like preparing food in a factory.

- SimpleImputer: Replaces missing ingredients.
- StandardScaler: Standardizes ingredient measurements.
- OneHotEncoder: Converts text categories into numerical representations.
- ColumnTransformer: Sends each ingredient to the correct processing section.
- Pipeline: Connects all processing stages.
- LogisticRegression: Makes the final prediction.

**The most important lesson:**

Scikit-learn is not just a collection of Machine Learning algorithms. It provides a complete, reusable workflow for preparing data, training models and generating predictions.