# 🎓 Student Marks Prediction: Polynomial Regression (Degree 3) Demo

This demo predicts a student's **final exam marks (out of 100)** from **one input: study hours per day**, using **Polynomial Regression of degree 3**.

Instead of a straight line, the model learns a **curve**:

```
final_marks = b0 + b1·x + b2·x² + b3·x³        (x = study_hours)
```

**Why a curve?** In this data, marks rise slowly at first, climb fast in the middle, then **level off** after about 8 hours (tiredness, diminishing returns). A straight line can't bend to follow that, but a cubic curve can.

> New to polynomial regression? Read **[POLYNOMIAL_REGRESSION_GUIDE.md](POLYNOMIAL_REGRESSION_GUIDE.md)** first.

---

## 📁 Project Files

| File | What it is |
|------|------------|
| `train.csv` | **Training data**: 120 students with their study hours **and** actual final marks |
| `predict.csv` | **New data**: 10 students with study hours only. Marks are unknown, so we predict them |
| `train.py` | Trains the degree-3 model, compares it with a straight line, and saves it as `model.pkl` |
| `predict.py` | **Interactive demo**: predict from a CSV file **or** from hours you type in |
| `polynomial_regression_from_scratch.py` | Teaching file that builds the same curve by hand with the Normal Equation |
| `requirements.txt` | Python packages needed |
| `README.md` | This file (how to run the demo) |
| `POLYNOMIAL_REGRESSION_GUIDE.md` | Teaching notes: what polynomial regression is and how it works |

---

## 📊 The Data

| Column | Meaning | Range |
|--------|---------|-------|
| `student_id` | Student ID | S001… / N001… |
| `study_hours` | **Input (x)**: hours studied per day | about 0.5 – 10 |
| `final_marks` | **Output (y)**: final exam marks (only in `train.csv`) | 0 – 100 |

*Note: this is synthetic (generated) data made for teaching.*

---

## ⚙️ Setup

You need **Python 3.8+**.

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Demo

### Step 1: Train the model

```bash
python train.py
```

Output:

```
[3] Evaluating on unseen test data ...
    Model                   R² score   Avg error (MAE)
    Straight line              0.933        3.88 marks
    Polynomial (degree 3)      0.976        2.53 marks

[4] The curve the model learned:
    final_marks = 32.008 -0.129·x +2.047·x² -0.1480·x³
    (x = study_hours)
```

The curve beats the straight line on students it has never seen. The model is saved as `model.pkl`.

### Step 2: Predict

```bash
python predict.py
```

You'll see a menu:

```
==================================================
   STUDENT MARKS PREDICTION (Polynomial, degree 3)
==================================================
  Model: marks = 32.01 -0.13x +2.05x² -0.148x³

  1) Predict from a CSV file
  2) Predict from user input
  3) Exit

Choose an option (1/2/3):
```

#### Option 1: Predict from a CSV file

Press **Enter** to use the default `predict.csv`, or type the path to your own file.
The predictions are printed and saved to **`predictions_output.csv`**.

```
Enter CSV file path [default: predict.csv]:

Predictions:
student_id  study_hours  predicted_marks
      N001            1             33.8
      N002            2             38.8
      N003            3             46.0
      N004            4             54.8
      N005            5             64.0
      N006            6             73.0
      N007            7             80.6
      N008            8             86.2
      N009            9             88.8
      N010           10             87.4

Saved results to 'predictions_output.csv'.
```

Notice the curve: +5 marks from 1→2 hours, +9 from 5→6 hours, and almost nothing after 9 hours.

#### Option 2: Predict from user input

Type in the study hours:

```
Enter study hours per day (0-24): 6
  Calculation: 32.008 -0.129×6.0 +2.047×6.0² -0.1480×6.0³ = 73.0
  >>> Predicted final marks: 73.0 / 100

Predict another? (y/n): y

Enter study hours per day (0-24): 14
  Calculation: 32.008 -0.129×14.0 +2.047×14.0² -0.1480×14.0³ = 25.4
  >>> Predicted final marks: 25.4 / 100
  WARNING: 14.0 hours is outside the training range (0.6-10.0). A cubic curve can
  shoot up or down quickly out here, so don't trust this prediction.
```

> If `model.pkl` doesn't exist yet, `predict.py` trains the model automatically first.

---

## 🧪 Try Your Own Data

- **Your own training data:** `python train.py my_training_data.csv`
  (it needs `study_hours` and `final_marks` columns)
- **Your own prediction file:** choose option 1 and enter your file path
  (it only needs a `study_hours` column)

---

## 🔬 Bonus: See How It Works Inside

```bash
python polynomial_regression_from_scratch.py
```

This turns each x into `[1, x, x², x³]` and solves for the coefficients with the **Normal Equation**. It finds the same curve as scikit-learn, compares it with a straight line, and shows what goes wrong at 15 hours. Read `POLYNOMIAL_REGRESSION_GUIDE.md` alongside it.

---

## 💡 Discussion Questions for Students

1. Why does the curve fit better than a straight line for this data?
2. Which coefficient makes the curve bend **down** at high study hours?
3. The model predicts 25 marks for 14 hours of study. Why is this wrong, and why does it happen?
4. If degree 3 is better than degree 1, would degree 15 be even better? (Hint: overfitting.)
