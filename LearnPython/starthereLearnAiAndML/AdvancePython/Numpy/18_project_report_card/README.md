# Lecture 18 — Project: class report card

Run: `python lecture.py`

A complete mini-project using everything so far. With lists this would need nested loops; with NumPy each question is one line.

## The data

- `names` — 5 students (1D)
- `subjects` — 4 subjects (1D)
- `marks` — a 5 × 4 table: rows = students, columns = subjects

## Questions and the NumPy tool for each

| Question | NumPy tool | Lecture |
|----------|-----------|---------|
| Each student's percentage | `marks.mean(axis=1)` | 15 |
| Grades A / B / C | nested `np.where` | 05, 11 |
| Who topped? | `argmax` + index into `names` | 14 |
| Average per subject | `marks.mean(axis=0)` | 15 |
| Hardest subject | `argmin` on subject averages | 14 |
| Fails per subject | mask `marks < 50` + `sum(axis=0)` | 09, 15 |
| Class ranking | `argsort` | 16 |
| Each student vs class average | broadcasting | 12 |

## Nested `np.where` for grades

```python
grade = np.where(percent >= 80, "A",
        np.where(percent >= 60, "B", "C"))
```
Read it as: *if ≥ 80 then A, else (if ≥ 60 then B, else C)*.

For many grade bands, `np.select` is cleaner:

```python
np.select([percent >= 90, percent >= 80, percent >= 60], ["A+", "A", "B"], default="C")
```

## `.tolist()`

Converts arrays back to normal Python lists — handy for building a dict or JSON.

## Expected output (first part)

```
Asha    78.8%  grade B
Ravi    88.5%  grade A
Meena   51.2%  grade C
John    78.5%  grade B
Zara    69.8%  grade B
Topper: Ravi
Subject averages: {'Maths': 73.0, 'Science': 72.4, 'English': 71.4, 'CS': 76.6}
Hardest subject: English
Failed (<50) per subject: [1 0 0 1]
```

## Extension exercises

1. Add a sixth student row and a matching name.
2. Give 5 grace marks to everyone in the hardest subject (cap at 100 with `np.clip`).
3. Print each student's best subject.
4. Which students failed *any* subject? (`(marks < 50).any(axis=1)`)

<details><summary>Hints</summary>

```python
marks = np.vstack([marks, [70, 75, 80, 85]]); names = np.append(names, "Ali")
h = marks.mean(axis=0).argmin(); marks[:, h] = np.clip(marks[:, h] + 5, 0, 100)
subjects[marks.argmax(axis=1)]
names[(marks < 50).any(axis=1)]
```
</details>

**Next →** [Lecture 19: Project — weather week](../19_project_weather_week/)
