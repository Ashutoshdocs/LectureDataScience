# Lecture 22: Clustering (unsupervised learning)

Run: `python lecture.py`

## No labels: find the groups

In clustering there is **no `y`**. The algorithm groups samples that are similar to each other. Typical uses: **customer segmentation**, grouping documents, image colour compression, anomaly detection, and exploring a new dataset.

```python
km = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = km.fit_predict(X)        # a cluster number for every row
```

Cluster numbers are just **names**: cluster 2 isn't "bigger" than cluster 0, and the numbering can change between runs.

## K-Means

```
1. place k centres          2. assign every point to its nearest centre
3. move each centre to the mean of its points          4. repeat 2–3 until nothing changes
```

| Parameter / attribute | Meaning |
|-----------------------|---------|
| `n_clusters` | **you must choose k** |
| `n_init` | restarts from different random centres; the best result (lowest inertia) is kept |
| `cluster_centers_` | the centres, in the scaled feature space |
| `labels_` | cluster of each training point |
| `inertia_` | sum of squared distances to the nearest centre: lower = tighter clusters |
| `predict(X_new)` | assign new points to the nearest centre |

**Assumptions:** clusters are roughly **round** (spherical), similar in size, and features are **scaled**. K-Means fails on moons, rings and elongated shapes.

`MiniBatchKMeans` is a faster variant for very large datasets.

## Choosing k

| Method | How | Pick |
|--------|-----|------|
| **Elbow** | plot `inertia_` vs k | the "bend" where adding clusters stops helping much (inertia **always** falls as k grows) |
| **Silhouette score** | `silhouette_score(X, labels)`: how much closer each point is to its own cluster than to the next one, from −1 to 1 | the **maximum** |
| Domain sense | "marketing can handle 4 segments" | what's useful |

## DBSCAN: clusters of any shape, plus noise

DBSCAN groups points in **dense regions**. A point with at least `min_samples` neighbours within distance `eps` is a core point, and clusters grow from core points.

| ✅ | ❌ |
|----|----|
| finds **any shape** (moons, rings) | sensitive to `eps` (scale the data!) |
| **no k needed** | struggles when clusters have very different densities |
| marks outliers as **noise (label −1)** | no `predict` for new points |

`HDBSCAN` is a newer variant that needs less tuning (no `eps`).

## Agglomerative (hierarchical) clustering

It starts with every point as its own cluster and repeatedly **merges the two closest clusters**. `linkage="ward"` (compact clusters), `"average"`, `"complete"` and `"single"` (can follow chains and shapes) decide what "closest" means. It's useful when you want a hierarchy (dendrogram).

## Evaluating clusters

| Have true labels? | Metric |
|-------------------|--------|
| no (the usual case) | `silhouette_score` (higher is better), `davies_bouldin_score` (lower is better) |
| yes (benchmarking only) | `adjusted_rand_score` (1 = perfect agreement, ~0 = random); ignores label numbering |

## Exercises

1. Run the elbow method and the silhouette score for k = 2…8 on scaled iris.
2. Compare K-Means and DBSCAN on `make_moons`.
3. Segment the customers in `lecture.py` and describe each segment in words.
4. Use K-Means to compress the colours of a random "image" array to 4 colours.

**Next →** [Lecture 23: PCA](../23_pca_dimensionality_reduction/)
