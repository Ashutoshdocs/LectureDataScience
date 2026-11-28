from pathlib import Path
import json
import logging

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, ConfusionMatrixDisplay
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "churn_training.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def main():
    df = pd.read_csv(INPUT_DIR / "customers.csv")
    target = "churn"

    # Separate model inputs from the target column.
    X = df.drop(columns=[target, "customer_id"])
    y = df[target]

    numeric_features = X.select_dtypes(include="number").columns.tolist()
    categorical_features = X.select_dtypes(exclude="number").columns.tolist()

    # Define independent preprocessing paths for numerical and categorical data.
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ])

    # Stratification preserves the churn/non-churn ratio in both partitions.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1500, random_state=42)),
    ])
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }

    # Save metrics, per-class report, predictions, and the full pipeline.
    (OUTPUT_DIR / "metrics.json").write_text(
        json.dumps(metrics, indent=4), encoding="utf-8"
    )
    (OUTPUT_DIR / "classification_report.txt").write_text(
        classification_report(y_test, predictions, zero_division=0),
        encoding="utf-8"
    )
    result = X_test.copy()
    result["actual_churn"] = y_test
    result["predicted_churn"] = predictions
    result["churn_probability"] = probabilities
    result.to_csv(OUTPUT_DIR / "predictions.csv", index=False)
    joblib.dump(model, OUTPUT_DIR / "churn_model.joblib")

    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(y_test, predictions, ax=ax, cmap="Blues")
    ax.set_title("Customer Churn — Confusion Matrix")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    logging.info("Churn model trained. Metrics: %s", metrics)
    print("Customer churn model evaluation:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
    print(f"Artifacts saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
