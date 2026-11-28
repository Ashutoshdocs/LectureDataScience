# NumPy – Complete Beginner-to-Advanced Course

> **Course continuity**
>
> This README follows:
> 1. **Python Vectors: Complete Foundation to NumPy** – where we learned vector concepts, performed operations using Python lists, and received our first introduction to NumPy arrays.
> 2. **NumPy Environment Setup – Theory and Practical** – where we installed Python and NumPy, created a virtual environment, and verified the setup.
>
> Now we will study NumPy in depth, starting with the fundamentals and gradually moving to advanced array operations and practical numerical analysis.

---

# Course outcomes

By completing this guide, students should be able to:

- Explain NumPy and why it is used for numerical computing.
- Create and inspect one-dimensional and multidimensional arrays.
- Understand array dimensions, shape, size, data types, and memory layout.
- Generate arrays using NumPy functions.
- Access, update, slice, reshape, combine, and split arrays.
- Perform arithmetic, comparison, and logical operations.
- Understand broadcasting and vectorization.
- Perform statistical calculations and aggregations.
- Filter data using Boolean masks and `where()`.
- Sort, search, and find unique values.
- Work with missing or invalid numerical values.
- Understand views, copies, and memory-sharing behavior.
- Use random number generation and reproducible experiments.
- Perform matrix operations and basic linear algebra.
- Read and write NumPy data files.
- Apply NumPy to two end-to-end data-analysis projects.

## Prerequisites

Students should know:

- Python variables and data types.
- Lists, tuples, loops, conditions, and functions.
- Basic arithmetic.
- Basic vector concepts from the previous course.

Required environment:

- Python 3.
- NumPy installed in the active virtual environment.
- A code editor such as VS Code, or Jupyter Notebook.

Activate the virtual environment created in the previous setup chapter, then verify NumPy:

```bash
python -c "import numpy as np; print(np.__version__)"
```

If NumPy is not installed in that environment:

```bash
python -m pip install numpy
```

## Recommended folder structure

```text
numpy-course/
│
├── .venv/
├── requirements.txt
│
├── 01_numpy_introduction.py
├── 02_array_creation.py
├── 03_array_attributes.py
├── 04_array_data_types.py
├── 05_indexing_slicing.py
├── 06_array_operations.py
├── 07_broadcasting.py
├── 08_aggregation_statistics.py
├── 09_boolean_filtering.py
├── 10_reshape_transpose.py
├── 11_join_split.py
├── 12_sort_search_unique.py
├── 13_missing_values.py
├── 14_copy_vs_view.py
├── 15_random_numbers.py
├── 16_linear_algebra.py
├── 17_file_operations.py
│
├── project_1_student_performance/
│   ├── README.md
│   ├── students.csv
│   └── main.py
│
└── project_2_sales_analysis/
    ├── README.md
    ├── sales.csv
    └── main.py
```

---

# Part 1 – NumPy foundations

## Chapter 1 – What is NumPy?

NumPy stands for **Numerical Python**. It is a Python library for working with numerical data.

Its central data structure is the `ndarray`, which stands for N-dimensional array.

A NumPy array can store numerical values in one or more dimensions and provides operations designed to work efficiently across those values.

### Why do we need NumPy if Python already has lists?

A Python list is a general-purpose collection. It can contain different kinds of Python objects.

```python
values = [10, 20, 30, 40]

print(values)
```

A NumPy array is designed for numerical operations.

```python
import numpy as np

values = np.array([10, 20, 30, 40])

print(values)
```

### List multiplication versus array multiplication

```python
# Python list
numbers_list = [1, 2, 3]

# Repeating a list repeats its elements.
print(numbers_list * 2)

# NumPy array
numbers_array = np.array([1, 2, 3])

# Multiplying an array by 2 multiplies each element by 2.
print(numbers_array * 2)
```

Expected output:

```text
[1, 2, 3, 1, 2, 3]
[2 4 6]
```

### Important differences

| Feature | Python list | NumPy array |
|---|---|---|
| Main purpose | General collection | Numerical and multidimensional data |
| Element types | Can contain mixed types | Usually one common data type |
| Arithmetic | Often requires loops or comprehensions | Supports element-wise arithmetic |
| Dimensions | Nested lists can represent tables | Has explicit dimensionality and shape |
| Numerical functions | Built-in functions and manual logic | Many numerical operations are provided |
| Memory/performance | General-purpose Python objects | Often more compact and faster for numerical workloads |

NumPy is often faster for large numerical operations because many operations are implemented in optimized low-level code. Performance depends on the operation, data size, and implementation.

### When should we use NumPy?

Use NumPy when working with:

- Numeric measurements.
- Vectors and matrices.
- Scientific calculations.
- Statistical operations.
- Image and signal data.
- Numerical preprocessing for machine learning.

Do not assume every list should become an array. Choose the data structure based on the task.

---

## Chapter 2 – Import NumPy

The common convention is:

```python
import numpy as np
```

`np` is an alias. It lets us write `np.array()` instead of `numpy.array()`.

```python
import numpy as np

print(np.__version__)
```

### First array

```python
import numpy as np

marks = np.array([75, 80, 92, 68, 88])

print(marks)
```

Expected output:

```text
[75 80 92 68 88]
```

### Understand what happened

1. `import numpy as np` loads the NumPy package.
2. `np.array()` creates a NumPy array.
3. The list supplies the values.
4. `marks` refers to the resulting array.
5. `print()` displays the array.

---

# Part 2 – Creating arrays

## Chapter 3 – One-dimensional arrays

A one-dimensional array contains values along one axis.

```python
import numpy as np

numbers = np.array([10, 20, 30, 40, 50])

print(numbers)
print("Dimensions:", numbers.ndim)
print("Shape:", numbers.shape)
print("Size:", numbers.size)
```

For this array:

- `ndim` is `1`.
- `shape` is `(5,)`.
- `size` is `5`.

The trailing comma in `(5,)` indicates a one-element shape tuple.

## Chapter 4 – Two-dimensional arrays

A two-dimensional array has rows and columns.

```python
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print(matrix)
print("Dimensions:", matrix.ndim)
print("Shape:", matrix.shape)
print("Size:", matrix.size)
```

