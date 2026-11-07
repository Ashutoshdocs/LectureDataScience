# 🔢 NumPy – 30 Basic Python Shell Labs

Beginner-friendly practicals for learning **NumPy** straight from the Python Shell (interactive mode). Every lab is a single command, with **no variables to create**: type it, press Enter, see the result.

> All commands and outputs in this guide were tested on **NumPy 2.5.3**. Small differences on other versions are covered in [Version Differences](#-version-differences).

---

## 📁 What's in this folder

| File | Use it for |
|---|---|
| `README.md` | This guide: theory, commands, expected outputs, explanations |
| `commands.txt` | Copy-and-paste sheet of every command, in order |
| `run_all_labs.py` | Runs all 30 labs in one go (the instructor's reference run) |
| `requirements.txt` | Dependency list for `pip install -r requirements.txt` |

---

## 📚 Table of Contents

- [What is NumPy?](#-what-is-numpy)
- [Setup](#%EF%B8%8F-setup)
- [Part A – Getting Started (Labs 1–2)](#part-a--getting-started-labs-12)
- [Part B – Creating Arrays (Labs 3–8)](#part-b--creating-arrays-labs-38)
- [Part C – Array Dimensions (Labs 9–12)](#part-c--array-dimensions-labs-912)
- [Part D – Array Properties (Labs 13–17)](#part-d--array-properties-labs-1317)
- [Part E – Indexing & Slicing (Labs 18–20)](#part-e--indexing--slicing-labs-1820)
- [Part F – Array Arithmetic (Labs 21–24)](#part-f--array-arithmetic-labs-2124)
- [Part G – Statistics (Labs 25–28)](#part-g--statistics-labs-2528)
- [Part H – Sorting & Reshaping (Labs 29–30)](#part-h--sorting--reshaping-labs-2930)
- [Version Differences](#-version-differences)
- [Quick Revision Cheat Sheet](#-quick-revision-cheat-sheet)
- [Practice Exercises](#-practice-exercises)
- [Troubleshooting](#%EF%B8%8F-troubleshooting)

---

## 🤔 What is NumPy?

**NumPy** (Numerical Python) is the core Python library for working with numbers. Its main object is the **array** (`ndarray`): a grid of values that all have the **same data type**.

Why use a NumPy array instead of a Python list?

| Python list | NumPy array |
|---|---|
| `[1, 2, 3] * 2` → `[1, 2, 3, 1, 2, 3]` (repeats the list) | `np.array([1, 2, 3]) * 2` → `array([2, 4, 6])` (does the maths) |
| Can mix types (`[1, "a", 2.5]`) | All elements have one type, so it's fast and compact |
| Loops needed for maths | Maths on the whole array at once (**vectorization**) |

NumPy is the foundation of Pandas, Matplotlib, scikit-learn, Dask and most data-science tools.

---

## ⚙️ Setup

### Step 1: Install NumPy (in your **system terminal**, not inside Python)

```bash
python -m pip install numpy
```

### Step 2: Open the Python Shell

```bash
python
```

### Step 3: Import NumPy once per session

```python
>>> import numpy as np
```

> ⚠️ **Don't type `>>>`.** That is the Python prompt. Type only what comes after it.
>
> 💡 You only need to import once per Shell session. If you close the Shell, import again.

---

## Part A – Getting Started (Labs 1–2)

### Lab 01 – Check NumPy Installation

**Purpose:** Import NumPy and give it the short name `np`.

```python
>>> import numpy as np
```

**Expected output:** Nothing. No message means success ✅.

**Explanation:** `import numpy` loads the library, and `as np` lets you type `np` instead of `numpy` every time. `np` is the standard name used worldwide. If you see `ModuleNotFoundError`, NumPy is not installed (see [Troubleshooting](#%EF%B8%8F-troubleshooting)).

---

### Lab 02 – Check NumPy Version

```python
>>> np.__version__
```

**Expected output (example):**
```
'2.5.3'
```

**Explanation:** `__version__` (two underscores on each side) holds the installed version.

---

## Part B – Creating Arrays (Labs 3–8)

### Lab 03 – Create a Simple Array

```python
>>> np.array([10, 20, 30, 40])
```

**Expected output:**
```
array([10, 20, 30, 40])
```

**Explanation:** `np.array()` turns a Python list into a NumPy array. The Shell shows it as `array([...])`. If you use `print()`, you get `[10 20 30 40]` with no commas, which is how you can tell an array from a list.

---

### Lab 04 – Create an Array of Zeros

```python
>>> np.zeros(5)
```

**Expected output:**
```
array([0., 0., 0., 0., 0.])
```

**Explanation:** `np.zeros(5)` creates 5 zeros. The dot in `0.` means the values are **floats** (decimals), the default type. Zeros arrays are often used as a starting point you fill in later.

---

### Lab 05 – Create an Array of Ones

```python
>>> np.ones(4)
```

**Expected output:**
```
array([1., 1., 1., 1.])
```

**Explanation:** `np.ones(4)` creates 4 ones, also as floats by default.

---

### Lab 06 – Create an Array Filled with a Value

```python
>>> np.full(5, 7)
```

**Expected output:**
```
array([7, 7, 7, 7, 7])
```

**Explanation:** `np.full(size, value)` creates `size` elements, each equal to `value`. Because `7` is an integer, the result is an integer array (no dots).

---

### Lab 07 – Create a Range of Values

```python
>>> np.arange(1, 11)
```

**Expected output:**
```
array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
```

**Explanation:** `np.arange(start, stop)` works like Python's `range()`. The **stop value is excluded**, so `arange(1, 11)` gives 1 to 10. Add a third argument for the step: `np.arange(0, 20, 5)` → `array([ 0,  5, 10, 15])`.

---

### Lab 08 – Create Evenly Spaced Values

```python
>>> np.linspace(0, 10, 5)
```

**Expected output:**
```
array([ 0. ,  2.5,  5. ,  7.5, 10. ])
```

**Explanation:** `np.linspace(start, stop, count)` creates `count` evenly spaced values. Unlike `arange`, the **stop value is included**.

> 🆚 **`arange` vs `linspace`**
> - `arange` → you choose the **step size**, stop is **excluded**
> - `linspace` → you choose **how many values**, stop is **included**

---

## Part C – Array Dimensions (Labs 9–12)

```
 1D (vector)        2D (matrix)          3D (stack of matrices)
 [1 2 3 4 5]        [[1 2 3]             [[[1 2]   [[5 6]
                     [4 5 6]]              [3 4]],   [7 8]]]
 shape: (5,)        shape: (2, 3)        shape: (2, 2, 2)
```

> 💡 **Count the opening brackets `[` at the start** to know the number of dimensions: `[` = 1D, `[[` = 2D, `[[[` = 3D.

### Lab 09 – Create a 1D Array

```python
>>> np.array([1, 2, 3, 4, 5])
```

**Expected output:**
```
array([1, 2, 3, 4, 5])
```

**Explanation:** A 1D array is a single row of values, like a list. It's also called a **vector**.

---

### Lab 10 – Create a 2D Array

```python
>>> np.array([[1, 2, 3], [4, 5, 6]])
```

**Expected output:**
```
array([[1, 2, 3],
       [4, 5, 6]])
```

**Explanation:** A list of lists makes a 2D array (a **matrix**). Each inner list is one **row**, so this array has 2 rows and 3 columns. All rows must have the same length.

---

### Lab 11 – Create a 3D Array

```python
>>> np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
```

**Expected output:**
```
array([[[1, 2],
        [3, 4]],

       [[5, 6],
        [7, 8]]])
```

**Explanation:** A 3D array is a stack of 2D arrays. Here there are 2 blocks, each a 2 × 2 matrix. The blank line in the output separates the blocks. Think of it as pages in a book, where each page is a table.

---

### Lab 12 – Create an Identity Matrix

```python
>>> np.eye(3)
```

**Expected output:**
```
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])
```

**Explanation:** An identity matrix has **1s on the diagonal** and 0s everywhere else. It is the "1" of matrix maths: multiplying a matrix by it leaves the matrix unchanged.

---

## Part D – Array Properties (Labs 13–17)

> 💡 These are **attributes**, not functions, so they have **no `()`**. Write `.shape`, not `.shape()`.

### Lab 13 – Check Number of Dimensions

```python
>>> np.array([[1, 2], [3, 4]]).ndim
```

**Expected output:**
```
2
```

**Explanation:** `.ndim` gives the number of dimensions (axes): 1 for 1D, 2 for 2D, 3 for 3D.

---

### Lab 14 – Check Array Shape

```python
>>> np.array([[1, 2, 3], [4, 5, 6]]).shape
```

**Expected output:**
```
(2, 3)
```

**Explanation:** `.shape` returns a tuple of `(rows, columns)`: here, 2 rows and 3 columns. A 1D array of 5 elements has shape `(5,)`. The trailing comma means it's a one-item tuple.

---

### Lab 15 – Count Array Elements

```python
>>> np.array([[1, 2, 3], [4, 5, 6]]).size
```

**Expected output:**
```
6
```

**Explanation:** `.size` is the total number of elements, which is rows × columns = 2 × 3 = **6**.

---

### Lab 16 – Check Data Type

```python
>>> np.array([1, 2, 3]).dtype
```

**Expected output:**
```
dtype('int64')
```

**Explanation:** `.dtype` shows the type of the elements. `int64` means 64-bit integers. Other common types are `float64` (decimals), `bool` (True/False) and `<U5` (text). Try `np.array([1.5, 2.5]).dtype` → `dtype('float64')`.

---

### Lab 17 – Check Bytes per Element

```python
>>> np.array([1, 2, 3], dtype=np.int32).itemsize
```

**Expected output:**
```
4
```

**Explanation:** `dtype=np.int32` forces 32-bit integers. 32 bits ÷ 8 = **4 bytes** per element. With the default `int64`, `itemsize` would be 8. Smaller types save memory on large datasets.

---

## Part E – Indexing & Slicing (Labs 18–20)

```
 Value:            10   20   30   40   50
 Positive index:    0    1    2    3    4
 Negative index:   -5   -4   -3   -2   -1
```

### Lab 18 – Access the First Element

```python
>>> np.array([10, 20, 30, 40])[0]
```

**Expected output:**
```
np.int64(10)
```

**Explanation:** Indexing starts at **0**, so `[0]` is the first element. NumPy 2.x shows the value as `np.int64(10)`, meaning "the number 10, stored as a NumPy 64-bit integer". `print()` shows just `10`.

---

### Lab 19 – Access the Last Element

```python
>>> np.array([10, 20, 30, 40])[-1]
```

**Expected output:**
```
np.int64(40)
```

**Explanation:** Negative indexes count from the end: `-1` is the last element and `-2` the second-last. This is handy when you don't know the array's length.

---

### Lab 20 – Slice an Array

```python
>>> np.array([10, 20, 30, 40, 50])[1:4]
```

**Expected output:**
```
array([20, 30, 40])
```

**Explanation:** `[start:stop]` returns elements from `start` up to **but not including** `stop`, so indexes 1, 2 and 3 here. Shortcuts: `[:3]` gives the first three and `[2:]` gives everything from index 2 onward.

---

## Part F – Array Arithmetic (Labs 21–24)

NumPy does maths **element by element**: the first value pairs with the first, the second with the second, and so on.

```
   [ 1,  2,  3]
 + [10, 20, 30]
 = [11, 22, 33]
```

### Lab 21 – Add Two Arrays

```python
>>> np.array([1, 2, 3]) + np.array([10, 20, 30])
```

**Expected output:**
```
array([11, 22, 33])
```

**Explanation:** Matching elements are added: 1+10, 2+20, 3+30. With Python lists, `+` would **join** them instead.

---

### Lab 22 – Subtract Arrays

```python
>>> np.array([10, 20, 30]) - np.array([1, 2, 3])
```

**Expected output:**
```
array([ 9, 18, 27])
```

**Explanation:** Matching elements are subtracted: 10−1, 20−2, 30−3. The extra space before `9` only lines up the columns.

---

### Lab 23 – Multiply Array Elements

```python
>>> np.array([2, 3, 4]) * np.array([5, 6, 7])
```

**Expected output:**
```
array([10, 18, 28])
```

**Explanation:** `*` multiplies matching elements (2×5, 3×6, 4×7). This is **not** matrix multiplication; for that, use `@` or `np.dot()`.

---

### Lab 24 – Multiply an Array by a Number

```python
>>> np.array([1, 2, 3]) * 10
```

**Expected output:**
```
array([10, 20, 30])
```

**Explanation:** A single number is applied to **every** element. This is called **broadcasting**. Compare with a list: `[1, 2, 3] * 10` repeats the list 10 times!

---

## Part G – Statistics (Labs 25–28)

> 💡 These functions accept a plain Python list **or** a NumPy array. NumPy converts the list for you.

### Lab 25 – Find the Sum

```python
>>> np.sum([10, 20, 30, 40])
```

**Expected output:**
```
np.int64(100)
```

**Explanation:** `np.sum()` adds all values: 10 + 20 + 30 + 40 = **100**.

---

### Lab 26 – Find the Mean

```python
>>> np.mean([10, 20, 30, 40])
```

**Expected output:**
```
np.float64(25.0)
```

**Explanation:** The mean (average) is sum ÷ count = 100 ÷ 4 = **25.0**. It is always a float because averages can have decimals.

---

### Lab 27 – Find the Maximum

```python
>>> np.max([10, 50, 20, 40])
```

**Expected output:**
```
np.int64(50)
```

**Explanation:** `np.max()` returns the largest value. To get its **position** instead, use `np.argmax([10, 50, 20, 40])` → `np.int64(1)` (index 1).

---

### Lab 28 – Find the Minimum

```python
>>> np.min([10, 50, 20, 40])
```

**Expected output:**
```
np.int64(10)
```

**Explanation:** `np.min()` returns the smallest value. Its position is given by `np.argmin()`.

---

## Part H – Sorting & Reshaping (Labs 29–30)

### Lab 29 – Sort an Array

```python
>>> np.sort([30, 10, 40, 20])
```

**Expected output:**
```
array([10, 20, 30, 40])
```

**Explanation:** `np.sort()` returns a **new** sorted array in ascending order. For descending order, reverse it: `np.sort([30, 10, 40, 20])[::-1]` → `array([40, 30, 20, 10])`.

---

### Lab 30 – Reshape an Array

```python
>>> np.arange(1, 7).reshape(2, 3)
```

**Expected output:**
```
array([[1, 2, 3],
       [4, 5, 6]])
```

**Explanation:** `np.arange(1, 7)` makes `[1 2 3 4 5 6]`, and `.reshape(2, 3)` rearranges it into 2 rows × 3 columns.

> ⚠️ **The total must match:** 6 elements fit into 2×3 or 3×2, but **not** 4×2:
> ```
> >>> np.arange(1, 7).reshape(4, 2)
> ValueError: cannot reshape array of size 6 into shape (4,2)
> ```
> 💡 Use `-1` to let NumPy work out one dimension: `np.arange(1, 7).reshape(3, -1)` → 3 rows × 2 columns.

---

## 🔄 Version Differences

| What you see | Why |
|---|---|
| `np.int64(10)` vs plain `10` | NumPy **2.0+** shows the type of single values. NumPy 1.x shows only `10`. Both are the same number. |
| `dtype('int32')` instead of `int64` in Lab 16 | Older NumPy (1.x) on **Windows** defaulted to 32-bit integers. NumPy 2.x uses `int64` everywhere. |
| A different version number in Lab 02 | Depends on when you installed NumPy. |

---

## 📋 Quick Revision Cheat Sheet

**Creating arrays**

| Function | Example | Result |
|---|---|---|
| `np.array()` | `np.array([1, 2, 3])` | `[1 2 3]` |
| `np.zeros()` | `np.zeros(3)` | `[0. 0. 0.]` |
| `np.ones()` | `np.ones(3)` | `[1. 1. 1.]` |
| `np.full()` | `np.full(3, 7)` | `[7 7 7]` |
| `np.arange()` | `np.arange(1, 5)` | `[1 2 3 4]` (stop excluded) |
| `np.linspace()` | `np.linspace(0, 1, 3)` | `[0.  0.5 1. ]` (stop included) |
| `np.eye()` | `np.eye(2)` | 2×2 identity matrix |

**Array properties** (no brackets!)

| Attribute | Gives |
|---|---|
| `.ndim` | Number of dimensions |
| `.shape` | Size of each dimension, e.g. `(rows, cols)` |
| `.size` | Total number of elements |
| `.dtype` | Data type of the elements |
| `.itemsize` | Bytes per element |

**Indexing, maths and statistics**

| Operation | Meaning |
|---|---|
| `a[0]`, `a[-1]` | First / last element |
| `a[1:4]` | Elements at index 1, 2, 3 |
| `a + b`, `a - b`, `a * b` | Element-wise maths |
| `a * 10` | Apply to every element (broadcasting) |
| `np.sum()` / `np.mean()` | Total / average |
| `np.max()` / `np.min()` | Largest / smallest |
| `np.sort()` | Sort ascending |
| `.reshape(r, c)` | Change shape (total must match) |

---

## ✍️ Practice Exercises

Try these on your own. Answers are in the collapsed section below.

1. Create an array of the even numbers from 2 to 20.
2. Create 6 zeros arranged as 2 rows × 3 columns.
3. Find the shape of `np.array([[1, 2], [3, 4], [5, 6]])`.
4. Get the **last three** elements of `np.array([5, 10, 15, 20, 25])`.
5. Divide every element of `[100, 200, 300]` by 10.
6. Find the average of `[45, 78, 62, 90, 55]`.
7. Turn the numbers 1 to 12 into a 3 × 4 matrix.

<details>
<summary>👉 Show answers</summary>

```python
# 1
np.arange(2, 21, 2)                            # array([ 2,  4,  6,  8, 10, 12, 14, 16, 18, 20])

# 2
np.zeros((2, 3))                               # note the double brackets: shape is a tuple

# 3
np.array([[1, 2], [3, 4], [5, 6]]).shape       # (3, 2)

# 4
np.array([5, 10, 15, 20, 25])[-3:]             # array([15, 20, 25])

# 5
np.array([100, 200, 300]) / 10                 # array([10., 20., 30.])

# 6
np.mean([45, 78, 62, 90, 55])                  # np.float64(66.0)

# 7
np.arange(1, 13).reshape(3, 4)
```
</details>

---

## 🛠️ Troubleshooting

| Problem | Cause & Fix |
|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | NumPy isn't installed. Exit Python with `exit()` and run `python -m pip install numpy`. |
| `NameError: name 'np' is not defined` | You skipped `import numpy as np`, or opened a new Shell. Import again. |
| `SyntaxError` when pasting | You copied the `>>>`, or curly quotes/dashes from a Word or PDF file. Retype using a plain keyboard. |
| `pip` gives `SyntaxError` | You ran `pip` *inside* Python. Type `exit()` first, then run it in the terminal. |
| `TypeError: 'tuple' object is not callable` | You wrote `.shape()`. Attributes have no brackets: use `.shape`. |
| `ValueError: cannot reshape array...` | The new shape's rows × columns doesn't equal the number of elements. |
| `ValueError: operands could not be broadcast together` | The two arrays have different lengths (e.g. 3 + 4 elements). |
| `IndexError: index 4 is out of bounds` | Indexes start at 0, so a 4-element array's last index is 3. |

---

## ▶️ Run Everything at Once (for instructors)

```bash
pip install -r requirements.txt
python run_all_labs.py
```

This prints every lab's command and output. Use it to check each computer before class.

---

**🎉 End of 30 NumPy Python Shell Labs. Happy learning!**
