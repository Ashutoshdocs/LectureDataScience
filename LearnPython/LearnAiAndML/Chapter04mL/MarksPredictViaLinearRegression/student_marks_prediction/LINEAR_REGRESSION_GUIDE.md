# 📘 Linear Regression: A Teaching Guide

A beginner-friendly guide to **what** linear regression is, **how** it works, and **how to use it in Python**. It uses the student-marks demo (study hours → marks) throughout.

---

## 1. What is Linear Regression?

**Linear Regression** is a machine learning method that predicts a **number** by finding the **best straight line** through the data.

**Examples of what it can predict:**
- A student's marks from study hours
- A house price from its size
- Ice-cream sales from temperature

It's a **supervised learning** algorithm: we train it on examples where we already know the answer, and it learns the pattern.

| Term | Meaning | In our demo |
|------|---------|-------------|
| **Input** (x, feature) | What we know | study hours |
| **Output** (y, target) | What we want to predict | final marks |
| **Training data** | Examples with known answers | `train.csv` |
| **Model** | The learned line | `model.pkl` |

---

## 2. The Big Idea: Fitting a Line

Remember the line equation from school maths:

```
y = m·x + c
```

- **x**: the input (study hours)
- **y**: the output (marks)
- **m**: the **slope**, how much y changes when x increases by 1
- **c**: the **intercept**, the value of y when x = 0

```
 Marks
 100 |                         ●
     |                    ●  /
  80 |               ●   / ●
     |           ●    /  ●
  60 |       ●     /  ●
     |    ●     / ●
  40 |  ●    /
     |    /  ●
  20 |
     +------------------------------
       1  2  3  4  5  6  7  8  9  10   Study hours
```

The dots are real students. Linear regression finds the line that passes **as close as possible to all the dots**.

**Our demo learns:** `marks = 5.98 × study_hours + 29.68`

- A student studying **6 hours** → 5.98 × 6 + 29.68 = **65.5 marks**
- Each extra hour of study adds about **6 marks** (the slope)
- With 0 hours, the model predicts about **30 marks** (the intercept)

---

## 3. How Does It Find the "Best" Line?

### Step 1: Measure the error

For each student, the **error** (or *residual*) is:

```
error = predicted marks − actual marks
```

```
   ●  ← actual (80)
   |
   |  error = 5
   |
 --x---- line   ← predicted (75)
```

### Step 2: Combine all the errors: Mean Squared Error (MSE)

```
MSE = (1/n) × Σ (predicted − actual)²
```

**Why square the errors?**
- So positive and negative errors don't cancel out
- So big mistakes are punished more than small ones

The **best line is the one with the smallest MSE**. This is called the **Least Squares** method.

### Step 3: Find the m and c that minimise MSE

There are two ways:

#### Method A: Exact formula (Ordinary Least Squares)

```
m = Σ (x − x̄)(y − ȳ) / Σ (x − x̄)²
c = ȳ − m·x̄
```

(x̄ and ȳ are the averages of x and y.)
This is what **scikit-learn's `LinearRegression`** calculates.

**Tiny worked example** (3 students):

| x (hours) | y (marks) | x − x̄ | y − ȳ | (x − x̄)(y − ȳ) | (x − x̄)² |
|---|---|---|---|---|---|
| 2 | 40 | −2 | −20 | 40 | 4 |
| 4 | 60 | 0 | 0 | 0 | 0 |
| 6 | 80 | 2 | 20 | 40 | 4 |
| x̄ = 4 | ȳ = 60 | | | **Σ = 80** | **Σ = 8** |

```
m = 80 / 8 = 10
c = 60 − 10 × 4 = 20
Line: marks = 10 × hours + 20
```

#### Method B: Gradient Descent (step by step)

Imagine standing on a hill in fog and wanting to reach the bottom. You feel the slope under your feet and take a small step downhill, again and again.

