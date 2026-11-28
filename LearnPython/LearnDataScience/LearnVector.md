# Python Vectors -- Complete Beginner-to-NumPy Learning Guide

**A chapter-wise practical course: start with core Python, understand
the mathematics, then learn NumPy.**

------------------------------------------------------------------------

## Course roadmap

This guide deliberately starts without NumPy. First, learn how Python
stores and processes numerical values. Then implement vector mathematics
yourself using lists and loops. Only after that will you introduce NumPy
and see how it makes numerical work simpler.

### Learning outcomes

By the end, you should be able to:

-   Explain what a mathematical vector is and where vectors are used.
-   Represent a one-dimensional vector using a Python list.
-   Use indexes, loops, conditions, functions, and list methods to
    process values.
-   Implement vector addition, subtraction, scalar multiplication,
    element-wise multiplication, division, and dot product.
-   Calculate totals, averages, minimums, maximums, and filtered
    results.
-   Explain the difference between a Python list and a NumPy array.
-   Create and manipulate one-dimensional NumPy arrays.
-   Use vectorized operations, Boolean filtering, and common NumPy
    functions.
-   Complete two practical projects first with core Python and then with
    NumPy.
-   Understand how vectors become useful in data analysis and machine
    learning.

### Recommended chapter order

  -----------------------------------------------------------------------
  Part                    Chapters                Focus
  ----------------------- ----------------------- -----------------------
  Part 1                  1--5                    Mathematical idea and
                                                  core Python foundation

  Part 2                  6--9                    Build vector operations
                                                  using Python lists

  Part 3                  10--11                  Two projects using only
                                                  core Python

  Part 4                  12--17                  Introduce NumPy and
                                                  learn array operations

  Part 5                  18--20                  NumPy projects,
                                                  revision, and
                                                  machine-learning
                                                  connection
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Part 1 -- Understand the foundation

# Chapter 1 -- What Is a Vector?

## 1.1 Start with a real-life example

Imagine a student receives these marks:

  Subject       Marks
  ----------- -------
  Maths            80
  Science          90
  English          75
  History          85
  Geography        95

We can write the values together:

``` python
marks = [80, 90, 75, 85, 95]
```

This is a Python list that represents a one-dimensional numerical
vector.

A **vector** is an ordered collection of numerical values in this
context. The order matters because each position has a meaning. In this
example, the first value is Maths, the second is Science, and so on.

A vector can represent:

-   Student marks in different subjects.
-   Sales across different months.
-   Temperatures recorded on different days.
-   Employee features such as age and years of experience.
-   Position, velocity, force, and other quantities in mathematics and
    engineering.

> Important distinction: a vector is a mathematical concept. A Python
> list is a data structure. We can use a list to represent a vector, but
> a list and a mathematical vector are not the same thing.

## 1.2 Why do we need vectors?

Imagine storing marks for 1,000 students as separate variables:

``` python
student1 = 80
student2 = 90
student3 = 75
student4 = 85
student5 = 95
```

This approach becomes difficult to manage as the number of values grows.

Instead, keep related values together:

``` python
marks = [80, 90, 75, 85, 95]
```

Now we can process all the values using one loop:

``` python
marks = [80, 90, 75, 85, 95]

updated_marks = []

for mark in marks:
    updated_marks.append(mark + 5)

print(updated_marks)
```

Output:

``` text
[85, 95, 80, 90, 100]
```

We processed every mark without writing a separate statement for every
student.

## 1.3 Where are vectors used?

  Area               Example
  ------------------ -------------------------------------
  Education          Marks of students
  Business           Monthly sales
  Data analysis      Salaries, prices, temperatures
  Machine learning   Features such as age and experience
  Engineering        Force, velocity, and position
  Image processing   Numerical pixel values

## 1.4 A simple mathematical view

A vector can be written as:

\[ A = \[10, 20, 30\] \]

It contains three values. We can refer to these values by their
positions:

-   First value: 10
-   Second value: 20
-   Third value: 30

In Python, positions are accessed using indexes, which start at zero. We
will practise this in the next chapter.

------------------------------------------------------------------------

# Chapter 2 -- Python Lists: Store Values Together

Before doing vector mathematics, understand the Python list.

## 2.1 Create a list

``` python
numbers = [10, 20, 30, 40, 50]

print(numbers)
print(type(numbers))
```

Output:

``` text
[10, 20, 30, 40, 50]
<class 'list'>
```

A list is built into Python. No installation is required.

## 2.2 A list can store different data types

``` python
student = ["Rahul", 21, 85.5, True]

print(student)
```

A list can contain strings, integers, floating-point numbers, Boolean
values, and even other lists.

When representing a numerical vector, we normally use values that are
suitable for the same mathematical operation.

## 2.3 Indexing: access an element

``` python
numbers = [10, 20, 30, 40, 50]

print(numbers[0])
print(numbers[1])
print(numbers[2])
```

Output:

``` text
10
20
30
```

Python indexing starts at zero.

    Index   Value
  ------- -------
        0      10
        1      20
        2      30
        3      40
        4      50

## 2.4 Access the last element

``` python
numbers = [10, 20, 30, 40, 50]

print(numbers[-1])
```

Output:

``` text
50
```

Negative indexing starts from the end of the list. `-1` means the last
element.

## 2.5 Update an element

``` python
numbers = [10, 20, 30, 40, 50]

numbers[0] = 100

print(numbers)
```

Output:

``` text
[100, 20, 30, 40, 50]
```

## 2.6 Find the number of elements

