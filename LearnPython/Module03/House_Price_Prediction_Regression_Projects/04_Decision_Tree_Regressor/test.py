"""
Evaluate the saved model using the separate test_data.csv.
Run train.py first, then: python test.py
"""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "house_price_model.joblib"
TEST_FILE = BASE_DIR / "test_data.csv"
OUTPUT_FILE = BASE_DIR / "test_predictions.csv"

def main():
    if not MODEL_FILE.exists():
        raise SystemExit("Model not found. Run: python train.py")

    saved = joblib.load(MODEL_FILE)
    model = saved["model"]
    features = saved["features"]

    data = pd.read_csv(TEST_FILE)
    X = data[features]
    actual = data["price_lakh"]
    predicted = model.predict(X)

    result = data.copy()
    result["predicted_price_lakh"] = predicted.round(2)
    result["error_lakh"] = (actual - predicted).round(2)
    result.to_csv(OUTPUT_FILE, index=False)
    result["absolute_error_lakh"] = (
    actual - predicted
).abs().round(2)

    rmse = mean_squared_error(actual, predicted) ** 0.5
    print("\nTEST RESULTS")
    print(f"Rows tested: {len(data)}")
    print(f"MAE : {mean_absolute_error(actual, predicted):.2f} lakh")
    print(f"RMSE: {rmse:.2f} lakh")
    print(f"R²  : {r2_score(actual, predicted):.4f}")
    print("\nFirst 10 predictions:")
    print(result[["price_lakh", "predicted_price_lakh", "error_lakh", "absolute_error_lakh"]].head(10).to_string(index=False))
    print(f"\nFull predictions saved to: {OUTPUT_FILE.name}")

if __name__ == "__main__":
    main()
