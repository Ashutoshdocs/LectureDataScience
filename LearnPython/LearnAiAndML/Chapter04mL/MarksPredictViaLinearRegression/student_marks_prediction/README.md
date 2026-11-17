# 🎓 Student Marks Prediction: Simple Linear Regression Demo

This demo predicts a student's **final exam marks (out of 100)** from **one input: study hours per day**, using **Simple Linear Regression**.

The model learns one straight line:

```
final_marks = m × study_hours + c
```

> New to linear regression? Read **[LINEAR_REGRESSION_GUIDE.md](LINEAR_REGRESSION_GUIDE.md)** first.

---

## 📁 Project Files

| File | What it is |
|------|------------|
| `train.csv` | **Training data**: 100 students with their study hours **and** actual final marks |
| `predict.csv` | **New data**: 10 students with study hours only. Marks are unknown, so we predict them |
| `train.py` | Trains the model on `train.csv` and saves it as `model.pkl` |
| `predict.py` | **Interactive demo**: predict from a CSV file **or** from hours you type in |
| `linear_regression_from_scratch.py` | Teaching file that builds the same line by hand (no ML library) |
| `requirements.txt` | Python packages needed |
| `README.md` | This file (how to run the demo) |
| `LINEAR_REGRESSION_GUIDE.md` | Teaching notes: what linear regression is and how it works |

---

## 📊 The Data

| Column | Meaning | Range |
|--------|---------|-------|
| `student_id` | Student ID | S001… / N001… |
| `study_hours` | **Input (x)**: hours studied per day | 0.5 – 10 |
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
    R² score            : 0.965  (1.0 = perfect)
    Mean Absolute Error : 2.49 marks

[4] The line the model learned:
    final_marks = 5.98 × study_hours + 29.68
    Slope (m)     = 5.98  -> each extra study hour adds ~6.0 marks
    Intercept (c) = 29.68  -> predicted marks with 0 study hours
```

The model is saved as `model.pkl`.

### Step 2: Predict

```bash
python predict.py
```

You'll see a menu:

```
==========================================
   STUDENT MARKS PREDICTION (Linear Reg.)
==========================================
  Model: final_marks = 5.98 × study_hours + 29.68

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
      N001          1.0             35.7
      N002          2.5             44.6
      N003          3.0             47.6
      ...
      N010         10.0             89.4

Saved results to 'predictions_output.csv'.
```

#### Option 2: Predict from user input

Type in the study hours:

```
Enter study hours per day (0-24): 6
  Calculation: 5.98 × 6.0 + 29.68
  >>> Predicted final marks: 65.5 / 100

Predict another? (y/n):
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
python linear_regression_from_scratch.py
```

This finds the same line using **gradient descent**, written from scratch, and checks it against the exact formula. Both give `5.98 × study_hours + 29.68`, the same as scikit-learn. Read `LINEAR_REGRESSION_GUIDE.md` alongside it.

---

## 💡 Discussion Questions for Students

1. What does the slope **5.98** mean in plain words?
2. What does the intercept **29.68** mean? Is it realistic?
3. What happens if someone enters `study_hours = 15`? Is the prediction believable? Why?
4. Does this prove that studying more *causes* higher marks?
