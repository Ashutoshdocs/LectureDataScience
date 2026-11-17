# 📘 Gradient Boosting Regressor: A Teaching Guide

A beginner-friendly guide to **what** gradient boosting is, **how** it works, and **how to use it in Python**. It uses the student-marks demo throughout:

> **Inputs:** study hours, coaching (Yes/No), live sessions attended, recorded course completion %
> **Output:** final marks

---

## 1. What is Gradient Boosting?

**Gradient Boosting** builds a strong model out of many **weak** models (small decision trees), added **one at a time**. Each new tree focuses on **what the model is still getting wrong**.

### An everyday analogy

A student practises for an exam:

1. Takes a practice test. Gets some questions wrong.
2. Studies **only the topics they got wrong**.
3. Takes another test. Still a few mistakes, but fewer.
4. Studies **those** topics.
5. Repeats, improving a little each time.

Gradient boosting does exactly this. Each tree "studies the mistakes" of the model so far.

| Term | Meaning | In our demo |
|------|---------|-------------|
| **Weak learner** | A simple model that's only slightly better than guessing | a tree of depth 2 |
| **Residual** | Actual value − current prediction (the mistake left to fix) | e.g. 62 − 59 = +3 marks |
| **Boosting** | Adding weak learners one after another, each fixing the last | |
| **Learning rate** | How much of each tree's correction is used | 0.05 |
| **`n_estimators`** | Number of trees added | 300 |

---

## 2. Boosting vs. Bagging (Random Forest)

Both combine many trees, but in opposite ways:

```
 RANDOM FOREST (bagging)                 GRADIENT BOOSTING
 Trees built INDEPENDENTLY, in parallel  Trees built IN SEQUENCE

   ┌─ Tree 1 ─┐                           Start ─► Tree 1 ─► Tree 2 ─► Tree 3 ─► ...
   ├─ Tree 2 ─┤                                     fixes     fixes     fixes
   ├─ Tree 3 ─┼─► AVERAGE                          start's   tree 1's  tree 2's
   └─ ...    ─┘                                    mistakes  mistakes  mistakes
```

| | Random Forest | Gradient Boosting |
|---|---|---|
| How trees are built | Independently (can be parallel) | One after another |
| Size of each tree | **Big**, deep trees | **Small**, shallow trees (depth 1–5) |
| How they're combined | **Average** | **Sum** of small corrections |
| Each tree learns from | A random sample of students | The **residuals** of the model so far |
| Main thing it reduces | Variance (overfitting of one tree) | Bias (underfitting of simple models) |
| Overfits with too many trees? | Almost never | **Yes, slowly** |
| Tuning needed | Little | More (learning rate, trees, depth) |

---

## 3. How Gradient Boosting Works, Step by Step

### Step 0: Start with a simple guess

Predict the **average** marks for every student.

```
 Average marks = 59.0  →  everyone is predicted 59.0
```

### Step 1: Calculate the residuals

```
 residual = actual marks − current prediction
```

| Student | Actual | Prediction | Residual |
|---------|--------|------------|----------|
| A | 38.6 | 59.0 | **−20.4** (predicted too high) |
| B | 62.1 | 59.0 | **+3.1** (predicted too low) |
| C | 81.0 | 59.0 | **+22.0** (predicted too low) |

### Step 2: Train a small tree to predict the residuals

The tree is **not** trained on marks. It's trained on the **residuals**, so it learns *which kinds of students the model is getting wrong, and by how much*.

From `gradient_boosting_from_scratch.py`, tree 1:

```
  study_hours <= 3.95?
    YES:
      live_sessions_attended <= 12.50?
        YES: -> correction -10.65 marks    (low study, few sessions: we guessed too high)
        NO:  -> correction  -2.03 marks
    NO:
      live_sessions_attended <= 6.50?
        YES: -> correction  -1.56 marks
        NO:  -> correction  +7.29 marks    (more study, many sessions: we guessed too low)
```

### Step 3: Add a small part of the correction

```
 new prediction = old prediction + learning_rate × tree's correction
```

For a student in the bottom-right leaf: `59.0 + 0.05 × 7.29 = 59.4`

### Step 4: Repeat

Calculate new residuals, train a new tree on them, add a small part of its correction. Do this 300 times.

```
 F₀(x) = average
 F₁(x) = F₀(x) + η · tree₁(x)        tree₁ trained on  y − F₀(x)
 F₂(x) = F₁(x) + η · tree₂(x)        tree₂ trained on  y − F₁(x)
 ...
 F₃₀₀(x) = F₂₉₉(x) + η · tree₃₀₀(x)

 (η = learning rate = 0.05)
```

