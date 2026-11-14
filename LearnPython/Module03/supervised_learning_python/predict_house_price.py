"""
Predict a house price using the saved supervised learning model.

Run:
    python predict_house_price.py

Train the model first with:
    python train_model.py
"""

from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "house_price_model.joblib"


def main():
    if not MODEL_FILE.exists():
        print("Trained model not found. Run: python train_model.py")
        return

    saved = joblib.load(MODEL_FILE)
    model = saved["model"]
    features = saved["features"]

    try:
        area = float(input("Enter house area in square feet: "))
        bedrooms = float(input("Enter number of bedrooms: "))

        if area <= 0 or bedrooms <= 0:
            raise ValueError("Area and bedroom count must be greater than zero.")

        new_house = pd.DataFrame(
            [[area, bedrooms]],
            columns=features,
        )

        predicted_price = model.predict(new_house)[0]

        print("\n========== PREDICTION ==========")
        print(f"Area: {area:,.0f} sq ft")
        print(f"Bedrooms: {bedrooms:g}")
        print(f"Estimated price: {predicted_price:.2f} lakh")
        print("\nThis is a teaching-model estimate, not a real property valuation.")

    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
