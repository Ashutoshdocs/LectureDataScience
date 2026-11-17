# 🎓 Student Marks Prediction — Linear Regression Demo

This demo predicts a student's **final exam marks (out of 100)** from five simple habits, using **Multiple Regression**.

> New to Multiple regression? Read **[MULTIPLE_REGRESSION_GUIDE.md]** first.

---

## 📁 Project Files

| File | What it is |
|------|------------|
| `train.csv` | **Training data**: 200 students, with their habits **and** their actual final marks |
| `predict.csv` | **New data**: 15 students, habits only. Marks are unknown, so we predict them |
| `train.py` | Trains the model on `train.csv` and saves it as `model.pkl` |
| `predict.py` | **Interactive demo**: predict from a CSV file **or** from values you type in |
| `linear_regression_from_scratch.py` | Teaching file that builds linear regression by hand (no ML library) |
| `requirements.txt` | Python packages needed |
| `README.md` | This file (how to run the demo) |
| `LINEAR_REGRESSION_GUIDE.md` | Teaching notes: what linear regression is and how it works |

---

## 📊 The Data

| Column | Meaning | Range |
|--------|---------|-------|
| `student_id` | Student ID | S001… / N001… |
| `study_hours` | Hours studied per day | 1 – 10 |
| `attendance_percent` | Class attendance % | 50 – 100 |
| `previous_marks` | Marks in the previous exam | 35 – 95 |
| `assignments_completed` | Assignments submitted (out of 10) | 0 – 10 |
| `sleep_hours` | Hours of sleep per night | 4 – 9 |
| `final_marks` | **Target**: final exam marks (only in `train.csv`) | 0 – 100 |

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

Sample output:

```
[3] Evaluating on unseen test data ...
    R² score            : 0.953  (1.0 = perfect)
    Mean Absolute Error : 2.25 marks

[4] What the model learned (the equation):
    final_marks = 1.01
                  +3.317 × study_hours
                  +0.284 × attendance_percent
                  +0.344 × previous_marks
                  +0.922 × assignments_completed
                  +1.069 × sleep_hours
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

student_id  study_hours  attendance_percent  ...  predicted_marks
      N001          2.7                  57  ...             60.0
      N002          1.6                  56  ...             62.0
      ...
Saved results to 'predictions_output.csv'.
```

#### Option 2: Predict from user input

Type in one student's details:

```
Enter the student's details:
  Study hours per day [0-24]: 6
  Attendance percentage [0-100]: 85
  Previous exam marks (out of 100) [0-100]: 70
  Assignments completed (out of 10) [0-10]: 8
  Sleep hours per day [0-24]: 7

  >>> Predicted final marks: 83.9 / 100

Predict another student? (y/n):
```

> If `model.pkl` doesn't exist yet, `predict.py` trains the model automatically first.

---

## 🧪 Try Your Own Data

- **Your own training data:** `python train.py my_training_data.csv`
  (it must have the 5 feature columns and `final_marks`)
- **Your own prediction file:** choose option 1 and enter your file path
  (it only needs the 5 feature columns)

---

## 🔬 Bonus: See How It Works Inside

```bash
python linear_regression_from_scratch.py
```

This trains a simple line (`study_hours → final_marks`) with **gradient descent**, written from scratch, and checks it against the exact formula. Read `LINEAR_REGRESSION_GUIDE.md` alongside it.

---

## 💡 Discussion Questions for Students

1. Which habit has the **biggest effect** per unit on marks? (Look at the coefficients.)
2. Why can't we compare coefficients directly when features have different ranges?
3. What happens if someone enters `study_hours = 20`? Is the prediction realistic? Why?
4. Does a high coefficient for `sleep_hours` prove sleep *causes* better marks?
