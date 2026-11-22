"""Lecture 16: Decision trees: Gini by hand, export_text, depth/leaf controls, pruning, importances, instability, regression."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text

np.set_printoptions(suppress=True)


def gini(labels):
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return 1 - np.sum(p ** 2)


print("=== 1. Gini impurity by hand ===")
for labels in [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 2, 0, 1, 2]]:
    print(f"  {labels!s:<20} gini = {gini(labels):.3f}")
print("  0 = pure node; a tree picks the split that lowers the weighted gini the most")

print("\n=== 2. Finding the best split on one feature ===")
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([0, 0, 0, 1, 0, 1, 1, 1])
best = None
for t in (x[:-1] + x[1:]) / 2:
    left, right = y[x <= t], y[x > t]
    w = (len(left) * gini(left) + len(right) * gini(right)) / len(y)
    best = min(best or (w, t), (w, t))
    print(f"  threshold {t:3.1f}: left {left.tolist()!s:<16} right {right.tolist()!s:<16} weighted gini {w:.3f}")
print(f"  best threshold {best[1]} | sklearn chose {DecisionTreeClassifier(max_depth=1).fit(x.reshape(-1, 1), y).tree_.threshold[0]}")

print("\n=== 3. Readable rules ===")
iris = load_iris()
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(iris.data, iris.target)
print(export_text(tree, feature_names=iris.feature_names))
print("  depth", tree.get_depth(), "| leaves", tree.get_n_leaves(),
      "| importances", dict(zip([n.split(" (")[0] for n in iris.feature_names], tree.feature_importances_.round(3).tolist())))
sample = [[6.0, 3.0, 4.5, 1.6]]
print("  sample", sample[0], "-> leaf", tree.apply(sample)[0], "proba", tree.predict_proba(sample)[0].round(3),
      "->", iris.target_names[tree.predict(sample)[0]])

print("\n=== 4. Complexity controls (breast cancer) ===")
X, yc = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, yc, stratify=yc, random_state=0)
for params in [{}, {"max_depth": 3}, {"min_samples_leaf": 10}, {"max_leaf_nodes": 8}, {"min_samples_split": 40}]:
    t = DecisionTreeClassifier(random_state=0, **params).fit(Xtr, ytr)
    print(f"  {str(params):<26} leaves {t.get_n_leaves():>3}  train {t.score(Xtr, ytr):.3f}  test {t.score(Xte, yte):.3f}")

print("\n=== 5. Cost-complexity pruning ===")
path = DecisionTreeClassifier(random_state=0).cost_complexity_pruning_path(Xtr, ytr)
alphas = path.ccp_alphas[::3]
scores = [cross_val_score(DecisionTreeClassifier(ccp_alpha=a, random_state=0), Xtr, ytr, cv=5).mean() for a in alphas]
best_alpha = alphas[int(np.argmax(scores))]
for a, s in list(zip(alphas, scores))[:8]:
    print(f"  ccp_alpha {a:.4f}  CV {s:.3f}")
pruned = DecisionTreeClassifier(ccp_alpha=best_alpha, random_state=0).fit(Xtr, ytr)
print(f"  chosen ccp_alpha {best_alpha:.4f}: leaves {pruned.get_n_leaves()}, test {pruned.score(Xte, yte):.3f}")

print("\n=== 6. Instability: small data changes, different trees ===")
for seed in range(3):
    idx = np.random.default_rng(seed).choice(len(Xtr), int(0.9 * len(Xtr)), replace=False)
    t = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr[idx], ytr[idx])
    root = load_breast_cancer().feature_names[t.tree_.feature[0]]
    print(f"  90% sample {seed}: root question on '{root}', test {t.score(Xte, yte):.3f}")
print("  -> averaging many trees (a random forest) fixes this; next lecture")

print("\n=== 7. Regression tree: step-shaped predictions ===")
rng = np.random.default_rng(0)
xr = np.sort(rng.uniform(0, 6, 80)).reshape(-1, 1)
yr = np.sin(xr).ravel() + rng.normal(0, 0.15, 80)
for depth in [1, 3, 10]:
    reg = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(xr, yr)
    preds = reg.predict(np.linspace(0, 6, 7).reshape(-1, 1))
    print(f"  depth {depth:>2}: {reg.get_n_leaves():>2} distinct values, predictions at x=0..6: {preds.round(2)}")
