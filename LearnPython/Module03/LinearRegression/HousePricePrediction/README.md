# Supervised Learning in Python – House Price Prediction

A beginner-friendly, hands-on **supervised learning** demo using Python, Pandas, and Scikit-learn.

The project predicts a house price from two input features:

- `area_sqft` – house area in square feet
- `bedrooms` – number of bedrooms
- `price_lakh` – known house price in lakh (the target/label)

The model learns from labelled examples in `house_prices.csv`. You can add new rows, retrain the model, and compare how the evaluation result and predictions change.

## 1. Project structure

```text
supervised_learning_python/
├── README.md
├── house_prices.csv
├── train_model.py
└── predict_house_price.py
```

## 2. How supervised learning works

```text
        Labelled CSV data
   (area, bedrooms, known price)
                |
                v
        Load and inspect data
                |
                v
       Split into train/test data
          /              \
         v                v
   Train the model    Test the model
         \                /
          v              v
        Evaluate performance
                |
                v
       Save the trained model
                |
                v
     Predict price for new houses
```

- **Features (X):** `area_sqft`, `bedrooms`
- **Label/target (y):** `price_lakh`
- **Training:** the algorithm learns a relationship from examples.
- **Testing:** the model predicts prices for rows it did not train on.
- **Prediction:** use the saved model for a new house.

This is a regression task because the target is a numeric value.

## 3. Requirements

Python 3.9 or later is recommended.

Install the required packages:

```bash
python -m pip install pandas scikit-learn joblib
```

On some Linux systems, use `python3` and `pip3` instead.

## 4. Run the project

Open a terminal in this project folder.

### Step 1 – Train the model

```bash
python train_model.py
```

The script will:
1. Read `house_prices.csv`.
2. Validate the required columns and data.
3. Split the data into training and testing sets.
4. Train a Linear Regression model.
5. Display MAE, RMSE, and R² evaluation metrics.
6. Save the trained model as `house_price_model.joblib`.

The first run creates the model file automatically.

### Step 2 – Predict a house price

```bash
python predict_house_price.py
```

The script asks for the house area and bedroom count, then predicts the price in lakh.

Example input:

```text
Enter house area in square feet: 1500
Enter number of bedrooms: 3
```

The model file must exist first. If it does not, run `train_model.py`.

## 5. Add new data and observe the impact

Open `house_prices.csv` in Excel, LibreOffice, or a text editor.

The CSV header must remain:

```csv
area_sqft,bedrooms,price_lakh
```

Add a new labelled example at the bottom. For example:

```csv
2000,4,110
```

This means a 2,000-square-foot house with 4 bedrooms has a known price of 110 lakh.

**Important:** Add real or intentionally chosen example data with a known price. Supervised learning needs both the input features and the correct target label during training. Do not add a blank price.

### Compare before and after

1. Run `python train_model.py` and note the metrics.
2. Run `python predict_house_price.py` and enter the same test house details. Note the prediction.
3. Add one or more new labelled rows to `house_prices.csv`.
4. Run `python train_model.py` again. This retrains the model using the updated CSV and overwrites the saved model.
5. Run `python predict_house_price.py` again with the exact same area and bedroom inputs.
6. Compare the new prediction and metrics with the values you recorded earlier.

You may observe that:
- the prediction changes because the model has learned from the additional examples;
- MAE/RMSE may improve or become worse;
- R² may increase or decrease.

Adding more rows does **not** guarantee better results. The quality, accuracy, representativeness, and quantity of data matter. With a small dataset, evaluation metrics can vary considerably.

## 6. Suggested classroom experiment

Try these experiments one at a time:

| Experiment | What to change | What to observe |
|---|---|---|
| A | Add a realistic 1,200 sq ft, 2-bedroom example with its known price | Does the prediction for a similar house change? |
| B | Add a larger 2,500 sq ft, 4-bedroom example | Does the model adjust its predictions for larger houses? |
| C | Add an unusual or incorrect price | Do the metrics or predictions become less reliable? |
| D | Add several representative examples | Does performance become more stable? |

Keep a copy of the original CSV if you want to repeat the experiment from the same starting point.

## 7. Understand the evaluation metrics

- **MAE (Mean Absolute Error):** average absolute prediction error, in lakh. Lower is generally better.
- **RMSE (Root Mean Squared Error):** penalizes large errors more strongly, in lakh. Lower is generally better.
- **R² score:** compares the model with a simple mean-value baseline. Closer to 1 is generally better; it can be negative when the model performs poorly.

Because this is a small teaching dataset, do not treat the metrics as evidence that the model is suitable for real property valuation.

## 8. Troubleshooting

**`ModuleNotFoundError`**
```bash
python -m pip install pandas scikit-learn joblib
```

**`Model file not found`**

Run the training script first:
```bash
python train_model.py
```

**CSV column or data error**

Check that the first line is exactly:
```csv
area_sqft,bedrooms,price_lakh
```
All three columns must contain numeric values, and `price_lakh` must not be blank.

**Prediction does not change after adding data**

Make sure you:
1. Saved the updated CSV.
2. Ran `python train_model.py` again.
3. Ran `python predict_house_price.py` after training.
4. Entered the same area and bedroom values for a fair comparison.

## 9. Key learning outcomes

After completing this practical, learners should be able to explain:

- What supervised learning is.
- The difference between features and labels.
- The difference between regression and classification.
- Why data is split into training and testing sets.
- How a model learns from labelled examples.
- How to evaluate a model.
- Why a model must be retrained after adding training data.
