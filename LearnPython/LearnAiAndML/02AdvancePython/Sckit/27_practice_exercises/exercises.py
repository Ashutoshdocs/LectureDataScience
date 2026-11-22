"""scikit-learn practice: fill in each function, then run:  python lecture.py exercises

Each docstring says exactly what the checker tests. Replace `...` with your code.
Imports you may need are already here.
"""
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
    """01. Load iris and return (X.shape, y.shape) -> ((150, 4), (150,))."""
    ...


def to_column(values):
    """02. Turn a flat list like [1, 2, 3] into a 2-D NumPy array of shape (n, 1)."""
    ...


def fit_predict_tree(X, y, X_new):
    """03. Fit DecisionTreeClassifier(random_state=0) on X, y and return its predictions for X_new."""
    ...


def split_data(X, y):
    """04. Return train_test_split(X, y) with test_size=0.2, random_state=0 and stratify=y
    (the usual 4 outputs, in the usual order)."""
    ...


def accuracy_by_hand(y_true, y_pred):
    """05. Fraction of positions where y_true == y_pred, as a float (no sklearn metrics)."""
    ...


def precision_recall(y_true, y_pred):
    """06. Return (precision, recall) for class 1."""
    ...


def rmse(y_true, y_pred):
    """07. Root mean squared error."""
    ...


def scale_train_test(X_train, X_test):
    """08. Fit a StandardScaler on X_train ONLY; return (X_train_scaled, X_test_scaled)."""
    ...


def one_hot(df, column):
    """09. One-hot encode df[column] with OneHotEncoder(sparse_output=False).
    Return a dense NumPy array (one column per category, categories in sorted order)."""
    ...


def impute_median(X):
    """10. Fill NaNs in each column with that column's median; return the filled array."""
    ...


def cv_mean_accuracy(model, X, y):
    """11. Mean of 5-fold cross_val_score accuracy for model on X, y."""
    ...


def slope_intercept(x, y):
    """12. Fit LinearRegression on one feature (x is a flat list) and return (slope, intercept) as floats."""
    ...


def make_scaled_knn(k):
    """13. Return an UNFITTED Pipeline: StandardScaler followed by KNeighborsClassifier(n_neighbors=k)."""
    ...


def best_k(X, y, ks):
    """14. For each k in ks, compute the 5-fold CV accuracy of a scaled KNN; return the k with the
    highest mean (the first one if tied)."""
    ...


def count_lasso_zeros(X, y, alpha):
    """15. Fit StandardScaler + Lasso(alpha=alpha) on X, y; return how many coefficients are exactly 0."""
    ...


def predict_with_threshold(model, X, threshold):
    """16. model is a FITTED binary classifier. Return 1 where predict_proba(X)[:, 1] >= threshold, else 0 (int array)."""
    ...


def build_preprocessor(num_cols, cat_cols):
    """17. Return a ColumnTransformer: num_cols -> median SimpleImputer then StandardScaler;
    cat_cols -> OneHotEncoder(handle_unknown="ignore"). Unlisted columns are dropped."""
    ...


def best_C(X, y):
    """18. GridSearchCV (cv=5, accuracy) over C in [0.01, 0.1, 1, 10] for StandardScaler + LogisticRegression(max_iter=5000).
    Return the best C."""
    ...


def kmeans_labels(X, k):
    """19. Return the cluster labels from KMeans(n_clusters=k, n_init=10, random_state=0)."""
    ...


def components_for_variance(X, share):
    """20. Scale X with StandardScaler, then return how many PCA components are needed to keep `share`
    (e.g. 0.95) of the variance."""
    ...
