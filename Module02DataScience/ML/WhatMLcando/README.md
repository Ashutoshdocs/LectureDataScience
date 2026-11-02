# Python vs Machine Learning — Beginner Demo

## Goal

Compare two ways to solve the same problem:

**Question:** Based on how many hours a student studies, will the student pass?

- `without_ml.py`: a Python programmer writes a fixed rule.
- `with_ml.py`: a machine-learning model learns a pattern from historical examples.

## 1. Setup

Use Python 3. Install the one dependency:

```bash
python -m pip install scikit-learn
```

## 2. Run the traditional Python program

```bash
python without_ml.py
```

Explain to learners:

1. The programmer decides the condition: 5 hours or more means PASS.
2. Python executes exactly that condition.
3. The computer has not learned anything from data.
4. If the rule is unsuitable, the programmer must change the code.

## 3. Run the machine-learning program

```bash
python with_ml.py
```

Explain to learners:

1. We give the program historical examples: study hours and actual results.
2. `X_train` contains the input feature (study hours).
3. `y_train` contains the known labels (0 = FAIL, 1 = PASS).
4. `model.fit()` trains the model by finding a pattern in the examples.
5. `model.predict()` predicts the result for a new student.
6. `predict_proba()` gives the model's estimated probability for PASS.

## 4. The key comparison

| Traditional Python | Machine Learning |
|---|---|
| Programmer writes the decision rule | Programmer supplies data, features and a learning method |
| Uses explicit conditions | Learns patterns/parameters from examples |
| Same rule until code changes | Model can change when retrained with new data |
| Best when rules are clear | Useful when patterns are hard to write as fixed rules |

## 5. Teaching discussion

Ask students:

- What happens if the fixed rule changes from 5 hours to 4 hours?
- What happens if we add more historical examples and train the ML model again?
- Does ML guarantee a correct answer? **No.** Predictions depend on data quality, representativeness and model choice.

## Important clarification

This is a deliberately tiny teaching example, not a real student assessment system.
Study hours alone cannot reliably determine whether someone will pass. The training
data is small and illustrative. In real projects, use representative data, evaluate
on separate test data, and consider other relevant factors.

## One-line takeaway

**Traditional programming:** Data + rules written by a programmer -> answer.

**Machine learning:** Data + known answers + learning algorithm -> trained model that predicts answers for new data.
