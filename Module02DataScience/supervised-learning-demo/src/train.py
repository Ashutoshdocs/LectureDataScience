"""
Step 3 - Train and compare several supervised models.

What happens:
  1. Load data, split into train (80%) / test (20%) with stratification.
  2. Build a preprocessing pipeline (impute -> scale numeric, one-hot categorical).
  3. Compare 3 models with 5-fold cross-validation on the TRAIN set only.
  4. Tune the best model with GridSearchCV.
  5. Save the final pipeline + the untouched test set.

Run:  python src/train.py
"""
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import (CATEGORICAL_FEATURES, DATA_PATH, FEATURES, MODEL_DIR, MODEL_PATH,
                    NUMERIC_FEATURES, RANDOM_STATE, TARGET, TEST_SET_PATH, TEST_SIZE)


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("num", numeric, NUMERIC_FEATURES),
        ("cat", categorical, CATEGORICAL_FEATURES),
    ])


CANDIDATES = {
    "logistic_regression": (
        LogisticRegression(max_iter=1000),
        {"model__C": [0.01, 0.1, 1, 10]},
    ),
    "random_forest": (
        RandomForestClassifier(random_state=RANDOM_STATE),
        {"model__n_estimators": [200, 400], "model__max_depth": [None, 6, 10],
         "model__min_samples_leaf": [1, 5]},
    ),
    "gradient_boosting": (
        GradientBoostingClassifier(random_state=RANDOM_STATE),
        {"model__n_estimators": [100, 200], "model__learning_rate": [0.05, 0.1],
         "model__max_depth": [2, 3]},
    ),
}


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    X, y = df[FEATURES], df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE)
    print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows\n")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # --- Compare baseline models -------------------------------------------
    print("=== 5-fold CV ROC-AUC (train set) ===")
    cv_scores = {}
    for name, (estimator, _) in CANDIDATES.items():
        pipe = Pipeline([("prep", build_preprocessor()), ("model", estimator)])
        scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc")
        cv_scores[name] = scores.mean()
        print(f"{name:<22} {scores.mean():.4f} ± {scores.std():.4f}")

    best_name = max(cv_scores, key=cv_scores.get)
    print(f"\nBest baseline: {best_name}\n")

    # --- Tune the winner ---------------------------------------------------
    estimator, grid = CANDIDATES[best_name]
    pipe = Pipeline([("prep", build_preprocessor()), ("model", estimator)])
    search = GridSearchCV(pipe, grid, cv=cv, scoring="roc_auc", n_jobs=-1)
    search.fit(X_train, y_train)
    print(f"Best params: {search.best_params_}")
    print(f"Tuned CV ROC-AUC: {search.best_score_:.4f}")

    # --- Save --------------------------------------------------------------
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"name": best_name, "pipeline": search.best_estimator_}, MODEL_PATH)
    X_test.assign(**{TARGET: y_test}).to_csv(TEST_SET_PATH, index=False)
    print(f"\nSaved model -> {MODEL_PATH.name}, held-out test set -> {TEST_SET_PATH.name}")


if __name__ == "__main__":
    main()
