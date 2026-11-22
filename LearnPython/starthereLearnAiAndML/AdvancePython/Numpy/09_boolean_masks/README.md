# Lecture 09 — Boolean masks: filter with a condition

Run: `python lecture.py`

## The idea

Comparing an array with a value gives a **boolean array** — a **mask** — with `True` where the condition holds.

```
marks : 45     82    67    91    38     74
mask  : False  True  True  True  False  True      (marks >= 50)
result:        82    67    91           74        marks[mask]
```

Putting the mask inside `[ ]` keeps only the `True` positions. This is the NumPy way to **filter** — no loop, no `if`.

## What you can do with a mask

| Code | Does |
|------|------|
| `marks[marks > 80]` | keep matching values |
| `(marks > 80).sum()` | **count** matches (True = 1, False = 0) |
| `(marks > 80).mean()` | **fraction** that match |
| `marks[marks < 50] = 50` | change only the matching values |
| `np.where(marks > 80)[0]` | **positions** of matches |
| `names[marks > 80]` | use a mask from one array to pick from **another** |

## Combining conditions

| Operator | Meaning |
|----------|---------|
| `&` | and |
| `\|` | or |
| `~` | not |

**Put each condition in brackets**, because `&` binds tighter than `>`:

```python
marks[(marks > 60) & (marks < 80)]   # ✅
marks[marks > 60 & marks < 80]       # ❌ error / wrong result
```

> ⚠️ Python's `and` / `or` don't work on arrays: `ValueError: The truth value of an array with more than one element is ambiguous`. Use `&` and `|`.

## Expected output (first part)

```
[False  True  True  True False  True]
[82 67 91 74]
[82 91]
Passed: 4 of 6
[67 74]
[50 82 67 91 50 74]
```

## Exercises

1. Print marks below 40 **or** above 90.
2. Count how many marks are even: `(marks % 2 == 0).sum()`.
3. What percentage of students passed?
4. Print the names of students who scored above 70.

<details><summary>Solutions</summary>

```python
marks[(marks < 40) | (marks > 90)]   # [91 38]
(marks % 2 == 0).sum()               # 3  (82, 38, 74)
(marks >= 50).mean() * 100           # 66.67
names[marks > 70]                    # see lecture.py
```
</details>

**Next →** [Lecture 10: Views vs copies](../10_views_vs_copies/)
