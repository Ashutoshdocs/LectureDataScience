# 🎓 Student Marks Prediction: Random Forest Regressor Demo

This demo predicts a student's **final exam marks (out of 100)** from **four inputs** using a **Random Forest Regressor**:

| Input | Meaning |
|-------|---------|
| `study_hours` | Hours of self-study per day |
| `coaching` | Does the student attend coaching classes? (Yes / No) |
| `live_sessions_attended` | Live online sessions attended (out of 20) |
| `recorded_course_completion` | % of the recorded video course watched (0–100) |

A **random forest** is a team of **many decision trees** (200 here). Each tree learns from a slightly different random sample of students, makes its own prediction, and the forest's answer is the **average** of all the trees.

```
 Student ──► Tree 1 → 68.2
         ──► Tree 2 → 71.5
         ──► Tree 3 → 64.8     ──►  average  ──►  70.0 marks
         ──►  ...
         ──► Tree 200 → 69.9
```

> New to random forests? Read **[RANDOM_FOREST_GUIDE.md](RANDOM_FOREST_GUIDE.md)** first.
> It helps to know decision trees first (see the Decision Tree demo).

---

## 📁 Project Files

| File | What it is |
|------|------------|
| `train.csv` | **Training data**: 200 students with all 4 inputs **and** their actual final marks |
| `predict.csv` | **New data**: 12 students with inputs only. Marks are unknown, so we predict them |
| `train.py` | Trains the forest, compares it with linear regression and a single tree, shows feature importance, saves `model.pkl` |
| `predict.py` | **Interactive demo**: predict from a CSV file **or** from details you type in (shows what the individual trees said) |
| `random_forest_from_scratch.py` | Teaching file that builds a forest in plain Python (no ML library) |
| `requirements.txt` | Python packages needed |
| `README.md` | This file (how to run the demo) |
| `RANDOM_FOREST_GUIDE.md` | Teaching notes: what a random forest is and how it works |

---

## 📊 The Data

| Column | Meaning | Range |
|--------|---------|-------|
| `student_id` | Student ID | S001… / N001… |
| `study_hours` | Self-study hours per day | 0.5 – 10 |
| `coaching` | Attends coaching classes | Yes / No |
| `live_sessions_attended` | Live sessions attended | 0 – 20 |
| `recorded_course_completion` | % of recorded course watched | 0 – 100 |
| `final_marks` | **Target**: final exam marks (only in `train.csv`) | 0 – 100 |

**Patterns hidden in the data** (the forest has to discover these on its own):
- Study hours help a lot at first, then the benefit **levels off**
- Live sessions also have **diminishing returns**
- Coaching adds marks
- The recorded course helps **more for students without coaching** (coaching already covers some of the same material)

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
[3] Evaluating: one model vs. a whole forest ...
    Model                     Train R²   Test R²    Test MAE
    Linear regression            0.777     0.763    3.94 marks
    Single decision tree         1.000     0.680    4.18 marks
    Random forest (200)          0.952     0.859    3.09 marks
    Single tree: perfect on training data, poor on new students (overfits).
    Forest: averaging many different trees cancels out their mistakes.

    Out-of-bag R² (all data): 0.829

[4] Feature importance (which inputs the forest relied on most):
    study_hours                  62.0%  ███████████████████████████████
    live_sessions_attended       21.2%  ███████████
    recorded_course_completion   11.9%  ██████
    coaching                      4.9%  ██
```

The forest beats both the straight line and a single tree on students it has never seen. The model is saved as `model.pkl`.

### Step 2: Predict

```bash
python predict.py
```

You'll see a menu:

```
==================================================
   STUDENT MARKS PREDICTION (Random Forest)
==================================================
  Model: forest of 200 decision trees
  Inputs: study hours, coaching, live sessions, recorded course

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
student_id  study_hours coaching  live_sessions_attended  recorded_course_completion  predicted_marks
      N001          7.9       No                      17                          28             61.3
      N002          2.1       No                       9                          41             48.4
      N003          7.3       No                       0                          33             52.4
      N004          7.6      Yes                      14                          75             71.2
      ...
Saved results to 'predictions_output.csv'.
```

The `coaching` column can be `Yes`/`No`, `Y`/`N` or `1`/`0`.

#### Option 2: Predict from user input

Type in one student's details. You'll see how much the trees disagreed and the average they agreed on:

```
Enter the student's details:
  Study hours per day [0-24]: 6
  Takes coaching classes? (y/n): y
  Live sessions attended (out of 20) [0-20]: 15
  Recorded course completed (%) [0-100]: 80

  The forest has 200 trees. Each one made its own prediction:
    Lowest tree   : 65.1
    Highest tree  : 76.1
    First 5 trees : 71.2, 71.5, 68.4, 68.6, 67.3 ...
  Average of all 200 trees = forest prediction

  >>> Predicted final marks: 70.0 / 100

Predict another student? (y/n):
```

> If `model.pkl` doesn't exist yet, `predict.py` trains the model automatically first.

---

## 🧪 Try Your Own Data

- **Your own training data:** `python train.py my_training_data.csv`
  (it needs all 4 input columns and `final_marks`)
- **Your own prediction file:** choose option 1 and enter your file path
  (it needs the 4 input columns)
- **Change the forest:** edit `N_TREES` and `MIN_SAMPLES_LEAF` at the top of `train.py`

---

## 🔬 Bonus: See How It Works Inside

```bash
python random_forest_from_scratch.py
```

In plain Python, this shows:
- what a **bootstrap sample** looks like (about 63% unique students)
- one tree vs. a forest of 50 trees on the same test students
- how much individual trees **disagree** for one student, and how the average lands close to the real mark
- how the test score improves as you add more trees

The scores won't exactly match `train.py`: random forests are random, and this version is simpler than scikit-learn's.

---

## 💡 Discussion Questions for Students

1. A single tree scores **1.000** on training data but only 0.68 on test data. Why?
2. Why does averaging 200 trees work better than one very good tree?
3. Try the same student with coaching **Yes** and then **No**. How much does coaching change the prediction?
4. Coaching has the lowest importance (4.9%), yet it changes marks by several points. How can both be true?
5. Does high importance for `study_hours` prove that studying *causes* better marks?
