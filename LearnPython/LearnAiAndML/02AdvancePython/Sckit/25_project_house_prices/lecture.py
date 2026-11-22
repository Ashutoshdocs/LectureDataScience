"""Lecture 25: Project: house-price regression, end to end on messy mixed data."""
import pathlib
import tempfile

import joblib
import numpy as np
import pandas as pd
from scipy.stats import loguniform, randint
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

pd.set_option("display.width", 140)


# ---------------------------------------------------------------- 1. data
def make_houses(n=2000, seed=0):
    """Synthetic but realistic city housing data (prices in lakh rupees)."""
    rng = np.random.default_rng(seed)
    city = rng.choice(["Mumbai", "Pune", "Bengaluru", "Jaipur"], n, p=[0.25, 0.3, 0.3, 0.15])
    city_rate = pd.Series(city).map({"Mumbai": 2.2, "Bengaluru": 1.4, "Pune": 1.1, "Jaipur": 0.7}).to_numpy()
    area = rng.gamma(6, 18, n).clip(25, 400).round()
    bedrooms = np.clip(np.round(area / 45 + rng.normal(0, 0.6, n)), 1, 6).astype(int)
    age = rng.integers(0, 40, n).astype(float)
    floor = rng.integers(0, 30, n)
    furnishing = rng.choice(["unfurnished", "semi", "full"], n, p=[0.4, 0.4, 0.2])
    metro_km = rng.exponential(3, n).round(1)
    parking = rng.choice(["yes", "no"], n, p=[0.6, 0.4])
    furn_bonus = pd.Series(furnishing).map({"unfurnished": 0, "semi": 0.05, "full": 0.12}).to_numpy()
    price = (area * 0.55 * city_rate * (1 + furn_bonus) * (1 - 0.006 * age) * (1 + 0.004 * floor)
             * np.exp(-0.04 * metro_km) * np.where(parking == "yes", 1.06, 1.0) * rng.lognormal(0, 0.12, n))
    df = pd.DataFrame({"city": city, "area_sqm": area, "bedrooms": bedrooms, "age_years": age, "floor": floor,
                       "furnishing": furnishing, "metro_km": metro_km, "parking": parking, "price_lakh": price.round(1)})
    df.loc[rng.random(n) < 0.08, "age_years"] = np.nan
    df.loc[rng.random(n) < 0.05, "metro_km"] = np.nan
    df.loc[rng.random(n) < 0.04, "furnishing"] = np.nan
    return df


df = make_houses()
print("=== 1. Explore ===")
print(df.head().to_string(index=False))
print("  shape", df.shape, "| missing:", df.isna().sum()[df.isna().sum() > 0].to_dict())
print(df["price_lakh"].describe().round(1).to_frame().T.to_string())
print(f"  skew: mean {df['price_lakh'].mean():.1f} > median {df['price_lakh'].median():.1f} -> right-skewed target (log may help)")
print("  median price by city:", df.groupby("city")["price_lakh"].median().round(1).sort_values().to_dict())

# ---------------------------------------------------------------- 2. split
X = df.drop(columns="price_lakh")
y = df["price_lakh"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\n=== 2. Split: {len(X_train)} train / {len(X_test)} test (test set locked away) ===")


# ---------------------------------------------------------------- 3. preprocessing
def add_features(frame):
    frame = frame.copy()
    frame["sqm_per_bedroom"] = frame["area_sqm"] / frame["bedrooms"]
    frame["is_new"] = (frame["age_years"] < 5).astype(float)
    return frame


numeric = ["area_sqm", "bedrooms", "age_years", "floor", "metro_km", "sqm_per_bedroom", "is_new"]
categorical = ["city", "furnishing", "parking"]
preprocess = Pipeline([
    ("features", FunctionTransformer(add_features)),
    ("columns", ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
    ])),
])

# ---------------------------------------------------------------- 4. compare models with CV
print("\n=== 3. Compare models (5-fold CV on train) ===")
cv = KFold(5, shuffle=True, random_state=0)
candidates = {
    "Dummy (mean)": DummyRegressor(),
    "Ridge": Ridge(alpha=1.0),
    "Ridge + log target": TransformedTargetRegressor(Ridge(alpha=1.0), func=np.log1p, inverse_func=np.expm1),
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1),
    "HistGradientBoosting": HistGradientBoostingRegressor(random_state=0),
    "HGB + log target": TransformedTargetRegressor(HistGradientBoostingRegressor(random_state=0), func=np.log1p, inverse_func=np.expm1),
}
results = {}
for name, reg in candidates.items():
    pipe = Pipeline([("prep", preprocess), ("model", reg)])
    r = cross_validate(pipe, X_train, y_train, cv=cv, scoring=["neg_mean_absolute_error", "r2"])
    results[name] = (-r["test_neg_mean_absolute_error"].mean(), r["test_r2"].mean())
    print(f"  {name:<22} MAE {results[name][0]:7.2f} lakh   R2 {results[name][1]:.3f}")

