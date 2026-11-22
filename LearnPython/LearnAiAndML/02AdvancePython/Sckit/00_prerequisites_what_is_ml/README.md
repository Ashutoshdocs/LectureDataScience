# Lecture 00: Prerequisites & what machine learning is

Run: `python lecture.py`

## What you should know first

scikit-learn sits on top of **NumPy** (and works well with **pandas**). You don't need to be an expert, but you should be comfortable with:

| Skill | Example | Why it matters here |
|-------|---------|---------------------|
| Python basics | functions, loops, lists, dicts, classes | every model is an object with methods |
| NumPy arrays | `a.shape`, `a[:, 0]`, `a.reshape(-1, 1)`, `a.mean(axis=0)` | `X` and `y` are arrays |
| Boolean masks | `a[a > 5]`, `(pred == y).mean()` | computing accuracy, filtering rows |
| pandas basics | `df["col"]`, `df.drop(columns=...)`, `df.describe()` | real data arrives as tables |
| A little statistics | mean, median, standard deviation | scaling, metrics, imputation |

`lecture.py` begins with a quick NumPy/pandas refresher covering exactly what this course uses.

## Rules vs learning

**Traditional programming:** you write the rules.

```python
def is_spam(email):
    return "free money" in email or email.count("!") > 5
```

**Machine learning:** you give **examples with answers**, and an algorithm **learns the rules**.

```
 examples (X) + answers (y)  ──▶  learning algorithm  ──▶  model (learned rule)
 new example                 ──▶  model               ──▶  predicted answer
```

Use ML when the rules are **too complex to write by hand** (recognising digits, spotting fraud), when they **change over time**, or when you have **lots of examples** but no clear formula.

Don't use ML when a simple rule works, when you have very little data, or when every decision must be 100% explainable and deterministic (tax calculations).

## Types of machine learning

| Type | Have answers (`y`)? | Goal | Examples | scikit-learn |
|------|--------------------|------|----------|--------------|
| **Supervised: classification** | ✅ categories | predict a **class** | spam/ham, disease yes/no, digit 0–9 | `LogisticRegression`, `RandomForestClassifier`, `SVC` |
| **Supervised: regression** | ✅ numbers | predict a **number** | house price, temperature, sales | `LinearRegression`, `Ridge`, `RandomForestRegressor` |
| **Unsupervised: clustering** | ❌ | find **groups** | customer segments | `KMeans`, `DBSCAN` |
| **Unsupervised: dimensionality reduction** | ❌ | **compress** features | visualisation, noise removal | `PCA` |
| Reinforcement learning | rewards | learn actions | games, robots | not in scikit-learn |

> **Classification or regression?** Ask: "is the answer a category or a quantity?" "Will it rain?" is classification. "How many mm of rain?" is regression.

## The machine learning workflow

1. **Define the problem**: what do you predict, and how will you measure success?
2. **Get the data**: features `X` and target `y`.
3. **Explore**: shapes, types, missing values, distributions.
4. **Split**: put a test set aside **before** anything else (Lecture 04).
5. **Prepare**: scale, encode and impute, learning only from the training data (08–10).
6. **Train** several models (12–19).
7. **Evaluate** with suitable metrics and cross-validation (05–07).
8. **Tune** hyperparameters (21).
9. **Final check** on the test set, **once**.
10. **Save and deploy** (24).

## Why scikit-learn?

| Strength | Meaning |
|----------|---------|
| **One consistent API** | every model has `fit` / `predict` / `score`, so switching models changes one line |
| **Batteries included** | preprocessing, models, metrics, cross-validation, tuning and pipelines in one library |
| **Excellent docs** | every class has a user guide with examples |
| **Production-ready** | stable, well-tested, used in industry |

What it's **not** for: deep learning on images and audio (use PyTorch or TensorFlow), or very large data that doesn't fit in memory (use Spark ML or Dask-ML).

## Exercises

1. Classify each as classification, regression or clustering: (a) predict a student's exam mark; (b) group songs by sound; (c) detect fraudulent transactions; (d) forecast tomorrow's electricity demand.
2. In `lecture.py`, change the hand-written rule and the learned model's training data. Which is easier to update when spam changes?
3. Create a NumPy array of shape `(5, 3)` and compute the mean of each column.

<details><summary>Answers</summary>

1. (a) regression, (b) clustering, (c) classification, (d) regression.
3. `np.arange(15).reshape(5, 3).mean(axis=0)` → `[6., 7., 8.]`
</details>

**Next →** [Lecture 01: Your first model](../01_first_model/)
