# 📘 Polynomial Regression (Degree 3): A Teaching Guide

A beginner-friendly guide to **what** polynomial regression is, **how** it works, and **how to use it in Python**. It uses the student-marks demo (study hours → marks) throughout.

---

## 1. What is Polynomial Regression?

**Polynomial Regression** predicts a **number** by fitting a **curve** through the data instead of a straight line.

Use it when the relationship **bends**, for example:
- Marks rise with study hours, then **level off** (diminishing returns)
- Crop yield rises with fertiliser, then **falls** (too much harms the plant)
- A car's fuel use is high at low speed, lowest in the middle, high again at top speed

| Term | Meaning | In our demo |
|------|---------|-------------|
| **Input** (x) | What we know | study hours |
| **Output** (y) | What we want to predict | final marks |
| **Degree** | The highest power of x in the equation | 3 |
| **Training data** | Examples with known answers | `train.csv` |
| **Model** | The learned curve | `model.pkl` |

---

## 2. From a Line to a Curve

**Straight line (degree 1):**
```
y = b0 + b1·x
```

**Quadratic (degree 2):** one bend
```
y = b0 + b1·x + b2·x²
```

**Cubic (degree 3):** up to two bends, which is what our demo uses
```
y = b0 + b1·x + b2·x² + b3·x³
```

```
 Degree 1            Degree 2              Degree 3
 (no bend)           (one bend)            (up to two bends)

      /               \      /                    ____
     /                 \    /                   /
    /                   \__/                   /
   /                                       ___/
```

**What each coefficient does in our model:**
`marks = 32.0 − 0.13·x + 2.05·x² − 0.148·x³`

| Term | Value | Effect |
|------|-------|--------|
| `b0` | 32.0 | Starting marks at 0 hours |
| `b1·x` | −0.13 | Tiny; almost no straight-line effect on its own |
| `b2·x²` | +2.05 | Pushes the curve **up faster and faster** (the steep middle) |
| `b3·x³` | −0.148 | Small, but x³ grows fast, so it **pulls the curve down** at high hours (the plateau) |

---

## 3. The Key Idea: It's Still Linear Regression!

This surprises most students. Polynomial regression is **linear regression on extra columns**.

We take the single input x and **create new features** from it:

| x | x² | x³ |
|---|----|----|
| 2 | 4 | 8 |
| 5 | 25 | 125 |
| 8 | 64 | 512 |

Then we run ordinary linear regression with **x, x², x³ as three inputs**.

The curve bends in terms of x, but the equation is still a straight **sum of coefficients × columns**. That's why it's called "linear" in the coefficients. Same maths, same least-squares method, just more columns.

```
 study_hours  →  [x, x², x³]  →  Linear Regression  →  b0, b1, b2, b3
                 (PolynomialFeatures)
```

---

## 4. How Does It Find the "Best" Curve?

Exactly like linear regression: it picks the coefficients that make the **Mean Squared Error** as small as possible.

### Step 1: Measure the error

```
error = predicted marks − actual marks
MSE   = (1/n) × Σ (predicted − actual)²
```

Squaring stops positive and negative errors cancelling out, and punishes big mistakes more.

### Step 2: Solve for the coefficients with the Normal Equation

Put the data into a **design matrix X** (one row per student, one column per power of x) and a vector **y** of marks:

```
      [ 1   x₁   x₁²   x₁³ ]          [ y₁ ]
  X = [ 1   x₂   x₂²   x₂³ ]      y = [ y₂ ]
      [ ...               ]          [ ...]
      [ 1   xₙ   xₙ²   xₙ³ ]          [ yₙ ]
```

The best coefficients are:

```
 b = (Xᵀ X)⁻¹ Xᵀ y
```

- `Xᵀ` is X transposed (rows become columns)
- `⁻¹` means matrix inverse
- The result `b` is `[b0, b1, b2, b3]`

👉 Run `python polynomial_regression_from_scratch.py` to see this calculated with numpy. It gives exactly the same answer as scikit-learn.

**What about gradient descent?** It works too, but x³ values (up to 1000) are far bigger than x values (up to 10), so the steps are badly balanced unless you **scale** the features first. For small problems like this, the Normal Equation is simpler and exact.

---

## 5. Choosing the Degree: Underfitting vs. Overfitting

The degree is the most important choice you make.

