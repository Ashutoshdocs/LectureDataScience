# 🐍 Python `int` Data Type – Complete Lab

A step-by-step practical for learning Python's **integer (`int`)** data type: 20 hands-on labs, common mistakes, a cheat sheet, and **20 practice questions with full answers**.

> All code and outputs in this guide were tested on **Python 3.13**. They work on any Python 3 version.

---

## 📁 What's in this folder

| File | Use it for |
|---|---|
| `README.md` | This guide: theory, 20 labs, gotchas, questions and answers |
| `int_lab.py` | All 20 labs in one script: `python int_lab.py` |
| `answers.py` | Runnable answers to the 20 practice questions: `python answers.py` |

---

## 📚 Table of Contents

- [What is the int Data Type?](#-what-is-the-int-data-type)
- [How to Run the Code](#%EF%B8%8F-how-to-run-the-code)
- [Part A – Creating Integers (Labs 1–5)](#part-a--creating-integers-labs-15)
- [Part B – Arithmetic Operators (Labs 6–12)](#part-b--arithmetic-operators-labs-612)
- [Part C – Comparison (Lab 13)](#part-c--comparison-lab-13)
- [Part D – Type Conversion (Labs 14–16)](#part-d--type-conversion-labs-1416)
- [Part E – Big Numbers & Built-in Functions (Labs 17–20)](#part-e--big-numbers--built-in-functions-labs-1720)
- [Common Mistakes & Gotchas](#%EF%B8%8F-common-mistakes--gotchas)
- [Cheat Sheet](#-cheat-sheet)
- [Practice Questions](#-practice-questions)
- [Answers](#-answers)

---

## 📌 What is the int Data Type?

`int` stands for **integer**. In Python, the `int` data type stores **whole numbers**: numbers without a decimal point.

```
 ✅ Integers:      10    100    -25    0    999999
 ❌ Not integers:  10.5  (float)   "10"  (string)   True  (bool)
```

### ⭐ Key features

| Feature | Meaning |
|---|---|
| No decimal point | `10` is an int, but `10.0` is a float |
| Positive and negative | `500` and `-10` are both ints |
| Zero is an integer | `0` is an int |
| Practically unlimited size | Python ints grow as big as your computer's memory allows. There's no overflow like in C or Java. |
| Immutable | An int value can't be changed in place. `x = x + 1` creates a **new** int object. |

> 💡 **Readability tip:** use underscores in big numbers. `1_000_000` is the same as `1000000`.

---

## ▶️ How to Run the Code

**Option 1: Script file (recommended for these labs)**
1. Save the code in a file, e.g. `lab01.py`.
2. Run it in the terminal: `python lab01.py` (use `python3` on Mac/Linux).

**Option 2: Python Shell (interactive)**
1. Type `python` in the terminal.
2. Type each line after the `>>>` prompt and press Enter.
3. In the Shell you can skip `print()`: typing `age` shows `25` directly.

**Run everything at once:**
```bash
python int_lab.py      # all 20 labs
python answers.py      # all 20 answers
```

---

## Part A – Creating Integers (Labs 1–5)

### Lab 01 – Creating an Integer Variable

```python
age = 25

print(age)
```

**▶ Output**
```
25
```

**💡 Explanation:** `age = 25` creates a variable called `age` and stores the integer `25` in it. `=` is the **assignment** operator: it means "store", not "equals". `print()` displays the value.

---

### Lab 02 – Checking the Data Type: `type()`

```python
number = 100

print(type(number))
```

**▶ Output**
```
<class 'int'>
```

**💡 Explanation:** `type()` tells you which data type is stored in a variable. `<class 'int'>` means it's an integer.

> 🔍 Compare: `type(100.0)` → `<class 'float'>` and `type("100")` → `<class 'str'>`.

---

### Lab 03 – Positive Integer

```python
number = 500

print(number)
```

**▶ Output**
```
500
```

**💡 Explanation:** Whole numbers **greater than 0** are positive integers. You don't need a `+` sign.

---

### Lab 04 – Negative Integer

```python
temperature = -10

print(temperature)
```

**▶ Output**
```
-10
```

**💡 Explanation:** Whole numbers **less than 0** are negative integers. Put a minus sign `-` in front.

---

### Lab 05 – Zero Integer

```python
number = 0

print(number)
print(type(number))
```

**▶ Output**
```
0
<class 'int'>
```

**💡 Explanation:** `0` is also an `int`. It's neither positive nor negative.

---

## Part B – Arithmetic Operators (Labs 6–12)

### Lab 06 – Integer Addition: `+`

```python
a = 10
b = 20

result = a + b

print(result)
```

**▶ Output**
```
30
```

**💡 Explanation:** The `+` operator adds two integers: 10 + 20 = **30**. The result is also an `int`.

---

### Lab 07 – Integer Subtraction: `-`

```python
a = 50
b = 20

result = a - b

print(result)
```

**▶ Output**
```
30
```

**💡 Explanation:** The `-` operator subtracts: 50 − 20 = **30**.

---

### Lab 08 – Integer Multiplication: `*`

```python
a = 10
b = 5

result = a * b

print(result)
```

**▶ Output**
```
50
```

**💡 Explanation:** The `*` operator multiplies: 10 × 5 = **50**. In Python the multiplication sign is `*`, not `×` or `x`.

---

### Lab 09 – Division: `/`

```python
a = 10
b = 2

result = a / b

print(result)
```

**▶ Output**
```
5.0
```

**💡 Explanation:** The `/` operator **always returns a float** in Python 3, even when the division is exact. That's why you see `5.0`, not `5`.

> ⚠️ Dividing by zero (`10 / 0`) raises `ZeroDivisionError`.

---

### Lab 10 – Floor Division: `//`

```python
a = 10
b = 3

result = a // b

print(result)
```

**▶ Output**
```
3
```

**💡 Explanation:** `//` divides and then **rounds down** to the nearest whole number. 10 ÷ 3 = 3.33…, rounded down to **3**. With two ints, the result is an `int`.

> ⚠️ **"Rounds down" means towards minus infinity, not towards zero:**
> ```python
> print(-10 // 3)    # -4   (because -3.33 rounds DOWN to -4)
> ```

---

### Lab 11 – Modulus (Remainder): `%`

```python
a = 10
b = 3

result = a % b

print(result)
```

**▶ Output**
```
1
```

**💡 Explanation:** `%` returns the **remainder** after division. 10 ÷ 3 = 3 with remainder **1** (because 3 × 3 = 9, and 10 − 9 = 1).

```
    10 // 3  →  3   (how many times 3 fits)
    10 %  3  →  1   (what's left over)
    Check:  3 × 3 + 1 = 10 ✅
```

> 💡 **Common use:** `number % 2 == 0` means the number is **even**.

---

### Lab 12 – Power Operator: `**`

```python
a = 2
b = 3

result = a ** b

print(result)
```

**▶ Output**
```
8
```

**💡 Explanation:** `**` raises a number to a power: 2 ** 3 = 2 × 2 × 2 = **8**.

> ⚠️ Don't use `^` for power. In Python `2 ^ 3` is a bitwise XOR and gives `1`.

---

## Part C – Comparison (Lab 13)

### Lab 13 – Integer Comparison

```python
a = 10
b = 20

print(a == b)
print(a < b)
print(a > b)
```

**▶ Output**
```
False
True
False
```

**💡 Explanation:** Comparison operators check the relationship between two values and return a **boolean** (`True` or `False`).

| Expression | Meaning | Result |
|---|---|---|
| `a == b` | Is 10 equal to 20? | `False` |
| `a < b` | Is 10 less than 20? | `True` |
| `a > b` | Is 10 greater than 20? | `False` |

> ⚠️ `=` **assigns** a value and `==` **compares** values. Mixing them up is a very common beginner mistake.

---

## Part D – Type Conversion (Labs 14–16)

### Lab 14 – Converting a String to an Integer: `int()`

```python
number = int("100")

print(number)
print(type(number))
```

**▶ Output**
```
100
<class 'int'>
```

**💡 Explanation:** `int()` converts a string of digits (or another compatible value) into an integer. This matters because `input()` always returns a **string**:

```python
age = int(input("Enter your age: "))   # convert the text to a number
```

> ⚠️ The string must hold a **whole number**:
> ```python
> int("100")    # ✅ 100
> int(" 42 ")   # ✅ 42  (spaces around the number are OK)
> int("10.5")   # ❌ ValueError: invalid literal for int() with base 10: '10.5'
> int("abc")    # ❌ ValueError
> ```

---

### Lab 15 – Converting a Float to an Integer

```python
number = int(10.99)

print(number)
```

**▶ Output**
```
10
```

**💡 Explanation:** `int()` **cuts off** the decimal part (truncation). It does **not** round, so 10.99 becomes 10, not 11. For negative numbers it cuts towards zero: `int(-10.99)` → `-10`. Use `round()` (Lab 20) if you want rounding.

---

### Lab 16 – Converting a Boolean to an Integer

```python
print(int(True))
print(int(False))
```

**▶ Output**
```
1
0
```

**💡 Explanation:** In Python, `True` → **1** and `False` → **0**. In fact, `bool` is a subtype of `int`, so `True + True` gives `2`. This is handy for counting: `sum([True, False, True])` → `2`.

---

## Part E – Big Numbers & Built-in Functions (Labs 17–20)

### Lab 17 – Large Integer

```python
number = 999999999999999999999999999999

print(number)
```

**▶ Output**
```
999999999999999999999999999999
```

**💡 Explanation:** Python integers have **no fixed size limit**. They can hold huge numbers that would overflow in languages like C or Java. Try `print(2 ** 100)` → `1267650600228229401496703205376`.

> ℹ️ **Python 3.11+ note:** by default, Python won't convert an int with **more than 4300 digits** to text (e.g. `print(10 ** 5000)`) and raises `ValueError`. The number itself is fine; only printing it is blocked. Raise the limit with `import sys; sys.set_int_max_str_digits(0)`.

---

### Lab 18 – Absolute Value: `abs()`

```python
number = -50

print(abs(number))
```

**▶ Output**
```
50
```

**💡 Explanation:** `abs()` returns the **distance from zero**, so it's always non-negative. `abs(-50)` → 50 and `abs(50)` → 50.

---

### Lab 19 – Power Function: `pow()`

```python
result = pow(2, 5)

print(result)
```

**▶ Output**
```
32
```

**💡 Explanation:** `pow(base, exponent)` does the same as `base ** exponent`: 2⁵ = 2 × 2 × 2 × 2 × 2 = **32**.

> 💡 **Bonus:** `pow()` accepts a third argument for the remainder: `pow(2, 10, 1000)` → `24` (2¹⁰ = 1024, and 1024 % 1000 = 24). This is fast even for huge numbers.

---

### Lab 20 – Rounding: `round()`

```python
number = 10.75

result = round(number)

print(result)
print(type(result))
```

**▶ Output**
```
11
<class 'int'>
```

**💡 Explanation:** `round()` rounds to the **nearest whole number**: 10.75 → **11**.

**Note:** `round()` can take a float as input. When you **don't** give a second argument (`ndigits`), the result is an `int`. When you do give it, the result stays a float: `round(10.75, 1)` → `10.8`.

> ⚠️ **Halfway values round to the nearest EVEN number** ("banker's rounding"):
> ```python
> print(round(2.5))   # 2   (not 3!)
> print(round(3.5))   # 4
> ```

---

## ⚠️ Common Mistakes & Gotchas

| Code | You might expect | Python gives | Why |
|---|---|---|---|
| `10 / 2` | `5` | `5.0` | `/` always returns a float |
| `-10 // 3` | `-3` | `-4` | `//` rounds **down** (towards −∞) |
| `int(10.99)` | `11` | `10` | `int()` truncates, it doesn't round |
| `round(2.5)` | `3` | `2` | Halves round to the nearest even number |
| `int("10.5")` | `10` | `ValueError` | Use `int(float("10.5"))` instead |
| `2 ^ 3` | `8` | `1` | `^` is XOR; use `**` for power |
| `"10" + 5` | `15` | `TypeError` | Convert first: `int("10") + 5` |
| `if a = b:` | comparison | `SyntaxError` | Use `==` to compare |
| `10 / 0` | — | `ZeroDivisionError` | Can't divide by zero (also for `//` and `%`) |

---

## 📋 Cheat Sheet

### Arithmetic operators

| Operator | Function | Example | Result |
|---|---|---|---|
| `+` | Addition | `10 + 3` | `13` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `10 * 3` | `30` |
| `/` | Division (float result) | `10 / 3` | `3.3333333333333335` |
| `//` | Floor division | `10 // 3` | `3` |
| `%` | Remainder (modulus) | `10 % 3` | `1` |
| `**` | Power | `10 ** 3` | `1000` |

### Comparison operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal to | `5 >= 5` | `True` |
| `<=` | Less than or equal to | `3 <= 5` | `True` |

### Built-in functions

| Function | Purpose | Example | Result |
|---|---|---|---|
| `int()` | Convert to integer | `int("42")` | `42` |
| `type()` | Check data type | `type(42)` | `<class 'int'>` |
| `abs()` | Absolute value | `abs(-7)` | `7` |
| `pow()` | Power | `pow(2, 4)` | `16` |
| `round()` | Round to nearest | `round(4.6)` | `5` |
| `divmod()` | Quotient and remainder together | `divmod(10, 3)` | `(3, 1)` |

### ⚡ Quick revision

| # | Topic | Answer |
|---|---|---|
| 01 | Integer example | `100` |
| 02 | Negative integer | `-25` |
| 03 | Zero | `0` |
| 04 | Data type check | `type()` |
| 05 | Convert to int | `int()` |
| 06 | Addition | `+` |
| 07 | Subtraction | `-` |
| 08 | Multiplication | `*` |
| 09 | Division | `/` |
| 10 | Floor division | `//` |
| 11 | Remainder | `%` |
| 12 | Power | `**` |
| 13 | Absolute value | `abs()` |
| 14 | Power function | `pow()` |
| 15 | Rounding | `round()` |

---

## 📝 Practice Questions

Try each question yourself **before** looking at the answers.

| # | Question |
|---|---|
| Q1 | Create an integer variable and print its value. |
| Q2 | Check the data type of an integer using `type()`. |
| Q3 | Create a positive integer. |
| Q4 | Create a negative integer. |
| Q5 | Create an integer with value 0. |
| Q6 | Perform addition of two integers. |
| Q7 | Perform subtraction of two integers. |
| Q8 | Perform multiplication of two integers. |
| Q9 | Perform division of two integers. |
| Q10 | Perform floor division of two integers. |
| Q11 | Find the remainder using `%`. |
| Q12 | Calculate power using `**`. |
| Q13 | Convert a string into an integer using `int()`. |
| Q14 | Convert a float into an integer. |
| Q15 | Find the absolute value using `abs()`. |
| Q16 | Calculate power using `pow()`. |
| Q17 | Compare two integers using comparison operators. |
| Q18 | Create and print a very large integer. |
| Q19 | Round a number using `round()`. |
| Q20 | Write a program demonstrating different integer operators. |

---

## ✅ Answers

> Many answers are possible. These are sample solutions. Any values that follow the same idea are correct. All answers are also in `answers.py`.

<details>
<summary><b>Q1. Create an integer variable and print its value</b></summary>

```python
marks = 85
print(marks)
```
**▶ Output**
```
85
```
`marks` stores the whole number 85, and `print()` displays it.
</details>

<details>
<summary><b>Q2. Check the data type of an integer using type()</b></summary>

```python
year = 2026
print(type(year))
```
**▶ Output**
```
<class 'int'>
```
</details>

<details>
<summary><b>Q3. Create a positive integer</b></summary>

```python
students = 45
print(students)
print(students > 0)
```
**▶ Output**
```
45
True
```
`students > 0` confirms the number is positive.
</details>

<details>
<summary><b>Q4. Create a negative integer</b></summary>

```python
balance = -750
print(balance)
print(balance < 0)
```
**▶ Output**
```
-750
True
```
</details>

<details>
<summary><b>Q5. Create an integer with value 0</b></summary>

```python
score = 0
print(score)
print(type(score))
```
**▶ Output**
```
0
<class 'int'>
```
</details>

<details>
<summary><b>Q6. Perform addition of two integers</b></summary>

```python
a = 25
b = 15
print(a + b)
```
**▶ Output**
```
40
```
</details>

<details>
<summary><b>Q7. Perform subtraction of two integers</b></summary>

```python
a = 100
b = 35
print(a - b)
```
**▶ Output**
```
65
```
</details>

<details>
<summary><b>Q8. Perform multiplication of two integers</b></summary>

```python
a = 12
b = 8
print(a * b)
```
**▶ Output**
```
96
```
</details>

<details>
<summary><b>Q9. Perform division of two integers</b></summary>

```python
a = 20
b = 4
print(a / b)
print(type(a / b))
```
**▶ Output**
```
5.0
<class 'float'>
```
`/` always gives a float, even though 20 ÷ 4 divides exactly.
</details>

<details>
<summary><b>Q10. Perform floor division of two integers</b></summary>

```python
a = 17
b = 5
print(a // b)
```
**▶ Output**
```
3
```
17 ÷ 5 = 3.4, rounded down to **3**.
</details>

<details>
<summary><b>Q11. Find the remainder using %</b></summary>

```python
a = 17
b = 5
print(a % b)
```
**▶ Output**
```
2
```
5 fits into 17 three times (15), leaving **2**. Check: 5 × 3 + 2 = 17 ✅
</details>

<details>
<summary><b>Q12. Calculate power using **</b></summary>

```python
base = 5
exponent = 3
print(base ** exponent)
```
**▶ Output**
```
125
```
5 × 5 × 5 = 125.
</details>

<details>
<summary><b>Q13. Convert a string into an integer using int()</b></summary>

```python
text = "250"
number = int(text)
print(number)
print(type(number))
print(number + 50)
```
**▶ Output**
```
250
<class 'int'>
300
```
After conversion you can do maths with it. `"250" + 50` would give a `TypeError`.
</details>

<details>
<summary><b>Q14. Convert a float into an integer</b></summary>

```python
price = 99.99
print(int(price))
```
**▶ Output**
```
99
```
`int()` drops the decimal part. It does not round up to 100.
</details>

<details>
<summary><b>Q15. Find the absolute value using abs()</b></summary>

```python
loss = -320
print(abs(loss))
```
**▶ Output**
```
320
```
</details>

<details>
<summary><b>Q16. Calculate power using pow()</b></summary>

```python
print(pow(3, 4))
```
**▶ Output**
```
81
```
3⁴ = 3 × 3 × 3 × 3 = 81.
</details>

<details>
<summary><b>Q17. Compare two integers using comparison operators</b></summary>

```python
x = 15
y = 25
print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)
```
**▶ Output**
```
False
True
False
True
False
True
```
</details>

<details>
<summary><b>Q18. Create and print a very large integer</b></summary>

```python
big = 123456789012345678901234567890123456789
print(big)
print(type(big))
print(2 ** 100)
```
**▶ Output**
```
123456789012345678901234567890123456789
<class 'int'>
1267650600228229401496703205376
```
Even a 39-digit number is still a plain `int`.
</details>

<details>
<summary><b>Q19. Round a number using round()</b></summary>

```python
print(round(7.6))
print(round(7.4))
print(round(3.14159, 2))
```
**▶ Output**
```
8
7
3.14
```
The second argument sets the number of decimal places to keep.
</details>

<details>
<summary><b>Q20. Write a program demonstrating different integer operators</b></summary>

```python
a = 17
b = 5
print("a =", a, " b =", b)
print("Addition       :", a + b)
print("Subtraction    :", a - b)
print("Multiplication :", a * b)
print("Division       :", a / b)
print("Floor Division :", a // b)
print("Remainder      :", a % b)
print("Power          :", a ** b)
print("Equal          :", a == b)
print("Not Equal      :", a != b)
print("Greater        :", a > b)
print("Less           :", a < b)
```
**▶ Output**
```
a = 17  b = 5
Addition       : 22
Subtraction    : 12
Multiplication : 85
Division       : 3.4
Floor Division : 3
Remainder      : 2
Power          : 1419857
Equal          : False
Not Equal      : True
Greater        : True
Less           : False
```
</details>

---

## 🚀 Bonus Challenges

1. Ask the user for two numbers with `input()`, convert them with `int()`, and print their sum.
2. Check whether a number is **even or odd** using `%`.
3. Convert 135 minutes into hours and minutes using `//` and `%`.
4. Find the last digit of `98765` using `%`.

<details>
<summary>👉 Show bonus answers</summary>

```python
# 1
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
print("Sum:", a + b)

# 2
number = 27
print(number % 2 == 0)        # False → odd

# 3
minutes = 135
print(minutes // 60, "hours", minutes % 60, "minutes")    # 2 hours 15 minutes

# 4
print(98765 % 10)             # 5
```
</details>

---

<p align="center"><b>🎯 Python int Lab – Complete · Happy Coding! 🐍</b></p>
