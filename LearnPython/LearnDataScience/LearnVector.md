# Python Vectors Without NumPy -- Learn the Foundation First

## Chapter objective

In this chapter, we will understand the foundation of vectors using
**only core Python**.

We will not use NumPy, Pandas, or any external library.

By the end, you will understand:

1.  What a vector means.
2.  Why vectors are useful.
3.  How to represent a vector using a Python list.
4.  How to perform vector addition, subtraction, and scalar
    multiplication manually.
5.  How to calculate vector length, sum, average, and dot product.
6.  How to access, update, and filter vector elements.
7.  How vectors are used in practical programs.
8.  How to build two beginner projects.

> Important: In this chapter, we use Python lists to represent
> mathematical vectors. A list is a Python data structure; a vector is a
> mathematical concept. A list can represent a vector when its elements
> are numerical values with a defined order.

------------------------------------------------------------------------

# Chapter 1 -- What Is a Vector?

## 1.1 Understand with a simple example

Imagine a student has marks in five subjects:

  Subject       Marks
  ----------- -------
  Maths            80
  Science          90
  English          75
  History          85
  Geography        95

We can represent all marks together:

``` python
marks = [80, 90, 75, 85, 95]
```

This is a Python list representing a one-dimensional numerical vector.

A vector is an ordered collection of values. In mathematics, vectors can
represent quantities such as:

-   Student marks
-   Monthly sales
-   Temperature readings
-   Employee salaries
-   Position and movement
-   Speed and direction

## 1.2 Why do we need vectors?

Suppose we want to increase every student's mark by 5.

We could create a separate variable for every student:

``` python
student1 = 80
student2 = 90
student3 = 75
student4 = 85
student5 = 95
```

But this becomes difficult when there are hundreds or thousands of
students.

Instead, keep the values together:

``` python
marks = [80, 90, 75, 85, 95]
```

Now we can process the collection using a loop.

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

We have processed all values using one loop.

------------------------------------------------------------------------

# Chapter 2 -- Python List: The Foundation

Before performing vector operations, understand the Python list.

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

## 2.2 A list can store different data types

``` python
student = ["Rahul", 21, 85.5, True]

print(student)
```

A Python list can contain strings, integers, floating-point numbers,
Boolean values, and even other lists.

However, when representing a mathematical numerical vector, we normally
keep values of compatible numerical types.

## 2.3 Access elements using an index

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

Python indexing starts from zero.

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

`len()` returns the number of elements in the list.

------------------------------------------------------------------------

# Chapter 3 -- Perform Vector Operations Manually

Now we will perform mathematical vector operations using normal Python.

## 3.1 Vector addition

Suppose:

``` text
A = [10, 20, 30]
B = [ 1,  2,  3]
```

Vector addition means adding corresponding elements:

``` text
A + B = [11, 22, 33]
```

Python code:

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

### Understand each line

-   `len(a)` gives the number of elements in vector A.
-   `range(len(a))` generates the indexes: 0, 1, 2.
-   `a[i]` accesses an element from the first vector.
-   `b[i]` accesses the corresponding element from the second vector.
-   `append()` adds the calculated value to the result list.

A reusable function:

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

## 3.2 Vector subtraction

Subtraction also happens element by element.

``` text
A = [10, 20, 30]
B = [ 1,  2,  3]

A - B = [9, 18, 27]
```

Python code:

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

## 3.3 Scalar multiplication

What if we want to multiply every element by 5?

``` text
A = [10, 20, 30]

5 × A = [50, 100, 150]
```

Python code:

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

Here, `number` is called a scalar: a single numerical value.

## 3.4 Element-wise multiplication

This is different from scalar multiplication.

``` text
A = [10, 20, 30]
B = [ 2,  3,  4]

A × B = [20, 60, 120]
```

Code:

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

## 3.5 Element-wise division

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

------------------------------------------------------------------------

# Chapter 4 -- Other Useful Vector Calculations

## 4.1 Calculate the sum of a vector

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

Python also provides the built-in `sum()` function:

``` python
print(sum(numbers))
```

## 4.2 Calculate the average

Average = Sum of values / Number of values.

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

## 4.3 Find the maximum value

``` python
numbers = [10, 50, 30, 90, 20]

highest = numbers[0]

for number in numbers:
    if number > highest:
        highest = number

print("Highest:", highest)
```

Output:

``` text
Highest: 90
```

Python also provides `max()`:

``` python
print(max(numbers))
```

## 4.4 Find the minimum value

``` python
numbers = [10, 50, 30, 90, 20]

lowest = numbers[0]

for number in numbers:
    if number < lowest:
        lowest = number

print("Lowest:", lowest)
```

Python also provides `min()`.

## 4.5 Calculate the dot product

The dot product is a useful mathematical operation.

Suppose:

``` text
A = [2, 3, 4]
B = [5, 6, 7]
```

Multiply corresponding elements and add the results:

