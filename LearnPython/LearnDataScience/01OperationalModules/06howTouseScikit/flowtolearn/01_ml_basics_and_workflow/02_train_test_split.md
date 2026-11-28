# Diabetes Progression Prediction Using Scikit-learn
## Understanding Train-Test Split, Model Training and Evaluation

# 1. What Is This Program Doing?

Imagine you are a teacher.

You have historical information about **442 diabetes patients**. You want to build a Machine Learning model that predicts disease progression based on medical measurements.

But there is one important question:

**How do you know whether your model will work for a new patient?**

You cannot simply train and test using the same data. The model might perform well because it has already seen those examples.

To solve this problem, we divide the dataset into two parts.

### Dataset Distribution

**Total dataset: 442 records**

| Dataset | Percentage | Records | Purpose |
|---|---:|---:|---|
| Training | 80% | 353 | Teach the model |
| Testing | 20% | 89 | Evaluate the model |

The model learns from 353 records and is evaluated using 89 records it did not see during training.

# 2. Understand Each Line of Code

## Step 1: Import Libraries

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
```

| Library / Function | Purpose |
|---|---|
| `load_diabetes` | Loads an example diabetes dataset |
| `train_test_split` | Divides data into training and testing |
| `LinearRegression` | Machine Learning regression algorithm |
| `mean_absolute_error` | Measures average prediction error |
| `r2_score` | Measures how well the model explains target variation |

## Step 2: Load the Dataset

```python
data = load_diabetes()
```

Scikit-learn provides a ready-made dataset.

Let's inspect it:

```python
print(data.data.shape)
print(data.target.shape)
print(data.feature_names)

print(data.data[0])
print(data.target[0])
```

Expected output:

```text
(442, 10)
(442,)
```

This means:

- 442 rows (patients).
- 10 input features per patient.
- 442 target values.

### What Are X and y?

In Machine Learning, we generally use two important variables:

**X = Input Features**

The medical measurements used by the model.

**y = Target**

The disease progression measure that we want to predict.

| X — Features | y — Target |
|---|---|
| 10 input measurements | 1 output value |
| Patient measurements | Disease progression measure |

The dataset contains ten features, including age, sex, BMI, blood pressure and six blood serum measurements.

Note: The target represents a quantitative measure of disease progression one year after baseline. This is an educational prediction example, not a diagnostic tool.

## Step 3: Split the Dataset

This is one of the most important lines:

```python
X_train, X_test, y_train, y_test = train_test_split(
    data.data,
    data.target,
    test_size=0.2,
    random_state=42
)
```

Let's understand the four variables.

| Variable | Meaning |
|---|---|
| `X_train` | Input features for training |
| `X_test` | Input features for testing |
| `y_train` | Actual answers for training |
| `y_test` | Actual answers for testing |

### What Does `test_size=0.2` Mean?

It means 20% of the dataset is reserved for testing.

The remaining 80% is used for training.

For 442 records:

- Training: 353 records
- Testing: 89 records

Scikit-learn uses the ceiling of the calculated test-set size, so 20% of 442 gives 89 test records.

### What Does `random_state=42` Mean?

It makes the random split reproducible.

If you execute the code again with the same data and settings, you get the same split.

You can use other integers instead of 42.

The number 42 has no special mathematical meaning here.

## Step 4: Create the Model

```python
model = LinearRegression()
```

Here, we create a Linear Regression model.

At this point, the model has not learned anything from our dataset.

Think of it as a student who is ready to learn.

## Step 5: Train the Model

```python
model.fit(X_train, y_train)
```

This is where learning happens.

The model:

1. Receives patient measurements (`X_train`).
2. Receives the corresponding actual outcomes (`y_train`).
3. Learns relationships between input features and outcomes.
4. Calculates coefficients and an intercept.

The model learns a mathematical relationship:

\[
y = b + w_1x_1 + w_2x_2 + \cdots + w_{10}x_{10}
\]

Where:

- \(x\) = Patient features.
- \(w\) = Learned coefficients.
- \(b\) = Intercept.
- \(y\) = Predicted disease progression.

## Step 6: Make Predictions

```python
pred = model.predict(X_test)
```

Now we give the model 89 patients it did not see during training.

The model predicts their outcomes.

**Important:** We do not provide `y_test` to `predict()`.

The actual answers are kept separately so that we can evaluate the predictions afterward.

## Step 7: Check Training and Testing Records

```python
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
```

Expected output:

```text
Training rows: 353
Testing rows: 89
```

This confirms how many records went into each set.

# 3. Understand Model Evaluation

Now comes the interesting part.

We have:

- Actual values: `y_test`
- Predicted values: `pred`

We compare them to understand how well the model performs.

## A. Mean Absolute Error (MAE)

```python
print("MAE:", round(mean_absolute_error(y_test, pred), 2))
```

MAE calculates the average absolute difference between actual and predicted values.

### Example

Imagine the model produces these predictions:

| Patient | Actual | Predicted | Absolute Error |
|---|---:|---:|---:|
| A | 100 | 110 | 10 |
| B | 200 | 180 | 20 |
| C | 150 | 160 | 10 |

The formula is:

\[
MAE = \frac{\sum_{i=1}^{n}|y_i-\hat y_i|}{n}
\]

Therefore:

\[
MAE = \frac{10+20+10}{3}
\]

\[
\boxed{MAE = 13.33}
\]

**Lower MAE is generally better.**

It means the model's predictions are closer to actual values on average.

Remember that MAE is expressed in the same units as the target.

## B. R² Score

```python
print("R2:", round(r2_score(y_test, pred), 3))
```

R² tells us how well the model explains the variation in the target values.

| R² Score | General Interpretation |
|---:|---|
| 1.0 | Perfect predictions |
| 0.8 | Strong explanatory performance |
| 0.5 | Moderate explanatory performance |
| 0.0 | No improvement over predicting the test-set mean |
| Negative | Worse than predicting the test-set mean |

These are illustrative interpretations, not universal quality thresholds.

The formula is:

\[
R^2=1-\frac{\sum(y_i-\hat y_i)^2}{\sum(y_i-\bar y)^2}
\]

Where:

- \(y_i\) = Actual value.
- \(\hat y_i\) = Predicted value.
- \(\bar y\) = Mean of actual target values.

**Important:** R² can be negative. It does not always lie between zero and one.

# 4. Complete Flow of the Program

```text
             DIABETES DATASET
                442 Records
                    |
                    |
             train_test_split()
                    |
             -----------------
             |               |
             |               |
         TRAINING          TESTING
          80%                20%
         353 rows           89 rows
             |               |
             |               |
         X_train            X_test
         y_train              |
             |                |
             |                |
         model.fit()          |
             |                |
             |                |
       MODEL LEARNS            |
       THE PATTERNS            |
             |                |
             |                |
             -----------      |
                       |      |
                  model.predict()
                       |
                       |
                 PREDICTIONS
                       |
                       |
              Compare with y_test
                       |
                       |
               MODEL EVALUATION
                  /       \
                 /         \
               MAE         R²
