# Lecture 01 — What is NumPy?

Run: `python lecture.py`

## Definition

**NumPy** (short for **Num**erical **Py**thon) is the free, open-source library that gives Python a fast way to store and calculate with lots of numbers.

Its central object is the **array**, called `ndarray` ("n-dimensional array"):

> An **array** is a block of values laid out side by side in memory, **all of the same type** (for example, all 64-bit integers). Because every item is the same size, NumPy can jump to any item instantly and process all of them in fast compiled C code.

## Your first array

```python
import numpy as np            # "np" is the universal nickname

marks = [72, 85, 90, 64]      # Python list
arr = np.array(marks)         # NumPy array made from the list
```

## Spot the difference

| | `[72, 85, 90, 64]` | `[72 85 90 64]` |
|---|---|---|
| What | Python **list** | NumPy **array** |
| Printed with | commas | **no** commas |
| Holds | anything, mixed | one type (`dtype`) for every item |
| Maths | needs a loop | works on the whole array at once |

## The three things every array has

| Attribute | Meaning | Example |
|-----------|---------|---------|
| `arr.dtype` | the one data type shared by all items | `int64` |
| `arr.shape` | size along each dimension | `(4,)` |
| `arr.ndim` | number of dimensions | `1` |

## Where NumPy fits

NumPy is the **foundation layer** of data work in Python. Other libraries are built on top of it:

```
          pandas   Matplotlib   scikit-learn   SciPy   OpenCV   PyTorch/TensorFlow
             \         |             |           |       |            /
              \________|_____________|___________|_______|___________/
                                       |
                                 NumPy ndarray
                                       |
                                    Python
```

Learn NumPy once, and you understand the data underneath all of these tools.

## Expected output

```
NumPy version: 2.5.3
[72, 85, 90, 64]
[72 85 90 64]
<class 'list'>
<class 'numpy.ndarray'>
int64
...
```
(Your version number may differ; Windows may show `int32`.)

## Common mistakes

- Running `pip install numpy` **inside** Python → do it in the terminal.
- Naming your own file `numpy.py` → Python imports *your* file instead of the library. Rename it.
- Forgetting the import alias: `numpy.array` works too, but everyone writes `np.array`.

## Exercises

1. Make an array from `[1.5, 2, 3]` and print its `dtype`. Why is it `float64`?
2. Print `len(arr)`, `arr.sum()` and `arr.max()`.
3. What happens with `np.array([1, 2, "3"])`? Check its dtype.

<details><summary>Solutions</summary>

1. `float64` — one value is a decimal, so NumPy converts *all* values to float to keep a single type.
2. `4`, `311`, `90`.
3. Everything becomes text: dtype `<U21` (Unicode string). One string forces the whole array to strings.
</details>

**Next →** [Lecture 02: List vs array](../02_list_vs_array/)
