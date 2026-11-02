# House Price Prediction — 2-File Machine Learning Demo

A beginner-friendly, self-contained machine-learning practical using **Linear Regression**.

## Files

```text
house_price_ml_demo/
├── house_price_prediction.py
└── README.md
```

## What you will learn

1. What a dataset is and how rows/columns represent examples and features.
2. The difference between input features (`X`) and the target (`y`).
3. Why we split data into training and testing sets.
4. How a Linear Regression model learns from examples.
5. How to evaluate predictions using MAE and R².
6. How to predict the price of a new house.

## Scenario

We want to estimate a house's price using:

| Feature | Meaning |
|---|---|
| `area_sqft` | House area in square feet |
| `bedrooms` | Number of bedrooms |
| `age_years` | Age of the house |
| `price_lakh` | Known price; this is the target |

Prices are illustrative and expressed in **Indian lakh rupees**. The small dataset is embedded in the Python file, so no separate dataset download is required.

## 1. Create and activate a virtual environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```bash
python -m pip install pandas scikit-learn
```

## 3. Run the demo

```bash
python house_price_prediction.py
```

The program prints a sample of the data, model evaluation metrics, a prediction for a 1,500 sq. ft. three-bedroom house, and the model coefficients.

## Teaching flow

```text
Sample data
    |
    v
Select features (X) and target (y)
    |
    v
Split into training and testing data
    |
    v
Train Linear Regression on training data
    |
    v
Predict prices for test data
    |
    v
Evaluate with MAE and R²
    |
    v
Predict the price of a new house
```

## Explain these key lines

- `X = df[[...]]`: selects the information the model can use to make a prediction.
- `y = df["price_lakh"]`: selects the value the model must learn to predict.
- `train_test_split(...)`: keeps some examples aside so we can test the trained model on data it did not train on.
- `model.fit(X_train, y_train)`: trains the model.
- `model.predict(...)`: asks the trained model to estimate a price.
- **MAE**: average absolute prediction error, in lakh rupees. Lower is generally better.
- **R²**: indicates how well the model explains variation in the target on the test set. It can be negative; closer to 1 is generally better.

## Classroom exercises

1. Change the new house area from `1500` to `2000`. Does the prediction change?
2. Change the bedroom count from `3` to `4`.
3. Add more rows to the dataset and retrain.
4. Remove `age_years` from `X` and compare the evaluation metrics.
5. Discuss why a model trained on a tiny, artificial dataset should not be used to decide the real market value of a property.

## Important limitation

This is a teaching example, not a production valuation tool. Real house prices depend on location, locality, property condition, amenities, market conditions, legal status, and many other factors. A reliable model needs a much larger, representative, verified dataset and careful validation.