### Watching one student's prediction

From `gradient_boosting_from_scratch.py`, a student whose actual mark is **38.6**:

```
  Start (average)  : 59.0
  After   1 trees  : 58.4   (still -19.8 to go)
  After  10 trees  : 55.1   (still -16.5 to go)
  After  25 trees  : 50.7   (still -12.1 to go)
  After  50 trees  : 48.4   (still -9.8 to go)
  After 100 trees  : 46.3   (still -7.7 to go)
  After 200 trees  : 44.8   (still -6.2 to go)
```

Every tree moves the prediction a little closer. (It doesn't reach 38.6 exactly, partly because some of that student's mark is random noise that no model could predict.)

👉 Run `python gradient_boosting_from_scratch.py` to see all of this in plain Python.

---

## 4. Why Is It Called "Gradient"?

Remember **gradient descent** from linear regression: take small steps **downhill** on the error to find the best answer.

For squared error, `Loss = ½ (actual − prediction)²`, the gradient with respect to the prediction is:

```
 ∂Loss/∂prediction = −(actual − prediction) = −residual
```

So **the residual is the negative gradient**. Training each tree on the residuals means each tree points "downhill", and the learning rate is the step size.

| Gradient descent (linear regression) | Gradient boosting |
|---|---|
| Adjusts the **numbers** m and c | Adds a whole new **tree** |
| Step = learning rate × gradient | Step = learning rate × tree fitted to the gradient |

Gradient boosting is **gradient descent where each step is a tree**. With other loss functions (e.g. absolute error), the trees fit that loss's gradient instead, but the idea is the same.

---

## 5. The Key Settings (Hyperparameters)

| Setting | What it does | Our demo |
|---------|--------------|----------|
| `n_estimators` | Number of trees | 300 |
| `learning_rate` | How much of each tree's correction is used | 0.05 |
| `max_depth` | Depth of each tree (kept small) | 2 |
| `subsample` | Fraction of students each tree learns from | 0.8 |
| `min_samples_leaf` | Minimum students in each leaf | default (1) |
| `loss` | What error to minimise | default (squared error) |

### Learning rate: small steps are safer

Same data, 300 trees, depth 2:

| Learning rate | Train R² | Test R² | |
|---------------|----------|---------|---|
| 1.0 | 0.988 | 0.667 | ❌ steps too big: overfits |
| 0.5 | 0.980 | 0.759 | |
| 0.1 | 0.953 | 0.863 | |
| **0.05** | 0.937 | **0.872** | ✅ best |
| 0.01 | 0.851 | 0.778 | ❌ steps too small: 300 trees isn't enough |

**Rule of thumb:** a smaller learning rate needs **more trees**, but usually gives a better model.

### Tree depth: weak learners work best

| `max_depth` | Train R² | Test R² | |
|-------------|----------|---------|---|
| 1 ("stumps") | 0.903 | 0.857 | |
| **2** | 0.937 | **0.872** | ✅ best |
| 3 | 0.966 | 0.862 | |
| 6 | **1.000** | 0.818 | ❌ trees too strong: overfits |

### Number of trees: yes, too many can hurt

Unlike a random forest, boosting **keeps fitting the training data** with every tree, so eventually it starts learning the noise:

| Trees | Test R² |
|-------|---------|
| 100 | 0.843 |
| **300** | **0.872** ✅ |
| 500 | 0.867 |
| 1,000 | 0.855 |
| 2,000 | 0.835 |

The best was around 300. The fix is **early stopping**: watch the test (validation) error and stop adding trees when it stops improving.

```python
model = GradientBoostingRegressor(
    n_estimators=2000, learning_rate=0.05, max_depth=2,
    validation_fraction=0.2, n_iter_no_change=20,   # stop if 20 trees in a row don't help
)
```

### Subsample: a little randomness helps

`subsample=0.8` means each tree learns from a random 80% of the students. This is called **stochastic gradient boosting**. It makes the trees a bit more different from each other and reduces overfitting (borrowing the random forest idea).

---

## 6. How Good Is the Model?

| Metric | Meaning | Good value |
|--------|---------|------------|
| **R² score** | How much of the variation in marks the model explains | Close to **1.0** |
| **MAE** (Mean Absolute Error) | Average size of the mistake, in marks | As **small** as possible |
| **RMSE** | Root mean squared error, in marks | As **small** as possible |

**All models in this series, on the same unseen students:**