Its shape is `(2, 3)`: 2 rows and 3 columns. Its total size is 6 elements.

### Visualize the structure

```text
              Column
           0    1    2
        +----+----+----+
Row  0  | 10 | 20 | 30 |
        +----+----+----+
Row  1  | 40 | 50 | 60 |
        +----+----+----+
```

## Chapter 5 – Three-dimensional arrays

A three-dimensional array can be understood as a collection of two-dimensional matrices.

```python
data = np.array([
    [
        [1, 2, 3],
        [4, 5, 6]
    ],
    [
        [7, 8, 9],
        [10, 11, 12]
    ]
])

print(data)
print("Dimensions:", data.ndim)
print("Shape:", data.shape)
print("Size:", data.size)
```

The shape is `(2, 2, 3)`:

- 2 blocks.
- 2 rows in each block.
- 3 columns in each row.

Common applications include batches of images, time-series data with multiple features, and scientific datasets.

## Chapter 6 – Array creation functions

NumPy provides functions to create arrays without manually writing every value.

### 6.1 `np.zeros()`

Creates an array filled with zeros.

```python
zeros_array = np.zeros(5)
print(zeros_array)
```

Two-dimensional example:

```python
zeros_matrix = np.zeros((2, 3))
print(zeros_matrix)
```

### 6.2 `np.ones()`

Creates an array filled with ones.

```python
ones_array = np.ones(4)
print(ones_array)
```

### 6.3 `np.full()`

Creates an array filled with a specified value.

```python
full_array = np.full((2, 3), 7)
print(full_array)
```

### 6.4 `np.empty()`

Creates an array without initializing its values to a particular useful number.

```python
empty_array = np.empty(4)
print(empty_array)
```

**Important:** The values in an `empty` array are not guaranteed to be zero. They may contain arbitrary values from the allocated memory. Assign values before using them.

### 6.5 `np.arange()`

Creates values over a half-open interval: the stop value is excluded.

```python
numbers = np.arange(1, 10, 2)
print(numbers)
```

Expected output:

```text
[1 3 5 7 9]
```

Syntax:

```python
np.arange(start, stop, step)
```

### 6.6 `np.linspace()`

Creates a specified number of evenly spaced values between endpoints.

```python
numbers = np.linspace(0, 10, 5)
print(numbers)
```

Expected output:

```text
[ 0.   2.5  5.   7.5 10. ]
```

Unlike `arange()`, `linspace()` uses the number of samples as its third positional argument.

### 6.7 Identity matrix with `np.eye()`

```python
identity = np.eye(3)
print(identity)
```

### 6.8 Diagonal matrix with `np.diag()`

```python
diagonal = np.diag([10, 20, 30])
print(diagonal)
```

### Comparison

| Function | Purpose |
|---|---|
| `np.array()` | Create an array from an existing sequence |
| `np.zeros()` | Fill with zeros |
| `np.ones()` | Fill with ones |
| `np.full()` | Fill with a chosen value |
| `np.empty()` | Allocate without setting a particular initial value |
| `np.arange()` | Generate values using a step |
| `np.linspace()` | Generate a chosen number of evenly spaced values |
| `np.eye()` | Create an identity-like matrix |
| `np.diag()` | Create or extract diagonal values |

---

# Part 3 – Array attributes and data types

## Chapter 7 – Important array attributes

```python
import numpy as np

matrix = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print("Array:", matrix)
print("ndim:", matrix.ndim)
print("shape:", matrix.shape)
print("size:", matrix.size)
print("dtype:", matrix.dtype)
print("itemsize:", matrix.itemsize)
print("nbytes:", matrix.nbytes)
```

| Attribute | Meaning |
|---|---|
| `ndim` | Number of dimensions |
| `shape` | Length along each dimension |
| `size` | Total number of elements |
| `dtype` | Data type of array elements |
| `itemsize` | Bytes used by one array element |
| `nbytes` | Total bytes used by the array elements |

`nbytes` describes the element buffer size; it is not the complete Python object memory footprint.

## Chapter 8 – NumPy data types (`dtype`)

A NumPy array generally stores elements using a common data type.

```python
numbers = np.array([10, 20, 30])

print(numbers.dtype)
```

### Common data types

| Type | Meaning | Example |
|---|---|---|
| `int32` | 32-bit integer | `10` |
| `int64` | 64-bit integer | `1000` |
| `float32` | 32-bit floating point | `10.5` |
| `float64` | 64-bit floating point | `99.99` |
| `bool_` | Boolean | `True` |
| `complex128` | Complex number | `2 + 3j` |
| `str_` | String type | `"Python"` |

Exact default integer and floating-point types can vary with platform and input.

### Specify the data type

```python
numbers = np.array([10, 20, 30], dtype=np.float32)

print(numbers)
print(numbers.dtype)
```

### Convert a data type using `astype()`

```python
numbers = np.array([10.8, 20.5, 30.9])

integer_numbers = numbers.astype(np.int32)

print(integer_numbers)
```

Converting floating-point values to integers truncates the fractional part; it does not round to the nearest integer.

### Mixed values

```python
values = np.array([10, 20.5, 30])

print(values)
print(values.dtype)
```

NumPy chooses a common type capable of representing the values under its type-promotion rules.

### Why does dtype matter?

- It affects how values are represented.
- It can affect memory usage.
- It can affect numerical precision and range.
- It can affect which operations are valid and how they behave.

Do not choose a smaller data type only to save memory if it cannot safely represent the values or precision your task requires.

---

# Part 4 – Indexing and slicing

## Chapter 9 – Access elements in a one-dimensional array

Python and NumPy use zero-based indexing.

```python
numbers = np.array([10, 20, 30, 40, 50])

print(numbers[0])
print(numbers[1])
print(numbers[-1])
```

Expected output:

```text
10
20
50
```

Update an element:

```python
numbers[0] = 100
print(numbers)
```

## Chapter 10 – Access elements in a two-dimensional array

```python
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print(matrix[0, 0])
print(matrix[0, 2])
print(matrix[1, 1])
```

Syntax:

```python
array[row_index, column_index]
```

You can also use chained indexing, but direct indexing such as `matrix[0, 2]` is generally clearer.

