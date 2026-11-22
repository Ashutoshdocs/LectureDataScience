"""Lecture 24: joblib save/load with metadata; FunctionTransformer; custom BaseEstimator+TransformerMixin;
clone/grid search compatibility; a custom classifier."""
import json
import pathlib
import tempfile

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin, clone
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.utils.validation import check_is_fitted

tmp = pathlib.Path(tempfile.mkdtemp())

print("=== 1. Save and load a whole pipeline ===")
X, y = load_breast_cancer(return_X_y=True)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
path = tmp / "cancer_model.joblib"
joblib.dump(pipe, path, compress=3)
meta = {"sklearn_version": sklearn.__version__, "trained_on_rows": len(X), "n_features": X.shape[1],
        "cv_accuracy": round(float(cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), X, y, cv=5).mean()), 4)}
(tmp / "cancer_model.json").write_text(json.dumps(meta, indent=2))
print(f"  saved {path.name} ({path.stat().st_size / 1024:.1f} KB) + metadata {meta}")
loaded = joblib.load(path)
print("  loaded:", loaded)
print("  identical predictions:", bool((loaded.predict(X) == pipe.predict(X)).all()))
print("  the scaler came along:", loaded[0].mean_[:3].round(2))

print("\n=== 2. FunctionTransformer for stateless steps ===")


def add_ratios(df):
    df = df.copy()
    df["price_per_m2"] = df["price"] / df["area"]
    df["rooms_per_100m2"] = df["rooms"] / df["area"] * 100
    return df


flats = pd.DataFrame({"price": [60, 90, 150], "area": [50, 80, 100], "rooms": [2, 3, 4]})
ratio_step = FunctionTransformer(add_ratios)
print(ratio_step.fit_transform(flats).round(2).to_string(index=False))
log_step = FunctionTransformer(np.log1p, inverse_func=np.expm1, feature_names_out="one-to-one")
print("  log1p step names out:", log_step.fit(flats).get_feature_names_out().tolist())
try:
    joblib.dump(FunctionTransformer(lambda d: d * 2), tmp / "lambda.joblib")
except Exception as e:
    print("  saving a lambda fails ->", type(e).__name__, "(use a named function instead)")


print("\n=== 3. A custom transformer that learns during fit ===")


class OutlierClipper(BaseEstimator, TransformerMixin):
    """Clip each column to quantiles learned from the training data."""

    def __init__(self, lower=0.01, upper=0.99):
        self.lower = lower
        self.upper = upper

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        self.low_ = np.quantile(X, self.lower, axis=0)
        self.high_ = np.quantile(X, self.upper, axis=0)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self)
        X = np.asarray(X, dtype=float)
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"expected {self.n_features_in_} features, got {X.shape[1]}")
        return np.clip(X, self.low_, self.high_)

    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features if input_features is not None else [f"x{i}" for i in range(self.n_features_in_)], dtype=object)


train = np.array([[1.0], [2.0], [3.0], [4.0], [100.0]])
clipper = OutlierClipper(lower=0.0, upper=0.75)
print("  fit_transform (free from TransformerMixin):", clipper.fit_transform(train).ravel())
print("  learned high_:", clipper.high_, "| new data [[50], [2]] ->", clipper.transform([[50], [2]]).ravel())
print("  repr from BaseEstimator:", clipper)
print("  get_params:", clipper.get_params())
try:
    OutlierClipper().transform(train)
except NotFittedError as e:
    print("  before fit ->", type(e).__name__)

print("\n=== 4. It works with clone, pipelines and GridSearchCV ===")
print("  clone:", clone(clipper), "| clone is fitted?", hasattr(clone(clipper), "low_"))
Xd, yd = load_diabetes(return_X_y=True)
Xd_out = Xd.copy()
Xd_out[::25, 2] = 5.0                                      # inject extreme bmi outliers
search = GridSearchCV(make_pipeline(OutlierClipper(), LinearRegression()),
                      {"outlierclipper__upper": [0.9, 0.99, 1.0]}, cv=5).fit(Xd_out, yd)
for upper, s in zip([0.9, 0.99, 1.0], search.cv_results_["mean_test_score"]):
    print(f"  upper={upper:<4} CV R2 {s:.3f}")
print("  best:", search.best_params_, "-> clipping outliers helps")
joblib.dump(search.best_estimator_, tmp / "with_custom_step.joblib")
print("  pipeline with the custom step saved and reloaded:", type(joblib.load(tmp / "with_custom_step.joblib")[0]).__name__)

print("\n=== 5. A custom classifier (ClassifierMixin gives score for free) ===")


class NearestCentroid(BaseEstimator, ClassifierMixin):
    """Predict the class whose average training point is closest."""

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y)
        self.classes_ = np.unique(y)
        self.centroids_ = np.array([X[y == c].mean(axis=0) for c in self.classes_])
        return self

    def predict(self, X):
        check_is_fitted(self)
        d = np.linalg.norm(np.asarray(X, dtype=float)[:, None, :] - self.centroids_[None], axis=2)
        return self.classes_[np.argmin(d, axis=1)]


print(f"  NearestCentroid in a pipeline, CV accuracy {cross_val_score(make_pipeline(StandardScaler(), NearestCentroid()), X, y, cv=5).mean():.3f}")
print(f"  .score() from ClassifierMixin: {make_pipeline(StandardScaler(), NearestCentroid()).fit(X, y).score(X, y):.3f}")
