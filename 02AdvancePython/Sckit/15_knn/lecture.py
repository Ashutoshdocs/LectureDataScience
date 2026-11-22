"""Lecture 15: KNN: voting by hand, choosing k, weights, metrics, scaling, curse of dimensionality, regression, kneighbors."""
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

print("=== 1. KNN by hand ===")
X = np.array([[1, 1], [1, 2], [2, 1], [6, 6], [7, 6], [6, 7], [3, 3]])
y = np.array(["red", "red", "red", "blue", "blue", "blue", "blue"])
new = np.array([2.5, 2.5])
dist = np.linalg.norm(X - new, axis=1)
order = np.argsort(dist)
for i in order[:5]:
    print(f"  {X[i]} {y[i]:<5} distance {dist[i]:.2f}")
for k in (1, 3, 5):
    labels, counts = np.unique(y[order[:k]], return_counts=True)
    vote = labels[np.argmax(counts)]
    sk = KNeighborsClassifier(n_neighbors=k).fit(X, y).predict([new])[0]
    print(f"  k={k}: votes {dict(zip(labels.tolist(), counts.tolist()))} -> {vote} (sklearn: {sk})")

print("\n=== 2. Choosing k with cross-validation (scaled wine) ===")
Xw, yw = load_wine(return_X_y=True)
results = {}
for k in [1, 3, 5, 9, 15, 25, 51, 101]:
    pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    results[k] = cross_val_score(pipe, Xw, yw, cv=5).mean()
    print(f"  k={k:<4} {results[k]:.3f} {'#' * int((results[k] - 0.85) * 300)}")
print("  best k:", max(results, key=results.get))

print("\n=== 3. weights and distance metric ===")
for weights in ["uniform", "distance"]:
    for p in [1, 2]:
        pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=51, weights=weights, p=p))
        print(f"  k=51 weights={weights:<8} p={p} ({'Manhattan' if p == 1 else 'Euclidean'}) -> {cross_val_score(pipe, Xw, yw, cv=5).mean():.3f}")

print("\n=== 4. Scaling ===")
print(f"  unscaled {cross_val_score(KNeighborsClassifier(), Xw, yw, cv=5).mean():.3f} | "
      f"scaled {cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier()), Xw, yw, cv=5).mean():.3f}")

print("\n=== 5. Curse of dimensionality: add noise features ===")
rng = np.random.default_rng(0)
for n_noise in [0, 10, 50, 200]:
    Xn = np.hstack([Xw, rng.normal(size=(len(Xw), n_noise))])
    s = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier()), Xn, yw, cv=5).mean()
    print(f"  13 real + {n_noise:>3} noise features -> {s:.3f}")

print("\n=== 6. Explaining a prediction with kneighbors ===")
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)).fit(Xw, yw)
query = Xw[[100]]
dists, idx = pipe[-1].kneighbors(pipe[0].transform(query))
print("  prediction:", pipe.predict(query)[0], "| neighbour rows:", idx[0].tolist(), "| their labels:", yw[idx[0]].tolist())
print("  distances:", dists[0].round(2).tolist(), "(the first is the row itself)")

print("\n=== 7. KNN regression: average of neighbours ===")
xr = np.sort(rng.uniform(0, 6, 60)).reshape(-1, 1)
yr = np.sin(xr).ravel() + rng.normal(0, 0.2, 60)
x_test = np.linspace(0, 6, 200).reshape(-1, 1)
for k in [1, 5, 25, 60]:
    reg = KNeighborsRegressor(n_neighbors=k).fit(xr, yr)
    print(f"  k={k:<3} train R2 {reg.score(xr, yr):.3f}  test R2 vs true sin {reg.score(x_test, np.sin(x_test).ravel()):.3f}")
