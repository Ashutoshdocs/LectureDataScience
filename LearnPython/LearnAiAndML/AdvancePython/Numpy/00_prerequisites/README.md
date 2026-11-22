# Lecture 00 — Prerequisites: the Python you need before NumPy

NumPy is a Python library, so you need a handful of core Python skills first. You don't need to be an expert — but if anything below feels unfamiliar, practise it before Lecture 01.

Run the examples: `python lecture.py`

---

## Checklist

| Skill | You should be able to… | Why NumPy needs it |
|-------|------------------------|--------------------|
| Variables & numbers | Use `int`, `float`, `bool`, and `+ - * / // % **` | Array maths uses exactly these operators |
| Lists | Create, index (`x[0]`, `x[-1]`), slice (`x[1:3]`), `len()`, `append()` | Arrays are built *from* lists and index the same way |
| Nested lists | Make a "table" as a list of lists and read `t[row][col]` | 2D arrays look like this |
| Loops | Write a `for` loop over a list and over `range()` | You must understand loops to see what NumPy *replaces* |
| `if` / `else` | Write conditions with `>`, `==`, `and`, `or` | Boolean masks are conditions on whole arrays |
| Functions | Define `def f(x): return ...` and call it | NumPy is mostly functions: `np.sqrt(x)` |
| List comprehensions | Read `[x * 2 for x in nums]` | The "Python way" that NumPy speeds up |
| Tuples | Know `(3, 4)` and unpacking `a, b = (3, 4)` | `arr.shape` is a tuple |
| Modules & imports | `import math`, `import x as y` | `import numpy as np` |
| Methods vs attributes | `s.upper()` (call) vs `c.real` (no brackets) | `arr.sum()` vs `arr.shape` |
| Installing packages | `python -m pip install <name>` in the terminal | You install NumPy this way |

---

## 1. Numbers and operators

```python
7 / 2    # 3.5   true division always gives a float
7 // 2   # 3     floor division
7 % 2    # 1     remainder
2 ** 10  # 1024  power
```

## 2. Lists — Python's general-purpose container

```python
marks = [72, 85, 90, 64]
marks[0]      # 72      first item (counting starts at 0)
marks[-1]     # 64      last item
marks[1:3]    # [85, 90] slice: start included, stop excluded
len(marks)    # 4
marks.append(99)
```

Lists can hold **anything, mixed**: `[1, "hello", 3.5, [1, 2]]`. That flexibility is great — and it is exactly what makes them slow for number crunching (see Lecture 03).

## 3. Lists of lists = tables

```python
table = [[1, 2, 3],
         [4, 5, 6]]
table[1][2]   # 6  → row 1, column 2
```

Getting a whole *column* needs a loop: `[row[2] for row in table]`. NumPy fixes this with `m[:, 2]`.

## 4. Loops — doing something to every item

```python
prices = [100, 250, 80]
doubled = []
for p in prices:
    doubled.append(p * 2)
```

Keep this pattern in mind: **empty list → loop → calculate → append**. Most of NumPy is about replacing it with a single expression.

## 5. List comprehensions — the compact loop

```python
doubled = [p * 2 for p in prices]
cheap   = [p for p in prices if p < 200]
```

## 6. Functions

```python
def with_tax(price, rate=0.18):
    return price * (1 + rate)
```

## 7. Tuples and unpacking

```python
shape = (3, 4)
rows, cols = shape
```

## 8. Modules and aliases

```python
import math
math.sqrt(16)          # 4.0 — but only ONE number at a time

import numpy as np     # the universal convention: always "np"
```

## 9. Methods vs attributes

```python
name = "numpy"
name.upper()   # method: has brackets, DOES something
z = 3 + 4j
z.real         # attribute: no brackets, just a stored value
```
NumPy uses both: `arr.mean()` (method) and `arr.shape` (attribute). Writing `arr.shape()` is a classic beginner error.

## 10. Installing NumPy

Open a **terminal / command prompt** (not the Python `>>>` prompt):

```bash
python -m pip install numpy
python -c "import numpy; print(numpy.__version__)"
```

Optional but recommended — use a virtual environment so projects don't clash:

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
python -m pip install numpy
```

---

## The problem NumPy solves

Run `lecture.py` and look at the last section. Plain Python can:
- add 5 to every price — only with a loop
- add two lists element by element — only with `zip` and a loop
- take a column from a table — only with a loop
- compute a mean — only with `sum(x) / len(x)`

All of this works, but it is **long to write** and **slow to run** for big data. NumPy turns each of these into one short, fast expression.

---

## Exercises

1. Write a loop that converts `[0, 25, 37, 100]` °C to °F (`F = C * 9/5 + 32`).
2. Rewrite exercise 1 as a list comprehension.
3. From `table = [[1,2,3],[4,5,6],[7,8,9]]`, collect the middle column into a list.
4. Write `def average(nums):` that returns the mean of a list.

<details><summary>Solutions</summary>

```python
c = [0, 25, 37, 100]
f = []
for x in c:
    f.append(x * 9 / 5 + 32)

f = [x * 9 / 5 + 32 for x in c]

table = [[1,2,3],[4,5,6],[7,8,9]]
middle = [row[1] for row in table]   # [2, 5, 8]

def average(nums):
    return sum(nums) / len(nums)
```
</details>

**Next →** [Lecture 01: What is NumPy?](../01_what_is_numpy/)