```
1. Start with a guess:  m = 0, c = 0
2. Calculate the MSE
3. Find which direction reduces the error (the gradient)
4. Move m and c a small step in that direction
5. Repeat until the error stops decreasing
```

The update rules:

```
m = m − learning_rate × ∂MSE/∂m
c = c − learning_rate × ∂MSE/∂c

where
∂MSE/∂m = (2/n) × Σ (predicted − actual) × x
∂MSE/∂c = (2/n) × Σ (predicted − actual)
```

- **Learning rate**: the step size. Too big and you overshoot; too small and it's very slow.
- **Epoch**: one full pass over the data.

👉 Run `python linear_regression_from_scratch.py` to watch this happen. The MSE falls and m, c settle on **5.98** and **29.68**, the same as the exact formula.

---

## 4. How Good Is the Model?

| Metric | Meaning | Good value |
|--------|---------|------------|
| **R² score** | How much of the variation in marks the line explains | Close to **1.0** |
| **MAE** (Mean Absolute Error) | Average size of the mistake, in marks | As **small** as possible |
| **MSE** | Average squared error | As **small** as possible |
| **RMSE** | √MSE, back in the original units (marks) | As **small** as possible |

Always test on data the model **hasn't seen** during training (a *train/test split*), otherwise you're just checking whether it memorised the answers.

In our demo: **R² ≈ 0.97** and **MAE ≈ 2.5 marks**, so predictions are usually within 2 to 3 marks.

---

## 5. Assumptions of Linear Regression

Linear regression works best when:

1. **Linearity**: the relationship between x and y is roughly a straight line
2. **Independence**: each data point is independent of the others
3. **Constant variance**: errors are about the same size along the whole line
4. **Normal errors**: errors are roughly bell-shaped around zero

---

## 6. Limitations ⚠️

- **Only straight lines**: it can't capture curves (e.g. marks levelling off after 8 hours)
- **Sensitive to outliers**: one extreme point can pull the line a lot
- **Extrapolation is risky**: training data only goes up to 10 hours, so predicting for 15 hours gives 5.98 × 15 + 29.68 = 119 marks, which is impossible. That's why `predict.py` caps marks at 0–100.
- **Correlation ≠ causation**: the line shows study hours and marks move together, not that one *causes* the other

---

## 7. Linear Regression in Python

### With scikit-learn (the usual way)

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load data
df = pd.read_csv("train.csv")
X = df[["study_hours"]]   # input  (double brackets = table with one column)
y = df["final_marks"]     # output

# 2. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
print("R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))

# 5. Look at the learned line
print("Slope (m):", model.coef_[0])
print("Intercept (c):", model.intercept_)

# 6. Predict for a new student
print("Predicted marks:", model.predict(pd.DataFrame({"study_hours": [6]}))[0])
```

### From scratch (to understand it)

See **`linear_regression_from_scratch.py`**, which uses no ML library at all.

---

## 8. Summary

```
 Data (x, y)  →  Find line that minimises squared error  →  y = m·x + c  →  Predict new y
```

- Linear regression predicts a **number** with a **straight line**
- It learns the **slope (m)** and **intercept (c)** by **minimising Mean Squared Error**
- It can be solved **exactly** (least squares formula) or **step by step** (gradient descent)
- Check it with **R²** and **MAE** on **unseen data**
- It's simple, fast and easy to explain, which makes it a great first ML algorithm

---

## 9. Practice Exercises ✏️

1. Work out m and c by hand for: (1, 35), (3, 50), (5, 60). Check your answer with Python.
2. Using the demo's line, predict marks for 0, 5 and 10 hours.
3. In `linear_regression_from_scratch.py`, change `learning_rate` to `0.05`, then `0.0001`. What happens?
4. Add 3 fake students to `train.csv` with `study_hours = 10` and `final_marks = 20`, then retrain. How do m and c change? (This shows the effect of outliers.)
5. Predict marks for 20 study hours. Why is the answer unrealistic?
