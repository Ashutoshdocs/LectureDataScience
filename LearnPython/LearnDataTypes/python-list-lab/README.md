# 🐍 Python `list` Data Type – Complete Lab

A beginner-friendly practical for learning Python **lists**: creating, indexing, slicing, adding, removing, searching, sorting and copying. It also includes a real-world project, common mistakes, a cheat sheet, and **10 practice tasks with full answers**.

> All code and outputs in this guide were tested on **Python 3.13**. Everything works on any Python 3 version.

---

## 📁 What's in this folder

| File | Use it for |
|---|---|
| `README.md` | This guide: basics, 25 labs, gotchas, practice tasks and answers |
| `list_lab.py` | All labs in one script: `python list_lab.py` |
| `answers.py` | Runnable answers to the 10 practice tasks: `python answers.py` |

> ⚠️ **Copy code from this README or the `.py` files, not from bold-text handouts.** Code typed in Unicode "bold" characters (like 𝐩𝐫𝐢𝐧𝐭 or 𝟎) won't run: bold digits cause `SyntaxError: invalid character`.

---

## 📚 Table of Contents

- [What is a List?](#-what-is-a-list)
- [List Methods Roadmap](#%EF%B8%8F-list-methods-roadmap)
- [Part 1 – Create a List (Lab 1)](#part-1--create-a-list-lab-1)
- [Part 2 – Indexing (Labs 2–3)](#part-2--indexing-labs-23)
- [Part 3 – Slicing (Lab 4)](#part-3--slicing-lab-4)
- [Part 4 – Add / Insert (Labs 5–7)](#part-4--add--insert-labs-57)
- [Part 5 – Remove (Labs 8–11)](#part-5--remove-labs-811)
- [Part 6 – Search / Count (Labs 12–14)](#part-6--search--count-labs-1214)
- [Part 7 – Sort / Reverse (Labs 15–16)](#part-7--sort--reverse-labs-1516)
- [Part 8 – Copy (Labs 17–18)](#part-8--copy-labs-1718)
- [Part 9 – Built-in Functions (Labs 19–23)](#part-9--built-in-functions-labs-1923)
- [Part 10 – Mutability (Lab 24)](#part-10--mutability-lab-24)
- [Real-World Project (Lab 25)](#-real-world-project-lab-25)
- [Common Mistakes & Gotchas](#%EF%B8%8F-common-mistakes--gotchas)
- [Cheat Sheet](#-cheat-sheet)
- [Practice Tasks](#-practice-tasks)
- [Answers](#-answers)

---

## 📌 What is a List?

A **list** is a **collection** data type: one variable that holds **many values**, in order, inside square brackets `[ ]`.

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students)
```

**📤 Output**
```
['Rahul', 'Amit', 'Neha', 'Priya']
```

### ⭐ Key properties

| Property | Meaning | Example |
|---|---|---|
| ✔ **Ordered** | Items keep the order you put them in | `["Rahul", "Amit"]` stays Rahul first |
| ✔ **Mutable** | You can change, add and remove items after creating it | `students[1] = "Rohit"` |
| ✔ **Allows duplicates** | The same value can appear more than once | `[10, 20, 10]` |
| ✔ **Mixed data types** | One list can hold different types | `["Rahul", 25, 85.5, True]` |
| ✔ **Indexing** | Get one item by its position | `students[0]` |
| ✔ **Slicing** | Get a range of items | `students[1:3]` |

---

## 🗺️ List Methods Roadmap

```
LIST
│
├── 🔹 CREATE / ACCESS ──── [ ]   index   slicing
├── 🔹 ADD / INSERT ─────── append()   insert()   extend()
├── 🔹 REMOVE ───────────── remove()   pop()   clear()   del
├── 🔹 SEARCH / COUNT ───── index()   count()   in
├── 🔹 SORT / REVERSE ───── sort()   reverse()
├── 🔹 COPY ─────────────── copy()   assignment (=)
└── 🔹 BUILT-IN FUNCTIONS ─ len()   min()   max()   sum()   sorted()
```

> 💡 **Methods vs functions:** a **method** is called with a dot after the list (`students.append("Neha")`). A **built-in function** takes the list inside brackets (`len(students)`).

---

## Part 1 – Create a List (Lab 1)

### 1️⃣ Lab 01 – Creating a List

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students)
```

**📤 Output**
```
['Rahul', 'Amit', 'Neha', 'Priya']
```

**Empty list:**

```python
students = []
print(students)
```

**📤 Output**
```
[]
```

**Mixed data types:**

```python
mixed = ["Rahul", 25, 85.5, True]
print(mixed)
```

**📤 Output**
```
['Rahul', 25, 85.5, True]
```

**💡 Explanation:** Put items inside `[ ]`, separated by commas. An empty list `[]` is useful as a starting point that you fill later with `append()`.

---

## Part 2 – Indexing (Labs 2–3)

Each item has a position number called an **index**. Counting starts at **0**.

```
   "Rahul"   "Amit"   "Neha"   "Priya"
      0         1        2        3       ← positive index
     -4        -3       -2       -1       ← negative index
```

### 2️⃣ Lab 02 – Positive Indexing

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students[0])
print(students[2])
```

**📤 Output**
```
Rahul
Neha
```

**💡 Explanation:** The **first** item is at index `0`, so in a list of 4 items the last index is `3`. Using an index that doesn't exist, like `students[10]`, raises `IndexError: list index out of range`.

---

### 3️⃣ Lab 03 – Negative Indexing

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students[-1])
print(students[-2])
```

**📤 Output**
```
Priya
Neha
```

**💡 Explanation:** Negative indexes count from the **end**: `-1` is the last item and `-2` the second-last. Use `[-1]` to get the last item without knowing the list's length.

---

## Part 3 – Slicing (Lab 4)

### 4️⃣ Lab 04 – List Slicing

**Syntax:** `list[start:stop]` returns a **new list** from `start` up to, **but not including**, `stop`.

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students[1:3])
```

**📤 Output**
```
['Amit', 'Neha']
```

**💡 Explanation:** `[1:3]` takes index 1 (Amit) and index 2 (Neha). Index 3 (Priya) is the **stop**, so it is **not included**.

**More slicing shortcuts:**

```python
print(students[:2])     # first two items
print(students[2:])     # from index 2 to the end
print(students[::-1])   # reversed copy
```

**📤 Output**
```
['Rahul', 'Amit']
['Neha', 'Priya']
['Priya', 'Neha', 'Amit', 'Rahul']
```

> 💡 Leaving out `start` means "from the beginning" and leaving out `stop` means "to the end". The full syntax is `[start:stop:step]`, so `[::-1]` steps backwards. Slicing never raises `IndexError`: `students[1:100]` simply stops at the end.

---

## Part 4 – Add / Insert (Labs 5–7)

### 5️⃣ Lab 05 – `append()`: Add at the End

**What does it do?** Adds **one** item to the **end** of the list.

```python
students = ["Rahul", "Amit"]
students.append("Neha")
print(students)
```

**📤 Output**
```
['Rahul', 'Amit', 'Neha']
```

**📌 Real-world use:** adding a new student to the class list.

---

### 6️⃣ Lab 06 – `insert()`: Add at a Specific Position

**What does it do?** Inserts an item at a **given index**.

```python
students = ["Rahul", "Amit", "Neha"]
students.insert(1, "Priya")
print(students)
```

**📤 Output**
```
['Rahul', 'Priya', 'Amit', 'Neha']
```

**💡 Explanation:** The syntax is `insert(position, value)`:
- `1` = the position (index) where the new item goes
- `"Priya"` = the new value

Items from that position onwards move one place to the right. If the index is bigger than the list, the item is simply added at the end.

---

### 7️⃣ Lab 07 – `extend()`: Add Multiple Items

**What does it do?** Adds **every item** from another list (or any iterable) to the end.

```python
students = ["Rahul", "Amit"]
new_students = ["Neha", "Priya"]
students.extend(new_students)
print(students)
```

**📤 Output**
```
['Rahul', 'Amit', 'Neha', 'Priya']
```

### ⚠️ `append()` vs `extend()`

```python
students = ["Rahul", "Amit"]
students.append(["Neha", "Priya"])
print(students)
```

**📤 Output:** the whole list is added as **one item** (a list inside a list)
```
['Rahul', 'Amit', ['Neha', 'Priya']]
```

```python
students = ["Rahul", "Amit"]
students.extend(["Neha", "Priya"])
print(students)
```

**📤 Output:** each item is added **separately**
```
['Rahul', 'Amit', 'Neha', 'Priya']
```

| Method | Adds | Length after adding `["Neha", "Priya"]` to a 2-item list |
|---|---|---|
| `append()` | 1 item (the whole list) | 3 |
| `extend()` | Each item separately | 4 |

---

## Part 5 – Remove (Labs 8–11)

### 8️⃣ Lab 08 – `remove()`: Remove by Value

```python
students = ["Rahul", "Amit", "Neha"]
students.remove("Amit")
print(students)
```

**📤 Output**
```
['Rahul', 'Neha']
```

**💡 Explanation:** You give the **value** to remove, not its position. Only the **first** match is removed: `[1, 2, 1]` → `remove(1)` → `[2, 1]`. If the value isn't in the list, you get `ValueError: list.remove(x): x not in list`.

---

### 9️⃣ Lab 09 – `pop()`: Remove by Index

**What does it do?** Removes the item at a given **index** and **returns** it.

```python
students = ["Rahul", "Amit", "Neha"]
student = students.pop(1)
print(student)
print(students)
```

**📤 Output**
```
Amit
['Rahul', 'Neha']
```

**💡 Explanation:** `pop()` removes the item **and gives it back to you**, so you can store it in a variable. That's the main difference from `remove()`.

**Without an index, it removes the last item:**

```python
students = ["Rahul", "Amit", "Neha"]
last = students.pop()
print(last)
print(students)
```

**📤 Output**
```
Neha
['Rahul', 'Amit']
```

---

### 🔟 Lab 10 – `clear()`: Remove All Items

```python
students = ["Rahul", "Amit", "Neha"]
students.clear()
print(students)
```

**📤 Output**
```
[]
```

**💡 Explanation:** The list still exists, but it's now empty.

---

### 1️⃣1️⃣ Lab 11 – `del`: Delete by Index or Slice

`del` is a Python **statement**, not a method, so there is no dot and no brackets after `del`.

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
del students[0]
print(students)
```

**📤 Output**
```
['Amit', 'Neha', 'Priya']
```

**Delete a range with a slice:**

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
del students[1:3]
print(students)
```

**📤 Output**
```
['Rahul', 'Priya']
```

> ⚠️ `del students` (without an index) deletes the **whole variable**. Using `students` afterwards gives a `NameError`.

### 🆚 Which remove should I use?

| You know… | Use | Returns the item? |
|---|---|---|
| The **value** (e.g. "Amit") | `remove("Amit")` | ❌ No |
| The **index** and want the item back | `pop(1)` | ✅ Yes |
| The **index or a range** | `del students[1]` / `del students[1:3]` | ❌ No |
| You want to empty the list | `clear()` | ❌ No |

---

## Part 6 – Search / Count (Labs 12–14)

### 1️⃣2️⃣ Lab 12 – `index()`: Find the Position

```python
students = ["Rahul", "Amit", "Neha"]
print(students.index("Amit"))
```

**📤 Output**
```
1
```

**💡 Explanation:** Returns the index of the **first** match. If the value isn't found, it raises `ValueError: 'Rohit' is not in list`, so check with `in` first if you're not sure.

---

### 1️⃣3️⃣ Lab 13 – `count()`: Count Occurrences

**What does it do?** Counts how many times a value appears in the list.

```python
numbers = [10, 20, 10, 30, 10]
print(numbers.count(10))
```

**📤 Output**
```
3
```

**💡 Explanation:** Returns `0` (not an error) if the value isn't there.

---

### 1️⃣4️⃣ Lab 14 – `in`: Membership Check

```python
students = ["Rahul", "Amit", "Neha"]
print("Amit" in students)
print("Rohit" in students)
```

**📤 Output**
```
True
False
```

**💡 Explanation:** `in` returns `True` or `False`. Use `not in` for the opposite. It's the safe way to check before calling `remove()` or `index()`:

```python
if "Rohit" in students:
    students.remove("Rohit")
```

---

## Part 7 – Sort / Reverse (Labs 15–16)

### 1️⃣5️⃣ Lab 15 – `sort()`: Sort the List

```python
numbers = [50, 10, 40, 20, 30]
numbers.sort()
print(numbers)
```

**📤 Output**
```
[10, 20, 30, 40, 50]
```

**Descending order:**

```python
numbers.sort(reverse=True)
print(numbers)
```

**📤 Output**
```
[50, 40, 30, 20, 10]
```

**💡 Explanation:** `sort()` changes the **original list** (in place). Strings are sorted alphabetically, but **uppercase comes before lowercase**: `["banana", "apple", "Cherry"]` sorts to `['Cherry', 'apple', 'banana']`. Use `sort(key=str.lower)` to ignore case.

> ⚠️ `sort()` returns `None`. Don't write `numbers = numbers.sort()`, or you'll lose your list!

---

### 1️⃣6️⃣ Lab 16 – `reverse()`: Reverse the List

```python
students = ["Rahul", "Amit", "Neha"]
students.reverse()
print(students)
```

**📤 Output**
```
['Neha', 'Amit', 'Rahul']
```

**💡 Explanation:** `reverse()` flips the current order. It does **not** sort. For a reversed **copy** that leaves the original unchanged, use `students[::-1]`.

---

## Part 8 – Copy (Labs 17–18)

### 1️⃣7️⃣ Lab 17 – `copy()`: Copy a List

```python
students = ["Rahul", "Amit", "Neha"]
new_students = students.copy()
print(new_students)
```

**📤 Output**
```
['Rahul', 'Amit', 'Neha']
```

**📌 Why copy?** It lets you work with a separate list while keeping the original safe.

---

### 1️⃣8️⃣ Lab 18 – Assignment (`=`) vs `copy()`

This is one of the **most important** list concepts. `=` does **not** make a copy. It gives the **same list** a second name.

```python
students = ["Rahul", "Amit", "Neha"]
same_list = students          # NOT a copy, both names point to ONE list
same_list.append("Priya")
print(students)
```

**📤 Output:** the original changed too!
```
['Rahul', 'Amit', 'Neha', 'Priya']
```

```python
students = ["Rahul", "Amit", "Neha"]
copied_list = students.copy() # a real, separate copy
copied_list.append("Priya")
print(students)
print(copied_list)
```

**📤 Output:** the original is safe
```
['Rahul', 'Amit', 'Neha']
['Rahul', 'Amit', 'Neha', 'Priya']
```

```
  Assignment (=):                     copy():
  students ──┐                        students ────► ['Rahul', 'Amit', 'Neha']
             ├──► ['Rahul', ...]
  same_list ─┘                        copied_list ─► ['Rahul', 'Amit', 'Neha', 'Priya']
  (one list, two names)               (two separate lists)
```

> 💡 Other ways to copy: `students[:]` and `list(students)`.
>
> ⚠️ `copy()` is a **shallow** copy. If the list contains other lists, those inner lists are still shared. Use `import copy` and `copy.deepcopy()` for nested lists.

---

## Part 9 – Built-in Functions (Labs 19–23)

### 1️⃣9️⃣ Lab 19 – `len()`: List Length

```python
students = ["Rahul", "Amit", "Neha", "Priya"]
print(len(students))
```

**📤 Output**
```
4
```

**💡 Explanation:** Returns the number of items. The last index is always `len(list) - 1`.

---

### 2️⃣0️⃣ Lab 20 – `min()`: Minimum Value

```python
numbers = [50, 10, 40, 20, 30]
print(min(numbers))
```

**📤 Output**
```
10
```

---

### 2️⃣1️⃣ Lab 21 – `max()`: Maximum Value

```python
numbers = [50, 10, 40, 20, 30]
print(max(numbers))
```

**📤 Output**
```
50
```

**💡 Explanation for Labs 20–21:** These work on numbers, or on strings (alphabetical order). An empty list raises `ValueError`, and mixing numbers and strings raises `TypeError`.

---

### 2️⃣2️⃣ Lab 22 – `sum()`: Total

```python
numbers = [10, 20, 30, 40]
print(sum(numbers))
```

**📤 Output**
```
100
```

**💡 Explanation:** Adds up all the numbers. It only works with numbers, not strings. **Average** = `sum(numbers) / len(numbers)`.

---

### 2️⃣3️⃣ Lab 23 – `sorted()`: Create a New Sorted List

```python
numbers = [50, 10, 30, 20]
result = sorted(numbers)
print(result)
print(numbers)
```

**📤 Output**
```
[10, 20, 30, 50]
[50, 10, 30, 20]
```

**💡 Explanation:** `sorted()` returns a **new** sorted list and leaves the original unchanged.

### 🆚 `sort()` vs `sorted()`

| | `numbers.sort()` | `sorted(numbers)` |
|---|---|---|
| Type | List **method** | Built-in **function** |
| Changes the original? | ✅ Yes | ❌ No |
| Returns | `None` | A **new** sorted list |
| Works on | Lists only | Any iterable (list, tuple, string…) |
| Descending | `sort(reverse=True)` | `sorted(numbers, reverse=True)` |

---

## Part 10 – Mutability (Lab 24)

### 2️⃣4️⃣ Lab 24 – A List is Mutable

**Mutable** means you can **change** the items after the list is created.

```python
students = ["Rahul", "Amit", "Neha"]
students[1] = "Rohit"
print(students)
```

**📤 Output**
```
['Rahul', 'Rohit', 'Neha']
```

**💡 Explanation:** `students[1] = "Rohit"` replaced Amit with Rohit **in the same list**. Strings and tuples are **immutable**: `"Amit"[0] = "B"` raises a `TypeError`.

---

## 🎯 Real-World Project (Lab 25)

A company keeps a list of its employees:

```python
employees = ["Rahul", "Amit", "Neha"]

employees.append("Priya")        # new employee joins
employees.remove("Amit")         # employee leaves
print("Neha" in employees)       # is Neha an employee?
print(len(employees))            # total employees
print(employees)                 # final list
```

**📤 Output**
```
True
3
['Rahul', 'Neha', 'Priya']
```

**💡 Explanation:** Step by step:

| Step | List after the step |
|---|---|
| Start | `['Rahul', 'Amit', 'Neha']` |
| `append("Priya")` | `['Rahul', 'Amit', 'Neha', 'Priya']` |
| `remove("Amit")` | `['Rahul', 'Neha', 'Priya']` |

---

## ⚠️ Common Mistakes & Gotchas

| Code | You might expect | Python gives | Why / Fix |
|---|---|---|---|
| `students[4]` on a 4-item list | `Priya` | `IndexError` | Indexes start at 0, so the last is `[3]` or `[-1]` |
| `numbers = numbers.sort()` | Sorted list | `None` | `sort()` changes the list and returns `None`. Just call `numbers.sort()`. |
| `x = students.append("A")` | Updated list | `None` | All in-place methods return `None` |
| `students.append(["A", "B"])` | 2 items added | 1 nested item | Use `extend()` to add items separately |
| `students.remove("Rohit")` | Nothing happens | `ValueError` | Check `if "Rohit" in students:` first |
| `students.pop()` on `[]` | Nothing happens | `IndexError` | The list is empty |
| `new = students`, then change `new` | Original unchanged | Original changes too | Use `students.copy()` |
| `print(students[1:3])` | 3 items | 2 items | The stop index is not included |
| `sorted(["b", "a", "C"])` | `['a', 'b', 'C']` | `['C', 'a', 'b']` | Uppercase sorts first. Use `key=str.lower`. |
| `sum(["10", "20"])` | `30` | `TypeError` | Convert the strings to numbers first |

---

## 📋 Cheat Sheet

### List methods

| Method | What it does | Example (on `s = [3, 1, 2]`) | Result |
|---|---|---|---|
| `append(x)` | Add `x` at the end | `s.append(4)` | `[3, 1, 2, 4]` |
| `insert(i, x)` | Add `x` at index `i` | `s.insert(0, 9)` | `[9, 3, 1, 2]` |
| `extend(list)` | Add many items | `s.extend([4, 5])` | `[3, 1, 2, 4, 5]` |
| `remove(x)` | Remove first `x` (by value) | `s.remove(1)` | `[3, 2]` |
| `pop(i)` | Remove and **return** item at `i` | `s.pop(0)` | returns `3`, s = `[1, 2]` |
| `pop()` | Remove and **return** the last item | `s.pop()` | returns `2`, s = `[3, 1]` |
| `clear()` | Remove all items | `s.clear()` | `[]` |
| `index(x)` | Position of first `x` | `s.index(2)` | `2` |
| `count(x)` | How many times `x` appears | `s.count(3)` | `1` |
| `sort()` | Sort in place (ascending) | `s.sort()` | `[1, 2, 3]` |
| `sort(reverse=True)` | Sort in place (descending) | `s.sort(reverse=True)` | `[3, 2, 1]` |
| `reverse()` | Reverse in place | `s.reverse()` | `[2, 1, 3]` |
| `copy()` | Make a separate copy | `t = s.copy()` | `t = [3, 1, 2]` |

### Operators & statements

| Syntax | What it does | Example | Result |
|---|---|---|---|
| `s[i]` | Get item at index | `s[0]` | `3` |
| `s[i] = x` | Change item at index | `s[0] = 9` | `[9, 1, 2]` |
| `s[a:b]` | Slice (stop excluded) | `s[0:2]` | `[3, 1]` |
| `del s[i]` | Delete item at index | `del s[0]` | `[1, 2]` |
| `x in s` | Is `x` in the list? | `2 in s` | `True` |
| `s + t` | Join two lists | `[1] + [2]` | `[1, 2]` |
| `s * n` | Repeat the list | `[0] * 3` | `[0, 0, 0]` |

### Built-in functions

| Function | What it does | Example (on `[3, 1, 2]`) | Result |
|---|---|---|---|
| `len()` | Number of items | `len(s)` | `3` |
| `min()` | Smallest value | `min(s)` | `1` |
| `max()` | Largest value | `max(s)` | `3` |
| `sum()` | Total of numbers | `sum(s)` | `6` |
| `sorted()` | **New** sorted list | `sorted(s)` | `[1, 2, 3]` |
| `list()` | Convert to a list | `list("abc")` | `['a', 'b', 'c']` |

---

## 🎯 Practice Tasks

Create this list:

```python
marks = [85, 72, 90, 65, 88]
```

Then do the following **in order**. Each task works on the list as it is after the previous task.

| # | Task |
|---|---|
| 1 | Add `95` |
| 2 | Remove `65` |
| 3 | Find the maximum marks |
| 4 | Find the minimum marks |
| 5 | Find the total marks |
| 6 | Find the number of students |
| 7 | Sort the marks in ascending order |
| 8 | Sort the marks in descending order |
| 9 | Reverse the list |
| 10 | Create a copy of the list |

---

## ✅ Answers

> All answers are also in `answers.py`. Run `python answers.py` to check them.
> Starting list: `[85, 72, 90, 65, 88]`

<details>
<summary><b>Q1. Add 95</b></summary>

```python
marks.append(95)
print(marks)
```
**📤 Output**
```
[85, 72, 90, 65, 88, 95]
```
`append()` adds the new value at the end.
</details>

<details>
<summary><b>Q2. Remove 65</b></summary>

```python
marks.remove(65)
print(marks)
```
**📤 Output**
```
[85, 72, 90, 88, 95]
```
`remove()` takes the **value** 65, not an index.
</details>

<details>
<summary><b>Q3. Find the maximum marks</b></summary>

```python
print(max(marks))
```
**📤 Output**
```
95
```
The 95 we added in Q1 is now the highest.
</details>

<details>
<summary><b>Q4. Find the minimum marks</b></summary>

```python
print(min(marks))
```
**📤 Output**
```
72
```
65 was removed in Q2, so 72 is now the lowest.
</details>

<details>
<summary><b>Q5. Find the total marks</b></summary>

```python
print(sum(marks))
```
**📤 Output**
```
430
```
85 + 72 + 90 + 88 + 95 = 430.
</details>

<details>
<summary><b>Q6. Find the number of students</b></summary>

```python
print(len(marks))
```
**📤 Output**
```
5
```
💡 **Bonus:** the average is `sum(marks) / len(marks)` → `86.0`.
</details>

<details>
<summary><b>Q7. Sort the marks in ascending order</b></summary>

```python
marks.sort()
print(marks)
```
**📤 Output**
```
[72, 85, 88, 90, 95]
```
</details>

<details>
<summary><b>Q8. Sort the marks in descending order</b></summary>

```python
marks.sort(reverse=True)
print(marks)
```
**📤 Output**
```
[95, 90, 88, 85, 72]
```
</details>

<details>
<summary><b>Q9. Reverse the list</b></summary>

```python
marks.reverse()
print(marks)
```
**📤 Output**
```
[72, 85, 88, 90, 95]
```
The list was in descending order after Q8, so reversing it makes it ascending again. `reverse()` only flips the current order. It doesn't sort.
</details>

<details>
<summary><b>Q10. Create a copy of the list</b></summary>

```python
marks_copy = marks.copy()
print(marks_copy)

marks_copy.append(100)          # prove the copy is separate
print("Copy    :", marks_copy)
print("Original:", marks)
```
**📤 Output**
```
[72, 85, 88, 90, 95]
Copy    : [72, 85, 88, 90, 95, 100]
Original: [72, 85, 88, 90, 95]
```
Changing the copy does **not** change the original.
</details>

---

## 🚀 Bonus Challenges

1. Find the **second highest** mark in `[85, 72, 90, 65, 88]`.
2. Remove all duplicates from `[10, 20, 10, 30, 20]`.
3. Make a list of the squares of 1 to 5.
4. Make a list of only the marks of 80 or above from `[85, 72, 90, 65, 88]`.

<details>
<summary>👉 Show bonus answers</summary>

```python
# 1
print(sorted([85, 72, 90, 65, 88])[-2])                  # 88

# 2  (dict.fromkeys keeps the original order)
print(list(dict.fromkeys([10, 20, 10, 30, 20])))         # [10, 20, 30]

# 3  (list comprehension)
print([n ** 2 for n in range(1, 6)])                     # [1, 4, 9, 16, 25]

# 4
print([m for m in [85, 72, 90, 65, 88] if m >= 80])      # [85, 90, 88]
```
</details>

---

<p align="center"><b>✅ End of Python List Lab · Practice → Understand → Code → Master Python 🐍</b></p>
