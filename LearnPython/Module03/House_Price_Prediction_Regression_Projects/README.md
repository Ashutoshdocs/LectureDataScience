# House Price Prediction — Six Regression Projects

This ZIP contains six independent Python projects. Each project uses the same example house-price dataset so you can compare regression approaches fairly.

## Projects
1. Simple Linear Regression
2. Multiple Linear Regression
3. Polynomial Regression
4. Decision Tree Regressor
5. Random Forest Regressor
6. Gradient Boosting Regressor

## Quick start
Open any project folder, create/activate a virtual environment, then run:

```bash
python -m pip install pandas scikit-learn joblib
python train.py
python test.py
```

Run training before testing. See each folder's README.md for model-specific details.

## Dataset columns
- `area_sqft`: built-up area in square feet
- `bedrooms`: number of bedrooms
- `bathrooms`: number of bathrooms
- `age_years`: age of the property
- `distance_to_city_km`: distance to city centre in kilometres
- `location_score`: illustrative location score from 1 to 10
- `price_lakh`: example house price in lakh rupees (target)

The data is synthetic and for teaching only. It does not represent actual market prices.
