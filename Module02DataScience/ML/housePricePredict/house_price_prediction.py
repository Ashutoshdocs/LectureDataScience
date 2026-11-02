"""
House Price Prediction - Beginner ML Demo
Run: python house_price_prediction.py

This demo uses a small sample dataset, trains a Linear Regression model,
evaluates it, and predicts the price for a new house.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def main():
    # 1. Sample dataset (area in square feet, bedrooms, age in years)
    data = {
        "area_sqft": [650, 800, 900, 1000, 1100, 1200, 1300, 1400,
                      1500, 1600, 1700, 1800, 1900, 2000, 2200, 2400],
        "bedrooms":  [1, 2, 2, 2, 2, 3, 3, 3,
                      3, 3, 3, 3, 4, 4, 4, 4],
        "age_years": [20, 15, 12, 10, 8, 10, 7, 6,
                      5, 8, 4, 3, 6, 4, 2, 1],
        # Illustrative prices in lakh rupees (₹ lakh)
        "price_lakh": [28, 35, 39, 43, 47, 50, 56, 60,
                       65, 67, 73, 78, 79, 88, 98, 110],
    }
    df = pd.DataFrame(data)

    print("\n=== HOUSE PRICE PREDICTION ===")
    print("\n1. Sample data:")
    print(df.head())

    # 2. Separate input features (X) and target (y)
    X = df[["area_sqft", "bedrooms", "age_years"]]
    y = df["price_lakh"]

    # 3. Split data: keep some rows aside to test the model
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # 4. Train the machine-learning model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5. Evaluate model predictions on test data
    test_predictions = model.predict(X_test)
    print("\n2. Model evaluation:")
    print(f"Mean Absolute Error: {mean_absolute_error(y_test, test_predictions):.2f} lakh")
    print(f"R² score: {r2_score(y_test, test_predictions):.2f}")

    # 6. Predict the price of a new house
    new_house = pd.DataFrame([{
        "area_sqft": 1500,
        "bedrooms": 3,
        "age_years": 5,
    }])
    predicted_price = model.predict(new_house)[0]

    print("\n3. New house details:")
    print(new_house.to_string(index=False))
    print(f"\nPredicted house price: ₹{predicted_price:.2f} lakh")

    # 7. Explain the learned relationship
    print("\n4. Model coefficients:")
    for feature, coefficient in zip(X.columns, model.coef_):
        print(f"{feature}: {coefficient:.3f}")
    print(f"Intercept: {model.intercept_:.3f}")

    print("\nDemo complete.")
    print("Note: This is a teaching dataset, not a real property valuation model.")


if __name__ == "__main__":
    main()
