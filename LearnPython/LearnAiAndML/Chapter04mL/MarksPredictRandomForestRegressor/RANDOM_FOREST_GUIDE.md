# 📘 Random Forest Regressor: A Teaching Guide

A beginner-friendly guide to **what** a random forest is, **how** it works, and **how to use it in Python**. It uses the student-marks demo throughout:

> **Inputs:** study hours, coaching (Yes/No), live sessions attended, recorded course completion %
> **Output:** final marks

---

## 1. What is a Random Forest?

A **Random Forest** is a team of **many decision trees**. Each tree makes its own prediction, and the forest combines them:

- **Regressor** (predicting a number): the forest takes the **average** of the trees
- **Classifier** (predicting a category): the forest takes a **majority vote**

### The "wisdom of the crowd" idea

Ask one teacher to guess a student's marks and they might be off by 10. Ask 200 teachers who each know slightly different things, then average their guesses. Their individual mistakes tend to **cancel out**, and the average is usually closer than almost any single guess.

That's a random forest.

| Term | Meaning | In our demo |
|------|---------|-------------|
| **Features** (inputs) | What we know | study hours, coaching, live sessions, recorded course |
| **Target** (output) | What we want to predict | final marks |
| **Estimator / tree** | One decision tree in the forest | |
| **`n_estimators`** | Number of trees | 200 |
| **Ensemble** | A model made by combining many models | the forest |

---

## 2. Quick Recap: One Decision Tree

A decision tree asks yes/no questions and ends in a **leaf** that predicts the average marks of the training students in it (simplified example):

```
                 study_hours <= 3.4?
              YES /              \ NO
   live_sessions <= 6?        coaching = Yes?
     /        \                /          \
   44.1      52.6           70.3      live_sessions <= 9?
                                        /        \
                                      58.9      66.2
```

**The problem:** a single deep tree **overfits**. It memorises the noise in its training students. In our demo:

| Model | Train R² | Test R² |
|-------|----------|---------|
| Single decision tree | **1.000** (perfect!) | 0.680 (poor) |

It's also **unstable**: change a few training students and you can get a very different tree.

Random forests fix both problems.

---

## 3. How a Random Forest Is Built

### Ingredient 1: Bootstrap sampling ("bagging")

Each tree is trained on its **own random sample** of the students, drawn **with replacement**:

```
 Original students:  A  B  C  D  E  F  G  H

 Tree 1's sample:    A  A  C  D  F  F  G  H     (B, E left out)
 Tree 2's sample:    B  C  C  D  E  E  G  G     (A, F, H left out)
 Tree 3's sample:    A  B  D  D  E  F  H  H     (C, G left out)
```

- Same size as the original data, but some students appear twice and some not at all
- On average each tree sees about **63%** of the unique students
- The **~37% left out** are called **out-of-bag (OOB)** students

**Bagging** = **B**ootstrap **agg**regat**ing** (sample, then combine).

### Ingredient 2: Random features at each split

When a tree chooses a question, it may only look at a **random subset of the features**.

```
 Split 1: allowed to look at [study_hours, coaching]           → picks study_hours
 Split 2: allowed to look at [live_sessions, recorded_course]  → picks live_sessions
 Split 3: allowed to look at [coaching, live_sessions]         → picks coaching
```

**Why?** Without this, every tree would pick `study_hours` (the strongest input) first, and all the trees would look alike. Forcing variety makes the trees **different**, and different trees make **different mistakes** that cancel when averaged.

> In scikit-learn this is `max_features`. For regression the default is `1.0` (all features), which relies only on bootstrapping for variety. Try `max_features="sqrt"` or `0.5` as an experiment.

### Ingredient 3: Average the predictions

```
                   ┌── Tree 1 (sample 1, random features)  → 71.2
                   ├── Tree 2 (sample 2, random features)  → 71.5
 New student  ──►  ├── Tree 3 (sample 3, random features)  → 68.4
                   ├──  ...
                   └── Tree 200                            → 69.0
                                                      ─────────────
                                         Average  =  70.0 marks
```

### The whole algorithm

```
 for each of the N trees:
     1. draw a bootstrap sample of the students
     2. grow a decision tree on it;
        at every split, only consider a random subset of the features
 to predict:
     run the student through every tree and average the answers
```

👉 Run `python random_forest_from_scratch.py` to see all three ingredients in plain Python.

---

## 4. Why Averaging Works

Each deep tree has **low bias** (it can follow complex patterns) but **high variance** (it jumps around depending on the data it saw). Averaging many such trees keeps the low bias but **reduces the variance**.

From `random_forest_from_scratch.py`, one student whose actual mark was **56.4**:

```
  First 8 trees predict: 52.5, 47.4, 53.0, 54.1, 42.4, 54.4, 49.7, 69.3 ...
  Range across trees   : 42.1 to 73.3
  Forest (average)     : 55.7
```

Individual trees were off by as much as 17 marks; the average was off by less than 1.

### More trees → more stable

```
    1 tree(s): Test R² = 0.376
    5 tree(s): Test R² = 0.679
   10 tree(s): Test R² = 0.688
   50 tree(s): Test R² = 0.687
```

The score jumps quickly, then **levels off**. Adding more trees almost never hurts accuracy; it just costs more time. 100–500 trees is typical.

---

## 5. Out-of-Bag (OOB) Score: A Free Test

Every tree has ~37% of students it never saw. To get an OOB score:

1. For each student, collect predictions **only from trees that didn't train on them**
2. Average those predictions and compare with the real marks

This gives a test score **without** setting aside a separate test set. In our demo: **OOB R² = 0.829**, close to the test-set R² of 0.859.