### Update an element

```python
matrix[1, 2] = 600
print(matrix)
```

## Chapter 11 – Slicing arrays

The general slicing syntax is:

```python
array[start:stop:step]
```

The stop index is excluded.

```python
numbers = np.array([10, 20, 30, 40, 50, 60])

print(numbers[1:4])
print(numbers[:3])
print(numbers[3:])
print(numbers[::2])
print(numbers[::-1])
```

### Two-dimensional slicing

```python
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

# First two rows, all columns
print(matrix[:2, :])

# All rows, first two columns
print(matrix[:, :2])

# First two rows and first two columns
print(matrix[:2, :2])
```

### Important: Slices may be views

Basic slicing often returns a view of the original array rather than an independent copy.

```python
numbers = np.array([10, 20, 30, 40])

part = numbers[1:3]
part[0] = 999

print(numbers)
print(part)
```

Changing `part` can change the original array because the slice shares data with it. We will examine views and copies in a later chapter.

---

# Part 5 – Arithmetic and vectorized operations

## Chapter 12 – Arithmetic operations

NumPy arithmetic is commonly element-wise when the arrays have compatible shapes.

```python
import numpy as np

A = np.array([10, 20, 30])
B = np.array([1, 2, 3])

print(A + B)
print(A - B)
print(A * B)
print(A / B)
print(A ** 2)
```

Expected output:

```text
[11 22 33]
[ 9 18 27]
[10 40 90]
[10. 10. 10.]
[100 400 900]
```

### Scalar operations

A scalar is a single value.

```python
prices = np.array([100, 200, 300])

print(prices + 10)
print(prices - 10)
print(prices * 2)
print(prices / 2)
```

The operation is applied to each element.

### Compound assignment

```python
numbers = np.array([10, 20, 30])

numbers += 5
print(numbers)

numbers *= 2
print(numbers)
```

## Chapter 13 – Comparison operations

Comparisons return Boolean arrays.

```python
marks = np.array([45, 67, 89, 32, 95])

print(marks > 60)
print(marks == 89)
print(marks <= 50)
```

Example result:

```text
[False  True  True False  True]
```

## Chapter 14 – Logical operations

Use NumPy logical functions to combine conditions.

```python
marks = np.array([45, 67, 89, 32, 95])

condition = np.logical_and(marks >= 40, marks <= 80)

print(condition)
```

You can also use `&` and `|` with parenthesized conditions:

```python
condition = (marks >= 40) & (marks <= 80)
print(marks[condition])
```

For element-wise Boolean logic, use `&`, `|`, and `~`, not Python's scalar `and`, `or`, and `not`.

## Chapter 15 – Vectorization

Vectorization means expressing operations over entire arrays rather than manually writing Python loops for each element.

### Without NumPy

```python
numbers = [10, 20, 30, 40]

result = []

for number in numbers:
    result.append(number * 2)

print(result)
```

### With NumPy

```python
numbers = np.array([10, 20, 30, 40])

result = numbers * 2

print(result)
```

### Why is vectorization useful?

- The code can be shorter and easier to read.
- Many NumPy operations execute in optimized compiled code.
- It is convenient to apply the same calculation to many values.
- It is a foundation for many numerical and machine-learning workflows.

Vectorization does not mean that every NumPy expression is always faster. For very small arrays, setup overhead can dominate. Measure performance for the actual workload.

---

# Part 6 – Broadcasting

## Chapter 16 – What is broadcasting?

Broadcasting is NumPy's mechanism for performing operations on arrays with compatible shapes without manually repeating values.

### Example 1 – Array and scalar

```python
numbers = np.array([10, 20, 30])

print(numbers + 5)
```

The scalar value `5` is applied to every element.

### Example 2 – Two compatible arrays

```python
A = np.array([10, 20, 30])
B = np.array([1, 2, 3])

print(A + B)
```

### Example 3 – Two-dimensional array and one-dimensional array

```python
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

row = np.array([1, 2, 3])

print(matrix + row)
```

The row values are applied to each row of the matrix.

### Broadcasting rules

Compare dimensions from right to left. Two dimensions are compatible when:

1. They are equal, or
2. One of them is `1`.

If one shape has fewer dimensions, it is treated as if it had leading dimensions of size `1`.

If dimensions are not compatible, NumPy raises a broadcasting error.

### Example of incompatible shapes

```python
A = np.array([1, 2, 3])
B = np.array([10, 20])

# This operation raises a broadcasting ValueError.
# print(A + B)
```

The shapes `(3,)` and `(2,)` are incompatible.

### Broadcasting with column and row vectors

```python
column = np.array([[1], [2], [3]])  # Shape (3, 1)
row = np.array([10, 20, 30, 40])    # Shape (4,)

result = column + row

print(result)
print(result.shape)
```

The result has shape `(3, 4)`.

---

# Part 7 – Aggregation and statistics

## Chapter 17 – Basic aggregation functions

```python
marks = np.array([70, 80, 90, 60, 100])

print("Sum:", np.sum(marks))
print("Mean:", np.mean(marks))
print("Median:", np.median(marks))
print("Minimum:", np.min(marks))
print("Maximum:", np.max(marks))
print("Standard deviation:", np.std(marks))
print("Variance:", np.var(marks))
```

### What do these functions mean?

| Function | Meaning |
|---|---|
| `np.sum()` | Sum of values |
| `np.mean()` | Arithmetic average |
| `np.median()` | Middle value after sorting |
| `np.min()` | Smallest value |
| `np.max()` | Largest value |
| `np.std()` | Standard deviation |
| `np.var()` | Variance |
| `np.prod()` | Product of values |

By default, `np.std()` and `np.var()` use the population convention (`ddof=0`). Use `ddof=1` when you need the sample standard deviation or sample variance.

## Chapter 18 – Axis in NumPy

The `axis` parameter tells NumPy which dimension to reduce.

```python
marks = np.array([
    [80, 90, 70],
    [60, 75, 85]
])

print("Overall average:", np.mean(marks))
print("Column averages:", np.mean(marks, axis=0))
print("Row averages:", np.mean(marks, axis=1))
```

For a 2D array:

