# Lecture 01: Your first model: create → fit → predict

Run: `python lecture.py`

## Every model follows the same three steps

```python
from sklearn.tree import DecisionTreeClassifier

# [hours studied, hours slept]  ->  1 = passed, 0 = failed
X = [[1, 4], [2, 5], [3, 6], [6, 7], [8, 6], [9, 8]]
y = [0, 0, 0, 1, 1, 1]

model = DecisionTreeClassifier(random_state=0)   # 1. choose and create a model
model.fit(X, y)                                  # 2. learn from examples
model.predict([[2, 7], [7, 5]])                  # 3. predict for new samples → array([0, 1])
```

| Step | What happens |
|------|--------------|
| **create** | an empty model object that stores only its **settings** (hyperparameters) |
| **`fit(X, y)`** | the algorithm studies the examples and stores what it learned **inside the object** |
| **`predict(X_new)`** | applies the learned rule to new rows and returns a NumPy array of answers |

## Vocabulary

| Word | Meaning | In the example |
|------|---------|----------------|
| **sample** (row, observation) | one example | one student |
| **feature** (column, variable) | one measurement about a sample | hours studied, hours slept |
| **X** (feature matrix) | all features, rows × columns, **always 2-D** | 6 × 2 |
| **y** (target, label) | the answer for each row, **1-D** | pass / fail |
| **estimator** | scikit-learn's word for any object that learns from data | `DecisionTreeClassifier` |
| **training** | calling `fit` | |
| **inference / prediction** | calling `predict` | |

Convention: `X` is upper-case (a 2-D matrix) and `y` is lower-case (a 1-D vector).

## Swapping models is one line

Because every estimator shares the API, you can replace the tree with K-nearest neighbours, logistic regression or a random forest by changing only the import and the constructor line. `lecture.py` does exactly this for four models.

## Classifier vs regressor

The pattern is identical for regression. Only the type of `y` changes (numbers instead of categories), and you use a `...Regressor` or `LinearRegression`.

## Where do the learned rules live?

In attributes that **end with an underscore**, which exist only after `fit`: for example `classes_`, `n_features_in_`, `feature_importances_` and `coef_`. Lecture 03 covers this in depth.

## Common mistakes

| Mistake | Error |
|---------|-------|
| `model.predict([2, 7])` (single brackets) | `ValueError: Expected 2D array` → use `[[2, 7]]` |
| predicting before fitting | `NotFittedError` |
| X and y with different numbers of rows | `ValueError: Found input variables with inconsistent numbers of samples` |

## Exercises

1. Predict for a third student `[5, 5]`.
2. Replace the tree with `KNeighborsClassifier(n_neighbors=3)`.
3. Turn the problem into regression: make `y` the exam **mark** (e.g. `[35, 42, 50, 71, 80, 92]`) and use `LinearRegression`.
4. Print `model.classes_` and `model.n_features_in_`.

**Next →** [Lecture 02: Datasets, X and y](../02_datasets_X_and_y/)