``` text
(2 × 5) + (3 × 6) + (4 × 7)

= 10 + 18 + 28

= 56
```

Code:

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

# Chapter 5 -- Filtering Vector Values

Suppose we have these marks:

``` python
marks = [45, 67, 89, 32, 95, 56]
```

We want to find students who passed, assuming 50 is the passing mark.

``` python
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

## 5.1 Find values above 80

``` python
numbers = [20, 45, 90, 75, 85, 30]

result = []

for number in numbers:
    if number > 80:
        result.append(number)

print(result)
```

Output:

``` text
[90, 85]
```

## 5.2 Count values matching a condition

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

## 5.3 Use list comprehension

Once you understand the loop, Python offers a shorter way to filter
values.

``` python
marks = [45, 67, 89, 32, 95, 56]

passed = [mark for mark in marks if mark >= 50]

print(passed)
```

This is called list comprehension.

Learn the normal loop first; list comprehension is a shorter
alternative.

------------------------------------------------------------------------

# Chapter 6 -- Important Difference: Python List vs Mathematical Vector

A Python list is a data structure. A mathematical vector is a
mathematical object.

The same Python list can represent a vector, but Python does not
automatically treat normal list operators as vector mathematics.

## 6.1 List addition

``` python
a = [10, 20, 30]
b = [1, 2, 3]

print(a + b)
```

Output:

``` text
[10, 20, 30, 1, 2, 3]
```

This joins the lists. It does not add corresponding elements.

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

## 6.2 List multiplication

``` python
numbers = [10, 20, 30]

print(numbers * 2)
```

Output:

``` text
[10, 20, 30, 10, 20, 30]
```

The list is repeated.

For scalar multiplication, use a loop:

``` python
result = []

for number in numbers:
    result.append(number * 2)

print(result)
```

Output:

``` text
[20, 40, 60]
```

## 6.3 Comparison table

  --------------------------------------------------------------------------
  Feature                 Python List             NumPy Vector
                          Representing a Vector   
  ----------------------- ----------------------- --------------------------
  Requires installation   No                      Yes, install NumPy

  Creation                `[10, 20, 30]`          `np.array([10, 20, 30])`

  Addition                Requires a loop for     `a + b`
                          element-wise addition   

  Scalar multiplication   Requires a loop         `a * 2`

  Filtering               Loop or list            Boolean indexing
                          comprehension           

  Data types              Can contain mixed types Normally one common array
                                                  data type

  Best for                Learning logic and      Numerical computing and
                          general collections     larger numerical workloads
  --------------------------------------------------------------------------

**Why learn lists first?**

Because they help you understand the actual logic behind vector
operations. NumPy makes these operations shorter and usually more
efficient for numerical workloads, but the underlying mathematical idea
remains the same.

------------------------------------------------------------------------

# Chapter 7 -- Project 1: Student Marks Analyzer

## Objective

Create a program that:

1.  Stores marks of students.
2.  Calculates total and average marks.
3.  Finds highest and lowest marks.
4.  Counts passed and failed students.
5.  Displays marks above 75.
6.  Increases marks by 5 using a loop.

## File: `student_marks.py`

``` python
# Store student marks in a Python list
marks = [45, 67, 89, 32, 95, 76, 55, 82]

# Calculate total marks
total = sum(marks)

# Calculate average
average = total / len(marks)

# Find highest marks
highest = max(marks)

# Find lowest marks
lowest = min(marks)

# Create counters
passed_count = 0
failed_count = 0

# Create an empty list for high scorers
high_scorers = []

# Check every student's marks
for mark in marks:

    # Check whether student passed
    if mark >= 50:
        passed_count += 1
    else:
        failed_count += 1

    # Find students scoring 75 or above
    if mark >= 75:
        high_scorers.append(mark)

# Increase each student's marks by 5
updated_marks = []

for mark in marks:
    new_mark = mark + 5

    # Do not allow marks to exceed 100
    if new_mark > 100:
        new_mark = 100

    updated_marks.append(new_mark)

# Display report
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

## What this project teaches

-   Lists
-   Loops
-   Conditions
-   `append()`
-   `sum()`, `min()`, and `max()`
-   Counting
-   Filtering
-   Mathematical calculations

### Practice tasks

1.  Add five students.
2.  Find marks between 60 and 80.
3.  Calculate the passing percentage.
4.  Find the second-highest mark.
5.  Assign grades using conditions.
6.  Display the marks in ascending order.

------------------------------------------------------------------------

# Chapter 8 -- Project 2: Monthly Sales Analyzer

## Objective

A company has monthly sales data. We will use a Python list to:

1.  Calculate annual sales.
2.  Calculate average monthly sales.
3.  Find the best and worst sales months.
4.  Identify months above average.
5.  Calculate projected sales after a 10% increase.
6.  Calculate the difference between projected and actual sales.

## File: `monthly_sales.py`

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

