# Iris Flower Classification Using Scikit-learn
## Understanding Logistic Regression, Classification, Pipeline and Model Evaluation

# 1. What Is This Program Doing?

Imagine you are a botanist studying different types of flowers.

You have collected measurements of 150 Iris flowers.

For every flower, you have recorded four measurements:

1. Sepal Length
2. Sepal Width
3. Petal Length
4. Petal Width

Your objective is to build a Machine Learning model that can identify the species of a flower based on these measurements.

There are three possible species:

- Setosa
- Versicolor
- Virginica

Now imagine someone gives you measurements of a new flower.

You want your Machine Learning model to predict which species it belongs to.

This is called **Classification**.

Unlike Regression, which predicts numerical values, Classification predicts categories or classes.

# 2. Understand the Dataset

Scikit-learn provides a built-in Iris dataset.

It contains:

- 150 flower records.
- 4 input features.
- 3 target classes.

### Dataset Structure

| Sepal Length | Sepal Width | Petal Length | Petal Width | Species |
|---:|---:|---:|---:|---|
| 5.1 | 3.5 | 1.4 | 0.2 | Setosa |
| 4.9 | 3.0 | 1.4 | 0.2 | Setosa |
| 6.3 | 3.3 | 4.7 | 1.6 | Versicolor |
| 5.8 | 2.7 | 5.1 | 1.9 | Virginica |

The values above are illustrative sample records.

Our objective is to learn the relationship between the four measurements and the flower species.

# 3. What Is Classification?

Classification is a supervised Machine Learning technique.

We provide:

- Input features (X).
- Known class labels (y).

The model learns the relationship and predicts the class of new records.

### Classification Examples

| Input | Prediction |
|---|---|
| Email content | Spam / Not Spam |
| Customer information | Will purchase / Will not purchase |
| Medical measurements | Possible disease category |
| Flower measurements | Flower species |
| Transaction details | Fraud / Not Fraud |

### Regression vs Classification

| Regression | Classification |
|---|---|
| Predicts numbers | Predicts categories |
| House price | House category |
| Student marks | Pass / Fail |
| Temperature | Weather category |
| Linear Regression | Logistic Regression |

# 4. Complete Python Program

```python
"""Classify Iris flowers into one of three species."""

from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

iris = load_iris()

Xtr, Xte, ytr, yte = train_test_split(
    iris.data,
    iris.target,
    test_size=0.25,
    random_state=42,
    stratify=iris.target
)

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

model.fit(Xtr, ytr)

pred = model.predict(Xte)

print("Species:", iris.target_names)

print("Accuracy:", round(accuracy_score(yte, pred), 3))

print("Confusion matrix:\n", confusion_matrix(yte, pred))

print(classification_report(
    yte,
    pred,
    target_names=iris.target_names
))

sample = [[5.1, 3.5, 1.4, 0.2]]

print(
    "Sample prediction:",
    iris.target_names[model.predict(sample)[0]]
)
```

Now let's understand every line.

# 5. Step 1: Import Libraries

### A. Load the Dataset

```python
from sklearn.datasets import load_iris
```

Scikit-learn provides a ready-made Iris dataset.

We do not need to download a CSV file.

### B. Split the Dataset

```python
from sklearn.model_selection import train_test_split
```

This function divides the dataset into training and testing portions.

Why?

We need to train the model on one set of examples and evaluate it using unseen examples.

### C. Pipeline

```python
from sklearn.pipeline import make_pipeline
```

Pipeline connects multiple Machine Learning operations into one workflow.

In our example:

1. StandardScaler
2. LogisticRegression

### D. StandardScaler

```python
from sklearn.preprocessing import StandardScaler
```

StandardScaler standardizes numerical features.

It helps Logistic Regression work with features that have different numerical scales.

### E. Logistic Regression

```python
from sklearn.linear_model import LogisticRegression
```

This imports our classification algorithm.

Despite having the word Regression in its name, Logistic Regression is commonly used for classification.

It estimates class probabilities and selects a predicted class.

### F. Evaluation Metrics

```python
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
```

These functions help us evaluate the model.

| Function | Purpose |
|---|---|
| accuracy_score | Calculates overall accuracy |
| confusion_matrix | Shows correct and incorrect classifications |
| classification_report | Displays precision, recall and F1-score |

# 6. Step 2: Load the Iris Dataset

```python
iris = load_iris()
```

We load the dataset into the variable `iris`.

Let's inspect it.

```python
print(iris)
```

This returns a dataset object containing features, target values, descriptions and feature names.

We can inspect individual properties:

```python
print(iris.data.shape)

print(iris.target.shape)

print(iris.feature_names)

print(iris.target_names)
```

Expected output:

