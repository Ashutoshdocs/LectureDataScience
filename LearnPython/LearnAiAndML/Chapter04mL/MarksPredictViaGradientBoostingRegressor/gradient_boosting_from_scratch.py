"""
gradient_boosting_from_scratch.py - Gradient Boosting Regressor with NO machine-learning library.

This is a teaching file. It shows what happens "inside" sklearn's
GradientBoostingRegressor, in plain Python.

The algorithm:
  1. Start by predicting the AVERAGE marks for every student.
  2. Work out each student's RESIDUAL = actual marks − current prediction.
     (This is the "mistake" still left to fix.)
  3. Train a SMALL tree to predict those residuals.
  4. Add a small fraction (the learning rate) of that tree's output to the prediction.
  5. Repeat steps 2–4 many times.

Each new tree fixes part of what the trees before it got wrong.

Why "gradient"? For squared error, the residual is exactly the (negative)
gradient of the loss, so each tree is a step of gradient descent.

Usage:
    python gradient_boosting_from_scratch.py
"""
import random

import pandas as pd

FEATURES = ["study_hours", "coaching", "live_sessions_attended", "recorded_course_completion"]
N_TREES = 300
LEARNING_RATE = 0.05
MAX_DEPTH = 2
MIN_SAMPLES_LEAF = 3
random.seed(42)


# ---------- A small regression tree (same idea as the Decision Tree demo) ----------

def best_split(rows, ys):
    """Try every threshold on every feature; return the lowest-error split."""
    best = None  # (error, feature_index, threshold)
    n = len(ys)
    for f in range(len(FEATURES)):
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
            error = (left_sq - left_sum ** 2 / k) + (right_sq - right_sum ** 2 / (n - k))
            if best is None or error < best[0]:
                best = (error, f, (xs[k - 1] + xs[k]) / 2)
    return best


def build_tree(rows, ys, depth=0):
    leaf = {"value": sum(ys) / len(ys)}
    if depth >= MAX_DEPTH or len(ys) < 2 * MIN_SAMPLES_LEAF:
        return leaf
    split = best_split(rows, ys)
    if split is None:
        return leaf
    _, f, t = split
    left = [i for i, r in enumerate(rows) if r[f] <= t]
    right = [i for i, r in enumerate(rows) if r[f] > t]
    return {
        "feature": f,
        "threshold": t,
        "left": build_tree([rows[i] for i in left], [ys[i] for i in left], depth + 1),
        "right": build_tree([rows[i] for i in right], [ys[i] for i in right], depth + 1),
    }


def tree_predict(tree, row):
    while "value" not in tree:
        tree = tree["left"] if row[tree["feature"]] <= tree["threshold"] else tree["right"]
    return tree["value"]


def describe(tree, indent="  "):
    if "value" in tree:
        print(f"{indent}-> correction {tree['value']:+.2f} marks")
        return
    print(f"{indent}{FEATURES[tree['feature']]} <= {tree['threshold']:.2f}?")
    print(f"{indent}  YES:")
    describe(tree["left"], indent + "    ")
    print(f"{indent}  NO:")
    describe(tree["right"], indent + "    ")


def rmse(actual, predicted):
    return (sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual)) ** 0.5


# ---------- 1. Load and prepare data ----------
df = pd.read_csv("train.csv")
df["coaching"] = (df["coaching"] == "Yes").astype(int)
data = list(zip(df[FEATURES].values.tolist(), df["final_marks"].tolist()))
random.shuffle(data)
cut = int(len(data) * 0.8)
train_rows, train_y = [r for r, _ in data[:cut]], [y for _, y in data[:cut]]
test_rows, test_y = [r for r, _ in data[cut:]], [y for _, y in data[cut:]]
print(f"Training on {len(train_rows)} students, testing on {len(test_rows)} unseen students.\n")

# ---------- 2. Step 0: predict the average for everyone ----------
start = sum(train_y) / len(train_y)
train_pred = [start] * len(train_rows)
test_pred = [start] * len(test_rows)
print(f"Step 0: predict the average ({start:.1f}) for every student.")
print(f"        Test RMSE = {rmse(test_y, test_pred):.2f} marks\n")

# ---------- 3. Add trees one by one, each fitting the current residuals ----------
trees = []
for t in range(1, N_TREES + 1):
    residuals = [y - p for y, p in zip(train_y, train_pred)]      # what's still wrong
    tree = build_tree(train_rows, residuals)                       # learn to predict it
    trees.append(tree)
    train_pred = [p + LEARNING_RATE * tree_predict(tree, r) for p, r in zip(train_pred, train_rows)]
    test_pred = [p + LEARNING_RATE * tree_predict(tree, r) for p, r in zip(test_pred, test_rows)]

    if t == 1:
        print("Tree 1 (trained on the residuals of step 0):")
        describe(tree)
        print(f"  Its corrections are multiplied by the learning rate ({LEARNING_RATE}) "
              "before being added.\n")
        print(f"{'Trees':>7}{'Train RMSE':>13}{'Test RMSE':>12}")
    if t in (1, 5, 10, 25, 50, 100, 200, 300):
        print(f"{t:>7}{rmse(train_y, train_pred):>11.2f}{rmse(test_y, test_pred):>12.2f}")

# ---------- 4. Follow one student's prediction as it is built ----------
# pick the test student whose marks are furthest from the average
i = max(range(len(test_y)), key=lambda k: abs(test_y[k] - start))
student, actual = test_rows[i], test_y[i]
print("\nExample student:", {f: (int(v) if float(v).is_integer() else v)
                             for f, v in zip(FEATURES, student)})
print(f"  Actual marks: {actual}")
pred = start
print(f"  Start (average)  : {pred:.1f}")
for t, tree in enumerate(trees, 1):
    pred += LEARNING_RATE * tree_predict(tree, student)
    if t in (1, 10, 25, 50, 100, 200, 300):
        print(f"  After {t:>3} trees  : {pred:.1f}   (still {actual - pred:+.1f} to go)")
