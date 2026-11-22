"""
polynomial_regression_from_scratch.py - Polynomial Regression (degree 3) by hand.

This is a teaching file. It shows what happens "inside" sklearn's
PolynomialFeatures + LinearRegression, using only numpy for the matrix maths.

The trick: a polynomial is just linear regression on extra columns.
    x  ->  [1, x, x², x³]
then solve for the best b0, b1, b2, b3 with the Normal Equation:
    b = (Xᵀ X)⁻¹ Xᵀ y

Usage:
    python polynomial_regression_from_scratch.py
"""
import numpy as np
import pandas as pd

DEGREE = 3

# ---- 1. Load data: x = study hours, y = final marks ----
df = pd.read_csv("train.csv")
x = df["study_hours"].to_numpy()
y = df["final_marks"].to_numpy()
n = len(x)

# ---- 2. Build the "design matrix": one column for each power of x ----
#      column 0: x⁰ = 1  (for the intercept b0)
#      column 1: x¹
#      column 2: x²
#      column 3: x³
X = np.column_stack([x ** p for p in range(DEGREE + 1)])
print("First 3 rows of the design matrix [1, x, x², x³]:")
for xi, row in zip(x[:3], X[:3]):
    print(f"  x = {xi:<4} ->  [{row[0]:.0f}, {row[1]:.1f}, {row[2]:.2f}, {row[3]:.3f}]")

# ---- 3. Normal Equation: solve (XᵀX) b = Xᵀy ----
XtX = X.T @ X
Xty = X.T @ y
b = np.linalg.solve(XtX, Xty)   # same as inv(XtX) @ Xty, but more stable
b0, b1, b2, b3 = b
print(f"\nLearned curve: final_marks = {b0:.3f} {b1:+.3f}·x {b2:+.3f}·x² {b3:+.4f}·x³")

# ---- 4. How good is it? Compare with a straight line (degree 1) ----
def r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return 1 - ss_res / ss_tot

poly_pred = X @ b
X_line = X[:, :2]                                   # only [1, x]
b_line = np.linalg.solve(X_line.T @ X_line, X_line.T @ y)
line_pred = X_line @ b_line

print(f"\nStraight line : R² = {r2(y, line_pred):.3f}, "
      f"MSE = {np.mean((y - line_pred) ** 2):.2f}")
print(f"Degree-3 curve: R² = {r2(y, poly_pred):.3f}, "
      f"MSE = {np.mean((y - poly_pred) ** 2):.2f}")

# ---- 5. Use it ----
print("\nPredictions from the curve:")
for hours in [2, 5, 8, 10]:
    marks = b0 + b1 * hours + b2 * hours ** 2 + b3 * hours ** 3
    print(f"  {hours:>2} hours/day -> {marks:.1f} marks")

# ---- 6. Danger zone: extrapolation ----
hours = 15
marks = b0 + b1 * hours + b2 * hours ** 2 + b3 * hours ** 3
print(f"\n  {hours} hours/day -> {marks:.1f} marks   <- outside training data ({x.min()}-{x.max()} h)!")
print("  The x³ term takes over and the curve dives. Never trust a polynomial")
print("  outside the range it was trained on.")