- `axis=0` reduces across rows, producing one result per column.
- `axis=1` reduces across columns, producing one result per row.

### Visual explanation

```text
                 Subject columns
              Math  Science  English
Student 0      80      90       70
Student 1      60      75       85
                |       |        |
              axis=0: average each column

axis=1: average the values across each student row
```

### Keep dimensions with `keepdims`

```python
marks = np.array([
    [80, 90, 70],
    [60, 75, 85]
])

row_averages = np.mean(marks, axis=1, keepdims=True)

print(row_averages)
print(row_averages.shape)
```

`keepdims=True` retains the reduced axis with length 1, which can be useful for broadcasting.

---

# Part 8 – Filtering and conditional selection

## Chapter 19 – Boolean indexing

Boolean indexing selects values where a condition is true.

```python
marks = np.array([35, 45, 67, 89, 32, 95])

passed = marks[marks >= 40]

print(passed)
```

### Multiple conditions

```python
marks = np.array([35, 45, 67, 89, 32, 95])

selected = marks[(marks >= 40) & (marks <= 80)]

print(selected)
```

### Filter two related arrays together

```python
names = np.array(["Amit", "Neha", "Ravi", "Sara"])
marks = np.array([35, 88, 42, 95])

passed_mask = marks >= 40

print(names[passed_mask])
print(marks[passed_mask])
```

The arrays must represent corresponding records in the same order.

## Chapter 20 – `np.where()`

`np.where()` can return matching indices or choose values based on a condition.

### Return indices

```python
marks = np.array([35, 45, 67, 89, 32, 95])

indices = np.where(marks >= 60)

print(indices)
```

### Choose values

```python
marks = np.array([35, 45, 67, 89, 32, 95])

results = np.where(marks >= 40, "Pass", "Fail")

print(results)
```

## Chapter 21 – `np.select()`

Use `np.select()` when there are multiple conditions.

```python
marks = np.array([95, 82, 65, 42, 25])

conditions = [
    marks >= 90,
    marks >= 75,
    marks >= 50,
    marks >= 35
]

choices = ["A", "B", "C", "D"]

grades = np.select(conditions, choices, default="F")

print(grades)
```

The first matching condition is used.

---

# Part 9 – Reshaping and changing array structure

## Chapter 22 – `reshape()`

`reshape()` changes an array's shape without changing the number of elements.

```python
numbers = np.arange(1, 13)

matrix = numbers.reshape(3, 4)

print(matrix)
print(matrix.shape)
```

The original array has 12 elements. A `(3, 4)` shape also requires 12 elements.

### Reshape using `-1`

NumPy can infer one dimension.

```python
numbers = np.arange(1, 13)

matrix = numbers.reshape(3, -1)

print(matrix)
```

Only one dimension can be inferred using `-1` in a reshape call.

## Chapter 23 – `flatten()` and `ravel()`

Both can turn a multidimensional array into a one-dimensional representation, but their memory behavior differs.

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

flat_copy = matrix.flatten()
flat_view_when_possible = matrix.ravel()

print(flat_copy)
print(flat_view_when_possible)
```

- `flatten()` returns a copy.
- `ravel()` returns a flattened view when possible; otherwise it returns a copy.

## Chapter 24 – Transpose

Transpose swaps the axes of an array. For a 2D matrix, rows become columns and columns become rows.

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(matrix.T)
```

The shape changes from `(2, 3)` to `(3, 2)`.

---

# Part 10 – Joining and splitting arrays

## Chapter 25 – Joining arrays

### `np.concatenate()`

```python
A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

result = np.concatenate((A, B))

print(result)
```

For 2D arrays, concatenate along an existing axis:

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(np.concatenate((A, B), axis=0))
print(np.concatenate((A, B), axis=1))
```

The arrays must have compatible dimensions except along the axis being joined.

### `np.vstack()` and `np.hstack()`

```python
A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

print(np.vstack((A, B)))
print(np.hstack((A, B)))
```

## Chapter 26 – Splitting arrays

```python
numbers = np.array([10, 20, 30, 40, 50, 60])

parts = np.split(numbers, 3)

print(parts)
```

`np.split()` requires equal-sized sections when an integer number of sections is supplied.

For unequal sections, use `np.array_split()`:

```python
numbers = np.array([10, 20, 30, 40, 50])

parts = np.array_split(numbers, 3)

print(parts)
```

---

# Part 11 – Sorting, searching, and unique values

## Chapter 27 – Sorting

```python
numbers = np.array([50, 10, 40, 20, 30])

sorted_numbers = np.sort(numbers)

print(sorted_numbers)
print(numbers)
```

`np.sort()` returns a sorted copy by default.

To sort an array in place:

```python
numbers.sort()
print(numbers)
```

### Sort a 2D array

```python
matrix = np.array([
    [30, 10, 20],
    [60, 40, 50]
])

print(np.sort(matrix, axis=0))
print(np.sort(matrix, axis=1))
```

## Chapter 28 – Search with `np.argmax()` and `np.argmin()`

These functions return the index of a maximum or minimum value.

```python
marks = np.array([70, 90, 65, 98, 82])

print("Highest mark:", np.max(marks))
print("Index of highest mark:", np.argmax(marks))

print("Lowest mark:", np.min(marks))
print("Index of lowest mark:", np.argmin(marks))
```

For multidimensional arrays, the default is to operate on the flattened array. Use `axis` when you need per-row or per-column indices.

## Chapter 29 – Unique values and counts

```python
values = np.array([10, 20, 10, 30, 20, 10])

print(np.unique(values))
```

Get counts:

```python
unique_values, counts = np.unique(values, return_counts=True)

print("Unique:", unique_values)
print("Counts:", counts)
```

---

# Part 12 – Missing and invalid numerical values

## Chapter 30 – Understanding `NaN`

`NaN` means “Not a Number”. It is commonly used to represent missing or undefined numerical values.

```python
values = np.array([10.0, 20.0, np.nan, 40.0])

