# Scikit-learn: Beginner to Medium Class Demo

Five hands-on modules explaining why scikit-learn is useful beyond basic Python file handling and NumPy.

## Why use scikit-learn?
Python and NumPy provide file I/O and numerical operations. Scikit-learn adds a consistent machine-learning workflow: preprocessing, train/test splitting, model training (`fit`), prediction (`predict`), evaluation, cross-validation, pipelines, and hyperparameter tuning.

## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```
Run scripts from this project root, e.g.:
```bash
python 01_ml_basics_and_workflow/01_first_model.py
```

## Course sequence
1. ML basics, features/target, fit/predict, train/test split.
2. Preprocessing: missing values, scaling, encoding, pipelines.
3. Regression: predicting numerical values with simple and multiple linear regression.
4. Classification: predicting categories with Logistic Regression and Decision Trees.
5. Evaluation and model selection: metrics, cross-validation, GridSearchCV.

Features (X) are inputs; target (y) is what we predict. `fit()` learns from training data. `predict()` makes predictions. Keep test data separate from training and model tuning.

These are classroom demonstrations, not production-ready models. Small sample datasets do not guarantee real-world performance.
