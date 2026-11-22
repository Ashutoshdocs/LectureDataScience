"""Lecture 12: Linear regression: coefficients, least squares, multiple features, interpretation, polynomial overfitting, outliers."""
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

np.set_printoptions(suppress=True)

print("=== 1. One feature: a straight line ===")
hours = np.array([[1], [2], [3], [4], [5]])
marks = np.array([52, 57, 66, 70, 75])
model = LinearRegression().fit(hours, marks)
print(f"  marks = {model.coef_[0]:.2f} x hours + {model.intercept_:.2f}")
print(f"  6 hours -> {model.predict([[6]])[0]:.1f} | by hand {model.coef_[0] * 6 + model.intercept_:.1f}")
print(f"  R2 on training data {model.score(hours, marks):.3f}")
print(f"  15 hours -> {model.predict([[15]])[0]:.0f} marks (extrapolation nonsense: max is 100!)")

print("\n=== 2. Least squares: the fitted line has the smallest squared error ===")
for slope, intercept in [(model.coef_[0], model.intercept_), (6.5, 45), (5.0, 50)]:
    sse = ((marks - (slope * hours.ravel() + intercept)) ** 2).sum()
    print(f"  slope {slope:5.2f}, intercept {intercept:5.2f} -> sum of squared errors {sse:7.2f}")

print("\n=== 3. Several features ===")
X2 = np.array([[1, 8], [2, 6], [3, 7], [4, 5], [5, 8], [6, 6]])       # [hours studied, hours slept]
y2 = np.array([50, 52, 62, 60, 78, 74])
m2 = LinearRegression().fit(X2, y2)
print(f"  coef_ {m2.coef_.round(2)} intercept_ {m2.intercept_:.2f}")
print(f"  -> +1 hour studied adds {m2.coef_[0]:.1f} marks, +1 hour slept adds {m2.coef_[1]:.1f} (holding the other fixed)")

print("\n=== 4. Real data: diabetes, standardised coefficients ===")
data = load_diabetes()
Xtr, Xte, ytr, yte = train_test_split(data.data, data.target, test_size=0.2, random_state=0)
pipe = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
coefs = pipe[-1].coef_
order = np.argsort(-np.abs(coefs))
print(f"  test R2 {pipe.score(Xte, yte):.3f}")
for i in order[:5]:
    print(f"  {data.feature_names[i]:<4} {coefs[i]:+7.1f} per 1 std")

print("\n=== 5. Correlated duplicate features make coefficients unstable ===")
rng = np.random.default_rng(0)
area = rng.uniform(40, 150, 100)
price = 0.5 * area + rng.normal(0, 5, 100)
X_dup = np.column_stack([area, area * 10.764 + rng.normal(0, 0.01, 100)])   # m2 and (almost) the same in ft2
for seed in range(3):
    idx = np.random.default_rng(seed).choice(100, 80, replace=False)
    c = LinearRegression().fit(X_dup[idx], price[idx]).coef_
    print(f"  sample {seed}: coef_ m2 {c[0]:+8.2f}, ft2 {c[1]:+8.3f}  (predictions fine, coefficients meaningless)")

print("\n=== 6. Polynomial degree: underfit -> good -> overfit ===")
x = np.sort(rng.uniform(0, 1, 30)).reshape(-1, 1)
y = np.sin(2 * np.pi * x).ravel() + rng.normal(0, 0.2, 30)
x_test = np.linspace(0, 1, 100).reshape(-1, 1)
y_test = np.sin(2 * np.pi * x_test).ravel()
for degree in [1, 3, 5, 9, 15]:
    poly = make_pipeline(PolynomialFeatures(degree), LinearRegression()).fit(x, y)
    print(f"  degree {degree:>2}: train R2 {poly.score(x, y):.3f}  test R2 {poly.score(x_test, y_test):8.3f}")

print("\n=== 7. Outliers drag the line: HuberRegressor resists ===")
Xo = np.arange(10).reshape(-1, 1).astype(float)
yo = 2 * Xo.ravel() + 1
yo[9] = 60                                          # one bad measurement (should be 19)
for reg in [LinearRegression(), HuberRegressor()]:
    reg.fit(Xo, yo)
    print(f"  {type(reg).__name__:<17} slope {reg.coef_[0]:.2f} (true 2.00) intercept {reg.intercept_:.2f} (true 1.00)")