print(values)
print(np.isnan(values))
```

### Why does ordinary mean produce NaN?

```python
print(np.mean(values))
```

A NaN value generally propagates through many ordinary arithmetic operations.

### Use `nanmean()`

```python
print(np.nanmean(values))
```

`np.nanmean()` calculates the mean while ignoring NaN values.

Other useful functions include:

```python
np.nansum(values)
np.nanmin(values)
np.nanmax(values)
np.nanmedian(values)
np.nanstd(values)
```

### Replace missing values

```python
values = np.array([10.0, 20.0, np.nan, 40.0])

mask = np.isnan(values)

values[mask] = np.nanmean(values)

print(values)
```

This is a simple demonstration, not a universal missing-data strategy. In real projects, decide how to handle missing data based on what the missing values mean.

### Check finite values

```python
values = np.array([10.0, np.inf, -np.inf, np.nan])

print(np.isfinite(values))
```

`np.isfinite()` identifies values that are neither infinite nor NaN.

---

# Part 13 – Views, copies, and memory

## Chapter 31 – View versus copy

This is an important topic because changing one array may unexpectedly affect another.

### A view

A view is a different array object that refers to the same underlying data.

```python
original = np.array([10, 20, 30, 40])

view_array = original[1:3]

view_array[0] = 999

print("Original:", original)
print("View:", view_array)
```

The original changes because the basic slice is a view.

### A copy

A copy has independent data.

```python
original = np.array([10, 20, 30, 40])

copy_array = original[1:3].copy()

copy_array[0] = 999

print("Original:", original)
print("Copy:", copy_array)
```

The original remains unchanged.

### `np.shares_memory()`

```python
original = np.array([10, 20, 30, 40])

view_array = original[1:3]
copy_array = original[1:3].copy()

print(np.shares_memory(original, view_array))
print(np.shares_memory(original, copy_array))
```

### When should we use copy?

Use `.copy()` when you need to modify a selected array independently and do not want those changes to affect the source.

Not every operation returns a view. Advanced indexing, for example, generally returns a copy. Check the behavior of the operation you are using.

---

# Part 14 – Random number generation

## Chapter 32 – Why do we need random numbers?

Random values are useful for:

- Simulations.
- Sampling.
- Testing numerical programs.
- Generating synthetic data.
- Machine-learning experiments.

Use NumPy's modern random number generator interface:

```python
rng = np.random.default_rng()

numbers = rng.random(5)

print(numbers)
```

## Chapter 33 – Common random functions

### Random floating-point values

```python
rng = np.random.default_rng()

print(rng.random(5))
```

Values are drawn from the interval `[0.0, 1.0)`.

### Random integers

```python
rng = np.random.default_rng()

print(rng.integers(1, 101, size=5))
```

The lower bound is included and the upper bound is excluded.

### Normal distribution

```python
rng = np.random.default_rng()

values = rng.normal(loc=50, scale=10, size=5)

print(values)
```

- `loc` is the distribution mean.
- `scale` is the standard deviation.

### Random choice

```python
rng = np.random.default_rng()

subjects = np.array(["Math", "Science", "English"])

selected = rng.choice(subjects, size=5)

print(selected)
```

## Chapter 34 – Reproducible random values

Use a seed when you need to reproduce a demonstration or experiment.

```python
rng = np.random.default_rng(seed=42)

print(rng.integers(1, 101, size=5))
```

Using the same seed and the same sequence of generator calls produces reproducible results with the same NumPy bit generator.

Prefer creating a generator with `default_rng()` rather than relying on the legacy global random state.

---

# Part 15 – Linear algebra

## Chapter 35 – Vector dot product

The dot product multiplies corresponding elements and adds the products.

```python
A = np.array([2, 3, 4])
B = np.array([5, 6, 7])

result = np.dot(A, B)

print(result)
```

Mathematically:

$$
A \cdot B = (2 \times 5) + (3 \times 6) + (4 \times 7) = 56
$$

For one-dimensional arrays, the `@` operator also performs the dot product:

```python
print(A @ B)
```

## Chapter 36 – Matrix multiplication

Element-wise multiplication and matrix multiplication are different.

```python
A = np.array([
    [1, 2],
    [3, 4]
])

B = np.array([
    [5, 6],
    [7, 8]
])

# Element-wise multiplication
print(A * B)

# Matrix multiplication
print(A @ B)
```

For matrix multiplication, the number of columns in the first matrix must equal the number of rows in the second matrix.

If A has shape `(m, n)` and B has shape `(n, p)`, the result has shape `(m, p)`.

## Chapter 37 – Useful linear algebra functions

```python
A = np.array([
    [4, 2],
    [1, 3]
])

print("Transpose:")
print(A.T)

print("Determinant:")
print(np.linalg.det(A))

print("Inverse:")
print(np.linalg.inv(A))

print("Eigenvalues:")
print(np.linalg.eigvals(A))
```

### Solve a system of linear equations

Suppose:

$$
2x + y = 8
$$

$$
x + 3y = 9
$$

Represent the coefficients as a matrix and the right-hand side as a vector.

```python
A = np.array([
    [2, 1],
    [1, 3]
])

b = np.array([8, 9])

solution = np.linalg.solve(A, b)

print("x and y:", solution)
```

Prefer `np.linalg.solve(A, b)` to explicitly calculating `inv(A) @ b` for solving a square system. The solve function is generally more numerically appropriate and efficient.

---

# Part 16 – File operations

## Chapter 38 – Save and load NumPy arrays

### Save one array in `.npy` format

```python
numbers = np.array([10, 20, 30, 40])

np.save("numbers.npy", numbers)
```

### Load an `.npy` file

```python
loaded = np.load("numbers.npy")

print(loaded)
```

### Save multiple arrays in `.npz` format

```python
marks = np.array([70, 80, 90])
attendance = np.array([85, 90, 95])

np.savez(
    "student_data.npz",
    marks=marks,
    attendance=attendance
)
```

Load:

```python
data = np.load("student_data.npz")

print(data["marks"])
print(data["attendance"])
```

### Save and load text files

```python
numbers = np.array([10, 20, 30, 40])

np.savetxt("numbers.csv", numbers, delimiter=",", fmt="%d")

loaded = np.loadtxt("numbers.csv", delimiter=",")

