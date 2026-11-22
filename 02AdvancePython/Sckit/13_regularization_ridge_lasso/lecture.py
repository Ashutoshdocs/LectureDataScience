"""Lecture 13: Ridge, Lasso, ElasticNet: alpha paths, sparsity, CV-chosen alpha, taming polynomial overfitting, scaling."""
import warnings

import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import ElasticNet, Lasso, LassoCV, LinearRegression, Ridge, RidgeCV
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

warnings.filterwarnings("ignore", category=ConvergenceWarning)
np.set_printoptions(suppress=True)
data = load_diabetes()
X, y, names = data.data, data.target, data.feature_names
Xs = StandardScaler().fit_transform(X)

print("=== 1. Ridge: coefficients shrink smoothly as alpha grows ===")
print("  alpha    " + " ".join(f"{n:>6}" for n in names))
for alpha in [0.01, 1, 10, 100, 1000, 10000]:
    c = Ridge(alpha=alpha).fit(Xs, y).coef_
    print(f"  {alpha:<8} " + " ".join(f"{v:6.1f}" for v in c))

print("\n=== 2. Lasso: coefficients hit exactly zero ===")
for alpha in [0.01, 1, 5, 10, 30]:
    c = Lasso(alpha=alpha).fit(Xs, y).coef_
    kept = [n for n, v in zip(names, c) if v != 0]
    print(f"  alpha {alpha:<5} zeros {np.sum(c == 0):>2}/10  kept {kept}")

print("\n=== 3. Cross-validated comparison ===")
models = {"LinearRegression": LinearRegression(), "Ridge(alpha=1)": Ridge(alpha=1), "Lasso(alpha=1)": Lasso(alpha=1),
          "ElasticNet(0.1, l1=0.5)": ElasticNet(alpha=0.1, l1_ratio=0.5), "Ridge(alpha=1000)": Ridge(alpha=1000)}
for name, model in models.items():
    s = cross_val_score(make_pipeline(StandardScaler(), model), X, y, cv=5).mean()
    print(f"  {name:<24} R2 {s:.3f}")
print("  too-strong regularisation (alpha=1000) underfits")

print("\n=== 4. Let cross-validation choose alpha ===")
ridge_cv = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13))).fit(X, y)
lasso_cv = make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0)).fit(X, y)
print(f"  RidgeCV chose alpha={ridge_cv[-1].alpha_:.3g}")
kept = [n for n, v in zip(names, lasso_cv[-1].coef_) if v != 0]
print(f"  LassoCV chose alpha={lasso_cv[-1].alpha_:.3g}, kept {len(kept)} features: {kept}")

print("\n=== 5. Regularisation tames a wild polynomial ===")
rng = np.random.default_rng(0)
x = np.sort(rng.uniform(0, 1, 25)).reshape(-1, 1)
yy = np.sin(2 * np.pi * x).ravel() + rng.normal(0, 0.2, 25)
x_test = np.linspace(0, 1, 100).reshape(-1, 1)
y_test = np.sin(2 * np.pi * x_test).ravel()
for name, reg in [("LinearRegression", LinearRegression()), ("Ridge(alpha=0.001)", Ridge(alpha=0.001)),
                  ("Ridge(alpha=0.1)", Ridge(alpha=0.1))]:
    pipe = make_pipeline(PolynomialFeatures(12), StandardScaler(), reg).fit(x, yy)
    biggest = np.abs(pipe[-1].coef_).max()
    print(f"  degree 12 + {name:<19} test R2 {pipe.score(x_test, y_test):8.3f}  largest |coef| {biggest:12.1f}")

print("\n=== 6. Why scaling matters for penalties ===")
X_units = X.copy()
X_units[:, 2] *= 1000                                   # bmi in different units
unscaled = Lasso(alpha=1).fit(X_units, y).coef_
scaled = make_pipeline(StandardScaler(), Lasso(alpha=1)).fit(X_units, y)[-1].coef_
print("  features kept without scaling:", [n for n, v in zip(names, unscaled) if v != 0])
print("  features kept with scaling   :", [n for n, v in zip(names, scaled) if v != 0])
