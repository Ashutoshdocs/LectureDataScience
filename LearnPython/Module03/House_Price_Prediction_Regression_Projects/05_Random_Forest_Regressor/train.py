"""
Random Forest Regressor - House Price Prediction
Run: python train.py
"""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "training_data.csv"
MODEL_FILE = BASE_DIR / "house_price_model.joblib"
METRICS_FILE = BASE_DIR / "training_metrics.json"

FEATURES = ['area_sqft', 'bedrooms', 'bathrooms', 'age_years', 'distance_to_city_km', 'location_score']
TARGET = "price_lakh"

def main():
    data = pd.read_csv(DATA_FILE)
    X = data[FEATURES]
    y = data[TARGET]

    # Keep a validation split aside to measure how well the model generalizes.
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = RandomForestRegressor(n_estimators=150, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    predictions = model.predict(X_valid)
    rmse = mean_squared_error(y_valid, predictions) ** 0.5
    metrics = {
        "model": "Random Forest Regressor",
        "validation_rows": int(len(y_valid)),
        "MAE_lakh": round(float(mean_absolute_error(y_valid, predictions)), 3),
        "RMSE_lakh": round(float(rmse), 3),
        "R2": round(float(r2_score(y_valid, predictions)), 4)
    }

    # Refit using all supplied training rows before saving the final model.
    model.fit(X, y)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_FILE)
    METRICS_FILE.write_text(json.dumps(metrics, indent=4))

    print("\nTraining completed!")
    print(f"Model saved: {MODEL_FILE.name}")
    print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    main()
