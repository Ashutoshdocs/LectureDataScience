# Supervised Learning Demo — Loan Approval Prediction (Python + scikit-learn)

A complete, beginner-friendly, end-to-end **supervised machine learning** project.
It predicts whether a loan application will be **Approved (1)** or **Rejected (0)**
from applicant details, and walks through every step of a real ML workflow:

> data → exploration → preprocessing → model comparison → tuning → evaluation → prediction

It can be used two ways:
- **Command line:** run each step's script and read the output (sections 5–6)
- **Browser UI:** a Streamlit web app for predictions, reports and data exploration (section 6A)

**Quick start (browser):**
```bash
pip install -r requirements.txt
streamlit run app.py          # opens http://localhost:8501
```

---

## 1. What is supervised learning?

In supervised learning, the model learns from **labeled examples** — inputs (features)
paired with the correct answer (label/target). After training, it predicts the label for
new inputs it has never seen.

| Type | Target | Example algorithms | Example |
|---|---|---|---|
| **Classification** | A category | Logistic Regression, Random Forest, Gradient Boosting | Approve / Reject a loan ← *this demo* |
| **Regression** | A number | Linear Regression, Random Forest Regressor | Predict house price |

```
 Labeled data ──► [ Train model ] ──► Trained model ──► Predict on new data
 (features + label)                        ▲
                                           │ evaluate on held-out test data
```

---

## 2. Project structure

```
supervised-learning-demo/
├── README.md                 ← you are here
├── app.py                    ← browser UI (Streamlit)
├── requirements.txt          ← Python dependencies
├── run_all.sh                ← runs every step in order
├── data/
│   ├── loan_data.csv         ← 1,000 labeled training rows (generated)
│   ├── new_applicants.csv    ← 5 unlabeled rows to predict on
│   └── predictions.csv       ← output of predict.py
├── src/
│   ├── config.py             ← paths, feature lists, settings
│   ├── generate_data.py      ← Step 1: create the dataset
│   ├── explore.py            ← Step 2: exploratory data analysis
│   ├── train.py              ← Step 3: compare, tune and save models
│   ├── evaluate.py           ← Step 4: test-set metrics + charts
│   └── predict.py            ← Step 5: predict on new data
├── models/
│   ├── best_model.joblib     ← saved pipeline (preprocessing + model)
│   └── test_set.csv          ← held-out 20% test data
└── reports/
    ├── metrics.txt
    ├── confusion_matrix.png
    ├── roc_curve.png
    └── feature_importance.png
```

---

## 3. The dataset

`data/loan_data.csv` — 1,000 synthetic applicants (reproducible with a fixed random seed).

| Column | Type | Description |
|---|---|---|
| `applicant_id` | ID | Unique identifier (not used as a feature) |
| `age` | numeric | 21–64 |
| `annual_income` | numeric | Yearly income (contains some missing values) |
| `loan_amount` | numeric | Amount requested |
| `credit_score` | numeric | 300–850 (contains some missing values) |
| `years_employed` | numeric | Years in current employment |
| `existing_debt` | numeric | Outstanding debt |
| `education` | categorical | High School / Bachelor / Master / PhD |
| `employment_type` | categorical | Salaried / Self-Employed / Contract (some missing) |
| **`approved`** | **target** | **1 = approved, 0 = rejected** |

Labels were generated from a hidden rule (higher credit score & income, lower loan & debt
→ more likely approved) plus random noise. ~2% missing values were injected on purpose so
the pipeline has to deal with realistic, messy data.

---

## 4. Setup

**Requirements:** Python 3.9+

