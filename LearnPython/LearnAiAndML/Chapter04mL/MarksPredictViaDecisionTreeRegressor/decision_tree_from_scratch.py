"""
decision_tree_from_scratch.py - A Decision Tree Regressor with NO machine-learning library.

This is a teaching file. It shows what happens "inside" sklearn's
DecisionTreeRegressor, in plain Python.

How it works:
  1. Try every possible split point "study_hours <= t".
  2. For each split, the left group predicts its average, the right group its average.
  3. Measure the error (MSE) of that split. Keep the split with the LOWEST error.
  4. Repeat on each side (recursion) until max_depth or too few students.
  5. A leaf predicts the average marks of the students in it.

Usage:
    python decision_tree_from_scratch.py
"""
import pandas as pd

MAX_DEPTH = 3
MIN_SAMPLES_LEAF = 5


def mean(values):
    return sum(values) / len(values)


def sse(values):
    """Sum of squared errors if we predict the mean for every value."""
    m = mean(values)
    return sum((v - m) ** 2 for v in values)


def best_split(xs, ys):
    """Find the threshold t that gives the lowest total error."""
    pairs = sorted(zip(xs, ys))
    best = None  # (error, threshold)
    for i in range(MIN_SAMPLES_LEAF, len(pairs) - MIN_SAMPLES_LEAF + 1):
        if pairs[i - 1][0] == pairs[i][0]:
            continue  # can't split between two equal x values
        t = (pairs[i - 1][0] + pairs[i][0]) / 2          # midpoint between neighbours
        left = [y for _, y in pairs[:i]]
        right = [y for _, y in pairs[i:]]
        error = sse(left) + sse(right)
        if best is None or error < best[0]:
            best = (error, t)
    return best


def build_tree(xs, ys, depth=0):
    """Return a nested dict: either a leaf or a question with two branches."""
    leaf = {"leaf": True, "value": mean(ys), "n": len(ys)}
    if depth >= MAX_DEPTH or len(ys) < 2 * MIN_SAMPLES_LEAF:
        return leaf
    split = best_split(xs, ys)
    if split is None or split[0] >= sse(ys):   # no split reduces the error
        return leaf
    _, t = split
    left_idx = [i for i, x in enumerate(xs) if x <= t]
    right_idx = [i for i, x in enumerate(xs) if x > t]
    return {
        "leaf": False,
        "threshold": t,
        "left": build_tree([xs[i] for i in left_idx], [ys[i] for i in left_idx], depth + 1),
        "right": build_tree([xs[i] for i in right_idx], [ys[i] for i in right_idx], depth + 1),
    }


def predict(tree, x):
    while not tree["leaf"]:
        tree = tree["left"] if x <= tree["threshold"] else tree["right"]
    return tree["value"]


def show(tree, indent=""):
    if tree["leaf"]:
        print(f"{indent}-> predict {tree['value']:.1f} marks  ({tree['n']} students)")
        return
    print(f"{indent}study_hours <= {tree['threshold']:.2f}?")
    print(f"{indent}  YES:")
    show(tree["left"], indent + "    ")
    print(f"{indent}  NO:")
    show(tree["right"], indent + "    ")


# ---- 1. Load data ----
df = pd.read_csv("train.csv")
x = df["study_hours"].tolist()
y = df["final_marks"].tolist()

# ---- 2. Show how the FIRST split is chosen ----
print("Choosing the first split (lower total error = better):")
pairs = sorted(zip(x, y))
for t in [2.0, 4.0, 5.0, 6.0, 8.0]:
    left = [yy for xx, yy in pairs if xx <= t]
    right = [yy for xx, yy in pairs if xx > t]
    print(f"  split at {t:>4}: left avg {mean(left):5.1f}, right avg {mean(right):5.1f},"
          f" total error = {sse(left) + sse(right):8.1f}")
err, t = best_split(x, y)
print(f"  BEST split found by checking every point: study_hours <= {t:.2f}"
      f" (total error = {err:.1f})")

# ---- 3. Build the full tree ----
tree = build_tree(x, y)
print(f"\nThe full tree (max_depth={MAX_DEPTH}):\n")
show(tree)

# ---- 4. Use it ----
print("\nPredictions:")
for hours in [2, 5, 8, 10, 15]:
    note = "   <- outside training data: same as the last leaf" if hours > max(x) else ""
    print(f"  {hours:>2} hours/day -> {predict(tree, hours):.1f} marks{note}")
