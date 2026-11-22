# Lecture 02: Datasets, X and y

Run: `python lecture.py`

## Built-in "toy" datasets (no download needed)

| Loader | Task | Samples × features | Target |
|--------|------|--------------------|--------|
| `load_iris` | classification (3 classes) | 150 × 4 | flower species |
| `load_wine` | classification (3 classes) | 178 × 13 | wine cultivar |
| `load_breast_cancer` | classification (2 classes) | 569 × 30 | malignant / benign |
| `load_digits` | classification (10 classes) | 1797 × 64 | handwritten digit 0–9 (8×8 pixels) |
| `load_diabetes` | regression | 442 × 10 | disease progression after one year |

> `fetch_california_housing`, `fetch_openml` and similar functions **download** bigger datasets the first time you use them. This course avoids them so everything runs offline.

## What a loader returns: a `Bunch`

```python
from sklearn.datasets import load_iris
iris = load_iris()
iris.data            # X: NumPy array (150, 4)
iris.target          # y: NumPy array (150,)
iris.feature_names   # column names
iris.target_names    # what 0, 1, 2 mean
iris.DESCR           # full description
```

Two handy options:

| Option | Returns |
|--------|---------|
| `return_X_y=True` | just the tuple `(X, y)` |
| `as_frame=True` | `X` as a pandas **DataFrame** and `y` as a **Series** (with column names) |

## Generated datasets: perfect for experiments

| Function | Makes |
|----------|-------|
| `make_classification(n_samples, n_features, n_informative, weights=...)` | classification data with controllable difficulty and imbalance |
| `make_regression(n_samples, n_features, noise)` | regression data with a known linear relationship |
| `make_blobs(n_samples, centers)` | round clusters (for clustering) |
| `make_moons`, `make_circles` | non-linear 2-D shapes (for trees, SVM kernels, DBSCAN) |

Always pass `random_state` to get the same data every run.

## Shapes: the rule that matters most

| | Shape | Type |
|--|-------|------|
| `X` | `(n_samples, n_features)` | 2-D: array, list of lists, DataFrame, sparse matrix |
| `y` | `(n_samples,)` | 1-D: array, list, Series |

They must have the **same number of rows**, and row *i* of `X` belongs to element *i* of `y`.

## Your own data (CSV → X, y)

```python
df = pd.read_csv("customers.csv")
X = df.drop(columns="churned")      # everything except the target
y = df["churned"]                   # the target
```

Always explore first: `df.shape`, `df.dtypes`, `df.isna().sum()`, `df.describe()`, `y.value_counts()`. Check **class balance** in classification problems: a 95/5 split changes how you evaluate (Lecture 05).

## Exercises

1. Load `load_wine(as_frame=True)` and print the number of samples per class.
2. Load the digits and print the 8×8 grid of the first image.
3. Make an imbalanced dataset with `make_classification(weights=[0.9, 0.1])` and check the counts.
4. Use `make_moons(noise=0.2)` and print the first five rows.

**Next →** [Lecture 03: The estimator API](../03_estimator_api/)
