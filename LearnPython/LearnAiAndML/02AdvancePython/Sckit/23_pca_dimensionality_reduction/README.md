# Lecture 23: PCA: dimensionality reduction

Run: `python lecture.py`

## Why reduce dimensions?

| Problem | How fewer features help |
|---------|-------------------------|
| you can't *see* 30-dimensional data | squeeze it to 2-D or 3-D for a scatter plot |
| many **correlated** features (height in cm and in inches; 64 neighbouring pixels) | combine them into a few informative directions |
| slow training, the curse of dimensionality (KNN) | faster, sometimes more accurate models |
| noise | the low-variance directions are often mostly noise |

## What PCA does

**Principal Component Analysis** finds new axes (**principal components**) that are:
1. **combinations** of the original features,
2. ordered by how much of the data's **variance** they capture (PC1 the most),
3. **uncorrelated** with each other (perpendicular).

Keeping only the first few components keeps most of the information in far fewer columns.

```python
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)
pca.explained_variance_ratio_      # share of variance per component, e.g. [0.73, 0.23]
pca.components_                    # loadings: how much each original feature contributes
pca.inverse_transform(X_2d)        # approximate reconstruction in the original space
```

## How many components?

| `n_components=` | Meaning |
|-----------------|---------|
| integer, e.g. `2` | exactly that many (visualisation) |
| float, e.g. `0.95` | as many as needed to keep **95% of the variance** |
| `None` | all; inspect `np.cumsum(explained_variance_ratio_)` first |

## Rules

1. **Scale first.** PCA follows variance, so a feature in big units would dominate PC1. Use `make_pipeline(StandardScaler(), PCA(...), model)`.
2. Fit PCA on **training data only** (pipelines handle this).
3. Components are **harder to interpret** than the original features. Read `components_` (loadings) to see what each one mixes.
4. PCA is **linear**. For curved structure in visualisations, look at `TSNE` (visualisation only: no `transform` for new data) or `KernelPCA`.
5. PCA is **unsupervised**: it ignores `y`. The highest-variance directions aren't guaranteed to be the most predictive. Check with cross-validation.

## Related tools

`TruncatedSVD` (works on sparse text matrices; "LSA"), `KernelPCA` (non-linear), `IncrementalPCA` (data that doesn't fit in memory), `TSNE` (2-D visualisation of clusters).

## Exercises

1. How many components keep 90%, 95% and 99% of the variance of the digits data?
2. Compare the CV accuracy of logistic regression on all 30 breast-cancer features vs 2, 5 and 10 components.
3. Print the loadings of PC1 for the wine data. Which features dominate?
4. Reconstruct a digit from 5, 15 and 40 components and print the reconstruction error.

**Next →** [Lecture 24: Saving models & custom transformers](../24_saving_and_custom_transformers/)