# Calculate annual sales
annual_sales = sum(sales)

# Calculate average sales
average_sales = annual_sales / len(sales)

# Find highest and lowest sales
highest_sales = max(sales)
lowest_sales = min(sales)

# Find the index of the highest sales
best_index = sales.index(highest_sales)

# Find the index of the lowest sales
worst_index = sales.index(lowest_sales)

# Find corresponding month names
best_month = months[best_index]
worst_month = months[worst_index]

# Store months with above-average sales
above_average_months = []

# Store projected sales
projected_sales = []

# Store projected increase
sales_increase = []

# Process each month's sales
for i in range(len(sales)):

    # Check whether sales are above average
    if sales[i] > average_sales:
        above_average_months.append(months[i])

    # Calculate a 10% increase
    projected = sales[i] * 1.10

    projected_sales.append(projected)

    # Calculate increase over actual sales
    increase = projected - sales[i]

    sales_increase.append(increase)

# Display report
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

Projected Sales:
[13200.0, 16500.0, 19800.0, 15400.0,
 24200.0, 27500.0, 22000.0, 30800.0,
 33000.0, 29700.0, 38500.0, 44000.0]
```

## What this project teaches

-   Two related lists.
-   Accessing corresponding elements using indexes.
-   Finding maximum and minimum values.
-   Searching for an element's index.
-   Filtering data.
-   Percentage calculations.
-   Creating a simple business report.

**Note:** The 10% increase is a hypothetical scenario, not a
machine-learning forecast.

### Practice tasks

1.  Find the second-highest sales value and month.
2.  Find all months with sales below 20,000.
3.  Calculate the first six months' total sales.
4.  Calculate the last six months' total sales.
5.  Calculate a 15% increase instead of 10%.
6.  Display each month with its actual and projected sales.

------------------------------------------------------------------------

# Chapter 9 -- Practice Questions

Try to solve these using only Python lists, loops, and conditions.

## Basic level

1.  Create a vector containing 10 numbers.
2.  Print every element using a `for` loop.
3.  Find the length of the vector.
4.  Find the sum of all elements without using `sum()`.
5.  Calculate the average without using `sum()`.
6.  Find the highest value without using `max()`.
7.  Find the lowest value without using `min()`.
8.  Print all even numbers.
9.  Print all odd numbers.
10. Count how many values are greater than 50.

## Intermediate beginner level

11. Add two vectors element by element.
12. Subtract two vectors element by element.
13. Multiply every element by 10.
14. Multiply two vectors element by element.
15. Find the dot product of two vectors.
16. Create a new list containing only values between 20 and 50.
17. Reverse a vector.
18. Sort a vector in ascending order.
19. Find the index of the highest value.
20. Increase employee salaries by 8%.

------------------------------------------------------------------------

# Chapter 10 -- Where Do We Go After This?

Once you understand vectors using Python lists, move towards NumPy.

## Learning progression

  -----------------------------------------------------------------------
  Stage                   Topic                   What you will learn
  ----------------------- ----------------------- -----------------------
  1                       Python Lists            Store numerical values

  2                       Loops                   Process each value

  3                       Vector operations       Add, subtract, multiply
                                                  and divide

  4                       Filtering               Select values based on
                                                  conditions

  5                       Functions               Reuse vector
                                                  calculations

  6                       NumPy arrays            Perform vector
                                                  calculations directly

  7                       Two-dimensional arrays  Understand matrices and
                                                  tabular numerical data

  8                       Pandas                  Work with real-world
                                                  datasets

  9                       Machine Learning        Use numerical features
                                                  for predictions
  -----------------------------------------------------------------------

## What changes when we learn NumPy?

With core Python:

``` python
a = [10, 20, 30]
b = [1, 2, 3]

result = []

for i in range(len(a)):
    result.append(a[i] + b[i])

print(result)
```

With NumPy:

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

The mathematical operation is the same. NumPy provides a convenient and
optimised way to perform numerical operations on arrays.

------------------------------------------------------------------------

# Final Revision

  Term                    Meaning
  ----------------------- ------------------------------------------------------
  Vector                  Ordered collection of numerical values
  Python list             Built-in Python collection
  Index                   Position of an element
  `len()`                 Number of elements
  `append()`              Add an element to a list
  `sum()`                 Calculate total
  `max()`                 Find highest value
  `min()`                 Find lowest value
  `range()`               Generate a sequence of indexes
  Loop                    Process values one by one
  Scalar                  A single numerical value
  Vector addition         Add corresponding elements
  Scalar multiplication   Multiply every element by one number
  Dot product             Multiply corresponding elements and add the products
  Filtering               Select values that satisfy a condition

## Key takeaway

Do not jump directly into NumPy.

First understand how a vector is represented, how indexes work, how
loops process values, and how mathematical operations are implemented.

Once you can write vector addition, multiplication, filtering, and dot
product using normal Python, learning NumPy becomes much easier.