| Degree | Result |
|--------|--------|
| **Too low** (e.g. 1) | **Underfitting**: too simple, misses the bend |
| **Just right** (e.g. 3 here) | Follows the real pattern |
| **Too high** (e.g. 15) | **Overfitting**: wiggles through every noisy point, fails on new students |

```
 Underfitting        Good fit              Overfitting
   (degree 1)        (degree 3)            (degree 15)

  ●    ●  /           ●  ____●             ●  /\  ●
    ● /  ●             /●                   \/  \/\●
   / ●               ●/                    ●/      ●
  /●                ●/                    /
```

**How to choose:** train several degrees and compare them on **test data the model hasn't seen**. Pick the one with the best test score, not the best training score.

In our demo, on unseen test students:

| Model | R² | Average error |
|-------|-----|---------------|
| Straight line | 0.933 | 3.88 marks |
| **Degree 3** | **0.976** | **2.53 marks** |

---

## 6. How Good Is the Model?

| Metric | Meaning | Good value |
|--------|---------|------------|
| **R² score** | How much of the variation in marks the curve explains | Close to **1.0** |
| **MAE** (Mean Absolute Error) | Average size of the mistake, in marks | As **small** as possible |
| **MSE** | Average squared error | As **small** as possible |
| **RMSE** | √MSE, back in the original units (marks) | As **small** as possible |

Always measure on a **train/test split**. A high-degree polynomial can score almost perfectly on training data and still be useless.

---

## 7. Limitations ⚠️

- **Extrapolation is very dangerous.** Outside the training range, the highest power takes over and the curve shoots up or dives. Our model was trained on 0.6–10 hours:

  | Hours | Prediction |
  |-------|------------|
  | 10 | 87.4 marks ✅ |
  | 14 | 25.4 marks ❌ |
  | 15 | −8.8 marks ❌ (impossible) |

  That's why `predict.py` warns you and caps marks at 0–100.
- **Overfitting** if the degree is too high
- **Sensitive to outliers**, even more than a straight line, because the curve can bend towards them
- **Correlation ≠ causation**: the curve describes a pattern; it doesn't prove that studying causes the marks

---

## 8. Polynomial Regression in Python

### With scikit-learn (the usual way)

```python
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load data
df = pd.read_csv("train.csv")
X = df[["study_hours"]]
y = df["final_marks"]

# 2. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Build the model: make [x, x², x³], then fit linear regression on them
model = make_pipeline(
    PolynomialFeatures(degree=3, include_bias=False),
    LinearRegression(),
)
model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
print("R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))

# 5. Look at the learned curve
lr = model.named_steps["linearregression"]
print("b0:", lr.intercept_)
print("b1, b2, b3:", lr.coef_)

# 6. Predict for a new student
print("Predicted marks:", model.predict(pd.DataFrame({"study_hours": [6]}))[0])
```

**See what PolynomialFeatures produces:**

```python
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

pf = PolynomialFeatures(degree=3, include_bias=False)
print(pf.fit_transform(np.array([[2], [5]])))
# [[  2.   4.   8.]
#  [  5.  25. 125.]]
```

### From scratch (to understand it)

See **`polynomial_regression_from_scratch.py`**, which builds the design matrix and solves the Normal Equation with numpy.

---

## 9. Summary

```
 x  →  [x, x², x³]  →  Linear Regression (least squares)  →  b0 + b1x + b2x² + b3x³  →  Predict
```

- Polynomial regression fits a **curve** by adding **powers of x** as extra features
- Under the hood it's **still linear regression**, just with more columns
- The **degree** controls how bendy the curve is: too low underfits, too high overfits
- Choose the degree using **test data**, not training data
- **Never trust it outside the training range**

---

## 10. Practice Exercises ✏️

1. Using the demo's curve, calculate marks for 3 hours by hand. Check with `predict.py`.
2. In `train.py`, change `DEGREE` to 1, 2, 3, 5 and 10. Record the test R² for each. Which is best?
3. Try degree 10 and predict for 0.5 hours and 10 hours. Do the answers look sensible?
4. Plot the data and the curve with matplotlib (`plt.scatter` for points, `plt.plot` for the curve over 0–10 hours).
5. Predict for 12, 15 and 20 hours. Explain why the answers go wrong.
6. Add 3 fake students with `study_hours = 9` and `final_marks = 30`, then retrain. How much does the curve change compared with the straight-line version?