| Model | Test R² | Avg error |
|-------|---------|-----------|
| Linear regression | 0.765 | 3.20 marks |
| Single decision tree | 0.634 | 4.03 marks |
| Random forest | 0.817 | 2.80 marks |
| **Gradient boosting** | **0.872** | **2.42 marks** |

---

## 7. Feature Importance

Like a random forest, gradient boosting reports which inputs it relied on most:

```
    study_hours                  47.3%  ████████████████████████
    live_sessions_attended       25.5%  █████████████
    recorded_course_completion   17.0%  ████████
    coaching                     10.2%  █████
```

For a student with 6 study hours, 10 live sessions and 50% of the recorded course:

| Coaching | Predicted marks |
|----------|-----------------|
| No | 63.9 |
| Yes | 68.8 |

Remember: importance shows **how useful a feature was for splitting**, not **how much it changes marks**, and never proves cause and effect.

---

## 8. Strengths and Limitations

### ✅ Strengths
- Often the **most accurate** model for tables of data (spreadsheet-style data)
- Finds **curves and interactions** on its own
- Uses **small trees**, so the model is compact
- Flexible: works with different loss functions

### ⚠️ Limitations
- **More tuning** needed (learning rate, number of trees, depth)
- **Can overfit** if the learning rate is too high or there are too many trees
- **Slower to train** than a random forest, because trees must be built one after another
- **Hard to explain**: 300 trees added together
- **Can't extrapolate**: 20 study hours gets the same prediction as 10 (72.8 marks)
- Sensitive to **noisy data and outliers** (it keeps trying to fix them)

### Popular libraries

The same idea powers some of the most widely used ML libraries, which add speed tricks and extra regularisation:
- **scikit-learn**: `GradientBoostingRegressor`, `HistGradientBoostingRegressor` (faster)
- **XGBoost**, **LightGBM**, **CatBoost**: popular in industry and competitions

---

## 9. Gradient Boosting in Python

### With scikit-learn (the usual way)

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load data and turn Yes/No into 1/0
df = pd.read_csv("train.csv")
df["coaching"] = (df["coaching"] == "Yes").astype(int)

features = ["study_hours", "coaching", "live_sessions_attended", "recorded_course_completion"]
X = df[features]
y = df["final_marks"]

# 2. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train
model = GradientBoostingRegressor(
    n_estimators=300, learning_rate=0.05, max_depth=2, subsample=0.8, random_state=42
)
model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
print("Test R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))

# 5. Watch the test score change as trees are added
for k, pred in enumerate(model.staged_predict(X_test), 1):
    if k in (1, 10, 50, 100, 300):
        print(k, "trees -> R²", round(r2_score(y_test, pred), 3))

# 6. Feature importance
for name, imp in zip(features, model.feature_importances_):
    print(f"{name}: {imp:.1%}")

# 7. Predict for a new student
new = pd.DataFrame([[6, 1, 15, 80]], columns=features)
print("Predicted marks:", model.predict(new)[0])
```

### From scratch (to understand it)

See **`gradient_boosting_from_scratch.py`**: start with the average, then repeatedly fit a small tree to the residuals and add a fraction of it.

---

## 10. Summary

```
 Start with the average
   └─► residuals = actual − prediction
         └─► fit a small tree to the residuals
               └─► prediction += learning_rate × tree
                     └─► repeat N times
```

- Gradient boosting adds **small trees one after another**
- Each tree is trained on the **residuals** (mistakes) of the model so far
- Residuals are the **negative gradient** of squared error, so this is **gradient descent with trees**
- A **small learning rate** with **enough trees** works best
- It **can overfit** with too many trees or too high a learning rate, so use a test set or early stopping
- It's often the **most accurate** model for tabular data

---

## 11. Practice Exercises ✏️

1. Using tree 1 from Section 3, what correction would a student with 2 study hours and 15 live sessions get? What would their prediction be after tree 1?
2. In `train.py`, set `LEARNING_RATE` to 1.0, 0.1 and 0.01. Record the Test R² for each. Explain the results.
3. Set `MAX_DEPTH` to 1 and then 6. What happens to Train R² and Test R²?
4. Set `N_TREES = 2000`. Look at the error table. When does the test error stop improving?
5. Add early stopping (`validation_fraction=0.2, n_iter_no_change=20`) and print `model.n_estimators_`. How many trees did it actually use?
6. Compare `predict.py` in this demo and the Random Forest demo for the same student. How do the two explanations differ ("trees voted" vs. "trees added corrections")?
7. Set `SUBSAMPLE = 1.0` (no randomness). Does the test score change?
