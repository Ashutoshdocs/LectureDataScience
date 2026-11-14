# Gradient Boosting Regressor — House Price Prediction

## 1. What this project teaches

Builds small trees sequentially; each new tree learns to reduce earlier prediction errors.

**Target:** `price_lakh` (house price in Indian lakh rupees).

## 2. Files in this folder

| File | Purpose |
|---|---|
| `train.py` | Loads training data, trains the regression model, evaluates a validation split and saves the model |
| `test.py` | Loads the saved model, predicts prices for unseen test rows and calculates test metrics |
| `training_data.csv` | Example labelled data used to train the model |
| `test_data.csv` | Separate labelled data used only for final evaluation |
| `diagram.png` | Visual explanation of the training and testing flow |

The scripts also create `house_price_model.joblib`, `training_metrics.json`, and `test_predictions.csv` after you run them.

## 3. Features used

- `area_sqft`
- `bedrooms`
- `bathrooms`
- `age_years`
- `distance_to_city_km`
- `location_score`

- Target column: `price_lakh`
- Dataset is synthetic and intended for learning. It is not a source of real property valuations.

## 4. Install Python libraries

Use Python 3.9 or newer.

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install pandas scikit-learn joblib
```

## 5. Run the project

Run these commands from this folder:

```bash
python train.py
python test.py
```

**Important:** Run `train.py` before `test.py`. The training script creates the saved model file that the test script loads.

## 6. Understand the output

- **MAE:** average absolute prediction error, in lakh. Lower is better.
- **RMSE:** penalizes large errors more strongly, in lakh. Lower is better.
- **R²:** proportion of target variation explained by the model. Closer to 1 is generally better; it can be negative on poor predictions.

`test.py` writes `test_predictions.csv`, containing actual price, predicted price and prediction error for every test row.

## 7. Add your own data

1. Make a backup of the CSV files.
2. Add rows to `training_data.csv` using the same column names and numeric formats.
3. Keep `test_data.csv` separate. Do not use the test rows to train the model.
4. Make sure every feature listed above and `price_lakh` is present.
5. Run `python train.py` again, followed by `python test.py`.
6. Compare MAE, RMSE and R² before and after your changes.

For a fair experiment, keep the test dataset unchanged while changing the training dataset. If you change the feature columns, update `FEATURES` in `train.py` and keep the same feature names in the test CSV.

## 8. What to observe

- More representative training examples can improve generalization.
- Incorrect or inconsistent values can reduce model quality.
- A model can perform well on training/validation data but poorly on genuinely new test data.
- Compare this project's metrics with the other five regression projects using the same CSV datasets.

## 9. Model idea

Each new learner corrects part of the previous model's remaining error

Open `diagram.png` to see the project flow.
