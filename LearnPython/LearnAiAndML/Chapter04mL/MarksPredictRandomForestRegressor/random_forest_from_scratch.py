"""
random_forest_from_scratch.py - A Random Forest Regressor with NO machine-learning library.

This is a teaching file. It shows what happens "inside" sklearn's
RandomForestRegressor, in plain Python.

A random forest is built from 3 ideas:
  1. BOOTSTRAP: each tree gets its own random sample of students
     (drawn WITH replacement, so some students appear twice, some not at all).
  2. RANDOM FEATURES: at every split, a tree may only look at a random
     subset of the inputs (here 2 of the 4).
  3. AVERAGE: the forest's prediction is the average of all the trees.

Because every tree sees different data and different features, they make
DIFFERENT mistakes, and averaging cancels many of those mistakes out.

Usage:
    python random_forest_from_scratch.py
"""
import random

import pandas as pd

FEATURES = ["study_hours", "coaching", "live_sessions_attended", "recorded_course_completion"]
N_TREES = 50
MAX_FEATURES = 2       # features each split is allowed to consider
MIN_SAMPLES_LEAF = 2
random.seed(42)


# ---------- A small decision tree (same idea as the Decision Tree demo) ----------

def best_split(rows, ys, feature_ids):
    """Try every threshold on the allowed features; return the lowest-error split."""
    best = None  # (error, feature_index, threshold)
    n = len(ys)
    for f in feature_ids:
        order = sorted(range(n), key=lambda i: rows[i][f])
        xs = [rows[i][f] for i in order]
        ys_sorted = [ys[i] for i in order]
        total, total_sq = sum(ys_sorted), sum(y * y for y in ys_sorted)
        left_sum = left_sq = 0.0
        for k in range(1, n):
            y = ys_sorted[k - 1]
            left_sum += y
            left_sq += y * y
            if k < MIN_SAMPLES_LEAF or n - k < MIN_SAMPLES_LEAF or xs[k - 1] == xs[k]:
                continue
            right_sum, right_sq = total - left_sum, total_sq - left_sq
            # SSE = Σy² − (Σy)²/n   for each side
            error = (left_sq - left_sum ** 2 / k) + (right_sq - right_sum ** 2 / (n - k))
            if best is None or error < best[0]:
                best = (error, f, (xs[k - 1] + xs[k]) / 2)
    return best


def build_tree(rows, ys, max_features):
    leaf = {"value": sum(ys) / len(ys)}
    if len(ys) < 2 * MIN_SAMPLES_LEAF:
        return leaf
    allowed = random.sample(range(len(FEATURES)), max_features)   # RANDOM FEATURES
    split = best_split(rows, ys, allowed)
    if split is None:
        return leaf
    _, f, t = split
    left = [i for i, r in enumerate(rows) if r[f] <= t]
    right = [i for i, r in enumerate(rows) if r[f] > t]
    return {
        "feature": f,
        "threshold": t,
        "left": build_tree([rows[i] for i in left], [ys[i] for i in left], max_features),
        "right": build_tree([rows[i] for i in right], [ys[i] for i in right], max_features),
    }


def tree_predict(tree, row):
    while "value" not in tree:
        tree = tree["left"] if row[tree["feature"]] <= tree["threshold"] else tree["right"]
    return tree["value"]


# ---------- The forest ----------

def build_forest(rows, ys):
    forest = []
    n = len(rows)
    for _ in range(N_TREES):
        sample = [random.randrange(n) for _ in range(n)]              # BOOTSTRAP
        forest.append(build_tree([rows[i] for i in sample], [ys[i] for i in sample], MAX_FEATURES))
    return forest


def forest_predict(forest, row):
    return sum(tree_predict(t, row) for t in forest) / len(forest)     # AVERAGE


def r2(y_true, y_pred):
    mean_y = sum(y_true) / len(y_true)
    ss_res = sum((a - b) ** 2 for a, b in zip(y_true, y_pred))
    ss_tot = sum((a - mean_y) ** 2 for a in y_true)
    return 1 - ss_res / ss_tot


# ---------- 1. Load and prepare data ----------
df = pd.read_csv("train.csv")
df["coaching"] = (df["coaching"] == "Yes").astype(int)
data = list(zip(df[FEATURES].values.tolist(), df["final_marks"].tolist()))
random.shuffle(data)
cut = int(len(data) * 0.8)
train_rows, train_y = [r for r, _ in data[:cut]], [y for _, y in data[:cut]]
test_rows, test_y = [r for r, _ in data[cut:]], [y for _, y in data[cut:]]
print(f"Training on {len(train_rows)} students, testing on {len(test_rows)} unseen students.\n")

# ---------- 2. Show what a bootstrap sample looks like ----------
sample = [random.randrange(len(train_rows)) for _ in range(len(train_rows))]
unique = len(set(sample))
print("Bootstrap sample for one tree:")
print(f"  Drew {len(sample)} students WITH replacement -> only {unique} different students "
      f"({unique / len(sample):.0%}).")
print(f"  The other {len(train_rows) - unique} were left out ('out-of-bag') for this tree.\n")

# ---------- 3. One full tree vs. a forest ----------
single = build_tree(train_rows, train_y, max_features=len(FEATURES))
single_pred = [tree_predict(single, r) for r in test_rows]
print(f"One decision tree (all data, all features): Test R² = {r2(test_y, single_pred):.3f}")

print(f"Building a forest of {N_TREES} trees ...")
forest = build_forest(train_rows, train_y)
forest_pred = [forest_predict(forest, r) for r in test_rows]
print(f"Random forest ({N_TREES} trees):              Test R² = {r2(test_y, forest_pred):.3f}")

# ---------- 4. Watch the trees disagree, then average ----------
student = test_rows[0]
votes = [tree_predict(t, student) for t in forest]
print("\nExample student:", {f: (int(v) if float(v).is_integer() else v) for f, v in zip(FEATURES, student)})
print(f"  Actual marks         : {test_y[0]}")
print(f"  First 8 trees predict: {', '.join(f'{v:.1f}' for v in votes[:8])} ...")
print(f"  Range across trees   : {min(votes):.1f} to {max(votes):.1f}")
print(f"  Forest (average)     : {sum(votes) / len(votes):.1f}")

# ---------- 5. More trees -> more stable ----------
print("\nHow the number of trees affects the test score:")
for k in [1, 5, 10, 25, 50]:
    preds = [sum(tree_predict(t, r) for t in forest[:k]) / k for r in test_rows]
    print(f"  {k:>3} tree(s): Test R² = {r2(test_y, preds):.3f}")
