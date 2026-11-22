"""Lecture 28: scikit-learn self-test: 25 questions, each answer computed by running real code.

Try to predict each answer before reading the line printed after it.
"""
import warnings

import numpy as np
from sklearn.base import clone
from sklearn.cluster import KMeans
from sklearn.datasets import load_breast_cancer, load_iris, load_wine, make_classification
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression
from sklearn.metrics import precision_score, r2_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")
QUESTIONS = []


def question(text):
    def register(func):
        QUESTIONS.append((text, func))
        return func
    return register


X_iris, y_iris = load_iris(return_X_y=True)
X_wine, y_wine = load_wine(return_X_y=True)


@question("What does model.fit(X, y) return?")
def q01():
    m = LinearRegression()
    return "the model itself" if m.fit([[1], [2]], [1, 2]) is m else "?"


@question("LinearRegression().fit([1, 2, 3], [1, 2, 3]) raises ... ?")
def q02():
    try:
        LinearRegression().fit([1, 2, 3], [1, 2, 3])
    except ValueError as e:
        return "ValueError: " + str(e).splitlines()[0]


@question("Calling predict on a model that was never fitted raises ... ?")
def q03():
    try:
        LogisticRegression().predict([[1, 2]])
    except NotFittedError:
        return "NotFittedError"


@question("Learned attributes (like coef_) are recognisable because they ...")
def q04():
    m = LinearRegression().fit([[1], [2]], [1, 2])
    return "end with an underscore: " + ", ".join(a for a in vars(m) if a.endswith("_") and not a.startswith("_"))


@question("Does clone(fitted_model) return a fitted model?")
def q05():
    m = LogisticRegression().fit(X_iris, y_iris)
    return hasattr(clone(m), "coef_")


@question("train_test_split returns its four arrays in which order?")
def q06():
    a, b, c, d = train_test_split(X_iris, y_iris, random_state=0)
    return [name for name, arr in zip(["X_train", "X_test", "y_train", "y_test"], [a, b, c, d])], (a.ndim, b.ndim, c.ndim, d.ndim)


@question("Unlimited-depth tree on breast cancer: training accuracy?")
def q07():
    X, y = load_breast_cancer(return_X_y=True)
    return DecisionTreeClassifier(random_state=0).fit(X, y).score(X, y)


@question("On 95/5 imbalanced data, the accuracy of DummyClassifier(most_frequent) is about ... ?")
def q08():
    X, y = make_classification(n_samples=2000, weights=[0.95, 0.05], random_state=0)
    return round(DummyClassifier().fit(X, y).score(X, y), 2)


@question("y_true=[1,1,1,0], y_pred=[1,0,0,0]: precision and recall for class 1?")
def q09():
    return precision_score([1, 1, 1, 0], [1, 0, 0, 0]), round(recall_score([1, 1, 1, 0], [1, 0, 0, 0]), 3)


@question("R2 of always predicting the mean of y?")
def q10():
    y = np.array([3.0, 5.0, 9.0, 11.0])
    return r2_score(y, np.full(4, y.mean()))


@question("Error metrics in cross_val_score are named neg_... because scikit-learn always ...")
def q11():
    s = cross_val_score(LinearRegression(), X_iris[:, :3], X_iris[:, 3], cv=3, scoring="neg_mean_absolute_error")
    return f"maximises scores (values are negative: {s.mean():.3f})"


@question("For a classifier, cv=5 uses which splitter by default?")
def q12():
    from sklearn.model_selection import check_cv
    return type(check_cv(5, y_iris, classifier=True)).__name__


@question("Fit StandardScaler on train=[10, 20, 30]; transform test=[40]. Result?")
def q13():
    return StandardScaler().fit([[10], [20], [30]]).transform([[40]]).round(2).item()


@question("KNN on wine: unscaled vs scaled CV accuracy?")
def q14():
    return (round(float(cross_val_score(KNeighborsClassifier(), X_wine, y_wine, cv=5).mean()), 3),
            round(float(cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier()), X_wine, y_wine, cv=5).mean()), 3))


@question("OneHotEncoder(handle_unknown='ignore') on an unseen category returns ... ?")
def q15():
    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit([["Pune"], ["Delhi"]])
    return enc.transform([["Goa"]]).tolist()


@question("OrdinalEncoder() default category order for ['S', 'M', 'L']?")
def q16():
    return OrdinalEncoder().fit([["S"], ["M"], ["L"]]).categories_[0].tolist()


@question("SimpleImputer(strategy='median') on [1, 2, NaN, 100] fills the NaN with ... ?")
def q17():
    return float(SimpleImputer(strategy="median").fit_transform([[1], [2], [np.nan], [100]])[2, 0])


@question("Small C in LogisticRegression/SVC means ... regularisation?")
def q18():
    X, y = load_breast_cancer(return_X_y=True)
    small = np.abs(make_pipeline(StandardScaler(), LogisticRegression(C=0.001)).fit(X, y)[-1].coef_).sum()
    big = np.abs(make_pipeline(StandardScaler(), LogisticRegression(C=100, max_iter=5000)).fit(X, y)[-1].coef_).sum()
    return f"STRONG (sum |coef| {small:.1f} vs {big:.1f} for C=100)"


@question("Which penalised linear model can set coefficients to exactly 0?")
def q19():
    from sklearn.datasets import load_diabetes
    X, y = load_diabetes(return_X_y=True)
    zeros = int(np.sum(make_pipeline(StandardScaler(), Lasso(alpha=10)).fit(X, y)[-1].coef_ == 0))
    return f"Lasso ({zeros} of 10 coefficients are 0 at alpha=10)"


@question("Do random forests need feature scaling?")
def q20():
    X, y = load_breast_cancer(return_X_y=True)
    a = cross_val_score(RandomForestClassifier(n_estimators=50, random_state=0), X, y, cv=3).mean()
    b = cross_val_score(make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=50, random_state=0)), X, y, cv=3).mean()
    return f"no (same score: {a:.3f} vs {b:.3f})"


@question("In a pipeline named ('scale', ...), ('svc', SVC()), how do you name C in a grid?")
def q21():
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC
    pipe = Pipeline([("scale", StandardScaler()), ("svc", SVC())])
    return "svc__C" if "svc__C" in pipe.get_params() else "?"


@question("GridSearchCV over 4 values of C and 3 of gamma with cv=5: how many fits (refit excluded)?")
def q22():
    return 4 * 3 * 5


@question("Does KMeans inertia_ always decrease as k grows?")
def q23():
    X = StandardScaler().fit_transform(X_iris)
    inertias = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_ for k in range(1, 7)]
    return bool(np.all(np.diff(inertias) < 0)), "-> so pick the elbow, not the minimum"


@question("How many PCA components keep 95% of the variance of scaled wine (13 features)?")
def q24():
    return int(PCA(n_components=0.95).fit(StandardScaler().fit_transform(X_wine)).n_components_)


@question("Should you choose the decision threshold using the test set?")
def q25():
    return "No: choose it on training/validation (e.g. out-of-fold) predictions; use the test set once"


def main():
    print(f"scikit-learn self-test: {len(QUESTIONS)} questions (answers computed by running the code)\n")
    for number, (text, func) in enumerate(QUESTIONS, start=1):
        print(f"Q{number:02d}. {text}")
        print(f"     -> {func()!r}\n")
    assert len(QUESTIONS) == 25
    print("If an answer surprised you, revisit the matching lecture (see the README sections).")


if __name__ == "__main__":
    main()
