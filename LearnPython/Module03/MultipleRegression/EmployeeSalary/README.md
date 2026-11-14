# Employee Salary Prediction – Multiple Linear Regression

A beginner-friendly supervised learning practical that predicts an employee's annual salary using **experience, education level, and job title**.

This project demonstrates multiple regression with both numeric and categorical input features. It uses `OneHotEncoder` to convert categories into model-friendly numeric columns and `LinearRegression` to learn from the examples.

> All salary records in this project are synthetic teaching data. They are not market salary benchmarks or compensation advice.

## 1. Project structure

```text
employee_salary_prediction/
├── README.md
├── employee_salary.csv
├── train_model.py
└── predict_salary.py
```

## 2. What will the model learn?

| Column | Type | Meaning |
|---|---|---|
| `experience_years` | Numeric feature | Years of relevant work experience |
| `education_level` | Categorical feature | Bachelor's, Master's, or PhD |
| `job_title` | Categorical feature | Job role |
| `salary_lpa` | Numeric target/label | Annual salary in lakh per annum (LPA) |

This is **supervised learning – regression**, because the model learns from examples with known salary values and predicts a numeric result.

## 3. How multiple regression works

```text
          employee_salary.csv
   Experience + Education + Job Title
             Known Salary
                  |
                  v
          Load and validate data
                  |
                  v
       Preprocess input features
        /                    \
 Numeric: experience     Categories:
                         education, title
        \                    /
         v                  v
         Combine processed features
                  |
                  v
       Split into train/test records
                  |
                  v
        Train Linear Regression
                  |
                  v
       Evaluate predictions (MAE,
               RMSE and R²)
                  |
                  v
          Save trained pipeline
                  |
                  v
        Predict a new employee salary
```

The model estimates salary from the combined contribution of all three inputs. The category columns are encoded using one-hot encoding; the pipeline applies the same preprocessing during training and prediction.

## 4. Requirements

Python 3.9 or later is recommended.

Install dependencies:

```bash
python -m pip install pandas scikit-learn joblib
```

On Linux, use `python3` if `python` is not configured.

## 5. Run the project

Open a terminal inside this project folder.

### Step 1 – Train the model

```bash
python train_model.py
```

The script:
1. Reads `employee_salary.csv`.
2. Validates the required columns and values.
3. Separates numeric and categorical features.
4. One-hot encodes education level and job title.
5. Splits records into training and testing sets.
6. Trains a multiple linear regression model.
7. Displays MAE, RMSE, and R².
8. Saves the complete preprocessing-and-model pipeline as `employee_salary_model.joblib`.

### Step 2 – Predict an employee salary

```bash
python predict_salary.py
```

Example inputs:

```text
Experience in years: 5
Education level: Master's
Job title: Data Scientist
```

The program prints an estimated annual salary in LPA.

Enter education and job title values exactly as listed in the CSV. The prediction script displays the available categories if an unsupported value is entered.

## 6. Add new employee data

Open `employee_salary.csv` in Excel, LibreOffice, or a text editor.

Keep the exact header:

```csv
experience_years,education_level,job_title,salary_lpa
```

Add a new labelled record. Example:

```csv
6,Master's,Data Scientist,14.5
```

This means the example employee has 6 years of experience, a Master's degree, a Data Scientist role, and a known annual salary of 14.5 LPA.

Save the CSV, then retrain the model:

```bash
python train_model.py
```

Run prediction again:

```bash
python predict_salary.py
```

Use the same employee inputs before and after retraining to compare the predictions fairly.

### Observe the impact

1. Train the original dataset and record the MAE, RMSE, R², and one prediction.
2. Add one or more new employee records with known salaries.
3. Save the CSV.
4. Run `python train_model.py` again.
5. Run `python predict_salary.py` with the same inputs as before.
6. Compare the metrics and predicted salary.

The prediction may change because the fitted model has changed. Evaluation scores may improve or worsen; adding rows does not guarantee better performance. With a small teaching dataset, test metrics can be unstable.

## 7. Classroom experiments

| Experiment | Change | What to observe |
|---|---|---|
| A | Increase experience from 2 to 8 years; keep education and title fixed | How does the estimate change? |
| B | Keep experience and title fixed; change Bachelor's to Master's | How does education affect the estimate learned from the examples? |
| C | Keep experience and education fixed; change Software Engineer to Engineering Manager | How does job title affect the estimate? |
| D | Add a new labelled employee row and retrain | Does the same employee's prediction change? |
| E | Add a very unusual or incorrect salary | How can outliers affect regression? |

The model learns associations in this synthetic dataset. It does not establish that a degree, job title, or extra year of experience causes a particular salary increase.

## 8. Understand the evaluation metrics

- **MAE:** average absolute prediction error in LPA. Lower is generally better.
- **RMSE:** prediction error in LPA, with larger errors penalized more strongly. Lower is generally better.
- **R²:** compares the model with a mean-value baseline. Closer to 1 is generally better; a negative score means it performs worse than that baseline on the test set.

## 9. Important notes

- This is a learning demo, not a real salary estimator.
- The CSV contains a small, synthetic dataset created for teaching.
- Real compensation depends on many factors not included here, such as location, company, industry, skills, performance, and market conditions.
- Avoid using a small or biased dataset for hiring, promotion, or pay decisions.
- The script uses a fixed train/test split for repeatability. Adding rows can change which rows land in each split.

## 10. Troubleshooting

**Missing packages**
```bash
python -m pip install pandas scikit-learn joblib
```

**Model file not found**

Train first:
```bash
python train_model.py
```

**Unknown education level or job title**

Use one of the values printed by `predict_salary.py`, or add a new category to the CSV with valid labelled examples, retrain, and then predict.

**CSV validation error**

Check:
- Header spelling is exactly correct.
- Experience and salary values are numeric.
- Education and job title cells are not blank.
- Experience is not negative.
- Salary is greater than zero.

## 11. Learning outcomes

After this practical, learners should understand:

- Supervised learning and regression
- Multiple linear regression with more than one input feature
- Numeric versus categorical features
- One-hot encoding
- Training/testing split
- Model evaluation using MAE, RMSE, and R²
- Making predictions for new records
- Retraining after adding labelled data
- Why data quality and fairness matter