```bash
# 1. Go into the project folder
cd supervised-learning-demo

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 5. Steps to implement

Run each step from the project root. To run everything at once: `bash run_all.sh`
(on Windows, run the five `python` commands below one by one).

### Step 1 — Generate the data
```bash
python src/generate_data.py
```
Creates `data/loan_data.csv`. (Already included — re-running produces the identical file.)

### Step 2 — Explore the data (EDA)
```bash
python src/explore.py
```
Prints shape, column types, missing values, class balance, summary stats, and approval
rates by category. **Why:** you should understand the data before modelling it — e.g.
approved applicants have a mean credit score of ~706 vs ~653 for rejected ones.

### Step 3 — Train and compare models
```bash
python src/train.py
```
What it does:
1. **Train/test split** — 80% train, 20% test, *stratified* to keep the same class ratio.
   The test set is locked away until Step 4.
2. **Preprocessing pipeline** (`ColumnTransformer`):
   - Numeric: fill missing with median → standardise (`StandardScaler`)
   - Categorical: fill missing with most frequent → one-hot encode
3. **Model comparison** with 5-fold cross-validation (ROC-AUC) on the training set:
   Logistic Regression, Random Forest, Gradient Boosting.
4. **Hyperparameter tuning** of the winner with `GridSearchCV`.
5. Saves the full pipeline to `models/best_model.joblib`.

> Preprocessing lives *inside* the pipeline, so it is learned only from training folds —
> this prevents **data leakage**.

### Step 4 — Evaluate on unseen test data
```bash
python src/evaluate.py
```
Writes `reports/metrics.txt` and three charts: confusion matrix, ROC curve, and
permutation feature importance.

### Step 5 — Predict on new applicants
```bash
python src/predict.py                         # uses data/new_applicants.csv
python src/predict.py my_applicants.csv       # or your own file (same columns)
```
Writes `data/predictions.csv` with an approval probability and a label for each row.

---

## 6A. Browser UI (Streamlit)

```bash
streamlit run app.py
```
Your browser opens at **http://localhost:8501**. Press `Ctrl+C` in the terminal to stop.

A trained model is already included. If it's missing, or you want to retrain after
changing the code, click **🔄 Train / retrain model** in the sidebar. That runs Steps 1, 3 and 4
for you.

| Tab | What you can do |
|---|---|
| 🔮 **Predict** | Fill in an applicant form (age, income, credit score, loan amount…) and get **Approved / Rejected** with a probability. A slider lets you move the decision threshold. |
| 📄 **Batch predict** | Download the sample CSV, upload your own CSV, view predictions for every row and download them. |
| 📊 **Model report** | Test-set accuracy, precision, recall, F1 and ROC-AUC, plus the confusion matrix, ROC curve and feature importance charts. |
| 🔍 **Data explorer** | Preview the training data, compare feature averages for approved vs rejected applicants, and see approval rate by category and missing values. |

**Things to try in the UI:**
- Start with the defaults, then raise the credit score from 600 to 780 and watch the probability jump.
- Increase the loan amount while keeping income fixed and see where the decision flips.
- Raise the threshold to 0.7 and notice that the model approves fewer applicants (more cautious, higher precision).

> To open the app from another device on your network:
> `streamlit run app.py --server.address 0.0.0.0`

---

## 6. Results (from the included run)

**Cross-validation (train set, ROC-AUC):**

| Model | CV ROC-AUC |
|---|---|
| **Logistic Regression** | **0.830 ± 0.046** ← selected (tuned `C=0.1`) |
| Gradient Boosting | 0.796 ± 0.056 |
| Random Forest | 0.789 ± 0.055 |

**Held-out test set (200 rows):**

| Metric | Score |
|---|---|
| Accuracy | **0.805** (vs 0.56 for always guessing "Approved") |
| Precision | 0.812 |
| Recall | 0.848 |
| F1 | 0.830 |
| ROC-AUC | **0.871** |

**Most important features:** `credit_score` ≫ `loan_amount` > `annual_income` >
`existing_debt` ≈ `years_employed`. `age` has ~zero importance — correct, since it
wasn't part of the hidden rule that generated the labels.

**Sample predictions:**

| ID | Credit | Income | Loan | P(approve) | Prediction |
|---|---|---|---|---|---|
| N001 | 760 | 85,000 | 120,000 | 0.979 | Approved |
| N002 | 590 | 32,000 | 250,000 | 0.008 | Rejected |
| N003 | 680 | 60,000 | 150,000 | 0.518 | Approved (borderline) |
| N004 | 720 | 120,000 | 300,000 | 0.949 | Approved |
| N005 | 640 | 45,000 | 90,000 | 0.219 | Rejected |

> Why did the simple model win? The labels came from a (logistic) linear rule, so a linear
> model matches the true pattern. On real-world data with non-linear interactions, tree
> ensembles often win — that's why you always compare.

---

## 7. Understanding the metrics

| Metric | Question it answers |
|---|---|
| **Accuracy** | What fraction of all predictions were correct? |
| **Precision** | Of applicants we *approved*, how many truly deserved approval? |
| **Recall** | Of applicants who *deserved* approval, how many did we approve? |
| **F1** | Harmonic mean of precision and recall |
| **ROC-AUC** | How well does the model *rank* approvals above rejections? (0.5 = random, 1.0 = perfect) |
| **Confusion matrix** | Counts of true/false positives and negatives |

Always compare against a **baseline** (here, 56% accuracy from always predicting the
majority class) — a model is only useful if it beats it clearly.

---

## 8. Key concepts demonstrated

- ✅ Train / test split with stratification
- ✅ Handling missing values (imputation)
- ✅ Feature scaling and one-hot encoding
- ✅ `Pipeline` + `ColumnTransformer` (no data leakage)
- ✅ K-fold cross-validation for fair model comparison
- ✅ Hyperparameter tuning with `GridSearchCV`
- ✅ Evaluation on truly unseen data + baseline comparison
- ✅ Model interpretation (permutation importance)
- ✅ Saving / loading a model with `joblib` for reuse

---

## 9. Try it yourself (exercises)

1. Change `N_ROWS` in `generate_data.py` to 200 or 5,000 — how do the scores change?
2. Add `SVC(probability=True)` or `KNeighborsClassifier()` to `CANDIDATES` in `train.py`.
3. Change the decision threshold in `predict.py` from 0.5 to 0.7 — what happens to
   precision vs recall?
4. Engineer a new feature such as `debt_to_income = existing_debt / annual_income`.
5. Turn it into **regression**: predict `credit_score` from the other columns using
   `RandomForestRegressor` and evaluate with MAE / RMSE / R².
6. Replace the synthetic data with a real dataset (e.g. Kaggle's *Loan Prediction* or
   scikit-learn's built-in `load_breast_cancer()`).

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the venv and run `pip install -r requirements.txt` |
| `FileNotFoundError: best_model.joblib` | Run `python src/train.py` before evaluate/predict |
| `Input file is missing columns` | Your CSV must contain all feature columns listed in `config.py` |
| Scripts can't find `config` | Run commands from the project root as shown (`python src/...`) |
| `streamlit: command not found` | Use `python -m streamlit run app.py` |
| UI says "No trained model found" | Click **Train / retrain model** in the sidebar |
| Port 8501 already in use | `streamlit run app.py --server.port 8502` |