```python
model = RandomForestRegressor(n_estimators=200, oob_score=True)
model.fit(X, y)
print(model.oob_score_)
```

---

## 6. Feature Importance

A forest can tell you which inputs it **relied on most**. Each time a feature is used for a split, the reduction in error is credited to that feature, and the totals are averaged across all trees:

```
    study_hours                  62.0%  ███████████████████████████████
    live_sessions_attended       21.2%  ███████████
    recorded_course_completion   11.9%  ██████
    coaching                      4.9%  ██
```

### ⚠️ Importance is not the same as effect size

Coaching has the lowest importance, yet for a student with 6 study hours, 10 live sessions and 50% of the recorded course:

| Coaching | Predicted marks |
|----------|-----------------|
| No | 65.2 |
| Yes | 69.6 |

That's a **4–5 mark difference**. Why is its importance so low?
- Coaching is **Yes/No**, so it can only be split once per branch; study hours (0.5–10) can be split many times
- Study hours cover a **much wider range of marks** (~28 marks from low to high), so splitting on it reduces more total error
- Part of coaching's effect **overlaps** with the recorded course (students without coaching gain more from it)

Importance tells you **how useful a feature was for splitting**, not **how much it changes the prediction**, and certainly not whether it *causes* the change.

---

## 7. Key Settings (Hyperparameters)

| Setting | What it does | Our demo |
|---------|--------------|----------|
| `n_estimators` | Number of trees. More = more stable, slower | 200 |
| `max_depth` | Max depth of each tree. `None` = grow fully | None |
| `min_samples_leaf` | Minimum students in each leaf | 2 |
| `max_features` | Features considered at each split | default (1.0) |
| `bootstrap` | Use bootstrap samples | True |
| `oob_score` | Calculate the out-of-bag score | True |
| `random_state` | Fixes the randomness so results repeat | 42 |

**Note:** unlike a single tree, the trees in a forest are usually grown **deep**. The averaging handles the overfitting.

---

## 8. Comparing All Four Models in This Series

| | Linear | Polynomial | Decision Tree | Random Forest |
|---|---|---|---|---|
| **Model shape** | Straight line | Smooth curve | Steps | Many steps averaged (smoother) |
| **Handles curves** | ❌ | ✅ | ✅ | ✅ |
| **Handles interactions** (e.g. coaching × recorded course) | ❌ unless added by hand | ❌ unless added by hand | ✅ | ✅ |
| **Overfitting risk** | Low | Medium (high degree) | **High** | Low |
| **Easy to explain** | ✅✅ | ✅ | ✅✅ | ❌ (200 trees!) |
| **Extrapolates beyond data** | Yes (keeps going) | Yes (wildly) | No (flat) | No (flat) |
| **Needs feature scaling** | No | Helps | No | No |

---

## 9. Strengths and Limitations

### ✅ Strengths
- **Accurate** out of the box, with little tuning
- **Resists overfitting** much better than one tree
- Finds **curves and interactions** on its own
- Handles **many features** and mixed types (numbers and Yes/No)
- Gives **feature importance** and a free **OOB score**

### ⚠️ Limitations
- **Hard to explain**: you can't draw 200 trees on a whiteboard
- **Can't extrapolate**: a student with 15 study hours gets roughly the same prediction as one with 10
- **Slower and bigger** than a single model
- Feature importance can be **misleading** (see Section 6)

---

## 10. Random Forests in Python

### With scikit-learn (the usual way)

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load data and turn Yes/No into 1/0
df = pd.read_csv("train.csv")
df["coaching"] = (df["coaching"] == "Yes").astype(int)

features = ["study_hours", "coaching", "live_sessions_attended", "recorded_course_completion"]
X = df[features]
y = df["final_marks"]

# 2. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train
model = RandomForestRegressor(n_estimators=200, min_samples_leaf=2,
                              oob_score=True, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
print("Test R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("OOB R²:", model.oob_score_)

# 5. Feature importance
for name, imp in zip(features, model.feature_importances_):
    print(f"{name}: {imp:.1%}")

# 6. Predict for a new student
new = pd.DataFrame([[6, 1, 15, 80]], columns=features)
print("Predicted marks:", model.predict(new)[0])

# 7. Look at what each tree said
tree_preds = [tree.predict(new.to_numpy())[0] for tree in model.estimators_]
print("Trees ranged from", min(tree_preds), "to", max(tree_preds))
```

### From scratch (to understand it)

See **`random_forest_from_scratch.py`**: bootstrap sampling, random features at each split, and averaging, in plain Python.

---

## 11. Summary

```
 Data ─► many bootstrap samples ─► one deep tree per sample (random features at each split)
      ─► every tree predicts ─► AVERAGE = forest prediction
```

- A random forest is **many decision trees averaged together**
- **Bootstrap samples** + **random features** make the trees different
- **Averaging** cancels out their individual mistakes → more accurate and stable than one tree
- **OOB score** gives a free test score
- **Feature importance** shows which inputs were used most, but not cause and effect

---

## 12. Practice Exercises ✏️

1. In `train.py`, set `N_TREES` to 1, 5, 20, 100 and 500. Record the Test R² for each. When does it stop improving?
2. Add `max_features="sqrt"` to the forest. Does the test score change? Does feature importance change?
3. Use `predict.py` option 2 for the same student with coaching **Yes** then **No**. Repeat for a student with 0% and 100% recorded course. Does coaching matter more or less when the recorded course is high?
4. Remove the `coaching` column from `FEATURES` and retrain. How much does the test score drop?
5. Predict for a student with 20 study hours. Compare with 10 hours. Why are they so similar?
6. In `random_forest_from_scratch.py`, change `MAX_FEATURES` to 4 (all features). Does the forest still beat the single tree?
