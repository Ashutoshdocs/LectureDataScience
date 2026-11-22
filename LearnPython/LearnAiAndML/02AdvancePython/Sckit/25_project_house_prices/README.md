# Lecture 25: Project: house prices (regression, end to end)

Run: `python lecture.py` (about 20 seconds)

**Goal:** predict flat prices (in lakh ₹) from messy, mixed data, the way you would at work. The dataset is generated inside the script (2,000 flats in 4 cities), so it runs offline, but it has real-world problems: **missing values**, **text categories**, a **right-skewed target**, and **interacting effects** (city × area).

## The workflow

| Step | What we do | Lectures |
|------|------------|----------|
| 1. Explore | shapes, missing values, target distribution, price by city | 02 |
| 2. Split | 80/20, test set locked away **before** any modelling | 04 |
| 3. Preprocess | `FunctionTransformer` (new features) → `ColumnTransformer` (impute + scale numbers; impute + one-hot categories) | 10, 11, 20, 24 |
| 4. Compare | 6 candidates with 5-fold CV on **train only**, scored by MAE and R² | 06, 07 |
| 5. Tune | `RandomizedSearchCV` over the best family, reaching **inside** `TransformedTargetRegressor` | 21 |
| 6. Evaluate | the test set, **once**; compare with the baseline | 06 |
| 7. Error analysis | errors by city and size; the biggest misses | 06 |
| 8. Explain | permutation importance | 11 |
| 9. Deploy | `joblib` save/load; price new raw listings with missing values | 24 |

## Results (from `lecture.py`)

| Model (5-fold CV) | MAE (lakh) | R² |
|-------------------|-----------:|---:|
| Dummy (mean) | 35.92 | −0.005 |
| Ridge | 11.96 | 0.874 |
| Ridge + log target | 10.11 | 0.830 |
| RandomForest | 9.41 | 0.912 |
| HistGradientBoosting | 9.17 | 0.917 |
| **HGB + log target** | **8.99** | **0.921** |
| HGB + log target, **tuned** | **8.45** | |

**Test set:** MAE **7.84 lakh**, MAPE **10.2%**, R² **0.939**: about 4.4× better than the baseline.

## Lessons from this project

1. **Always start with a baseline.** The dummy's MAE of 35.9 gives every other number meaning.
2. **Trees beat linear models here** because price depends on *products* of features (city rate × area × age). A linear model can only *add* effects.
3. **The log target** helped HGB (MAE 9.17 → 8.99) and helped Ridge's MAE (11.96 → 10.11), even though Ridge's R² fell. Different metrics can disagree, so pick the one that matches the business goal.
4. **Tuning added a modest gain** (8.99 → 8.45). Choosing the right model family mattered more.
5. **Error analysis reveals weak spots:** the biggest absolute errors are large Mumbai flats, and percentage errors are highest for very large flats (200+ m²), where there's little training data.
6. **Permutation importance** shows area and city dominate. `bedrooms` adds nothing once area is known (they're strongly correlated), which makes it a candidate to drop.
7. **The saved pipeline accepts raw data**, including missing ages and furnishing, because every preprocessing step lives inside it.

## Hyperparameter paths inside nested objects

`model__regressor__learning_rate` = step `model` (the `TransformedTargetRegressor`) → its `regressor` → `learning_rate`. Print `pipe.get_params().keys()` to see every reachable name.

## Extension exercises

1. Add a `price_per_sqm` *target* instead of price, then multiply back. Does MAE improve?
2. Try `GradientBoostingRegressor(loss="huber")`.
3. Add an interaction feature `area × city_rate` and retry Ridge. How close does it get to the trees?
4. Report a prediction **interval** using `HistGradientBoostingRegressor(loss="quantile", quantile=0.1/0.9)`.

**Next →** [Lecture 26: Project: tumour classifier](../26_project_tumour_classifier/)
