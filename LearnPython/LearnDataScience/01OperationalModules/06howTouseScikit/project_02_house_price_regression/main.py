from pathlib import Path
import logging

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=LOG_DIR / "house_price_training.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def make_preprocessor(numeric_features, categorical_features):
    numeric = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("numeric", numeric, numeric_features),
        ("categorical", categorical, categorical_features),
    ])

def main():
    df = pd.read_csv(INPUT_DIR / "houses.csv")
    X = df.drop(columns=["sale_price", "property_id"])
    y = df["sale_price"]
    numeric_features = X.select_dtypes(include="number").columns.tolist()
    categorical_features = X.select_dtypes(exclude="number").columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    estimators = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=250, min_samples_leaf=2, random_state=42, n_jobs=-1
        ),
    }
    fitted = {}
    rows = []

    for name, estimator in estimators.items():
        pipeline = Pipeline([
            ("preprocessor", make_preprocessor(numeric_features, categorical_features)),
            ("model", estimator),
        ])
        pipeline.fit(X_train, y_train)
        prediction = pipeline.predict(X_test)
        mse = mean_squared_error(y_test, prediction)
        rows.append({
            "model": name,
            "mae": mean_absolute_error(y_test, prediction),
            "rmse": mse ** 0.5,
            "r2": r2_score(y_test, prediction),
        })
        fitted[name] = (pipeline, prediction)

    comparison = pd.DataFrame(rows).sort_values("mae")
    comparison.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)
    best_name = comparison.iloc[0]["model"]
    best_pipeline, best_prediction = fitted[best_name]
    joblib.dump(best_pipeline, OUTPUT_DIR / "best_house_price_model.joblib")

    result = X_test.copy()
    result["actual_price"] = y_test
    result["predicted_price"] = best_prediction
    result.to_csv(OUTPUT_DIR / "predictions.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(y_test, best_prediction, alpha=0.75)
    low = min(float(y_test.min()), float(best_prediction.min()))
    high = max(float(y_test.max()), float(best_prediction.max()))
    ax.plot([low, high], [low, high], linestyle="--",
            color="red", label="Perfect prediction")
    ax.set_title(f"Actual vs Predicted House Prices — {best_name}")
    ax.set_xlabel("Actual sale price")
    ax.set_ylabel("Predicted sale price")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "actual_vs_predicted.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    logging.info("House price models evaluated. Best model: %s", best_name)
    print(comparison.to_string(index=False))
    print(f"Best model: {best_name}")
    print(f"Artifacts saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