```text
(150, 4)
(150,)

['sepal length (cm)',
 'sepal width (cm)',
 'petal length (cm)',
 'petal width (cm)']

['setosa' 'versicolor' 'virginica']
```

This means:

- 150 flower records.
- 4 input features.
- 150 target values.
- 3 possible species.

### Understand X and y

```python
X = iris.data

y = iris.target
```

**X = Input Features**

```text
Sepal Length
Sepal Width
Petal Length
Petal Width
```

**y = Target**

The species is represented numerically:

| Numeric Value | Species |
|---:|---|
| 0 | Setosa |
| 1 | Versicolor |
| 2 | Virginica |

The model learns to predict these numerical class labels.

# 7. Step 3: Split the Dataset

This is one of the most important steps.

```python
Xtr, Xte, ytr, yte = train_test_split(
    iris.data,
    iris.target,
    test_size=0.25,
    random_state=42,
    stratify=iris.target
)
```

Let's understand each argument.

### What Does test_size=0.25 Mean?

It means 25% of the dataset is reserved for testing.

Our dataset contains 150 records.

| Dataset | Percentage | Records |
|---|---:|---:|
| Training | 75% | 112 |
| Testing | 25% | 38 |

The model learns from 112 records and is evaluated using 38 unseen records.

### Understand the Four Variables

| Variable | Meaning |
|---|---|
| Xtr | Training input features |
| Xte | Testing input features |
| ytr | Actual training labels |
| yte | Actual testing labels |

### What Does random_state=42 Mean?

It makes the random split reproducible.

If you run the same program again, you get the same split.

### What Does stratify=iris.target Mean?

This is especially important for classification.

Our dataset contains three species.

We want the training and testing sets to maintain approximately the same class proportions as the original dataset.

For example:

| Species | Original Records |
|---|---:|
| Setosa | 50 |
| Versicolor | 50 |
| Virginica | 50 |

With stratification, the split approximately preserves the class distribution.

For the 75/25 split:

| Species | Training | Testing |
|---|---:|---:|
| Setosa | 37 | 13 |
| Versicolor | 37 | 13 |
| Virginica | 38 | 12 |

This makes the evaluation more representative of the original class distribution.

# 8. Step 4: Why Do We Need StandardScaler?

Look at the input features:

| Feature | Approximate Values |
|---|---|
| Sepal Length | 4–8 |
| Sepal Width | 2–5 |
| Petal Length | 1–7 |
| Petal Width | 0–3 |

Although their scales are not extremely different, standardization can help Logistic Regression.

We use:

```python
StandardScaler()
```

It transforms features to have approximately:

- Mean = 0
- Standard deviation = 1

Formula:

\[
z = \frac{x-\mu}{\sigma}
\]

Where:

- x = Original value.
- μ = Mean of the feature.
- σ = Standard deviation.
- z = Scaled value.

Example:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_scaled = scaler.fit_transform(Xtr)

print(X_scaled[:5])
```

The original measurements are converted into standardized numerical values.

### Important

We should fit the scaler only on training data.

Why?

Because the test dataset must remain unseen during training.

Our Pipeline automatically follows this rule.

# 9. Step 5: What Is make_pipeline()?

Our code:

```python
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)
```

What is happening here?

We are combining two operations.

### First: StandardScaler

```python
StandardScaler()
```

It standardizes the numerical features.

### Second: LogisticRegression

```python
LogisticRegression(max_iter=1000)
```

It learns the relationship between the standardized measurements and flower species.

### What Does max_iter=1000 Mean?

Logistic Regression uses an iterative optimization process to learn its parameters.

`max_iter=1000` allows up to 1000 iterations for the optimization process.

It does not mean the model trains on 1000 records.

### Complete Pipeline Flow

```text
             ORIGINAL FLOWER DATA
                       |
                       |
                       v
                 STANDARD SCALER
                       |
                       |
                       v
                SCALED FEATURES
                       |
                       |
                       v
               LOGISTIC REGRESSION
                       |
                       |
                       v
                 TRAINED MODEL
```

### Why Is Pipeline Useful?

Without Pipeline, we would write:

```python
scaler = StandardScaler()

Xtr_scaled = scaler.fit_transform(Xtr)

Xte_scaled = scaler.transform(Xte)

model = LogisticRegression(max_iter=1000)

model.fit(Xtr_scaled, ytr)

pred = model.predict(Xte_scaled)
```

With Pipeline:

```python
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

model.fit(Xtr, ytr)

