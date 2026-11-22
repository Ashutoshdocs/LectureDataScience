# Lecture 00: Prerequisites, what you need before pandas

pandas sits on top of Python **and** NumPy. You need a handful of skills from each first.

Run the examples: `python lecture.py`

---

## Checklist

| Skill | You should be able to… | Why pandas needs it |
|-------|------------------------|---------------------|
| Lists & loops | index, slice, loop, comprehensions | Columns start life as lists |
| **Dictionaries** | `{"name": "Asha", "age": 34}`, `d["name"]`, `d.keys()` | A DataFrame is built from a dict of columns, and a row looks like a dict |
| List of dicts | `[{"a": 1}, {"a": 2}]` | The shape of JSON / API data, which pandas reads directly |
| Functions & lambda | `def f(x): ...`, `lambda x: x * 2` | Used with `apply`, `map`, `agg` |
| f-strings | `f"{price:,.2f}"` | Printing reports |
| **NumPy arrays** | `np.array`, vectorized maths, `dtype` | Every pandas column *is* a NumPy-style array |
| **Boolean masks** | `a[a > 5]`, `&`, `|`, `~` with brackets | Filtering rows works exactly the same way |
| `axis` | `axis=0` down columns, `axis=1` across rows | Same meaning in pandas |
| `np.where`, `np.nan` | vectorized if/else, missing values | Used constantly in pandas |
| Files & paths | what a CSV file is, relative vs absolute path | `pd.read_csv("data/sales.csv")` |

If NumPy feels shaky, do the NumPy course first, at least lectures 01–09.

---

## 1. Dictionaries: the key to pandas

```python
student = {"name": "Asha", "maths": 78, "science": 85}
student["maths"]          # 78
student["english"] = 62   # add a key
for key, value in student.items():
    print(key, value)
```

## 2. Two ways to store a table in plain Python

**Dict of lists (column-oriented)**, which is how a DataFrame thinks:
```python
table = {
    "name":  ["Asha", "Ravi", "Meena"],
    "maths": [78, 92, 45],
}
```

**List of dicts (row-oriented)**, which is how JSON / APIs deliver data:
```python
rows = [
    {"name": "Asha",  "maths": 78},
    {"name": "Ravi",  "maths": 92},
    {"name": "Meena", "maths": 45},
]
```

Both become a DataFrame with one call: `pd.DataFrame(table)` or `pd.DataFrame(rows)`.

## 3. The pain of plain-Python tables

With the structures above, try to answer:
- *What is the average maths mark?* You need a loop or comprehension.
- *Who scored above 60?* Another loop with `if`.
- *Sort by maths mark.* Use `sorted(rows, key=lambda r: r["maths"])`.
- *Average mark per class?* You need a dict of lists, a loop, and then more loops.
- *Read a 1-million-row CSV?* You need the `csv` module, manual type conversion, and a lot of memory.

`lecture.py` does all of these the hard way. In pandas, each one is a single line.

## 4. lambda: tiny one-line functions

```python
double = lambda x: x * 2
sorted(rows, key=lambda r: r["maths"])
```

## 5. NumPy recap

```python
import numpy as np
marks = np.array([78, 92, 45])
marks.mean()           # 71.67
marks[marks > 60]      # [78 92]
np.where(marks >= 50, "pass", "fail")
```

pandas uses all of this. It adds **labels** (column names, row index), **mixed types per column**, **missing-value handling**, **file I/O** and **grouping**.

## 6. Installing

```bash
python -m pip install pandas matplotlib openpyxl
python -c "import pandas as pd; print(pd.__version__)"
```

The convention is always `import pandas as pd`.

---

## Exercises

1. Turn `rows` (list of dicts) into a dict of lists by hand.
2. Using only plain Python, find the name of the student with the highest maths mark.
3. With NumPy, compute the fraction of students who passed (≥ 50).

<details><summary>Solutions</summary>

```python
table = {"name": [r["name"] for r in rows], "maths": [r["maths"] for r in rows]}
max(rows, key=lambda r: r["maths"])["name"]     # 'Ravi'
(np.array([78, 92, 45]) >= 50).mean()           # 0.667
```
</details>

**Next →** [Lecture 01: What is pandas?](../01_what_is_pandas/)