print(loaded)
```

For structured CSV files with headers, mixed columns, and missing values, pandas may be more convenient. NumPy's text functions are useful for simpler numerical text data.

**Security note:** Only load `.npy` or `.npz` files from trusted sources. Avoid enabling pickle-based loading for untrusted files.

---

# Part 17 – Performance and best practices

## Chapter 39 – Measure execution time

Do not assume one approach is faster. Measure it on your own data and machine.

```python
import time
import numpy as np

size = 1_000_000

python_list = list(range(size))
numpy_array = np.arange(size)

# Python list calculation
start = time.perf_counter()

python_result = [value * 2 for value in python_list]

python_time = time.perf_counter() - start

# NumPy calculation
start = time.perf_counter()

numpy_result = numpy_array * 2

numpy_time = time.perf_counter() - start

print("Python list time:", python_time)
print("NumPy time:", numpy_time)
```

Timing varies with hardware, Python and NumPy versions, and system load. Run the experiment more than once and avoid treating one measurement as a universal benchmark.

## Chapter 40 – Best practices

1. Use `import numpy as np`.
2. Check `.shape` and `.dtype` when debugging array problems.
3. Prefer vectorized operations where they make the code clearer.
4. Understand broadcasting before combining arrays of different shapes.
5. Use parentheses around each condition when combining Boolean masks.
6. Know when a slice is a view and when an operation creates a copy.
7. Use `np.random.default_rng()` for random-number generation.
8. Use `np.linalg.solve()` to solve linear systems rather than calculating an inverse unnecessarily.
9. Choose data types based on required range and precision.
10. Validate input shapes and values before numerical calculations.
11. Handle NaN and infinite values deliberately.
12. Measure performance instead of assuming it.

---

# Part 18 – Project 1: Student Performance Analyzer

<badge color="success">Beginner to intermediate project</badge>

## Project objective

Build a student performance analysis program using NumPy.

The program will store student marks in a two-dimensional array and calculate:

- Total marks for each student.
- Average marks for each student.
- Subject-wise average.
- Highest and lowest marks.
- Pass/fail status.
- Grade for each student.
- Top-performing student.
- Students who need improvement.

## Problem statement

A teacher has marks for five students across three subjects:

- Mathematics
- Science
- English

The teacher wants a quick report without manually calculating every value.

## Step 1 – Create the data

Create `project_1_student_performance/main.py`.

```python
import numpy as np

# Each row represents one student.
# Each column represents one subject.
students = np.array([
    "Amit",
    "Neha",
    "Ravi",
    "Sara",
    "Priya"
])

subjects = np.array([
    "Mathematics",
    "Science",
    "English"
])

marks = np.array([
    [85, 90, 78],
    [92, 88, 95],
    [45, 55, 60],
    [70, 65, 72],
    [35, 40, 38]
])

print("Student names:")
print(students)

print("\nSubjects:")
print(subjects)

print("\nMarks:")
print(marks)
```

## Step 2 – Calculate total marks

```python
total_marks = np.sum(marks, axis=1)

print("Total marks:")
print(total_marks)
```

Why `axis=1`?

Each row represents one student. We want to add the subject marks across each row.

## Step 3 – Calculate average marks

```python
average_marks = np.mean(marks, axis=1)

print("Average marks:")
print(average_marks)
```

## Step 4 – Calculate subject-wise average

```python
subject_averages = np.mean(marks, axis=0)

print("Subject-wise averages:")
for subject, average in zip(subjects, subject_averages):
    print(subject, ":", average)
```

Why `axis=0`?

Each column represents one subject. We want the average across all students for each column.

## Step 5 – Find highest and lowest marks

```python
highest_mark = np.max(marks)
lowest_mark = np.min(marks)

print("Highest mark:", highest_mark)
print("Lowest mark:", lowest_mark)
```

Find the student with the highest average:

```python
top_index = np.argmax(average_marks)

print("Top student:", students[top_index])
print("Top average:", average_marks[top_index])
```

## Step 6 – Pass/fail status

For this project, assume a student must score at least 40 in every subject to pass.

```python
passed = np.all(marks >= 40, axis=1)

print("Pass status:")
for name, status in zip(students, passed):
    print(name, ":", "Pass" if status else "Fail")
```

`np.all(..., axis=1)` checks whether every subject mark in a student's row meets the condition.

## Step 7 – Assign grades

Use the student's average:

- A: 90 and above
- B: 75 to below 90
- C: 60 to below 75
- D: 40 to below 60
- F: below 40

```python
conditions = [
    average_marks >= 90,
    average_marks >= 75,
    average_marks >= 60,
    average_marks >= 40
]

choices = ["A", "B", "C", "D"]

grades = np.select(conditions, choices, default="F")

print("Grades:")
for name, average, grade in zip(students, average_marks, grades):
    print(name, "Average:", round(average, 2), "Grade:", grade)
```

The conditions are evaluated in order. The first matching condition determines the grade.

## Step 8 – Find students who need improvement

For this project, identify students whose average is below 60.

```python
needs_improvement = average_marks < 60

print("Students who need improvement:")
print(students[needs_improvement])
```

## Step 9 – Display a complete report

```python
print("\n========== STUDENT PERFORMANCE REPORT ==========")

for index, name in enumerate(students):
    print("\nStudent:", name)
    print("Marks:", marks[index])
    print("Total:", total_marks[index])
    print("Average:", round(average_marks[index], 2))
    print("Grade:", grades[index])
    print("Result:", "Pass" if passed[index] else "Fail")

print("\nSubject-wise average:")
for subject, average in zip(subjects, subject_averages):
    print(subject, ":", round(average, 2))

