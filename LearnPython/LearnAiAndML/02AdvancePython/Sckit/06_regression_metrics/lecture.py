"""Lecture 06: MAE, MSE, RMSE, R2, MAPE, residuals, baselines."""
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_absolute_error, mean_absolute_percentage_error, mean_squared_error,
                             median_absolute_error, r2_score, root_mean_squared_error)
from sklearn.model_selection import train_test_split

print("=== 1. Metrics on a tiny example (prices in lakh) ===")
y = np.array([50, 60, 70, 80, 90])
p = np.array([52, 58, 73, 79, 88])
print(f"  MAE  {mean_absolute_error(y, p):.2f}   MSE {mean_squared_error(y, p):.2f}   RMSE {root_mean_squared_error(y, p):.2f}")
print(f"  R2   {r2_score(y, p):.3f}   MAPE {mean_absolute_percentage_error(y, p):.3%}   MedAE {median_absolute_error(y, p):.2f}")
r2_hand = 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
print(f"  R2 by hand: {r2_hand:.3f}")

print("\n=== 2. One big error: RMSE reacts far more than MAE ===")
p_bad = p.copy()
p_bad[-1] = 130                                     # one prediction off by 40
for label, pred in [("small errors", p), ("one big error", p_bad)]:
    print(f"  {label:<14} MAE {mean_absolute_error(y, pred):6.2f}  RMSE {root_mean_squared_error(y, pred):6.2f}  "
          f"MedAE {median_absolute_error(y, pred):5.2f}")

print("\n=== 3. R2 can be negative ===")
for label, pred in [("perfect", y), ("predict the mean", np.full(5, y.mean())), ("constant 200", np.full(5, 200))]:
    print(f"  {label:<16} R2 = {r2_score(y, pred):8.3f}")

print("\n=== 4. Real model vs baseline (diabetes) ===")
X, yd = load_diabetes(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, yd, test_size=0.2, random_state=0)
for model in [DummyRegressor(strategy="mean"), LinearRegression()]:
    pred = model.fit(Xtr, ytr).predict(Xte)
    print(f"  {type(model).__name__:<16} MAE {mean_absolute_error(yte, pred):6.1f}  RMSE {root_mean_squared_error(yte, pred):6.1f}"
          f"  R2 {r2_score(yte, pred):6.3f}  (score() = {model.score(Xte, yte):.3f})")
print(f"  target range {yd.min():.0f}-{yd.max():.0f}, std {yd.std():.1f}")

print("\n=== 5. Residuals ===")
lin = LinearRegression().fit(Xtr, ytr)
pred = lin.predict(Xte)
res = yte - pred
print(f"  mean residual {res.mean():.1f} (close to 0 = no overall bias)")
bins = np.quantile(pred, [0, 1 / 3, 2 / 3, 1])
for lo, hi in zip(bins[:-1], bins[1:]):
    mask = (pred >= lo) & (pred <= hi)
    print(f"  predictions {lo:5.0f}-{hi:5.0f}: mean |residual| {np.abs(res[mask]).mean():5.1f} over {mask.sum()} rows")
worst = np.argsort(-np.abs(res))[:3]
print("  three worst predictions (actual vs predicted):", [(int(yte[i]), int(pred[i])) for i in worst])