pred = model.predict(Xte)
```

The Pipeline automatically handles the transformations.

It also ensures that the scaler learned from training data is reused when processing testing data.

# 10. Step 6: Train the Model

```python
model.fit(Xtr, ytr)
```

This is where learning happens.

The pipeline:

1. Receives training flower measurements.
2. Standardizes the features.
3. Passes the transformed data to Logistic Regression.
4. Learns relationships between measurements and species labels.

The model is now trained.

# 11. Step 7: Make Predictions

```python
pred = model.predict(Xte)
```

Now we provide the testing flower measurements.

The model predicts the species for each flower.

Remember:

- `Xte` contains the measurements.
- `yte` contains the actual species.
- `pred` contains the model's predictions.

We do not provide `yte` to `predict()`.

We use it afterward to check how well the model performed.

# 12. Step 8: Understand Accuracy

```python
print("Accuracy:", round(accuracy_score(yte, pred), 3))
```

Accuracy calculates the percentage of correct predictions.

Formula:

\[
Accuracy = \frac{CorrectPredictions}{TotalPredictions}
\]

Imagine:

- Total test records = 38.
- Correct predictions = 36.

Then:

\[
Accuracy = \frac{36}{38}
\]

\[
Accuracy = 0.947
\]

In percentage:

\[
Accuracy = 94.7\%
\]

A higher accuracy generally indicates better classification performance.

# 13. Step 9: Understand Confusion Matrix

```python
print(confusion_matrix(yte, pred))
```

A confusion matrix helps us understand which classes were predicted correctly and incorrectly.

For three classes, it produces a 3 × 3 matrix.

The rows represent actual classes.

The columns represent predicted classes.

Example:

```text
[[13  0  0]
 [ 0 12  1]
 [ 0  1 11]]
```

This is an illustrative example of a confusion matrix.

### Understand the Matrix

| Actual / Predicted | Setosa | Versicolor | Virginica |
|---|---:|---:|---:|
| Setosa | 13 | 0 | 0 |
| Versicolor | 0 | 12 | 1 |
| Virginica | 0 | 1 | 11 |

How do we interpret it?

**Setosa**

- 13 flowers were correctly classified.
- 0 were incorrectly classified.

**Versicolor**

- 12 were correctly classified.
- 1 was incorrectly classified as Virginica.

**Virginica**

- 11 were correctly classified.
- 1 was incorrectly classified as Versicolor.

### Important

The diagonal values represent correct predictions.

The off-diagonal values represent incorrect predictions.

A good classifier generally has large values on the diagonal and small values outside it.

# 14. Step 10: Understand Classification Report

```python
print(classification_report(
    yte,
    pred,
    target_names=iris.target_names
))
```

This produces a detailed evaluation report.

It includes:

- Precision
- Recall
- F1-score
- Support

### A. Precision

Precision answers:

**Out of all flowers predicted as a particular species, how many were actually that species?**

Formula:

\[
Precision = \frac{TP}{TP+FP}
\]

Where:

- TP = True Positives.
- FP = False Positives.

Higher precision means fewer incorrect positive predictions.

### B. Recall

Recall answers:

**Out of all actual flowers belonging to a particular species, how many did the model correctly identify?**

Formula:

\[
Recall = \frac{TP}{TP+FN}
\]

Where:

- TP = True Positives.
- FN = False Negatives.

Higher recall means fewer actual examples of a class are missed.

### C. F1-Score

F1-score combines precision and recall using their harmonic mean.

Formula:

\[
F1 = 2 \times \frac{Precision \times Recall}{Precision+Recall}
\]

It is useful when we want to balance precision and recall.

### D. Support

Support tells us how many actual test records belong to each class.

Example:

| Species | Support |
|---|---:|
| Setosa | 13 |
| Versicolor | 13 |
| Virginica | 12 |

These counts add up to 38 test records.

# 15. Step 11: Predict a Completely New Flower

Now comes the most interesting part.

Imagine someone gives you a new flower.

Its measurements are:

| Feature | Measurement |
|---|---:|
| Sepal Length | 5.1 |
| Sepal Width | 3.5 |
| Petal Length | 1.4 |
| Petal Width | 0.2 |

We create:

```python
sample = [[5.1, 3.5, 1.4, 0.2]]
```

Why double square brackets?

Because Scikit-learn expects a two-dimensional feature matrix.

This represents:

- One flower.
- Four features.

Now:

```python
model.predict(sample)
```

The model:

1. Receives the new flower measurements.
2. Applies the previously learned StandardScaler.
3. Passes the transformed values to Logistic Regression.
4. Predicts the species.

The output will be a numerical class label.

To convert that number into the actual species name:

```python
iris.target_names[model.predict(sample)[0]]
```

For this sample, the predicted species is:

```text
setosa
```

### Why Do We Use iris.target_names?

Because the model returns numerical labels:

| Prediction | Species |
|---:|---|
| 0 | setosa |
| 1 | versicolor |
| 2 | virginica |

`iris.target_names` converts the predicted number into a readable species name.

# 16. Complete Program Flow

```text
                 IRIS DATASET
                   150 RECORDS
                       |
                       |
                train_test_split()
                       |
              ---------------------
              |                   |
              v                   v
           TRAINING             TESTING
           112 records          38 records
              |                   |
              v                   |
        STANDARD SCALER            |
              |                   |
              v                   |
        LOGISTIC REGRESSION        |
              |                   |
              v                   |
         TRAINED MODEL             |
              |                   |
              ---------------------
                       |
                       v
                 PREDICTIONS
                       |
                       v
              COMPARE WITH yte
                       |
                       v
                MODEL EVALUATION
                       |
          ---------------------------
          |            |            |
          v            v            v
       Accuracy    Confusion     Classification
                   Matrix         Report
                       |
                       v
               PREDICT NEW FLOWER
                       |
                       v
             SETOSA / VERSICOLOR /
                   VIRGINICA