print("\nTop performer:", students[top_index])
print("Highest individual mark:", highest_mark)
print("Lowest individual mark:", lowest_mark)
```

## NumPy concepts used in Project 1

| Concept | Where used |
|---|---|
| `np.array()` | Student, subject, and marks data |
| 2D arrays | Marks table |
| `np.sum()` | Student totals |
| `np.mean()` | Student and subject averages |
| `axis=0` | Subject-wise calculations |
| `axis=1` | Student-wise calculations |
| `np.max()` / `np.min()` | Highest and lowest marks |
| `np.argmax()` | Top student index |
| `np.all()` | Pass condition across subjects |
| Boolean indexing | Identify students needing improvement |
| `np.select()` | Grade assignment |
| `zip()` | Display related values together |

## Project 1 – Student challenges

1. Add two more students.
2. Add a fourth subject.
3. Find the highest scorer in each subject.
4. Find the lowest scorer in each subject.
5. Count how many students passed.
6. Calculate the class average.
7. Identify students who scored above the class average.
8. Find students who failed in at least one subject.
9. Calculate the percentage for each student if each subject is out of 100.
10. Save the marks array to an `.npy` file and load it again.

---

# Part 19 – Project 2: Monthly Sales Analysis

<badge color="success">Intermediate to advanced project</badge>

## Project objective

Build a sales analysis program using NumPy.

The company has sales data for four products across six months.

The program should calculate:

- Total sales for each product.
- Total sales for each month.
- Average monthly sales per product.
- Best-selling product.
- Best-performing month.
- Month with the lowest sales.
- Sales above a threshold.
- Month-over-month change.
- Percentage contribution of each product.
- A simple sales target analysis.

## Problem statement

A business sells:

- Laptop
- Mobile
- Tablet
- Monitor

The sales team wants to understand product performance and monthly trends.

## Step 1 – Create sales data

Create `project_2_sales_analysis/main.py`.

```python
import numpy as np

products = np.array([
    "Laptop",
    "Mobile",
    "Tablet",
    "Monitor"
])

months = np.array([
    "January",
    "February",
    "March",
    "April",
    "May",
    "June"
])

# Each row represents one product.
# Each column represents one month.
sales = np.array([
    [120, 135, 150, 145, 160, 175],
    [200, 220, 210, 250, 260, 280],
    [80, 75, 90, 95, 100, 110],
    [60, 70, 65, 80, 85, 90]
])

print("Sales data:")
print(sales)
```

For this teaching project, values represent units sold. In a real business report, revenue and units sold should be stored as separate measures.

## Step 2 – Total sales per product

```python
product_totals = np.sum(sales, axis=1)

print("Product totals:")
for product, total in zip(products, product_totals):
    print(product, ":", total)
```

## Step 3 – Total sales per month

```python
monthly_totals = np.sum(sales, axis=0)

print("Monthly totals:")
for month, total in zip(months, monthly_totals):
    print(month, ":", total)
```

## Step 4 – Find the best-selling product

```python
best_product_index = np.argmax(product_totals)

print("Best-selling product:", products[best_product_index])
print("Units sold:", product_totals[best_product_index])
```

## Step 5 – Find the best and lowest performing months

```python
best_month_index = np.argmax(monthly_totals)
lowest_month_index = np.argmin(monthly_totals)

print("Best month:", months[best_month_index])
print("Best month total:", monthly_totals[best_month_index])

print("Lowest month:", months[lowest_month_index])
print("Lowest month total:", monthly_totals[lowest_month_index])
```

## Step 6 – Calculate average monthly sales per product

```python
product_averages = np.mean(sales, axis=1)

for product, average in zip(products, product_averages):
    print(product, "average units per month:", round(average, 2))
```

## Step 7 – Find sales above a threshold

Assume we want to find product-month combinations with more than 150 units sold.

```python
high_sales_mask = sales > 150

print("High sales mask:")
print(high_sales_mask)

print("Values above 150:")
print(sales[high_sales_mask])
```

Find the row and column positions:

```python
row_indices, column_indices = np.where(sales > 150)

for row, column in zip(row_indices, column_indices):
    print(products[row], months[column], sales[row, column])
```

## Step 8 – Calculate month-over-month change

Use `np.diff()` to calculate the difference between consecutive months.

```python
monthly_change = np.diff(sales, axis=1)

print("Month-over-month unit change:")
print(monthly_change)
```

A positive value indicates an increase; a negative value indicates a decrease.

### Percentage change

```python
previous_month = sales[:, :-1]
current_month = sales[:, 1:]

percentage_change = np.divide(
    (current_month - previous_month) * 100,
    previous_month,
    out=np.full(current_month.shape, np.nan, dtype=float),
    where=previous_month != 0
)

print("Percentage change:")
print(np.round(percentage_change, 2))
```

This calculation handles a zero previous-month value by leaving the corresponding percentage as NaN instead of dividing by zero.

## Step 9 – Product contribution percentage

```python
grand_total = np.sum(sales)

product_contribution = (product_totals / grand_total) * 100

for product, contribution in zip(products, product_contribution):
    print(product, "contribution:", round(contribution, 2), "%")
```

## Step 10 – Sales target analysis

Assume the monthly target is 500 units across all products.

```python
monthly_target = 500

target_met = monthly_totals >= monthly_target

for month, total, achieved in zip(months, monthly_totals, target_met):
    print(
        month,
        "Sales:", total,
        "Target:", "Met" if achieved else "Not Met"
    )
```

## Step 11 – Create a complete report

```python
print("\n========== MONTHLY SALES REPORT ==========")

print("\nProduct totals:")
for product, total in zip(products, product_totals):
    print(product, ":", total)

print("\nMonthly totals:")
for month, total in zip(months, monthly_totals):
    print(month, ":", total)

print("\nBest-selling product:", products[best_product_index])
print("Best-performing month:", months[best_month_index])
print("Lowest-performing month:", months[lowest_month_index])

print("\nGrand total units sold:", grand_total)
print("Monthly target:", monthly_target)
print("Months meeting target:", np.count_nonzero(target_met))
```

## NumPy concepts used in Project 2

| Concept | Where used |
|---|---|
| 2D arrays | Product-by-month sales table |
| `np.sum()` | Product and monthly totals |
| `np.mean()` | Average monthly sales |
| `np.argmax()` | Best product and month |
| `np.argmin()` | Lowest-performing month |
| `np.where()` | Locate high-sales cells |
| Boolean indexing | Select sales above a threshold |
| `np.diff()` | Month-over-month changes |
| Broadcasting / array arithmetic | Percentage calculations |
| `np.divide()` | Safe division with a `where` condition |
| `np.count_nonzero()` | Count months meeting the target |

## Project 2 – Student challenges

1. Add July, August, and September.
2. Add two more products.
3. Find the best month for each product.
4. Find the best product for each month.
5. Calculate each product's percentage contribution per month.
6. Find products whose total sales are below the overall product average.
7. Calculate cumulative sales over the months using `np.cumsum()`.
8. Calculate a three-month moving average.
9. Generate a target array with a different target for each month and compare it with monthly totals.
10. Save the sales data in `.npy` format and reload it.

---

# Part 20 – Additional advanced practice

## Chapter 41 – Cumulative operations

```python
numbers = np.array([10, 20, 30, 40])

