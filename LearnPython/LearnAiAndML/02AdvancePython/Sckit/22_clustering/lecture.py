"""Lecture 22: KMeans step by step, choosing k (elbow, silhouette), scaling, DBSCAN, agglomerative, customer segmentation, evaluation."""
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import load_iris, make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

np.set_printoptions(suppress=True)

print("=== 1. KMeans on obvious groups ===")
X = np.array([[2, 2], [3, 2.5], [2, 2.2], [10, 9], [11, 9.5], [12, 10], [6, 5], [7, 5.5]])
km = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = km.fit_predict(X)
print("  labels :", labels.tolist())
print("  centres:", km.cluster_centers_.round(1).tolist())
print("  inertia:", round(km.inertia_, 2), "| new point [9, 8] -> cluster", km.predict([[9, 8]])[0])

print("\n=== 2. n_init: restarts avoid bad starting positions ===")
Xb, true_b = make_blobs(n_samples=400, centers=6, cluster_std=0.7, random_state=7)
for seed in range(4):
    k = KMeans(n_clusters=6, init="random", n_init=1, random_state=seed).fit(Xb)
    print(f"  one random start (seed {seed}): inertia {k.inertia_:7.1f}  ARI vs truth {adjusted_rand_score(true_b, k.labels_):.3f}  iterations {k.n_iter_}")
best = KMeans(n_clusters=6, init="random", n_init=10, random_state=0).fit(Xb)
print(f"  n_init=10 keeps the best      : inertia {best.inertia_:7.1f}  ARI vs truth {adjusted_rand_score(true_b, best.labels_):.3f}")

print("\n=== 3. Choosing k: elbow and silhouette (scaled iris) ===")
Xi, yi = load_iris(return_X_y=True)
Xi = StandardScaler().fit_transform(Xi)
print(f"  {'k':>2} {'inertia':>8} {'silhouette':>10}")
for k in range(2, 8):
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xi)
    print(f"  {k:>2} {m.inertia_:8.1f} {silhouette_score(Xi, m.labels_):10.3f}  {'#' * int(m.inertia_ / 8)}")
print("  silhouette is highest at k=2 (setosa vs the rest); the true answer is 3 species, so use domain sense too")

print("\n=== 4. Scaling matters ===")
rng = np.random.default_rng(0)
people = np.column_stack([np.r_[rng.normal(25, 3, 50), rng.normal(55, 3, 50)],        # age: the real groups
                          rng.normal(50_000, 15_000, 100)])                            # income: noise, big units
truth = np.r_[np.zeros(50), np.ones(50)]
for name, data in [("unscaled", people), ("scaled", StandardScaler().fit_transform(people))]:
    lab = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(data)
    print(f"  {name:<8} ARI with the true age groups: {adjusted_rand_score(truth, lab):.3f}")

print("\n=== 5. Non-round shapes: KMeans vs DBSCAN vs Agglomerative ===")
Xm, ym = make_moons(n_samples=300, noise=0.06, random_state=0)
Xm = StandardScaler().fit_transform(Xm)
models = {"KMeans(k=2)": KMeans(n_clusters=2, n_init=10, random_state=0),
          "DBSCAN(eps=0.3)": DBSCAN(eps=0.3, min_samples=5),
          "Agglomerative ward": AgglomerativeClustering(n_clusters=2, linkage="ward"),
          "Agglomerative single": AgglomerativeClustering(n_clusters=2, linkage="single")}
for name, m in models.items():
    lab = m.fit_predict(Xm)
    print(f"  {name:<21} ARI {adjusted_rand_score(ym, lab):.3f}  clusters {len(set(lab) - {-1})}  noise points {np.sum(lab == -1)}")

print("\n=== 6. DBSCAN eps and outliers ===")
Xo = np.vstack([make_blobs(n_samples=200, centers=[[0, 0], [5, 5]], cluster_std=0.6, random_state=1)[0], [[10, -5], [-6, 8]]])
for eps in [0.2, 0.6, 3.0]:
    lab = DBSCAN(eps=eps, min_samples=5).fit_predict(Xo)
    print(f"  eps={eps:<4} clusters {len(set(lab) - {-1})}  noise {np.sum(lab == -1):>3}  last two points (outliers) -> {lab[-2:].tolist()}")

print("\n=== 7. Customer segmentation ===")
seg = pd.DataFrame({
    "visits_per_month": np.r_[rng.normal(2, 0.7, 60), rng.normal(8, 1.5, 60), rng.normal(15, 2, 30)],
    "avg_spend": np.r_[rng.normal(300, 80, 60), rng.normal(900, 150, 60), rng.normal(2500, 300, 30)],
    "days_since_last": np.r_[rng.normal(40, 10, 60), rng.normal(10, 4, 60), rng.normal(3, 1.5, 30)],
}).clip(lower=0)
scaled = StandardScaler().fit_transform(seg)
seg["segment"] = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(scaled)
profile = seg.groupby("segment").mean().round(1)
profile["customers"] = seg["segment"].value_counts().sort_index()
print(profile.to_string())
print(f"  silhouette {silhouette_score(scaled, seg['segment']):.3f} | Davies-Bouldin {davies_bouldin_score(scaled, seg['segment']):.3f} (lower is better)")
names = {profile["avg_spend"].idxmin(): "occasional", profile["avg_spend"].idxmax(): "VIP"}
print("  segment names from the profile:", {int(k): names.get(k, "regular") for k in profile.index})