```

# 5. Try This Experiment With Students

Change only `test_size` and observe what happens.

```python
test_size=0.1
test_size=0.2
test_size=0.3
test_size=0.4
```

### Experiment: Dataset Distribution

| Test Percentage | Training Records | Testing Records |
|---:|---:|---:|
| 10% | 397 | 45 |
| 20% | 353 | 89 |
| 30% | 309 | 133 |
| 40% | 265 | 177 |

These counts use scikit-learn's test-set ceiling behavior.

### Ask Students

1. What happens if we increase testing data?
2. What happens to the amount of data available for learning?
3. Can a model perform better with more training data?
4. Does a larger testing dataset always mean a better model?
5. Why should testing data remain separate from training?

### Expected Understanding

- Increasing test data reduces training data.
- Reducing training data may affect how well the model learns.
- A larger test dataset can provide a more stable evaluation.
- We need a balance between training and testing.

# 6. Important Concepts Students Should Remember

| Concept | Explanation |
|---|---|
| Dataset | Complete collection of records |
| Features (X) | Inputs given to the model |
| Target (y) | Output we want to predict |
| Training data | Data used for learning |
| Testing data | Unseen data used for evaluation |
| `.fit()` | Train the model |
| `.predict()` | Generate predictions |
| MAE | Average absolute prediction error |
| R² | Explains variation in target values |
| `random_state` | Makes the random split reproducible |

# 7. Complete Python Program

Create a file named:

`diabetes_train_test.py`

```python
# Step 1: Import libraries
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Step 2: Load dataset
data = load_diabetes()

# Step 3: Separate features and target
X = data.data
y = data.target

# Step 4: Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Step 5: Create model
model = LinearRegression()

# Step 6: Train model
model.fit(X_train, y_train)

# Step 7: Make predictions
pred = model.predict(X_test)

# Step 8: Display dataset distribution
print("Total records:", len(X))
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# Step 9: Evaluate model
print("MAE:", round(mean_absolute_error(y_test, pred), 2))
print("R2:", round(r2_score(y_test, pred), 3))
```

Run:

```bash
python diabetes_train_test.py
```

# 8. Important Teaching Point: What Comes Next?

This program demonstrates a **holdout evaluation**, not a guarantee of future performance.

The test data should not be repeatedly used to tune the model.

For more reliable evaluation, we can introduce:

1. Cross-validation.
2. K-Fold Cross-Validation.
3. Model comparison.
4. Hyperparameter tuning.
5. Pipeline-based preprocessing.

These concepts will help students understand how real-world Machine Learning projects are evaluated.

---

# Final Teaching Analogy

"Training is like teaching a student using 80 questions. Testing is like giving that student 20 new questions to check whether they actually learned the concept or simply memorized the answers."

**The main lesson:** A Machine Learning model is not useful merely because it learns from historical data. We also need to check how well it performs on data it has never seen.