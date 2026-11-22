"""Lecture 23: PCA: correlated features, explained variance, choosing components, scaling, loadings,
PCA in a pipeline, reconstruction, 2-D view."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_digits, load_wine
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

np.set_printoptions(suppress=True)

print("=== 1. Two correlated features -> one component ===")
rng = np.random.default_rng(0)
height_cm = rng.normal(170, 10, 200)
height_in = height_cm / 2.54 + rng.normal(0, 0.5, 200)
X2 = StandardScaler().fit_transform(np.column_stack([height_cm, height_in]))
pca2 = PCA().fit(X2)
print("  explained_variance_ratio_:", pca2.explained_variance_ratio_.round(4), "-> PC1 alone keeps almost everything")
print("  PC1 direction (loadings):", pca2.components_[0].round(3), "(equal mix of both features)")

print("\n=== 2. Explained variance on real data ===")
wine = load_wine()
Xw = StandardScaler().fit_transform(wine.data)
pca = PCA().fit(Xw)
cum = np.cumsum(pca.explained_variance_ratio_)
for i, (r, c) in enumerate(zip(pca.explained_variance_ratio_, cum), start=1):
    if i <= 6:
        print(f"  PC{i}: {r:.3f}  cumulative {c:.3f}  {'#' * int(r * 100)}")
for target in [0.8, 0.9, 0.95]:
    print(f"  components needed for {target:.0%}: {PCA(n_components=target).fit(Xw).n_components_} of 13")

print("\n=== 3. Scaling first matters ===")
raw = PCA(n_components=2).fit(wine.data)
print("  unscaled PC1 explains", raw.explained_variance_ratio_[0].round(3), "- dominated by:",
      wine.feature_names[np.argmax(np.abs(raw.components_[0]))], f"(values up to {wine.data[:, 12].max():.0f})")
print("  scaled   PC1 explains", PCA(n_components=2).fit(Xw).explained_variance_ratio_[0].round(3), "- a real mix of features")

print("\n=== 4. Reading the loadings of PC1 ===")
load1 = PCA(n_components=2).fit(Xw).components_[0]
for i in np.argsort(-np.abs(load1))[:5]:
    print(f"  {wine.feature_names[i]:<30} {load1[i]:+.3f}")

print("\n=== 5. 2-D view: classes separate along the components ===")
X_2d = PCA(n_components=2).fit_transform(Xw)
for c in range(3):
    pts = X_2d[wine.target == c]
    print(f"  class {c}: mean PC1 {pts[:, 0].mean():+.2f}  PC2 {pts[:, 1].mean():+.2f}  ({len(pts)} wines)")

print("\n=== 6. PCA inside a pipeline: accuracy vs components ===")
Xc, yc = load_breast_cancer(return_X_y=True)
print(f"  all 30 features: {cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), Xc, yc, cv=5).mean():.3f}")
for n in [1, 2, 5, 10]:
    pipe = make_pipeline(StandardScaler(), PCA(n_components=n), LogisticRegression())
    print(f"  {n:>2} components   : {cross_val_score(pipe, Xc, yc, cv=5).mean():.3f}")

print("\n=== 7. Digits: 64 pixels -> far fewer components, nearly the same accuracy ===")
digits = load_digits()
Xd, yd = digits.data, digits.target
for n in [None, 40, 20, 10]:
    steps = [StandardScaler()] + ([PCA(n_components=n, random_state=0)] if n else []) + [KNeighborsClassifier()]
    score = cross_val_score(make_pipeline(*steps), Xd, yd, cv=5).mean()
    print(f"  {('all 64' if n is None else n):>6} features: accuracy {score:.3f}")

print("\n=== 8. Reconstruction: what is lost? ===")
for n in [5, 15, 40]:
    p = PCA(n_components=n).fit(Xd)
    recon = p.inverse_transform(p.transform(Xd[:1]))
    err = np.abs(recon - Xd[:1]).mean()
    print(f"  {n:>2} components keep {p.explained_variance_ratio_.sum():.0%} of the variance, mean pixel error {err:.2f} (pixels 0-16)")
p = PCA(n_components=15).fit(Xd)
img = p.inverse_transform(p.transform(Xd[:1])).reshape(8, 8)
print("  digit", yd[0], "rebuilt from 15 numbers:")
for row in img:
    print("   ", "".join("#" if v > 8 else "+" if v > 3 else "." for v in row))
