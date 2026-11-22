# Lecture 17: Ensembles: random forests, gradient boosting & voting

Run: `python lecture.py`

## The wisdom of crowds

One decision tree is unstable and overfits. **Many** models combined, each wrong in a *different* way, average out their mistakes. That's an **ensemble**.

| Family | How models are combined | Reduces | scikit-learn |
|--------|-------------------------|---------|--------------|
| **Bagging** | many models trained **independently** on random bootstrap samples; average/vote | variance (overfitting) | `BaggingClassifier`, **`RandomForest*`**, `ExtraTrees*` |
| **Boosting** | models trained **one after another**, each fixing the previous ones' errors | bias (underfitting) | **`GradientBoosting*`**, **`HistGradientBoosting*`**, `AdaBoost*` |
| **Voting / stacking** | different model types combined | both | `VotingClassifier`, `StackingClassifier` |

## Random forest

Each tree sees (1) a **bootstrap sample** of the rows (drawn with replacement) and (2) a **random subset of features at every split**. This makes the trees different from each other; then they vote.

| Parameter | Meaning | Tip |
|-----------|---------|-----|
| `n_estimators` | number of trees | adding trees doesn't cause overfitting: the CV score rises, then levels off (small ups and downs on one test split are noise); 200–500 is common |
| `max_features` | features tried per split (`"sqrt"` default for classification) | lower = more diverse trees |
| `max_depth`, `min_samples_leaf` | tree size | forests usually work fine with deep trees |
| `oob_score=True` | evaluate each tree on the rows it **didn't** see (out-of-bag) | a free validation score |
| `n_jobs=-1` | use all CPU cores | |
| `class_weight="balanced"` | for imbalance | |

✅ An excellent **default for tabular data**: little tuning, no scaling, robust, gives `feature_importances_`.

## Gradient boosting

Start with a simple prediction, then repeatedly add a **small tree that predicts the remaining errors** (residuals). Each tree's contribution is multiplied by the **`learning_rate`**.

| Parameter | Meaning | Trade-off |
|-----------|---------|-----------|
| `n_estimators` / `max_iter` | number of boosting rounds | too many → overfits (unlike forests!) |
| `learning_rate` | how much each tree counts | smaller = needs more rounds, usually generalises better |
| `max_depth` / `max_leaf_nodes` | size of each small tree | shallow trees (3–8 levels) are typical |
| `early_stopping` + `validation_fraction` + `n_iter_no_change` | stop automatically when the validation score stops improving | strongly recommended |
| `subsample < 1` | stochastic boosting | adds randomness, reduces overfitting |

### `HistGradientBoostingClassifier/Regressor`: use this one

It bins features into histograms, so it's **much faster** on large data (10k+ rows). It also **handles NaN natively**, supports `categorical_features`, and has early stopping built in. It's scikit-learn's answer to LightGBM and XGBoost.

## Forest vs boosting

| | Random forest | Gradient boosting |
|--|---------------|-------------------|
| trees | deep, independent, parallel | shallow, sequential |
| tuning needed | little | more (learning rate, rounds, depth) |
| overfitting from more trees | no | yes, so use early stopping |
| typical accuracy | very good | often the best on tabular data |

## Voting & stacking

- `VotingClassifier(estimators=[...], voting="soft")` averages the predicted probabilities of different models.
- `StackingClassifier` trains a final model on the base models' (cross-validated) predictions.

They help most when the base models are **good and different** (e.g. logistic regression + forest + KNN).

## Exercises

1. Plot (print) the forest's test accuracy for `n_estimators` = 1, 5, 20, 100, 500.
2. Compare the `oob_score_` with the cross-validated score.
3. Gradient boosting: compare `learning_rate` 1.0 vs 0.1 vs 0.01 with 300 trees.
4. Build a soft `VotingClassifier` from three different models and compare it with each one alone.

**Next →** [Lecture 18: Support vector machines](../18_svm/)
