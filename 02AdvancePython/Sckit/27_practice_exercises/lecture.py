"""Lecture 27: Checker for the scikit-learn practice exercises.

    python lecture.py             -> checks solutions.py (should be 20/20)
    python lecture.py exercises   -> checks YOUR exercises.py

Expected answers are computed here independently, so the checker does not trust either file.
"""
import importlib
import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris, load_wine, make_blobs
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
target = sys.argv[1] if len(sys.argv) > 1 else "solutions"
m = importlib.import_module(target)

X_iris, y_iris = load_iris(return_X_y=True)
X_wine, y_wine = load_wine(return_X_y=True)
X_cancer, y_cancer = load_breast_cancer(return_X_y=True)
X_diab, y_diab = load_diabetes(return_X_y=True)


def expect(what, actual, expected):
    if isinstance(expected, float) or isinstance(actual, (float, np.floating)):
        ok = actual is not None and np.isclose(float(actual), float(expected), atol=1e-6)
    elif isinstance(expected, np.ndarray):
        ok = actual is not None and np.shape(actual) == expected.shape and np.allclose(np.asarray(actual, dtype=float), expected)
    else:
        ok = actual == expected
    if not ok:
        shown = actual if not isinstance(actual, np.ndarray) or actual.size < 8 else f"array of shape {actual.shape}"
        raise AssertionError(f"{what}: got {shown!r}, expected {expected if not isinstance(expected, np.ndarray) or expected.size < 8 else 'array of shape ' + str(expected.shape)!r}")


def check_01():
    expect("iris_shapes()", m.iris_shapes(), ((150, 4), (150,)))


def check_02():
    out = m.to_column([1, 2, 3])
    expect("to_column([1, 2, 3]).shape", getattr(out, "shape", None), (3, 1))
    expect("values", out, np.array([[1.0], [2.0], [3.0]]))


def check_03():
    X = [[1, 4], [2, 5], [3, 6], [6, 7], [8, 6], [9, 8]]
    y = [0, 0, 0, 1, 1, 1]
    expect("fit_predict_tree(...)", m.fit_predict_tree(X, y, [[2, 7], [7, 5]]), np.array([0, 1]))


def check_04():
    out = m.split_data(X_iris, y_iris)
    if out is None or len(out) != 4:
        raise AssertionError("split_data must return 4 arrays")
    X_tr, X_te, y_tr, y_te = out
    expect("X_train shape", X_tr.shape, (120, 4))
    expect("X_test shape", X_te.shape, (30, 4))
    expect("stratified test counts per class", np.bincount(y_te).tolist(), [10, 10, 10])


def check_05():
    expect("accuracy_by_hand", m.accuracy_by_hand([1, 0, 1, 1], [1, 1, 1, 0]), 0.5)


def check_06():
    p, r = m.precision_recall([1, 0, 1, 1, 0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 0, 1, 1, 0, 1, 1]) or (None, None)
    expect("precision", p, 5 / 6)
    expect("recall", r, 5 / 6)


def check_07():
    expect("rmse([3, 5], [1, 5])", m.rmse([3, 5], [1, 5]), float(np.sqrt(2)))


def check_08():
    tr, te = m.scale_train_test(np.array([[10.0], [20.0], [30.0]]), np.array([[40.0]])) or (None, None)
    expect("scaled train", tr, np.array([[-1.224745], [0.0], [1.224745]]))
    expect("scaled test (with TRAIN mean/std)", te, np.array([[2.449490]]))


def check_09():
    df = pd.DataFrame({"city": ["Pune", "Delhi", "Pune"]})
    expect("one_hot(df, 'city')", m.one_hot(df, "city"), np.array([[0.0, 1.0], [1.0, 0.0], [0.0, 1.0]]))


def check_10():
    X = np.array([[1.0, 10.0], [np.nan, 20.0], [3.0, np.nan], [100.0, 40.0]])
    expect("impute_median", m.impute_median(X), np.array([[1.0, 10.0], [3.0, 20.0], [3.0, 20.0], [100.0, 40.0]]))


def check_11():
    from sklearn.model_selection import cross_val_score
    model = LogisticRegression(max_iter=1000)
    expect("cv_mean_accuracy(logistic, iris)", m.cv_mean_accuracy(model, X_iris, y_iris),
           float(cross_val_score(LogisticRegression(max_iter=1000), X_iris, y_iris, cv=5).mean()))


def check_12():
    out = m.slope_intercept([1, 2, 3, 4], [3, 5, 7, 9])
    if out is None:
        raise AssertionError("slope_intercept returned None")
    expect("slope", out[0], 2.0)
    expect("intercept", out[1], 1.0)