print("Cumulative sum:", np.cumsum(numbers))
print("Cumulative product:", np.cumprod(numbers))
```

Cumulative sum is useful for running totals such as cumulative sales.

## Chapter 42 – Difference between consecutive values

```python
temperatures = np.array([25, 27, 26, 30, 32])

print(np.diff(temperatures))
```

This is useful for changes in measurements, sales, and time-series data.

## Chapter 43 – Clipping values

`np.clip()` limits values to a specified range.

```python
marks = np.array([-10, 20, 50, 110])

limited = np.clip(marks, 0, 100)

print(limited)
```

This example demonstrates clipping only. In a real application, investigate why values fall outside the valid range instead of silently changing them.

## Chapter 44 – Conditional replacement with `np.copyto()`

```python
marks = np.array([35, 45, 67, 89, 32, 95])

adjusted = marks.copy()

np.copyto(adjusted, 40, where=adjusted < 40)

print(adjusted)
```

This replaces values below 40 in the copy. The original array remains unchanged.

## Chapter 45 – Moving average

A simple moving average can be calculated with a sliding window.

```python
sales = np.array([100, 120, 130, 150, 170, 160])

window_size = 3

moving_average = np.convolve(
    sales,
    np.ones(window_size) / window_size,
    mode="valid"
)

print(moving_average)
```

For a window size of 3, each output is the average of three consecutive input values.

---

# Part 21 – Common mistakes

## Chapter 46 – Mistakes students should understand

### Mistake 1: Using `and` with array conditions

Incorrect:

```python
# marks > 40 and marks < 80
```

Correct:

```python
(marks > 40) & (marks < 80)
```

### Mistake 2: Forgetting parentheses

Incorrect:

```python
# marks > 40 & marks < 80
```

Correct:

```python
(marks > 40) & (marks < 80)
```

### Mistake 3: Confusing `*` and `@`

```python
A * B  # Element-wise multiplication
A @ B  # Matrix multiplication, when shapes are compatible
```

### Mistake 4: Confusing shape and size

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix.shape)  # (2, 3)
print(matrix.size)   # 6
```

### Mistake 5: Incorrect axis

For a matrix with students as rows and subjects as columns:

- `axis=1` calculates per student.
- `axis=0` calculates per subject.

### Mistake 6: Assuming every slice is a copy

Basic slices are generally views. Use `.copy()` when independent data is required.

### Mistake 7: Dividing by zero

Check denominators or use `np.divide()` with an appropriate `where` condition.

### Mistake 8: Assuming `np.empty()` returns zeros

It does not. Initialize values before using them.

### Mistake 9: Ignoring NaN

A NaN can affect calculations. Check and handle missing values deliberately.

### Mistake 10: Assuming arrays with different shapes can always be added

Check broadcasting compatibility before combining arrays.

---

# Part 22 – Revision questions

## Beginner questions

1. What is NumPy?
2. What is an `ndarray`?
3. How is a NumPy array different from a Python list?
4. What does `np.array()` do?
5. What is a one-dimensional array?
6. What is a two-dimensional array?
7. What is the difference between `shape` and `size`?
8. What does `dtype` represent?
9. What is the purpose of `np.zeros()`?
10. What is the difference between `np.arange()` and `np.linspace()`?

## Intermediate questions

11. How do you access the second row and third column of a matrix?
12. What does `array[1:4]` select?
13. What is element-wise multiplication?
14. What is vectorization?
15. What is broadcasting?
16. What is the difference between `axis=0` and `axis=1` for a 2D array?
17. How do you filter values greater than 50?
18. What does `np.where()` do?
19. What is the difference between `reshape()` and `transpose()`?
20. What is the difference between `np.concatenate()` and `np.split()`?

## Advanced questions

21. What is the difference between a view and a copy?
22. How can you check whether two arrays share memory?
23. What is NaN and how can you detect it?
24. What is the purpose of `np.nanmean()`?
25. Why should you use `np.random.default_rng()`?
26. What is the difference between `*` and `@`?
27. What shape rules apply to matrix multiplication?
28. How can you solve a system of linear equations using NumPy?
29. What is the difference between `flatten()` and `ravel()`?
30. How would you calculate month-over-month percentage change while avoiding division by zero?

---

# Final learning roadmap

| Stage | Topics | Outcome |
|---|---|---|
| 1. Foundation | NumPy introduction, arrays, dimensions | Understand NumPy arrays |
| 2. Creation | `array`, `zeros`, `ones`, `arange`, `linspace` | Create arrays in different ways |
| 3. Structure | Shape, size, dtype, indexing, slicing | Inspect and access data |
| 4. Operations | Arithmetic, comparisons, vectorization | Perform numerical calculations |
| 5. Intermediate | Broadcasting, aggregation, filtering | Analyze numerical data |
| 6. Advanced | Reshaping, joining, sorting, missing values | Manipulate real datasets |
| 7. Internals | Views, copies, random generation | Understand memory and reproducibility |
| 8. Numerical methods | Linear algebra and file operations | Solve numerical problems |
| 9. Projects | Student performance and sales analysis | Apply NumPy to practical tasks |

## What should students learn after NumPy?

A natural next sequence is:

1. **pandas** – work with rows, columns, CSV files, and tabular datasets.
2. **Matplotlib** – create charts and visualizations.
3. **Exploratory Data Analysis** – inspect, clean, and understand datasets.
4. **scikit-learn** – prepare data and build machine-learning models.

**Teaching recommendation:** Do not rush through the chapters. First make sure students understand the difference between a Python list and a NumPy array, then spend extra time on `shape`, `axis`, broadcasting, Boolean filtering, and views versus copies. These ideas are used repeatedly in data analysis and machine learning.
