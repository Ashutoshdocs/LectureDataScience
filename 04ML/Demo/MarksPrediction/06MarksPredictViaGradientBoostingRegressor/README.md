# 🎓 Student Marks Prediction: Gradient Boosting Regressor Demo

This demo predicts a student's **final exam marks (out of 100)** from **four inputs** using a **Gradient Boosting Regressor**:

| Input | Meaning |
|-------|---------|
| `study_hours` | Hours of self-study per day |
| `coaching` | Does the student attend coaching classes? (Yes / No) |
| `live_sessions_attended` | Live online sessions attended (out of 20) |
| `recorded_course_completion` | % of the recorded video course watched (0–100) |

**Gradient boosting** builds **small trees one after another**. Each new tree learns to fix the **mistakes** the previous trees still make. The final prediction is the starting guess plus all the small corrections:

```
 prediction = average marks
            + 0.05 × (tree 1's correction)
            + 0.05 × (tree 2's correction)
            + ...
            + 0.05 × (tree 300's correction)
```

**Random forest vs. gradient boosting:**
- **Random forest:** 200 big trees built **independently**, then **averaged** (a team voting)
- **Gradient boosting:** 300 small trees built **in sequence**, each **correcting** the last (a student revising answers again and again)

> New to gradient boosting? Read **[GRADIENT_BOOSTING_GUIDE.md](GRADIENT_BOOSTING_GUIDE.md)** first.
> It helps to know decision trees and random forests first (see those demos).

---

## 📁 Project Files

| File | What it is |
|------|------------|
| `train.csv` | **Training data**: 400 students with all 4 inputs **and** their actual final marks |
| `predict.csv` | **New data**: 12 students with inputs only. Marks are unknown, so we predict them |
| `train.py` | Trains the model, compares it with the other models in this series, shows the error falling tree by tree, saves `model.pkl` |
| `predict.py` | **Interactive demo**: predict from a CSV file **or** from details you type in (shows the prediction being built tree by tree) |
| `gradient_boosting_from_scratch.py` | Teaching file that builds gradient boosting in plain Python (no ML library) |
| `requirements.txt` | Python packages needed |
| `README.md` | This file (how to run the demo) |
| `GRADIENT_BOOSTING_GUIDE.md` | Teaching notes: what gradient boosting is and how it works |

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

**Patterns hidden in the data** (the model has to discover these on its own):
- Study hours help a lot at first, then the benefit **levels off**
- Live sessions also have **diminishing returns**
- Coaching adds marks
- The recorded course helps **more for students without coaching**

*Note: this is synthetic (generated) data made for teaching. It uses the same columns as the Random Forest demo, but has 400 students instead of 200.*

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
[3] Evaluating against the other models in this series ...
    Model                       Train R²   Test R²    Test MAE
    Linear regression              0.819     0.765    3.20 marks
    Single decision tree           1.000     0.634    4.03 marks
    Random forest (200)            0.954     0.817    2.80 marks
    Gradient boosting (300)        0.937     0.872    2.42 marks

    How the error changes as trees are added:
      Trees   Train RMSE   Test RMSE
          1       9.07        8.16
         10       7.28        6.78
         50       3.93        4.16
        100       2.88        3.32
        200       2.51        3.02
        300       2.34        3.00
    Each tree fixes part of the remaining error, so the error keeps falling.

[4] Feature importance (which inputs the model relied on most):
    study_hours                  47.3%  ████████████████████████
    live_sessions_attended       25.5%  █████████████
    recorded_course_completion   17.0%  ████████
    coaching                     10.2%  █████
```

Gradient boosting is the most accurate model on students it has never seen. The model is saved as `model.pkl`.

### Step 2: Predict

```bash
python predict.py
```

You'll see a menu:

```
==================================================
   STUDENT MARKS PREDICTION (Gradient Boosting)
==================================================
  Model: 300 small trees, added one after another
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
      N001          7.9       No                      17                          28             63.5
      N002          2.1       No                       9                          41             47.0
      N003          7.3       No                       0                          33             46.6
      N004          7.6      Yes                      14                          75             72.8
      ...
Saved results to 'predictions_output.csv'.
```

The `coaching` column can be `Yes`/`No`, `Y`/`N` or `1`/`0`.

#### Option 2: Predict from user input

Type in one student's details and watch the prediction being built:

```
Enter the student's details:
  Study hours per day [0-24]: 6
  Takes coaching classes? (y/n): y
  Live sessions attended (out of 20) [0-20]: 15
  Recorded course completed (%) [0-100]: 80

  How the prediction is built, one tree at a time:
    Start with the average of all students     : 59.4
    Tree 1 says 'add +7.1', × learning rate 0.05 = +0.35  -> 59.7
    After   5 trees                             : 61.0
    After  10 trees                             : 62.2
    After  25 trees                             : 65.3
    After  50 trees                             : 68.1
    After 100 trees                             : 70.7
    After 200 trees                             : 71.8
    After 300 trees                             : 71.7

  >>> Predicted final marks: 71.7 / 100

Predict another student? (y/n):
```

Each tree nudges the prediction a little. Big steps early on, tiny adjustments at the end.

> If `model.pkl` doesn't exist yet, `predict.py` trains the model automatically first.

---

## 🧪 Try Your Own Data

- **Your own training data:** `python train.py my_training_data.csv`
  (it needs all 4 input columns and `final_marks`)
- **Your own prediction file:** choose option 1 and enter your file path
  (it needs the 4 input columns)
- **Change the model:** edit `N_TREES`, `LEARNING_RATE`, `MAX_DEPTH` and `SUBSAMPLE` at the top of `train.py`

---

## 🔬 Bonus: See How It Works Inside

```bash
python gradient_boosting_from_scratch.py
```

In plain Python, this shows:
- step 0: predicting the average for everyone
- **tree 1**, trained on the residuals (mistakes) of step 0, and the corrections it learned
- the training and test error falling as trees are added
- one student's prediction moving from the average towards their real marks, tree by tree

The scores won't exactly match `train.py` (this version uses a different random split and no subsampling).

---

## 💡 Discussion Questions for Students

1. Why does gradient boosting use **small** trees (depth 2), while a random forest uses **big** ones?
2. Why multiply each tree's correction by 0.05 instead of using all of it?
3. In the error table, the test error almost stops improving after 200 trees. What might happen with 2,000 trees?
4. Random forest trees can be built at the same time on different computers. Can gradient boosting trees? Why not?
5. Try the same student with coaching **Yes** then **No**. How many marks does coaching add?