def check_13():
    pipe = m.make_scaled_knn(7)
    expect("is a Pipeline", isinstance(pipe, Pipeline), True)
    expect("first step is StandardScaler", isinstance(pipe.steps[0][1], StandardScaler), True)
    expect("last step n_neighbors", pipe.steps[-1][1].get_params().get("n_neighbors"), 7)
    expect("unfitted", hasattr(pipe.steps[0][1], "mean_"), False)


def check_14():
    from sklearn.model_selection import cross_val_score
    from sklearn.neighbors import KNeighborsClassifier
    ks = [1, 5, 9, 25, 101]
    scores = [cross_val_score(Pipeline([("s", StandardScaler()), ("k", KNeighborsClassifier(n_neighbors=k))]),
                              X_wine, y_wine, cv=5).mean() for k in ks]
    expect("best_k on wine", m.best_k(X_wine, y_wine, ks), ks[int(np.argmax(scores))])


def check_15():
    expect("count_lasso_zeros(diabetes, alpha=10)", m.count_lasso_zeros(X_diab, y_diab, 10), 6)
    expect("count_lasso_zeros(diabetes, alpha=0.01)", m.count_lasso_zeros(X_diab, y_diab, 0.01), 0)


def check_16():
    X = np.array([[0.5], [1], [1.5], [2], [3], [3.5], [4], [5]])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    clf = LogisticRegression().fit(X, y)
    expect("threshold 0.5", m.predict_with_threshold(clf, [[1], [2.5], [4]], 0.5), np.array([0, 0, 1]))
    expect("threshold 0.4", m.predict_with_threshold(clf, [[1], [2.5], [4]], 0.4), np.array([0, 1, 1]))


def check_17():
    df = pd.DataFrame({"age": [20, np.nan, 40, 30], "income": [1, 2, 3, 4], "city": ["A", "B", "A", "C"], "id": [1, 2, 3, 4]})
    prep = m.build_preprocessor(["age", "income"], ["city"])
    out = prep.fit_transform(df)
    out = out.toarray() if hasattr(out, "toarray") else np.asarray(out)
    expect("output shape (2 numeric + 3 cities, id dropped)", out.shape, (4, 5))
    expect("missing age imputed with the median then scaled (row 1 age)", round(float(out[1, 0]), 4), 0.0)
    new = prep.transform(pd.DataFrame({"age": [25], "income": [2], "city": ["Z"], "id": [9]}))
    new = new.toarray() if hasattr(new, "toarray") else np.asarray(new)
    expect("unknown city -> all zeros", new[0, 2:].tolist(), [0.0, 0.0, 0.0])


def check_18():
    from sklearn.model_selection import GridSearchCV
    pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=5000))])
    ref = GridSearchCV(pipe, {"clf__C": [0.01, 0.1, 1, 10]}, cv=5).fit(X_cancer, y_cancer).best_params_["clf__C"]
    expect("best_C on breast cancer", m.best_C(X_cancer, y_cancer), ref)


def check_19():
    X, truth = make_blobs(n_samples=200, centers=3, cluster_std=0.5, random_state=1)
    labels = m.kmeans_labels(X, 3)
    expect("number of labels", len(labels), 200)
    expect("clusters match the true blobs (ARI)", round(adjusted_rand_score(truth, labels), 3), 1.0)


def check_20():
    expect("components for 95% of scaled wine", int(m.components_for_variance(X_wine, 0.95)), 10)
    expect("components for 80% of scaled wine", int(m.components_for_variance(X_wine, 0.80)), 5)


TITLES = ["iris shapes", "2-D column", "fit & predict", "stratified split", "accuracy by hand",
          "precision & recall", "RMSE", "scale train/test", "one-hot", "median impute",
          "cross-validation", "linear slope", "pipeline", "tune k", "Lasso zeros",
          "custom threshold", "ColumnTransformer", "GridSearchCV", "KMeans", "PCA variance"]
CHECKS = [globals()[f"check_{i:02d}"] for i in range(1, 21)]

print(f"Checking {target}.py\n")
score = 0
for num, (title, check) in enumerate(zip(TITLES, CHECKS), start=1):
    try:
        check()
    except Exception as e:
        kind = "" if isinstance(e, AssertionError) else type(e).__name__ + ": "
        print(f"  ✘ {num:02d} {title:<19} {kind}{str(e).splitlines()[0][:110] if str(e) else ''}")
    else:
        score += 1
        print(f"  ✔ {num:02d} {title}")
print(f"\n  Score: {score} / {len(CHECKS)}")

if target == "solutions" and score != len(CHECKS):
    sys.exit(1)
