# 🎓 Student Marks Prediction: Decision Tree Regressor Demo

This demo predicts a student's **final exam marks (out of 100)** from **one input: study hours per day**, using a **Decision Tree Regressor**.

Instead of an equation, the model learns a set of **yes/no questions**:

```
Is study_hours <= 4.65?
├── YES → Is study_hours <= 2.60? → ...
└── NO  → Is study_hours <= 5.10? → ...
                                   → predict 75.5 marks
```

Each final box (**leaf**) predicts the **average marks** of the training students who landed in it.

**About the data:** marks rise with study hours, then level off and dip slightly after about 8 hours (tiredness). It's also noisy, like real students. A straight line can't follow this shape; a tree can.

> New to decision trees? Read **[DECISION_TREE_GUIDE.md](DECISION_TREE_GUIDE.md)** first.

---

## 📁 Project Files

| File | What it is |
|------|------------|
| `train.csv` | **Training data**: 120 students with their study hours **and** actual final marks |
| `predict.csv` | **New data**: 10 students with study hours only. Marks are unknown, so we predict them |
| `train.py` | Trains the tree, compares it with a straight line and an unlimited tree, prints the tree, saves `model.pkl` |
| `predict.py` | **Interactive demo**: predict from a CSV file **or** from hours you type in (shows the questions the tree asks) |
| `decision_tree_from_scratch.py` | Teaching file that builds the same tree in plain Python (no ML library) |
| `requirements.txt` | Python packages needed |
| `README.md` | This file (how to run the demo) |
| `DECISION_TREE_GUIDE.md` | Teaching notes: what a decision tree is and how it works |

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
[3] Evaluating ...
    Model                     Train R²   Test R²    Test MAE
    Straight line                0.824     0.773    6.19 marks
    Tree, depth 3                0.936     0.912    4.05 marks
    Tree, no depth limit         0.968     0.792    6.05 marks
    Straight line : too simple for the curved pattern -> UNDERFITTING
    No depth limit: memorises training students (high Train R²) but does
                    worse on new students (lower Test R²) -> OVERFITTING

[4] The tree the model learned (7 leaves):

|--- study_hours <= 4.65
|   |--- study_hours <= 2.60
|   |   |--- study_hours <= 1.25
|   |   |   |--- value: [27.74]
|   |   |--- study_hours >  1.25
|   |   |   |--- value: [36.49]
|   |--- study_hours >  2.60
|   |   |--- study_hours <= 3.10
|   |   |   |--- value: [45.03]
|   |   |--- study_hours >  3.10
|   |   |   |--- value: [55.13]
|--- study_hours >  4.65
|   |--- study_hours <= 5.10
|   |   |--- value: [65.01]
|   |--- study_hours >  5.10
|   |   |--- study_hours <= 6.50
|   |   |   |--- value: [75.45]
|   |   |--- study_hours >  6.50
|   |   |   |--- value: [81.17]
```

The depth-3 tree is the best of the three on students it has never seen. The model is saved as `model.pkl`.

### Step 2: Predict

```bash
python predict.py
```

You'll see a menu:

```
==================================================
   STUDENT MARKS PREDICTION (Decision Tree)
==================================================
  Model: tree with depth 3 and 7 leaves

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
      N001            1             27.7
      N002            2             36.5
      N003            3             45.0
      N004            4             55.1
      N005            5             65.0
      N006            6             75.5
      N007            7             81.2
      N008            8             81.2
      N009            9             81.2
      N010           10             81.2

Note: students who land in the same leaf get exactly the same prediction.
```

Notice that 7, 8, 9 and 10 hours all get **81.2**: they fall in the same leaf. A tree predicts in **steps**, not a smooth line.

#### Option 2: Predict from user input

Type in the study hours and see the path through the tree:

```
Enter study hours per day (0-24): 6
  The tree asks:
    1. Is study_hours <= 4.65?  NO
    2. Is study_hours <= 5.10?  NO
    3. Is study_hours <= 6.50?  YES
  -> Reached a leaf with 15 training students, average marks 75.5
  >>> Predicted final marks: 75.5 / 100

Predict another? (y/n): y

Enter study hours per day (0-24): 15
  The tree asks:
    1. Is study_hours <= 4.65?  NO
    2. Is study_hours <= 5.10?  NO
    3. Is study_hours <= 6.50?  NO
  -> Reached a leaf with 46 training students, average marks 81.2
  >>> Predicted final marks: 81.2 / 100
  NOTE: 15.0 hours is outside the training range (0.7-10.0). A tree can't
  extrapolate: it just uses the nearest leaf.
```

> If `model.pkl` doesn't exist yet, `predict.py` trains the model automatically first.

---

## 🧪 Try Your Own Data

- **Your own training data:** `python train.py my_training_data.csv`
  (it needs `study_hours` and `final_marks` columns)
- **Your own prediction file:** choose option 1 and enter your file path
  (it only needs a `study_hours` column)
- **Change the tree's size:** edit `MAX_DEPTH` and `MIN_SAMPLES_LEAF` at the top of `train.py`

---

## 🔬 Bonus: See How It Works Inside

```bash
python decision_tree_from_scratch.py
```

This shows how the first split is chosen (trying split points and comparing their error), then builds the whole tree in plain Python. It finds **exactly the same tree** as scikit-learn. Read `DECISION_TREE_GUIDE.md` alongside it.

---

## 💡 Discussion Questions for Students

1. Why do students with 7 and 10 study hours get the same prediction?
2. Why does the unlimited tree score higher on training data but lower on test data?
3. What does the tree predict for 15 hours? How is that different from what linear or polynomial regression would do?
4. What would happen with `MAX_DEPTH = 1`? Draw the tree.