``` python
numbers = [10, 20, 30, 40, 50]

print(len(numbers))
```

Output:

``` text
5
```

`len()` returns the number of elements.

## 2.7 Slicing: access a range

``` python
numbers = [10, 20, 30, 40, 50]

print(numbers[1:4])
```

Output:

``` text
[20, 30, 40]
```

The starting index is included and the ending index is excluded.

## 2.8 Add and remove values

``` python
numbers = [10, 20, 30]

numbers.append(40)
print(numbers)

numbers.remove(20)
print(numbers)
```

Output:

``` text
[10, 20, 30, 40]
[10, 30, 40]
```

`append()` adds an item at the end. `remove()` removes the first
matching value.

## 2.9 Loop through a list

``` python
numbers = [10, 20, 30, 40]

for number in numbers:
    print(number)
```

A loop lets us perform the same task for every value.

------------------------------------------------------------------------

# Chapter 3 -- Python Concepts Needed for Vector Operations

This chapter revises the core Python concepts used throughout the
course.

## 3.1 The `for` loop

``` python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

The loop takes one value at a time.

## 3.2 The `range()` function and indexes

``` python
numbers = [10, 20, 30]

for i in range(len(numbers)):
    print("Index:", i, "Value:", numbers[i])
```

Output:

``` text
Index: 0 Value: 10
Index: 1 Value: 20
Index: 2 Value: 30
```

Use this pattern when you need to access corresponding positions in two
lists.

## 3.3 Conditions

``` python
marks = [45, 67, 89, 32, 95]

for mark in marks:
    if mark >= 50:
        print(mark, "Passed")
    else:
        print(mark, "Failed")
```

## 3.4 Build a new list using `append()`

``` python
numbers = [10, 20, 30]

doubled = []

for number in numbers:
    doubled.append(number * 2)

print(doubled)
```

Output:

``` text
[20, 40, 60]
```

## 3.5 Functions: reuse logic

``` python
def greet():
    print("Hello")

greet()
```

A function can accept input values and return a result:

``` python
def add(a, b):
    result = a + b
    return result

answer = add(10, 20)
print(answer)
```

Output:

``` text
30
```

We will use functions to write reusable vector operations.

## 3.6 Useful built-in functions

``` python
numbers = [10, 50, 30, 90, 20]

print("Count:", len(numbers))
print("Total:", sum(numbers))
print("Highest:", max(numbers))
print("Lowest:", min(numbers))
```

These functions will help us analyse numerical lists.

------------------------------------------------------------------------

# Part 2 -- Implement vector mathematics using core Python

# Chapter 4 -- Vector Addition and Subtraction

Now we will implement mathematical vector operations using only normal
Python. No NumPy is used in this part.

## 4.1 Understand vector addition

Suppose:

\[ A = \[10, 20, 30\] \]

\[ B = \[1, 2, 3\] \]

Add corresponding values:

\[ A+B = \[10+1, 20+2, 30+3\] \]

Result:

``` text
[11, 22, 33]
```

## 4.2 Write the code using a loop

``` python
a = [10, 20, 30]
b = [1, 2, 3]

result = []

for i in range(len(a)):
    result.append(a[i] + b[i])

