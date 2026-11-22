"""Lecture 08: Why scale; Standard/MinMax/Robust/MaxAbs/Normalizer; fit on train only; which models care."""
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, Normalizer, RobustScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

np.set_printoptions(suppress=True)

print("=== 1. Why scale: distances are dominated by big units ===")
a = np.array([25, 50_000])
b = np.array([60, 51_000])          # 35 years older, similar salary
c = np.array([26, 60_000])          # same age, salary +10,000
print(f"  distance(a, b) = {np.linalg.norm(a - b):8.1f}  (35-year age gap barely counts)")
print(f"  distance(a, c) = {np.linalg.norm(a - c):8.1f}")

X, y = load_wine(return_X_y=True)
print("  wine feature ranges:", f"{X.min():.2f} to {X.max():.0f}")
for name, model in [("KNN", KNeighborsClassifier()), ("SVC", SVC()), ("Tree", DecisionTreeClassifier(random_state=0))]:
    raw = cross_val_score(model, X, y, cv=5).mean()
    scaled = cross_val_score(make_pipeline(StandardScaler(), model), X, y, cv=5).mean()
    print(f"  {name:<5} unscaled {raw:.3f} -> scaled {scaled:.3f}")
print("  (trees don't care about scale)")

print("\n=== 2. The scalers side by side (one outlier at 1000) ===")
col = np.array([[10.0], [20.0], [30.0], [40.0], [1000.0]])
for scaler in [StandardScaler(), MinMaxScaler(), RobustScaler(), MaxAbsScaler()]:
    out = scaler.fit_transform(col).ravel()
    print(f"  {type(scaler).__name__:<15} {np.round(out, 2)}")
print("  MinMax squashes the normal values into 0-0.03 because of the outlier; Robust keeps them spread")

print("\n=== 3. Learned attributes and inverse_transform ===")
people = np.array([[25, 30_000], [35, 60_000], [45, 90_000]], dtype=float)
ss = StandardScaler().fit(people)
print("  mean_ :", ss.mean_, "| scale_:", ss.scale_.round(1))
scaled = ss.transform(people)
print("  scaled:\n", scaled.round(2))
print("  inverse_transform gives back:", ss.inverse_transform(scaled)[0])
mm = MinMaxScaler().fit(people)
print("  MinMax data_min_:", mm.data_min_, "data_max_:", mm.data_max_)

print("\n=== 4. Fit on train, transform test ===")
train = np.array([[10.0], [20.0], [30.0]])
test = np.array([[40.0]])
scaler = StandardScaler().fit(train)
print("  train mean:", scaler.mean_[0], "| test 40 ->", scaler.transform(test).ravel().round(2), "(outside the train range is fine)")
leaky = StandardScaler().fit(np.vstack([train, test]))
print("  leaky mean (fit on all):", leaky.mean_[0], "| test 40 ->", leaky.transform(test).ravel().round(2))
wrong = StandardScaler().fit_transform(test)
print("  fit_transform on the test set alone ->", wrong.ravel(), "(meaningless: every single row becomes 0)")

print("\n=== 5. Leakage inflates scores (feature selection example) ===")
rng = np.random.default_rng(0)
Xn = rng.normal(size=(100, 2000))                       # pure noise
yn = rng.integers(0, 2, 100)                            # random labels: true accuracy is 0.5
from sklearn.feature_selection import SelectKBest       # noqa: E402
from sklearn.linear_model import LogisticRegression     # noqa: E402
X_leaky = SelectKBest(k=20).fit_transform(Xn, yn)        # selecting features using ALL labels (leak)
leaky_score = cross_val_score(LogisticRegression(), X_leaky, yn, cv=5).mean()
honest = cross_val_score(make_pipeline(SelectKBest(k=20), LogisticRegression()), Xn, yn, cv=5).mean()
print(f"  preprocessing outside CV: {leaky_score:.3f}  <- looks like the model learned something from noise!")
print(f"  inside a pipeline       : {honest:.3f}  <- honest (about 0.5)")

print("\n=== 6. Normalizer works on ROWS ===")
rows = np.array([[3.0, 4.0], [1.0, 1.0]])
print("  Normalizer:", Normalizer().fit_transform(rows).round(3).tolist(), "(each row now has length 1)")
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier()).fit(Xtr, ytr)
print(f"  wine KNN with a pipeline (scaler fit on train only): test accuracy {pipe.score(Xte, yte):.3f}")
