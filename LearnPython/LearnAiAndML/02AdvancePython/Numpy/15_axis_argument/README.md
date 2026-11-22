# Lecture 15 — The `axis` argument

Run: `python lecture.py`

On a 2D array, statistics can work on **everything**, **down each column**, or **across each row**.

```
                 Maths  Science  English
student 0   [[    78,      85,      62],
student 1    [    92,      88,      79],
student 2    [    55,      70,      81],
student 3    [    83,      64,      90]]

        axis=0 ↓  (down the rows → one result per COLUMN)
        axis=1 →  (across the columns → one result per ROW)
```

| Call | Collapses | One result per | Shape here |
|------|-----------|----------------|------------|
| `marks.mean()` | everything | whole table | scalar |
| `marks.mean(axis=0)` | the rows ↓ | **column** (subject) | `(3,)` |
| `marks.sum(axis=1)` | the columns → | **row** (student) | `(4,)` |

> **Memory trick:** the axis you name is the one that **disappears**. Shape `(4, 3)` with `axis=0` → `(3,)`; with `axis=1` → `(4,)`.

## Works with almost everything

`sum`, `mean`, `min`, `max`, `argmin`, `argmax`, `std`, `median`, `cumsum`, `sort`, `any`, `all`, `concatenate` … all accept `axis=`.

## `keepdims=True`

Keeps the collapsed axis as size 1 — handy for broadcasting back:

```python
row_means = marks.mean(axis=1, keepdims=True)   # shape (4, 1)
marks - row_means                               # each student relative to their own average
```

## 3D and beyond

For shape `(2, 3, 4)`: `axis=0` → `(3, 4)`, `axis=1` → `(2, 4)`, `axis=2` → `(2, 3)`. Negative axes count from the end: `axis=-1` = last axis.

## Exercises

1. Each student's lowest mark: `marks.min(axis=1)`.
2. Which subject has the best average? Use `argmax`.
3. How many students scored above 80 in each subject?

<details><summary>Solutions</summary>

```python
marks.min(axis=1)                       # [62 79 55 64]
subjects[marks.mean(axis=0).argmax()]   # 'English'
(marks > 80).sum(axis=0)                # [2 2 2]
```
</details>

**Next →** [Lecture 16: Reshape, sort & join](../16_reshape_sort_join/)
