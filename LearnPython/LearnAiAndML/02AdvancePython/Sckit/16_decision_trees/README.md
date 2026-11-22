# Lecture 16: Decision trees

Run: `python lecture.py`

## The idea: a flowchart of yes/no questions

```
            petal width <= 0.8 ?
            /                 \
         yes                   no
       setosa          petal width <= 1.75 ?
                        /              \
                   versicolor        virginica
```

A tree learns the questions from data. At each node it tries **every feature and every threshold** and picks the split that makes the two groups **purest**.

## How "purity" is measured

| Criterion | Task | Formula idea |
|-----------|------|--------------|
| **Gini impurity** (default) | classification | chance of mislabelling a random sample with the node's class mix: 0 = pure |
| **Entropy / log_loss** | classification | information-theory version; very similar results |
| **squared_error** (default) | regression | variance within the node; leaves predict the **mean** |
| absolute_error, poisson | regression | for outliers / count data |

Splitting continues until leaves are pure or a stopping rule kicks in.

## Controlling complexity (the hyperparameters that matter)

An unrestricted tree grows until it **memorises** the training data (train accuracy 1.0, test worse: Lecture 04).

| Parameter | Effect |
|-----------|--------|
| `max_depth` | maximum number of questions on any path: the main knob |
| `min_samples_split` | a node needs at least this many samples to be split |
| `min_samples_leaf` | every leaf must have at least this many samples (smooths predictions) |
| `max_leaf_nodes` | cap on the total number of leaves |
| `max_features` | consider only a random subset of features at each split (used by forests) |
| `ccp_alpha` | **cost-complexity pruning**: grow a full tree, then prune branches that add little. `cost_complexity_pruning_path` lists candidate alphas |
| `class_weight="balanced"` | for imbalanced classes |

## Reading a tree

| Tool | Shows |
|------|-------|
| `export_text(tree, feature_names=...)` | the rules as indented text |
| `plot_tree(tree)` | a drawing (needs matplotlib) |
| `tree.get_depth()`, `tree.get_n_leaves()` | size |
| `tree.feature_importances_` | total impurity reduction per feature (sums to 1) |
| `tree.predict_proba` | the class mix in the leaf a sample lands in |
| `tree.apply(X)` | which leaf each sample ends up in |

## Strengths and weaknesses

| ✅ | ❌ |
|----|----|
| **explainable**: you can print the rules | a single tree **overfits** easily |
| **no scaling** needed; handles mixed feature scales | **unstable**: small data changes can produce a very different tree |
| captures non-linear patterns and interactions | boundaries are axis-aligned "staircases" |
| fast to train and predict; handles NaN (since 1.3) | usually beaten by ensembles of trees (Lecture 17) |

## When to use

✅ When you must **explain** decisions with simple rules (credit policies, triage); as a building block for forests and boosting; quick exploration of which features matter.

❌ When you need the best accuracy: use a random forest or gradient boosting.

## Exercises

1. Print the rules of a depth-3 tree on iris. How many leaves does it have?
2. Sweep `min_samples_leaf` (1, 5, 20, 50) on the breast-cancer data and compare train vs test scores.
3. Use `cost_complexity_pruning_path` and choose `ccp_alpha` by cross-validation.
4. Fit a `DecisionTreeRegressor` on `sin(x)` and see the step-shaped predictions.

**Next →** [Lecture 17: Ensembles: forests & boosting](../17_ensembles_forests_boosting/)