```

# 17. Complete Improved Program

Here is the same program with additional explanations and a few extra outputs.

```python
# Step 1: Import libraries

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Step 2: Load dataset

iris = load_iris()

X = iris.data
y = iris.target

print("Dataset shape:", X.shape)
print("Target shape:", y.shape)
print("Species:", iris.target_names)

# Step 3: Split dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Step 4: Create pipeline

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

# Step 5: Train model

model.fit(X_train, y_train)

# Step 6: Make predictions

predictions = model.predict(X_test)

# Step 7: Evaluate model

print("Accuracy:", round(
    accuracy_score(y_test, predictions), 3
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("Classification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=iris.target_names
))

# Step 8: Predict a new flower

sample = [[5.1, 3.5, 1.4, 0.2]]

prediction = model.predict(sample)[0]

print("Predicted Flower:", iris.target_names[prediction])

# Step 9: Get predicted probabilities

probabilities = model.predict_proba(sample)[0]

print("Class probabilities:")

for species, probability in zip(
    iris.target_names,
    probabilities
):
    print(species, round(probability * 100, 2), "%")
```

# 18. Additional Concept: predict_proba()

This is an interesting concept to demonstrate in class.

Instead of just asking:

"What is the predicted species?"

We can ask:

"What probability did the model assign to each species?"

```python
probabilities = model.predict_proba(sample)[0]

print(probabilities)
```

Example output might look like:

```text
[0.97 0.02 0.01]
```

This means the model assigned approximately:

| Species | Estimated Probability |
|---|---:|
| Setosa | 97% |
| Versicolor | 2% |
| Virginica | 1% |

These are illustrative probabilities.

The predicted class is the class with the highest estimated probability.

**Important:** A predicted probability is not necessarily a guarantee that the prediction is correct. Probability calibration and model validation matter.

# 19. Practice Exercises for Students

## Beginner

1. Print the complete Iris dataset.
2. Print all four feature names.
3. Print all three species names.
4. Change `test_size=0.25` to `test_size=0.20`.
5. Print the number of training and testing records.
6. Predict another flower using new measurements.

## Intermediate

7. Remove StandardScaler and compare the model's performance.
8. Change `max_iter=1000` to `max_iter=100`.
9. Print the confusion matrix.
10. Explain precision and recall.
11. Print the predicted probability for each species.
12. Compare the predicted class with the actual class.

## Challenge

13. Train a Decision Tree Classifier on the same dataset.
14. Compare Logistic Regression and Decision Tree.
15. Compare their accuracy scores.
16. Use cross-validation to evaluate both algorithms.
17. Identify which species is most frequently misclassified.

# 20. Important Concepts to Remember

| Concept | Explanation |
|---|---|
| Classification | Predicts categories |
| Iris dataset | Dataset containing 150 flower records |
| Features (X) | Four flower measurements |
| Target (y) | Flower species |
| Logistic Regression | Classification algorithm |
| StandardScaler | Standardizes numerical features |
| Pipeline | Connects preprocessing and model |
| train_test_split() | Separates training and testing data |
| stratify | Maintains approximate class proportions |
| fit() | Trains the model |
| predict() | Predicts the class |
| predict_proba() | Returns estimated class probabilities |
| Accuracy | Overall correct prediction percentage |
| Confusion Matrix | Shows correct and incorrect classifications |
| Precision | Measures correctness of positive predictions |
| Recall | Measures how many actual positives were found |
| F1-score | Combines precision and recall |

# Final Teaching Summary

Think of this project as teaching a student to identify flowers.

- X = Four measurements of a flower.
- y = Actual flower species.
- StandardScaler = Standardizes the measurements.
- Logistic Regression = Learns patterns between measurements and species.
- fit() = Teaches the model.
- predict() = Identifies a new flower.
- Accuracy = Measures overall correctness.
- Confusion Matrix = Shows which species were confused.
- Classification Report = Gives detailed performance information.

**The main lesson:**

Classification allows a Machine Learning model to learn from labelled examples and predict which category a new record belongs to.