print(result)
```

Output:

``` text
[11, 22, 33]
```

Understand each line:

-   `len(a)` gives the number of elements.
-   `range(len(a))` generates indexes 0, 1, and 2.
-   `a[i]` accesses a value from the first list.
-   `b[i]` accesses the value at the same position in the second list.
-   `append()` stores the calculated result.

## 4.3 Make it reusable with a function

``` python
def vector_add(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    result = []

    for i in range(len(a)):
        result.append(a[i] + b[i])

    return result


a = [10, 20, 30]
b = [1, 2, 3]

print(vector_add(a, b))
```

The length check is important: this basic operation expects both vectors
to have the same number of elements.

## 4.4 Vector subtraction

\[ A = \[10, 20, 30\] \]

\[ B = \[1, 2, 3\] \]

\[ A-B = \[9, 18, 27\] \]

``` python
def vector_subtract(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    result = []

    for i in range(len(a)):
        result.append(a[i] - b[i])

    return result


print(vector_subtract([10, 20, 30], [1, 2, 3]))
```

Output:

``` text
[9, 18, 27]
```

## 4.5 Why do we use the same index?

The first value of one vector is combined with the first value of the
other vector, the second with the second, and so on.

``` text
A = [10, 20, 30]
     |   |   |
B = [ 1,  2,  3]
     |   |   |
     +   +   +
     11  22  33
```

This is called an element-wise operation.

------------------------------------------------------------------------

# Chapter 5 -- Multiplication, Division, and Dot Product

## 5.1 Scalar multiplication

A scalar is a single numerical value.

If we multiply every element of a vector by 5:

\[5 \times [10,20,30] = [50,100,150]\]

``` python
def scalar_multiply(vector, number):
    result = []

    for value in vector:
        result.append(value * number)

    return result


numbers = [10, 20, 30]

print(scalar_multiply(numbers, 5))
```

Output:

``` text
[50, 100, 150]
```

## 5.2 Element-wise multiplication

This operation multiplies corresponding elements of two vectors.

\[[10,20,30] \times [2,3,4] = [20,60,120]\]

``` python
def vector_multiply(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    result = []

    for i in range(len(a)):
        result.append(a[i] * b[i])

    return result


print(vector_multiply([10, 20, 30], [2, 3, 4]))
```

## 5.3 Element-wise division

``` python
def vector_divide(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    result = []

    for i in range(len(a)):
        if b[i] == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        result.append(a[i] / b[i])

    return result


print(vector_divide([10, 20, 30], [2, 4, 5]))
```

Output:

``` text
[5.0, 5.0, 6.0]
```

## 5.4 Dot product

The dot product is a mathematical operation. Multiply corresponding
elements and add all the products.

Given:

$$
A = [2, 3, 4], \qquad B = [5, 6, 7]
$$

The dot product is:

$$
A \cdot B = (2 \times 5) + (3 \times 6) + (4 \times 7) = 10 + 18 + 28 = 56
$$

Python implementation:

``` python
def dot_product(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    result = 0

    for i in range(len(a)):
        result += a[i] * b[i]

    return result


a = [2, 3, 4]
b = [5, 6, 7]

print(dot_product(a, b))
```

Output:

``` text
56
```

Dot products are used in machine learning and many other mathematical
applications.

------------------------------------------------------------------------

# Chapter 6 -- Sum, Average, Minimum, Maximum, and Filtering

## 6.1 Calculate the sum manually

``` python
numbers = [10, 20, 30, 40, 50]

total = 0

for number in numbers:
    total = total + number

print("Total:", total)
```

Output:

``` text
Total: 150
```

Python also has a built-in function:

``` python
print(sum(numbers))
```

## 6.2 Calculate the average

Average = total / number of values.

``` python
marks = [80, 90, 75, 85, 95]

total = sum(marks)
count = len(marks)

average = total / count

print("Average:", average)
```

Output:

``` text
Average: 85.0
```

For an empty list, do not divide by zero. Check that the list contains
values before calculating an average.

## 6.3 Find the maximum manually

``` python
numbers = [10, 50, 30, 90, 20]

highest = numbers[0]

for number in numbers:
    if number > highest:
        highest = number

print("Highest:", highest)
```

Python also provides `max(numbers)`.

## 6.4 Find the minimum manually

``` python
numbers = [10, 50, 30, 90, 20]

lowest = numbers[0]

for number in numbers:
    if number < lowest:
        lowest = number

print("Lowest:", lowest)
```

Python also provides `min(numbers)`.

## 6.5 Filter values using a condition

Find students who passed, assuming 50 is the passing mark:

``` python
marks = [45, 67, 89, 32, 95, 56]

passed = []

for mark in marks:
    if mark >= 50:
        passed.append(mark)

print(passed)
```

Output:

``` text
[67, 89, 95, 56]
```

## 6.6 Count values matching a condition

``` python
marks = [45, 67, 89, 32, 95, 56]

passed_count = 0

for mark in marks:
    if mark >= 50:
        passed_count += 1

print("Passed students:", passed_count)
```

Output:

``` text
Passed students: 4
```

## 6.7 List comprehension

After understanding the loop, learn the shorter alternative:

``` python
marks = [45, 67, 89, 32, 95, 56]

passed = [mark for mark in marks if mark >= 50]

print(passed)
```

This is called list comprehension. Learn the normal loop first.

## 6.8 Sort values

``` python
numbers = [40, 10, 30, 20]

numbers.sort()

print(numbers)
```

Output:

``` text
[10, 20, 30, 40]
```

`sort()` changes the original list. `sorted(numbers)` returns a new
sorted list.

------------------------------------------------------------------------

# Chapter 7 -- Python List vs Other Data Structures vs Mathematical Vector

A Python list is a general-purpose container. Other Python data
structures solve different problems.

## 7.1 List

``` python
student = ["Rahul", 22, 85.5]
```

Use a list for an ordered, changeable collection.

## 7.2 Tuple

``` python
coordinates = (10, 20, 30)
```

A tuple is ordered but cannot be modified after creation.

## 7.3 Set

``` python
numbers = {10, 20, 20, 30}

print(numbers)
```

A set stores unique values and does not provide positional indexing.

## 7.4 Dictionary

``` python
student = {
    "name": "Rahul",
    "age": 22,
    "marks": 85
}

print(student["name"])
```

A dictionary stores key-value pairs.

## 7.5 Comparison

  -----------------------------------------------------------------------
  Requirement                         Suitable structure
  ----------------------------------- -----------------------------------
  Ordered, changeable collection      List

  Fixed collection                    Tuple

  Unique values                       Set

  Key-value information               Dictionary

  Numerical vector calculations       Python list with loops, or NumPy
                                      array
  -----------------------------------------------------------------------

## 7.6 The important distinction

A Python list is not automatically a mathematical vector. For example:

``` python
a = [10, 20, 30]
b = [1, 2, 3]

print(a + b)
```

Output:

``` text
[10, 20, 30, 1, 2, 3]
```

This joins the lists. It does not add corresponding values.

To perform vector addition, we wrote a loop:

``` python
result = []

for i in range(len(a)):
    result.append(a[i] + b[i])

print(result)
```

Output:

``` text
[11, 22, 33]
```

The same issue occurs with multiplication:

``` python
numbers = [10, 20, 30]

print(numbers * 2)
```

Output:

``` text
[10, 20, 30, 10, 20, 30]
```

The list repeats. For scalar multiplication, use a loop.

------------------------------------------------------------------------

# Chapter 8 -- Project 1: Student Marks Analyzer Using Core Python

## Objective

Build a program that:

1.  Stores student marks.
2.  Calculates total and average marks.
3.  Finds highest and lowest marks.
4.  Counts passed and failed students.
5.  Displays marks of high scorers.
6.  Increases marks by 5, without allowing a score above 100.

## File: `student_marks_core_python.py`

``` python
# Store student marks in a Python list
marks = [45, 67, 89, 32, 95, 76, 55, 82]

# Calculate total marks
total = sum(marks)

# Calculate average
average = total / len(marks)

# Find highest and lowest marks
highest = max(marks)
lowest = min(marks)

# Create counters
passed_count = 0
failed_count = 0

# Create an empty list for high scorers
high_scorers = []

# Check every student's marks
for mark in marks:

    # Check whether the student passed
    if mark >= 50:
        passed_count += 1
    else:
        failed_count += 1

    # Find students scoring 75 or above
    if mark >= 75:
        high_scorers.append(mark)

# Increase every student's marks by 5
updated_marks = []

for mark in marks:
    new_mark = mark + 5

    # Do not allow marks to exceed 100
    if new_mark > 100:
        new_mark = 100

    updated_marks.append(new_mark)

# Display the report
print("STUDENT MARKS ANALYZER")
print("---------------------")
print("Original Marks:", marks)
print("Total:", total)
print("Average:", average)
print("Highest:", highest)
print("Lowest:", lowest)
print("Passed:", passed_count)
print("Failed:", failed_count)
print("High Scorers:", high_scorers)
print("Updated Marks:", updated_marks)
```

## Expected output

``` text
STUDENT MARKS ANALYZER
---------------------
Original Marks: [45, 67, 89, 32, 95, 76, 55, 82]
Total: 541
Average: 67.625
Highest: 95
Lowest: 32
Passed: 6
Failed: 2
High Scorers: [89, 95, 76, 82]
Updated Marks: [50, 72, 94, 37, 100, 81, 60, 87]
```

## What you learned

-   Lists and indexes.
-   Loops and conditions.
-   `append()`, `sum()`, `min()`, and `max()`.
-   Counters and filtering.
-   Mathematical calculations.

## Practice tasks

1.  Add five more students.
2.  Find marks between 60 and 80.
3.  Calculate the passing percentage.
4.  Find the second-highest mark.
5.  Assign grades using conditions.
6.  Display marks in ascending order.

------------------------------------------------------------------------

# Chapter 9 -- Project 2: Monthly Sales Analyzer Using Core Python

## Objective

A company has recorded sales for 12 months. Use Python lists to:

1.  Calculate annual sales.
2.  Calculate average monthly sales.
3.  Find the best and worst sales months.
4.  Identify months with above-average sales.
5.  Calculate projected sales after a 10% increase.
6.  Calculate the difference between projected and actual sales.

## File: `monthly_sales_core_python.py`

``` python
# Store month names
months = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

# Store monthly sales
sales = [
    12000, 15000, 18000, 14000,
    22000, 25000, 20000, 28000,
    30000, 27000, 35000, 40000
]

# Calculate annual sales and average sales
annual_sales = sum(sales)
average_sales = annual_sales / len(sales)

# Find highest and lowest sales
highest_sales = max(sales)
lowest_sales = min(sales)

# Find the indexes of the best and worst months
best_index = sales.index(highest_sales)
worst_index = sales.index(lowest_sales)

# Find corresponding month names
best_month = months[best_index]
worst_month = months[worst_index]

# Prepare result lists
above_average_months = []
projected_sales = []
sales_increase = []

# Process every month
for i in range(len(sales)):

    # Check whether sales are above average
    if sales[i] > average_sales:
        above_average_months.append(months[i])

    # Calculate a hypothetical 10% increase
    projected = sales[i] * 1.10
    projected_sales.append(projected)

    # Calculate the increase over actual sales
    increase = projected - sales[i]
    sales_increase.append(increase)

# Display the report
print("MONTHLY SALES ANALYZER")
print("----------------------")
print("Annual Sales:", annual_sales)
print("Average Sales:", average_sales)
print("Highest Sales:", highest_sales)
print("Lowest Sales:", lowest_sales)
print("Best Month:", best_month)
print("Worst Month:", worst_month)
print("Above Average Months:", above_average_months)
print("Projected Sales:", projected_sales)
print("Sales Increase:", sales_increase)
```

## Expected output

``` text
MONTHLY SALES ANALYZER
----------------------
Annual Sales: 286000
Average Sales: 23833.333333333332
Highest Sales: 40000
Lowest Sales: 12000
Best Month: Dec
Worst Month: Jan
Above Average Months: ['Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
Projected Sales: [13200.0, 16500.0, 19800.0, 15400.0, 24200.0, 27500.0, 22000.0, 30800.0, 33000.0, 29700.0, 38500.0, 44000.0]
```

**Note:** The 10% increase is a hypothetical scenario, not a
machine-learning forecast.

## What you learned

-   Working with two related lists.
-   Accessing corresponding values using indexes.
-   Finding maximum and minimum values.
-   Finding an element's index.
-   Filtering data.
-   Percentage calculations.
-   Creating a simple business report.

## Practice tasks

1.  Find the second-highest sales value and month.
2.  Find all months with sales below 20,000.
3.  Calculate sales for the first six months.
4.  Calculate sales for the last six months.
5.  Calculate a 15% increase instead of 10%.
6.  Display each month with actual and projected sales.

------------------------------------------------------------------------

# Part 3 -- Move from core Python to NumPy

# Chapter 10 -- Why Do We Need NumPy?

You have now implemented vector operations using lists and loops. This
is important because you understand what happens behind the calculation.

But imagine processing millions of numerical values. Writing and
managing a separate loop for every operation can become inconvenient.

NumPy is a Python library designed for numerical computing. It provides
arrays and operations that work efficiently on numerical data.

## 10.1 Core Python approach

``` python
a = [10, 20, 30]
b = [1, 2, 3]

result = []

for i in range(len(a)):
    result.append(a[i] + b[i])

print(result)
```

Output:

``` text
[11, 22, 33]
```

## 10.2 NumPy approach

``` python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

print(a + b)
```

Output:

``` text
[11 22 33]
```

Both perform the same mathematical operation. NumPy lets us express it
directly and is generally more efficient for large numerical workloads.

## 10.3 Python list vs NumPy array

  --------------------------------------------------------------------------
  Feature                 Python List             NumPy Array
  ----------------------- ----------------------- --------------------------
  Installation            Built into Python       Requires NumPy

  Creation                `[10, 20, 30]`          `np.array([10, 20, 30])`

  Main use                General-purpose         Numerical computing
                          collection              

  Data types              Can contain mixed types Normally uses one common
                                                  data type

  Addition                Joins lists             Adds corresponding
                                                  elements

  Multiplication by a     Repeats the list        Multiplies each element
  number                                          

  Filtering               Loop or list            Boolean indexing
                          comprehension           

  Dimensions              Nested lists can        Supports multidimensional
                          represent dimensions    arrays
  --------------------------------------------------------------------------

------------------------------------------------------------------------

# Chapter 11 -- Install NumPy and Create Your First Array

## 11.1 Check Python

Open a terminal:

``` bash
python --version
```

If your system uses `python3`:

``` bash
python3 --version
```

## 11.2 Install NumPy

``` bash
pip install numpy
```

If required, use:

``` bash
python -m pip install numpy
```

On systems where Python 3 uses `python3`:

``` bash
python3 -m pip install numpy
```

## 11.3 Import NumPy

``` python
import numpy as np
```

`np` is the commonly used short alias for NumPy.

## 11.4 Create a NumPy array from a list

``` python
import numpy as np

numbers = np.array([10, 20, 30, 40, 50])

print(numbers)
print(type(numbers))
```

Output:

``` text
[10 20 30 40 50]
<class 'numpy.ndarray'>
```

A one-dimensional NumPy array is commonly used as a numerical vector.

## 11.5 Inspect the array

``` python
numbers = np.array([10, 20, 30, 40, 50])

print("Number of elements:", numbers.size)
print("Shape:", numbers.shape)
print("Dimensions:", numbers.ndim)
print("Data type:", numbers.dtype)
```

For this one-dimensional array:

-   `size` is the number of elements.
-   `shape` describes the dimensions; here it is `(5,)`.
-   `ndim` is the number of dimensions; here it is `1`.
-   `dtype` tells you the array's element data type.

------------------------------------------------------------------------

# Chapter 12 -- Create NumPy Vectors in Different Ways

## 12.1 Create from a list

``` python
numbers = np.array([10, 20, 30, 40, 50])
print(numbers)
```

## 12.2 Create a vector of zeros

``` python
zeros = np.zeros(5)
print(zeros)
```

Output:

``` text
[0. 0. 0. 0. 0.]
```

Useful when you need to initialise values with zero.

## 12.3 Create a vector of ones

``` python
ones = np.ones(5)
print(ones)
```

Output:

``` text
[1. 1. 1. 1. 1.]
```

## 12.4 Create a sequence using `arange()`

``` python
numbers = np.arange(1, 11)
print(numbers)
```

Output:

``` text
[ 1  2  3  4  5  6  7  8  9 10]
```

The ending value is excluded.

Another example:

``` python
numbers = np.arange(2, 11, 2)
print(numbers)
```

Output:

``` text
[ 2  4  6  8 10]
```

Syntax:

``` python
np.arange(start, stop, step)
```

## 12.5 Create evenly spaced values using `linspace()`

``` python
numbers = np.linspace(0, 100, 5)
print(numbers)
```

Output:

``` text
[  0.  25.  50.  75. 100.]
```

Here, 0 is the starting value, 100 is the ending value, and 5 is the
number of values to generate.

Difference:

-   `arange()` uses a step size.
-   `linspace()` uses the number of values.

------------------------------------------------------------------------

# Chapter 13 -- NumPy Vector Arithmetic

Assume we have two vectors:

``` python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([2, 4, 6])
```

## 13.1 Addition

``` python
result = a + b
print(result)
```

Output:

``` text
[12 24 36]
```

## 13.2 Subtraction

``` python
result = a - b
print(result)
```

Output:

``` text
[ 8 16 24]
```

## 13.3 Element-wise multiplication

``` python
result = a * b
print(result)
```

Output:

``` text
[ 20  80 180]
```

## 13.4 Element-wise division

``` python
result = a / b
print(result)
```

Output:

``` text
[5. 5. 5.]
```

## 13.5 Add a single number to every element

``` python
numbers = np.array([10, 20, 30])

print(numbers + 5)
```

Output:

``` text
[15 25 35]
```

## 13.6 Multiply every element by a number

``` python
numbers = np.array([10, 20, 30])

print(numbers * 3)
```

Output:

``` text
[30 60 90]
```

## 13.7 Square every element

``` python
numbers = np.array([2, 3, 4, 5])

print(numbers ** 2)
```

Output:

``` text
[ 4  9 16 25]
```

## 13.8 Calculate square roots

``` python
numbers = np.array([4, 9, 16, 25])

print(np.sqrt(numbers))
```

Output:

``` text
[2. 3. 4. 5.]
```

------------------------------------------------------------------------

# Chapter 14 -- NumPy Indexing, Slicing, and Updating

## 14.1 Access one element

``` python
marks = np.array([70, 80, 90, 85, 95])

print(marks[0])
print(marks[2])
```

Output:

``` text
70
90
```

Python indexing starts at zero.

## 14.2 Access the last element

``` python
print(marks[-1])
```

Output:

``` text
95
```

## 14.3 Slicing

``` python
print(marks[1:4])
```

Output:

``` text
[80 90 85]
```

The ending index is excluded.

## 14.4 Update an element

``` python
marks[0] = 75

print(marks)
```

Output:

``` text
[75 80 90 85 95]
```

------------------------------------------------------------------------

# Chapter 15 -- NumPy Statistics and Useful Functions

Use these functions frequently when working with numerical data.

``` python
import numpy as np

marks = np.array([60, 75, 80, 90, 95])

print("Total:", np.sum(marks))
print("Average:", np.mean(marks))
print("Highest:", np.max(marks))
print("Lowest:", np.min(marks))
print("Median:", np.median(marks))
print("Standard deviation:", np.std(marks))
print("Sorted:", np.sort(marks))
print("Index of maximum:", np.argmax(marks))
print("Index of minimum:", np.argmin(marks))
print("Number of elements:", marks.size)
print("Shape:", marks.shape)
print("Data type:", marks.dtype)
```

  Function or property   Purpose
  ---------------------- -------------------------------
  `np.sum(values)`       Adds all values
  `np.mean(values)`      Calculates average
  `np.max(values)`       Finds maximum
  `np.min(values)`       Finds minimum
  `np.median(values)`    Finds middle value
  `np.std(values)`       Calculates standard deviation
  `np.sort(values)`      Returns sorted values
  `np.argmax(values)`    Returns index of maximum
  `np.argmin(values)`    Returns index of minimum
  `values.size`          Number of elements
  `values.shape`         Array shape
  `values.dtype`         Element data type

Important difference:

``` python
numbers = np.array([10, 20, 30])

print(np.argmax(numbers))
print(np.max(numbers))
```

Output:

``` text
2
30
```

`argmax()` returns the index of the maximum value. `max()` returns the
value itself.

------------------------------------------------------------------------

# Chapter 16 -- NumPy Filtering and Conditions

## 16.1 Compare every element

``` python
marks = np.array([45, 67, 89, 32, 95])

print(marks > 50)
```

Output:

``` text
[False  True  True False  True]
```

Each value is compared with 50. The result is a Boolean array.

## 16.2 Filter values

``` python
marks = np.array([45, 67, 89, 32, 95, 56])

passed = marks[marks >= 50]

print(passed)
```

Output:

``` text
[67 89 95 56]
```

This is called Boolean indexing.

## 16.3 Count matching values

``` python
marks = np.array([45, 67, 89, 32, 95, 56])

count = np.sum(marks >= 50)

print("Students passed:", count)
```

Output:

``` text
Students passed: 4
```

## 16.4 Combine conditions

Use parentheses around each condition.

``` python
marks = np.array([45, 67, 89, 32, 95])

result = marks[(marks >= 50) & (marks <= 90)]

print(result)
```

Output:

``` text
[67 89]
```

-   `&` means AND.
-   `|` means OR.
-   `~` means NOT.

## 16.5 Use `np.where()` to assign grades

``` python
marks = np.array([45, 67, 89, 32, 95, 76, 55, 82])

grades = np.where(
    marks >= 90, "A",
    np.where(
        marks >= 75, "B",
        np.where(marks >= 50, "C", "F")
    )
)

print(grades)
```

Output:

``` text
['F' 'C' 'B' 'F' 'A' 'B' 'C' 'B']
```

------------------------------------------------------------------------

# Chapter 17 -- What Is Vectorization?

Consider two NumPy arrays:

``` python
a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

result = a + b
```

NumPy applies the operation to corresponding elements:

``` text
a      = [10, 20, 30]
b      = [ 1,  2,  3]
result = [11, 22, 33]
```

This behaviour is called **vectorization**.

Vectorization allows us to express operations on entire arrays without
writing an explicit Python loop for every element.

Compare the two approaches:

Core Python:

``` python
a = [10, 20, 30]
b = [1, 2, 3]

result = []

for i in range(len(a)):
    result.append(a[i] + b[i])

print(result)
```

NumPy:

``` python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

print(a + b)
```

Both produce:

``` text
[11, 22, 33]
```

Important points:

-   Corresponding elements are combined.
-   Basic element-wise operations require compatible array shapes.
-   A one-dimensional array has one axis.
-   NumPy arrays generally use a common data type for their elements.
-   NumPy also supports two-dimensional and higher-dimensional arrays;
    those are the next topic after this beginner guide.

------------------------------------------------------------------------

# Part 4 -- Repeat the Projects Using NumPy

# Chapter 18 -- Project 1: Student Marks Analyzer Using NumPy

## Objective

Build the same student marks analyser using NumPy. Compare it with the
core Python version from Chapter 8.

## File: `student_marks_numpy.py`

``` python
import numpy as np

# Store marks in a NumPy vector
marks = np.array([45, 67, 89, 32, 95, 76, 55, 82])

# Calculate total and average
total = np.sum(marks)
average = np.mean(marks)

# Find highest and lowest marks
highest = np.max(marks)
lowest = np.min(marks)

# Count students who passed and failed
passed_count = np.sum(marks >= 50)
failed_count = np.sum(marks < 50)

# Filter students scoring 75 or above
high_scorers = marks[marks >= 75]

# Increase every mark by 5
updated_marks = marks + 5

# Prevent marks from exceeding 100
updated_marks = np.minimum(updated_marks, 100)

# Assign grades using conditions
grades = np.where(
    marks >= 90, "A",
    np.where(
        marks >= 75, "B",
        np.where(marks >= 50, "C", "F")
    )
)

# Display results
print("STUDENT MARKS ANALYZER")
print("----------------------")
print("All Marks:", marks)
print("Total Marks:", total)
print("Average Marks:", average)
print("Highest Marks:", highest)
print("Lowest Marks:", lowest)
print("Passed Students:", passed_count)
print("Failed Students:", failed_count)
print("Students scoring 75 or above:", high_scorers)
print("Updated Marks:", updated_marks)
print("Student Grades:", grades)
```

## Expected output

``` text
STUDENT MARKS ANALYZER
----------------------
All Marks: [45 67 89 32 95 76 55 82]
Total Marks: 541
Average Marks: 67.625
Highest Marks: 95
Lowest Marks: 32
Passed Students: 6
Failed Students: 2
Students scoring 75 or above: [89 95 76 82]
Updated Marks: [ 50  72  94  37 100  81  60  87]
Student Grades: ['F' 'C' 'B' 'F' 'A' 'B' 'C' 'B']
```

## Compare the two versions

  Task                     Core Python                 NumPy
  ------------------------ --------------------------- -----------------------
  Total                    `sum(marks)`                `np.sum(marks)`
  Average                  `sum(marks) / len(marks)`   `np.mean(marks)`
  Add 5 to every mark      Loop and append             `marks + 5`
  Filter passing marks     Loop and condition          `marks[marks >= 50]`
  Count passing students   Counter in a loop           `np.sum(marks >= 50)`
  Assign grades            Conditions in a loop        `np.where()`

## Practice tasks

1.  Add five more students.
2.  Find the second-highest mark.
3.  Calculate passing percentage.
4.  Display marks between 60 and 80.
5.  Increase marks by 5 without exceeding 100.
6.  Compare the code with the core Python version.

------------------------------------------------------------------------

# Chapter 19 -- Project 2: Monthly Sales Analyzer Using NumPy

## Objective

Use NumPy arrays to analyse monthly sales.

## File: `monthly_sales_numpy.py`

``` python
import numpy as np

# Store monthly sales in a NumPy vector
sales = np.array([
    12000, 15000, 18000, 14000,
    22000, 25000, 20000, 28000,
    30000, 27000, 35000, 40000
])

# Store month names
months = np.array([
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
])

# Calculate annual and average sales
annual_sales = np.sum(sales)
average_sales = np.mean(sales)

# Find highest and lowest sales
highest_sales = np.max(sales)
lowest_sales = np.min(sales)

# Find the index of highest and lowest sales
highest_index = np.argmax(sales)
lowest_index = np.argmin(sales)

# Find the corresponding months
best_month = months[highest_index]
worst_month = months[lowest_index]

# Filter months with above-average sales
above_average_months = months[sales > average_sales]

# Calculate projected sales after a 10% increase
projected_sales = sales * 1.10

# Calculate the increase over actual sales
sales_increase = projected_sales - sales

# Display report
print("MONTHLY SALES ANALYZER")
print("----------------------")
print("Monthly Sales:", sales)
print("Annual Sales:", annual_sales)
print("Average Monthly Sales:", average_sales)
print("Highest Sales:", highest_sales)
print("Lowest Sales:", lowest_sales)
print("Best Month:", best_month)
print("Worst Month:", worst_month)
print("Months Above Average:", above_average_months)
print("Projected Sales:", projected_sales)
print("Sales Increase:", sales_increase)
```

## Expected output

``` text
MONTHLY SALES ANALYZER
----------------------
Annual Sales: 286000
Average Monthly Sales: 23833.333333333332
Highest Sales: 40000
Lowest Sales: 12000
Best Month: Dec
Worst Month: Jan
Months Above Average: ['Jun' 'Aug' 'Sep' 'Oct' 'Nov' 'Dec']
Projected Sales: [13200. 16500. 19800. 15400. 24200. 27500.
 22000. 30800. 33000. 29700. 38500. 44000.]
```

**Note:** The 10% increase is a hypothetical scenario, not a
machine-learning forecast.

## Practice tasks

1.  Find the month with the lowest sales.
2.  Find all months with sales below 20,000.
3.  Calculate sales after a 15% increase.
4.  Calculate the difference between projected and actual sales.
5.  Find the average sales for the first six months.
6.  Find total sales for the last six months.

------------------------------------------------------------------------

# Part 5 -- Revision and Next Steps

# Chapter 20 -- Common Beginner Mistakes

## Mistake 1: Forgetting to import NumPy

Incorrect:

``` python
numbers = np.array([10, 20, 30])
```

Correct:

``` python
import numpy as np

numbers = np.array([10, 20, 30])
```

## Mistake 2: Expecting list addition behaviour from NumPy

``` python
a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

print(a + b)
```

Output:

``` text
[11 22 33]
```

NumPy adds corresponding elements; it does not concatenate arrays.

## Mistake 3: Using incompatible shapes

``` python
a = np.array([10, 20, 30])
b = np.array([1, 2])

print(a + b)
```

This produces a broadcasting error because these shapes are incompatible
for this operation.

## Mistake 4: Confusing index and value

``` python
numbers = np.array([10, 20, 30])

print(np.argmax(numbers))
```

Output:

``` text
2
```

`argmax()` returns the index of the maximum value, not the maximum value
itself.

Use:

``` python
print(np.max(numbers))
```

Output:

``` text
30
```

## Mistake 5: Forgetting that the ending slice index is excluded

``` python
numbers = np.array([10, 20, 30, 40, 50])

print(numbers[1:4])
```

Output:

``` text
[20 30 40]
```

## Mistake 6: Dividing by zero

Before calculating an average, check that the list or array contains at
least one value. Before element-wise division, check that the divisor is
not zero.

------------------------------------------------------------------------

# Chapter 21 -- Practice Questions

Try solving these without looking at the earlier examples.

## Level 1 -- Core Python foundation

1.  Create a list containing 10 numbers.
2.  Print every element using a `for` loop.
3.  Find the length of the list.
4.  Find the sum without using `sum()`.
5.  Calculate the average.
6.  Find the highest value without using `max()`.
7.  Find the lowest value without using `min()`.
8.  Print all even numbers.
9.  Print all odd numbers.
10. Count values greater than 50.

## Level 2 -- Manual vector operations

11. Add two vectors element by element.
12. Subtract two vectors element by element.
13. Multiply every element by 10.
14. Multiply two vectors element by element.
15. Find the dot product of two vectors.
16. Filter values between 20 and 50.
17. Reverse a vector.
18. Sort a vector in ascending order.
19. Find the index of the highest value.
20. Increase employee salaries by 8%.

## Level 3 -- NumPy

21. Create a NumPy array from a list.
22. Create an array of five zeros.
23. Create an array of five ones.
24. Generate numbers from 1 to 20 using `arange()`.
25. Generate five evenly spaced values between 0 and 100 using
    `linspace()`.
26. Add two NumPy arrays.
27. Multiply every element by 5.
28. Find the mean, median, maximum, and minimum.
29. Filter all values greater than 50.
30. Find the index of the maximum value.

## Level 4 -- Real-life numerical practice

31. Create a vector of 10 temperatures and convert Celsius to Fahrenheit
    using `F = C * 9/5 + 32`.
32. Create a vector of employee salaries and increase every salary by
    8%.
33. Given product-price and quantity vectors, calculate each product's
    cost and the total cost.
34. Create a vector of daily expenses and calculate the total and
    average expense.
35. Compare the same calculation using core Python and NumPy.

------------------------------------------------------------------------

# Chapter 22 -- How Vectors Connect to Machine Learning

Vectors are an important foundation for machine learning.

Imagine a dataset containing employee information:

  Employee     Age   Experience   Salary
  ---------- ----- ------------ --------
  A             25            2    30000
  B             30            5    45000
  C             35            8    60000

For employee A, the input features can be represented as a vector:

``` python
employee_a = [25, 2]
```

Here:

-   25 represents age.
-   2 represents years of experience.

The salary (30,000) is the target value that a machine-learning model
may try to predict.

With NumPy:

``` python
import numpy as np

employee_a = np.array([25, 2])
```

When we have many employees, we usually organise their features into a
two-dimensional array. Each row represents one employee and each column
represents one feature. That is the next step after one-dimensional
vectors.

------------------------------------------------------------------------

# Final Revision -- Important Terms

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Vector                              Ordered collection of numerical
                                      values

  Python list                         Built-in Python collection

  NumPy                               Python library for numerical
                                      computing

  `np.array()`                        Creates a NumPy array

  Index                               Position of an element

  `len()`                             Number of elements in a Python
                                      collection

  `append()`                          Adds an element to a list

  `sum()`                             Calculates a total

  `max()`                             Finds the highest value

  `min()`                             Finds the lowest value

  Scalar                              A single numerical value

  Vector addition                     Adds corresponding elements

  Scalar multiplication               Multiplies every element by one
                                      number

  Element-wise multiplication         Multiplies corresponding elements

  Dot product                         Multiplies corresponding elements
                                      and adds the products

  Indexing                            Accesses an element by position

  Slicing                             Accesses a range of elements

  Filtering                           Selects values that satisfy a
                                      condition

  Boolean indexing                    Filters NumPy arrays using Boolean
                                      conditions

  Vectorization                       Applies an operation to an entire
                                      array
  -----------------------------------------------------------------------

## Recommended teaching sequence

1.  Teach Chapter 1: understand the vector concept.
2.  Teach Chapter 2: Python lists, indexing, slicing, and updates.
3.  Teach Chapter 3: loops, conditions, and functions.
4.  Teach Chapters 4--6: implement vector mathematics manually.
5.  Teach Chapter 7: compare lists and other data structures.
6.  Complete Chapters 8 and 9: both projects using core Python.
7.  Teach Chapters 10 and 11: why NumPy is needed and how to install it.
8.  Teach Chapters 12--17: create arrays and perform NumPy operations.
9.  Complete Chapters 18 and 19: repeat both projects using NumPy.
10. Finish with revision, practice questions, and the machine-learning
    connection.

## Key takeaway

Do not jump directly into NumPy.

First understand how a vector is represented, how indexes work, how
loops process values, and how mathematical operations are implemented.

Once students can write vector addition, multiplication, filtering, and
dot product using normal Python, NumPy becomes much easier to
understand. NumPy does not change the underlying mathematical idea; it
provides a convenient and efficient way to work with numerical arrays.
