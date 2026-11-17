"""
linear_regression_from_scratch.py - Linear Regression with NO machine-learning library.

This is a teaching file. It shows what happens "inside" sklearn's LinearRegression,
using gradient descent on ONE feature (study_hours -> final_marks) so you can
follow the maths step by step.

Usage:
    python linear_regression_from_scratch.py
"""
import pandas as pd

# ---- 1. Load data (one feature, to keep it simple) ----
df = pd.read_csv("train.csv")
x = df["study_hours"].tolist()
y = df["final_marks"].tolist()
n = len(x)

# ---- 2. Start with a random guess for the line y = m*x + c ----
m = 0.0  # slope
c = 0.0  # intercept
learning_rate = 0.01
epochs = 5000

# ---- 3. Gradient descent: nudge m and c to reduce the error ----
for epoch in range(epochs):
    predictions = [m * xi + c for xi in x]
    errors = [pi - yi for pi, yi in zip(predictions, y)]

    # Mean Squared Error = average of (error^2)
    mse = sum(e ** 2 for e in errors) / n

    # Gradients (partial derivatives of MSE w.r.t. m and c)
    dm = (2 / n) * sum(e * xi for e, xi in zip(errors, x))
    dc = (2 / n) * sum(errors)

    # Move a small step in the opposite direction of the gradient
    m -= learning_rate * dm
    c -= learning_rate * dc

    if epoch % 1000 == 0 or epoch == epochs - 1:
        print(f"Epoch {epoch:4d} | MSE = {mse:8.2f} | m = {m:.3f} | c = {c:.3f}")

print(f"\nLearned line:  final_marks = {m:.2f} × study_hours + {c:.2f}")

# ---- 4. Compare with the exact closed-form answer (least squares) ----
x_mean = sum(x) / n
y_mean = sum(y) / n
m_exact = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y)) / sum(
    (xi - x_mean) ** 2 for xi in x
)
c_exact = y_mean - m_exact * x_mean
print(f"Exact formula: final_marks = {m_exact:.2f} × study_hours + {c_exact:.2f}")

# ---- 5. Use it ----
hours = 6
print(f"\nA student who studies {hours} hours/day is predicted to score "
      f"{m * hours + c:.1f} marks.")
