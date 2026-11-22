"""Reference solutions for exercises.py."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


def iris_shapes():
    X, y = load_iris(return_X_y=True)
    return X.shape, y.shape


def to_column(values):
    return np.asarray(values).reshape(-1, 1)


def fit_predict_tree(X, y, X_new):
    return DecisionTreeClassifier(random_state=0).fit(X, y).predict(X_new)


def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)


def accuracy_by_hand(y_true, y_pred):
    return float(np.mean(np.asarray(y_true) == np.asarray(y_pred)))


def precision_recall(y_true, y_pred):
    return precision_score(y_true, y_pred), recall_score(y_true, y_pred)


def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def scale_train_test(X_train, X_test):
    scaler = StandardScaler().fit(X_train)
    return scaler.transform(X_train), scaler.transform(X_test)


def one_hot(df, column):
    return OneHotEncoder(sparse_output=False).fit_transform(df[[column]])


def impute_median(X):
    return SimpleImputer(strategy="median").fit_transform(X)


def cv_mean_accuracy(model, X, y):
    return cross_val_score(model, X, y, cv=5).mean()


def slope_intercept(x, y):
    m = LinearRegression().fit(np.asarray(x).reshape(-1, 1), y)
    return float(m.coef_[0]), float(m.intercept_)


def make_scaled_knn(k):
    return Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=k))])


def best_k(X, y, ks):
    scores = [cross_val_score(make_scaled_knn(k), X, y, cv=5).mean() for k in ks]
    return ks[int(np.argmax(scores))]


def count_lasso_zeros(X, y, alpha):
    pipe = make_pipeline(StandardScaler(), Lasso(alpha=alpha)).fit(X, y)
    return int(np.sum(pipe[-1].coef_ == 0))


def predict_with_threshold(model, X, threshold):
    return (model.predict_proba(X)[:, 1] >= threshold).astype(int)


def build_preprocessor(num_cols, cat_cols):
    numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    return ColumnTransformer([("num", numeric, num_cols),
                              ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)])


def best_C(X, y):
    pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=5000))])
    search = GridSearchCV(pipe, {"clf__C": [0.01, 0.1, 1, 10]}, cv=5).fit(X, y)
    return search.best_params_["clf__C"]


def kmeans_labels(X, k):
    return KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)


def components_for_variance(X, share):
    return PCA(n_components=share).fit(StandardScaler().fit_transform(X)).n_components_
