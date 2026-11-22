# Lecture 26: Project: tumour classifier (classification, end to end)

Run: `python lecture.py` (about 10 seconds)

**Goal:** classify breast tumours as malignant or benign from 30 cell measurements, where the two kinds of mistake have **very different costs**.

## Frame the problem first

| Mistake | Meaning | Cost |
|---------|---------|------|
| **False negative** | a malignant tumour called benign | 🚨 a missed cancer: very high |
| False positive | a benign tumour called malignant | an extra biopsy: inconvenient, much lower |

So the target is **recall(malignant) ≥ 0.97**, with precision as high as possible. We make **malignant = 1** (the positive class), because scikit-learn's recall and precision refer to class 1 by default. The original dataset codes malignant as 0!

## The workflow

| Step | What we do | Lectures |
|------|------------|----------|
| 1. Frame | choose the positive class, the costly error and the success metric | 05 |
| 2. Split | stratified 80/20; test set locked away | 04 |
| 3. Compare | 6 models with stratified 5-fold CV, reporting accuracy, recall, precision and ROC AUC together | 05, 07 |
| 4. Tune | `GridSearchCV` over `C` and `class_weight`, optimising **ROC AUC** (threshold-independent) | 14, 21 |
| 5. Threshold | `cross_val_predict(method="predict_proba")` gives **out-of-fold** probabilities on train; pick the highest threshold that meets the recall goal | 05, 07 |
| 6. Final test | evaluate once, at both the default and the chosen threshold | 05 |
| 7. Explain | standardised logistic coefficients | 14 |
| 8. Package | a function that returns the probability and a human-readable decision | 24 |

## Results (from `lecture.py`)

| Model (CV on train) | Accuracy | Recall | Precision | ROC AUC |
|---------------------|---------:|-------:|----------:|--------:|
| Dummy | 0.626 | 0.000 | 0.000 | 0.500 |
| **Logistic** | **0.978** | **0.959** | 0.983 | **0.995** |
| KNN | 0.965 | 0.918 | 0.987 | 0.982 |
| SVC | 0.971 | 0.947 | 0.976 | 0.994 |
| RandomForest | 0.958 | 0.935 | 0.953 | 0.987 |
| HistGB | 0.956 | 0.918 | 0.964 | 0.990 |

Tuned logistic regression: `C ≈ 0.32`, CV ROC AUC **0.995**.

**Threshold choice** (out-of-fold, training data): at 0.5 the recall is 0.947 (9 missed). At **0.4** the recall is **0.971** (5 missed) and precision is still 0.959.

**Test set (114 tumours):**

| Threshold | Recall | Precision | Missed cancers | False alarms |
|-----------|-------:|----------:|---------------:|-------------:|
| default 0.5 | 0.952 | 1.000 | 2 | 0 |
| **chosen 0.4** | **0.976** | 0.976 | **1** | 1 |

The lower threshold trades **one extra biopsy for one fewer missed cancer**. Given the costs, that's the right trade.

## Lessons from this project

1. **Accuracy alone would hide the real question.** All good models score 96–98% accuracy, but recall varies from 0.92 to 0.96.
2. **The simplest strong model won:** scaled logistic regression beat forests and boosting on this clean, roughly linear data. Always include simple baselines.
3. **Tune on a threshold-free metric** (ROC AUC), **then** choose the operating threshold for the business goal.
4. **Choose the threshold on training data** (out-of-fold predictions), never on the test set. Otherwise the final test score is no longer honest.
5. **Report the confusion matrix** in plain language ("1 missed cancer, 1 extra biopsy out of 114"). Stakeholders understand counts better than F1.

## Extension exercises

1. Make recall ≥ 0.99 the goal. What happens to precision and to the number of false alarms?
2. Repeat the threshold analysis with the SVC model (use `CalibratedClassifierCV` for probabilities).
3. Use `TunedThresholdClassifierCV` (scikit-learn ≥ 1.5) to choose the threshold automatically for a custom cost.
4. Remove the 10 least important features (smallest |coef|). Does recall change?

**Next →** [Lecture 27: Practice exercises](../27_practice_exercises/)
