# 📘 Decision Tree Regressor: A Teaching Guide

A beginner-friendly guide to **what** a decision tree regressor is, **how** it works, and **how to use it in Python**. It uses the student-marks demo (study hours → marks) throughout.

---

## 1. What is a Decision Tree Regressor?

A **Decision Tree Regressor** predicts a **number** by asking a series of **yes/no questions** about the input, like a flowchart.

It's how a teacher might guess marks without any maths:

> "Did they study more than 4–5 hours? No. More than 2–3 hours? Yes. Students like that usually score around 45–55."

| Term | Meaning | In our demo |
|------|---------|-------------|
| **Input** (x, feature) | What we know | study hours |
| **Output** (y, target) | What we want to predict | final marks |
| **Root** | The first question at the top | `study_hours <= 4.65?` |
| **Node / split** | A yes/no question | `study_hours <= 2.60?` |
| **Branch** | The YES or NO path from a question | |
| **Leaf** | A final box with no more questions; it gives the prediction | `predict 75.5` |
| **Depth** | How many questions from the root to the deepest leaf | 3 |

> "Regressor" = predicts a **number**. A "Decision Tree **Classifier**" works the same way but predicts a **category** (e.g. pass/fail).

---

## 2. What the Tree Looks Like

Our trained tree:

```
                     study_hours <= 4.65?
                 YES /                  \ NO
      study_hours <= 2.60?          study_hours <= 5.10?
       YES /        \ NO             YES /        \ NO
   <= 1.25?      <= 3.10?           65.0      <= 6.50?
   /     \        /     \                     /      \
 27.7   36.5    45.0   55.1                 75.5    81.2
```

**To predict for 6 hours:** 6 ≤ 4.65? No → 6 ≤ 5.10? No → 6 ≤ 6.50? Yes → **75.5 marks**.

### Predictions come in steps

Because every student in a leaf gets the **same** prediction, the tree's predictions look like a **staircase**, not a smooth line:

```
 Marks
  85 |                          ________________________  81.2
  75 |                   ______| 75.5
  65 |                __| 65.0
  55 |         ______| 55.1
  45 |      __| 45.0
  35 |  ___| 36.5
  25 |_| 27.7
     +-----------------------------------------------------
      0  1   2   3   4   5   6   7   8   9   10   Study hours
```

More depth = more, smaller steps.

---

## 3. How Does the Tree Choose Its Questions?

The goal of every split is to make each group of students **as similar as possible** in their marks. Then the group's average is a good prediction for everyone in it.

### Step 1: Measure how "mixed" a group is

For a group of students, predict their **average** marks and add up the squared errors:

```
SSE = Σ (marks − group average)²
```

- Low SSE → students in the group have similar marks → good
- High SSE → marks are all over the place → bad

(This is the same squared-error idea used in linear regression. Dividing by the number of students gives the **MSE**.)

### Step 2: Try every possible split

For each possible threshold `t`, split students into:
- **Left:** `study_hours <= t`
- **Right:** `study_hours > t`

Then calculate:

```
total error = SSE(left) + SSE(right)
```

From our data (`decision_tree_from_scratch.py` prints this):

| Split at | Left avg | Right avg | Total error |
|----------|----------|-----------|-------------|
| 2.0 | 28.9 | 67.4 | 28,807 |
| 4.0 | 41.8 | 76.2 | 10,803 |
| **4.65** | | | **10,685** ← best |
| 5.0 | 47.4 | 79.8 | 12,255 |
| 6.0 | 50.9 | 80.3 | 17,863 |
| 8.0 | 59.4 | 80.0 | 34,930 |

### Step 3: Keep the best split, then repeat

The split with the **lowest total error** becomes the question. Then the same process runs **again on each side**, separately. This is called **recursive splitting**.

### Step 4: Stop

The tree stops splitting when:
- it reaches **`max_depth`** (3 in our demo), or
- a split would leave fewer than **`min_samples_leaf`** students (5 in our demo) in a leaf, or
- no split reduces the error

Each leaf then predicts the **average marks** of its students.

```
 All students → find best split → split into 2 groups
                                     ↓              ↓
                       find best split    find best split
                              ↓                   ↓
                             ...                 ...
                   stop → leaf = average marks
```

👉 Run `python decision_tree_from_scratch.py` to see this in plain Python. It builds **exactly the same tree** as scikit-learn.

---

## 4. Tree Size: Underfitting vs. Overfitting

The most important settings control **how big the tree can grow**:

| Setting | What it does | Our demo |
|---------|--------------|----------|
| `max_depth` | Maximum number of questions from top to bottom | 3 |
| `min_samples_leaf` | Each leaf must have at least this many students | 5 |
| `min_samples_split` | A node needs at least this many students to be split | default (2) |
| `max_leaf_nodes` | Maximum number of leaves | default (no limit) |

```
 Too small                Just right               Too big (no limit)
 (depth 1)                (depth 3)                (one leaf per student)

  ________                    ___                   _   _-_
          |________        __|                    _| |_|   |_-_
                        __|                     _|
                     __|                       |
  UNDERFITTING            GOOD FIT               OVERFITTING
  too few steps           follows the pattern    follows every bit of noise
```

**Our results on students the model has never seen:**

| Model | Train R² | Test R² | Test error |
|-------|----------|---------|------------|
| Straight line | 0.824 | 0.773 | 6.19 marks |
| **Tree, depth 3** | 0.936 | **0.912** | **4.05 marks** |
| Tree, no depth limit | **0.968** | 0.792 | 6.05 marks |

The unlimited tree has the **best training score** but a much **worse test score**. It memorised the noise in the training students instead of learning the general pattern. That's **overfitting**, and it's the biggest weakness of decision trees.

**How to choose:** try several `max_depth` values and pick the one with the best **test** score (or use cross-validation).

---

## 5. How Good Is the Model?

| Metric | Meaning | Good value |
|--------|---------|------------|
| **R² score** | How much of the variation in marks the model explains | Close to **1.0** |
| **MAE** (Mean Absolute Error) | Average size of the mistake, in marks | As **small** as possible |
| **MSE** | Average squared error | As **small** as possible |
| **RMSE** | √MSE, back in the original units (marks) | As **small** as possible |

Always compare **Train** and **Test** scores. A big gap (high train, low test) means overfitting.

---

## 6. Strengths and Limitations

### ✅ Strengths
- **Easy to explain**: you can draw it and follow the questions by hand
- **Handles curves and jumps** without you choosing an equation
- **No feature scaling needed**: it only compares values with thresholds
- Works with several inputs, and with numbers or categories

### ⚠️ Limitations
- **Overfits easily** unless you limit its size
- **Predictions are steps**, not smooth: 7 hours and 10 hours both get 81.2
- **Can't extrapolate**: anything beyond the training range gets the nearest leaf's value. 15 hours → 81.2 marks, the same as 10 hours. (Linear regression would keep rising; polynomial would shoot up or dive.)
- **Unstable**: a small change in the training data can produce a quite different tree
  (Random Forests fix this by averaging many trees)

---

## 7. Decision Trees in Python

### With scikit-learn (the usual way)

```python
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load data
df = pd.read_csv("train.csv")
X = df[["study_hours"]]
y = df["final_marks"]

# 2. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train
model = DecisionTreeRegressor(max_depth=3, min_samples_leaf=5, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
print("R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))

# 5. Look at the learned tree
print(export_text(model, feature_names=["study_hours"]))

# 6. Predict for a new student
print("Predicted marks:", model.predict(pd.DataFrame({"study_hours": [6]}))[0])
```

### Draw the tree as a picture

```python
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(14, 6))
plot_tree(model, feature_names=["study_hours"], filled=True, rounded=True)
plt.show()
```

(Needs `pip install matplotlib`.)

### From scratch (to understand it)

See **`decision_tree_from_scratch.py`**, which builds the tree with plain Python: try every split, keep the one with the lowest error, repeat.

---

## 8. Summary

```
 Data → try every split → keep the one with the lowest error → repeat on each side
      → stop at max_depth / min_samples_leaf → each leaf predicts its group's average
```

- A decision tree predicts with **yes/no questions**, not an equation
- Each split is chosen to make the groups' marks **as similar as possible** (lowest squared error)
- Each **leaf predicts the average** of its training students, so predictions are **steps**
- **Limit the tree's size** (`max_depth`, `min_samples_leaf`) to avoid overfitting
- It **can't extrapolate** beyond the training data

---

## 9. Practice Exercises ✏️

1. Using the tree in Section 2, predict marks by hand for 1, 3.5 and 5 hours. Check with `predict.py`.
2. In `train.py`, set `MAX_DEPTH` to 1, 2, 3, 5 and 10. Record the Train R² and Test R² for each. Which depth is best? When does overfitting start?
3. Set `MAX_DEPTH = 1` and draw the tree. How many different predictions can it make?
4. Change `MIN_SAMPLES_LEAF` to 1 and then 20. How does the tree change?
5. Delete 10 random rows from `train.csv` and retrain. Does the tree change much? (This shows trees are unstable.)
6. Predict for 0, 12 and 20 hours. Compare with what a straight line would predict.