# ---------------------------------------------------------------- 5. tune the best family
print("\n=== 4. Tune HistGradientBoosting (log target) with RandomizedSearchCV ===")
tune_pipe = Pipeline([("prep", preprocess),
                      ("model", TransformedTargetRegressor(HistGradientBoostingRegressor(random_state=0),
                                                           func=np.log1p, inverse_func=np.expm1))])
space = {"model__regressor__learning_rate": loguniform(0.02, 0.3),
         "model__regressor__max_leaf_nodes": randint(8, 64),
         "model__regressor__min_samples_leaf": randint(5, 60),
         "model__regressor__l2_regularization": loguniform(1e-3, 10)}
search = RandomizedSearchCV(tune_pipe, space, n_iter=20, cv=cv, scoring="neg_mean_absolute_error",
                            random_state=0, n_jobs=-1).fit(X_train, y_train)
print("  best params:", {k.split("__")[-1]: (round(float(v), 4) if isinstance(v, float) else int(v)) for k, v in search.best_params_.items()})
print(f"  tuned CV MAE {-search.best_score_:.2f} lakh (untuned {results['HGB + log target'][0]:.2f})")

# ---------------------------------------------------------------- 6. final test evaluation
print("\n=== 5. Final evaluation on the test set (used once) ===")
final = search.best_estimator_
pred = final.predict(X_test)
print(f"  MAE {mean_absolute_error(y_test, pred):.2f} lakh | MAPE {mean_absolute_percentage_error(y_test, pred):.1%} | R2 {r2_score(y_test, pred):.3f}")
dummy_mae = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print(f"  baseline (always the mean) MAE {dummy_mae:.2f} lakh -> model is {dummy_mae / mean_absolute_error(y_test, pred):.1f}x better")

# ---------------------------------------------------------------- 7. error analysis
print("\n=== 6. Error analysis: where is the model weak? ===")
errors = X_test.assign(actual=y_test, predicted=pred.round(1), abs_err=np.abs(y_test - pred),
                       pct_err=np.abs(y_test - pred) / y_test)
print(errors.groupby("city")[["abs_err", "pct_err"]].mean().round(3).rename(columns={"abs_err": "MAE", "pct_err": "MAPE"}).to_string())
errors["size"] = pd.cut(errors["area_sqm"], [0, 60, 120, 200, 400], labels=["<60", "60-120", "120-200", "200+"])
print(errors.groupby("size", observed=True)["pct_err"].agg(["mean", "count"]).round(3).rename(columns={"mean": "MAPE"}).to_string())
print("  biggest misses:")
print(errors.nlargest(3, "abs_err")[["city", "area_sqm", "bedrooms", "age_years", "actual", "predicted"]].to_string(index=False))

# ---------------------------------------------------------------- 8. what drives price?
print("\n=== 7. Permutation importance on the test set ===")
imp = permutation_importance(final, X_test, y_test, scoring="neg_mean_absolute_error", n_repeats=5, random_state=0)
for col, val in sorted(zip(X_test.columns, imp.importances_mean), key=lambda t: -t[1]):
    print(f"  {col:<11} MAE rises by {val:6.2f} lakh when shuffled")

# ---------------------------------------------------------------- 9. save and use
print("\n=== 8. Save the pipeline and price new listings ===")
path = pathlib.Path(tempfile.mkdtemp()) / "house_price_model.joblib"
joblib.dump(final, path)
model = joblib.load(path)
new = pd.DataFrame({"city": ["Pune", "Mumbai", "Jaipur"], "area_sqm": [85, 60, 150], "bedrooms": [2, 1, 4],
                    "age_years": [3, np.nan, 20], "floor": [5, 12, 1], "furnishing": ["semi", "full", None],
                    "metro_km": [1.5, 0.4, np.nan], "parking": ["yes", "no", "yes"]})
new["predicted_lakh"] = model.predict(new).round(1)
print(new.to_string(index=False))
