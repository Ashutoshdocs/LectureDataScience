# 🐍 Python String (`str`) – Complete Methods Lab

A hands-on practical covering **48 string methods**, with code, output and an easy explanation for each. It also includes common mistakes, a cheat sheet, and **15 practice tasks with full answers**.

> All code and outputs in this guide were tested on **Python 3.13**. `removeprefix()` and `removesuffix()` need **Python 3.9 or newer**. Everything else works on any Python 3.

---

## 📁 What's in this folder

| File | Use it for |
|---|---|
| `README.md` | This guide: basics, 48 labs, gotchas, practice tasks and answers |
| `string_lab.py` | All 48 labs in one script: `python string_lab.py` |
| `answers.py` | Runnable answers to the 15 practice tasks: `python answers.py` |

> ⚠️ **Copy code from this README or the `.py` files, not from bold-text handouts.** Code typed in Unicode "bold" letters (like 𝗽𝗿𝗶𝗻𝘁) looks normal but behaves differently: the bold text inside quotes is *not* changed by `upper()`, so you'd get the wrong output with no error message.

---

## 📚 Table of Contents

- [String Basics](#-string-basics)
- [Part A – Case Conversion (Labs 1–6)](#part-a--case-conversion-labs-16)
- [Part B – Searching & Counting (Labs 7–13)](#part-b--searching--counting-labs-713)
- [Part C – Replacing & Cleaning (Labs 14–17)](#part-c--replacing--cleaning-labs-1417)
- [Part D – Splitting & Joining (Labs 18–23)](#part-d--splitting--joining-labs-1823)
- [Part E – Alignment & Padding (Labs 24–27)](#part-e--alignment--padding-labs-2427)
- [Part F – Checking Methods: is…() (Labs 28–39)](#part-f--checking-methods-is-labs-2839)
- [Part G – Encoding & Formatting (Labs 40–42)](#part-g--encoding--formatting-labs-4042)
- [Part H – Advanced Methods (Labs 43–48)](#part-h--advanced-methods-labs-4348)
- [Common Mistakes & Gotchas](#%EF%B8%8F-common-mistakes--gotchas)
- [Cheat Sheet](#-cheat-sheet)
- [Practice Tasks](#-practice-tasks)
- [Answers](#-answers)

---

## 📌 String Basics

A **string** is a **sequence of characters**: letters, digits, spaces and symbols written inside quotes.

```python
name = "Sanjay"
city = 'Noida'          # single or double quotes both work
note = """This can
span many lines"""      # triple quotes for multi-line text
```

Every string belongs to the `str` class:

```python
print(type("Sanjay"))   # <class 'str'>
```

### 🔢 Indexing: each character has a position

```
  S    a    n    j    a    y
  0    1    2    3    4    5      ← positive index
 -6   -5   -4   -3   -2   -1      ← negative index
```

```python
name = "Sanjay"
print(name[0])      # S
print(name[-1])     # y
print(name[0:3])    # San   (slice: index 0 up to, not including, 3)
print(len(name))    # 6
```

### 🔒 Strings are immutable: methods return a NEW string

A string method **never changes the original string**. It returns a new one.

```python
name = "Sanjay"
print(name.upper())   # SANJAY
print(name)           # Sanjay   ← original is unchanged!

name = name.upper()   # to keep the result, store it
print(name)           # SANJAY
```

> 💡 **How to call a method:** `string.method()`. Put a dot after the string, then the method name and brackets. Don't forget the `()`!

---

## Part A – Case Conversion (Labs 1–6)

### 🔤 Lab 01 – `upper()`

**Purpose:** Converts the string to UPPERCASE.

```python
name = "sanjay"
print(name.upper())
```

**📤 Output**
```
SANJAY
```

**💡 Explanation:** Every lowercase letter becomes uppercase. Digits, spaces and symbols stay the same.

---

### 🔡 Lab 02 – `lower()`

**Purpose:** Converts the string to lowercase.

```python
name = "SANJAY"
print(name.lower())
```

**📤 Output**
```
sanjay
```

**💡 Explanation:** Every uppercase letter becomes lowercase. This is useful for comparing user input: `answer.lower() == "yes"` matches `YES`, `Yes` and `yes`.

---

### 🔠 Lab 03 – `capitalize()`

**Purpose:** Makes the first character uppercase.

```python
name = "sanjay dahiya"
print(name.capitalize())
```

**📤 Output**
```
Sanjay dahiya
```

**💡 Explanation:** Only the **first character of the whole string** is capitalized. It also makes **all other letters lowercase**: `"pYTHON pROGRAMMING".capitalize()` → `Python programming`.

---

### 🔤 Lab 04 – `title()`

**Purpose:** Makes the first character of every word uppercase.

```python
name = "sanjay dahiya"
print(name.title())
```

**📤 Output**
```
Sanjay Dahiya
```

**💡 Explanation:** Each word starts with a capital letter, and the rest of each word becomes lowercase.

> ⚠️ `title()` treats an apostrophe as the end of a word: `"they're".title()` → `They'Re`.

| Method | Input `"sanjay dahiya"` |
|---|---|
| `capitalize()` | `Sanjay dahiya` (first letter of the string) |
| `title()` | `Sanjay Dahiya` (first letter of every word) |

---

### 🔄 Lab 05 – `swapcase()`

**Purpose:** Swaps the case: uppercase becomes lowercase and lowercase becomes uppercase.

```python
name = "SaNjAy"
print(name.swapcase())
```

**📤 Output**
```
sAnJaY
```

---

### 🔎 Lab 06 – `casefold()`

**Purpose:** Converts the string to lowercase **for comparison**.

```python
name = "SANJAY"
print(name.casefold())
```

**📤 Output**
```
sanjay
```

**💡 Explanation:** `casefold()` is a stronger version of `lower()`, built for **case-insensitive comparison**. For English text they give the same result, but `casefold()` also handles special letters. For example, the German `ß` becomes `ss`:

```python
print("Straße".lower() == "STRASSE".lower())        # False
print("Straße".casefold() == "STRASSE".casefold())  # True
```

> 💡 **Rule of thumb:** use `lower()` to display text and `casefold()` to compare text.

---

## Part B – Searching & Counting (Labs 7–13)

### 🔢 Lab 07 – `count()`

**Purpose:** Counts how many times a character or substring appears.

```python
name = "banana"
print(name.count("a"))
```

**📤 Output**
```
3
```

**💡 Explanation:** b-**a**-n-**a**-n-**a** contains 3 a's. `count()` is case-sensitive and does **not** count overlapping matches: `"banana".count("ana")` → `1`.

---

### 🔍 Lab 08 – `find()`

**Purpose:** Returns the index of the **first** match, or `-1` if there is no match.

```python
name = "sanjay"
print(name.find("j"))
```

**📤 Output**
```
3
```

**💡 Explanation:** In s(0) a(1) n(2) **j(3)** a(4) y(5), `j` is at index 3. If the text isn't found, you get `-1`: `"sanjay".find("z")` → `-1`.

---

### 🔍 Lab 09 – `rfind()`

**Purpose:** Returns the index of the **last** match (it searches from the right).

```python
name = "banana"
print(name.rfind("a"))
```

**📤 Output**
```
5
```

**💡 Explanation:** b(0) a(1) n(2) a(3) n(4) **a(5)**. The last `a` is at index 5. The index is still counted from the left. Returns `-1` if not found.

---

### 🔍 Lab 10 – `index()`

**Purpose:** Returns the index of the first match, like `find()`.

```python
name = "sanjay"
print(name.index("j"))
```

**📤 Output**
```
3
```

**💡 Explanation:** `index()` works like `find()`, with one big difference: if the text is **not found**, it raises an **error** instead of returning `-1`.

```python
print("sanjay".find("z"))    # -1
print("sanjay".index("z"))   # ValueError: substring not found
```

| Method | When found | When NOT found |
|---|---|---|
| `find()` / `rfind()` | index | `-1` |
| `index()` / `rindex()` | index | ❌ `ValueError` |

---

### 🔍 Lab 11 – `rindex()`

**Purpose:** Returns the index of the last match. Raises an error if not found.

```python
name = "banana"
print(name.rindex("a"))
```

**📤 Output**
```
5
```

---

### ✅ Lab 12 – `startswith()`

**Purpose:** Checks whether the string **starts** with a given value.

```python
name = "sanjay"
print(name.startswith("san"))
```

**📤 Output**
```
True
```

**💡 Explanation:** Returns `True` or `False`. It's case-sensitive, so `"sanjay".startswith("San")` → `False`. You can check several options at once with a tuple: `url.startswith(("http://", "https://"))`.

---

### ✅ Lab 13 – `endswith()`

**Purpose:** Checks whether the string **ends** with a given value.

```python
name = "sanjay"
print(name.endswith("jay"))
```

**📤 Output**
```
True
```

**💡 Explanation:** A common use is checking file types: `filename.endswith(".pdf")`.

---

## Part C – Replacing & Cleaning (Labs 14–17)

### 🔁 Lab 14 – `replace()`

**Purpose:** Replaces one part of the string with another.

```python
name = "Hello Sanjay"
print(name.replace("Sanjay", "Rahul"))
```

**📤 Output**
```
Hello Rahul
```

**💡 Explanation:** `replace(old, new)` replaces **every** match. Add a third argument to limit how many: `"banana".replace("a", "o", 1)` → `bonana`.

---

### ✂️ Lab 15 – `strip()`

**Purpose:** Removes extra spaces from **both** ends.

```python
name = "   Sanjay   "
print(name.strip())
```

**📤 Output**
```
Sanjay
```

**💡 Explanation:** Removes spaces, tabs (`\t`) and newlines (`\n`) from the start and end, but **not** from the middle. You can also remove other characters: `"##Python##".strip("#")` → `Python`.

> 💡 Use `strip()` on user input: `name = input("Name: ").strip()`.

---

### ⬅️ Lab 16 – `lstrip()`

**Purpose:** Removes spaces from the **left** side only.

```python
name = "   Sanjay"
print(name.lstrip())
```

**📤 Output**
```
Sanjay
```

---

### ➡️ Lab 17 – `rstrip()`

**Purpose:** Removes spaces from the **right** side only.

```python
name = "Sanjay   "
print(name.rstrip())
```

**📤 Output**
```
Sanjay
```

> 🔍 **Tip:** spaces are invisible when printed. Use `repr()` to see them: `print(repr("Sanjay   ".rstrip()))` → `'Sanjay'`.

---

## Part D – Splitting & Joining (Labs 18–23)

### ✂️ Lab 18 – `split()`

**Purpose:** Breaks a string into a **list** of words.

```python
name = "Sanjay Dahiya Trainer"
print(name.split())
```

**📤 Output**
```
['Sanjay', 'Dahiya', 'Trainer']
```

**💡 Explanation:** With no argument, `split()` splits on any whitespace and ignores extra spaces. You can also split on a specific character:

```python
print("a,b,c".split(","))       # ['a', 'b', 'c']
print("a,b,,c".split(","))      # ['a', 'b', '', 'c']   ← empty item between ,,
```

---

### ✂️ Lab 19 – `rsplit()`

**Purpose:** Splits from the **right** side.

```python
data = "Python-Docker-Kubernetes"
print(data.rsplit("-", 1))
```

**📤 Output**
```
['Python-Docker', 'Kubernetes']
```

**💡 Explanation:** The `1` is **maxsplit**: split only once. `rsplit` starts from the right, so only the **last** `-` is used. Compare with `split("-", 1)` → `['Python', 'Docker-Kubernetes']`. Without maxsplit, `split()` and `rsplit()` give the same result.

---

### 📄 Lab 20 – `splitlines()`

**Purpose:** Breaks a multi-line string into a list of lines.

```python
data = "Python\nDocker\nKubernetes"
print(data.splitlines())
```

**📤 Output**
```
['Python', 'Docker', 'Kubernetes']
```

**💡 Explanation:** `\n` is the **newline** character. `splitlines()` splits at every line break. This is very useful when reading text files.

---

### 🔀 Lab 21 – `partition()`

**Purpose:** Splits the string into exactly **3 parts** at the first match.

```python
data = "Python-Docker"
print(data.partition("-"))
```

**📤 Output**
```
('Python', '-', 'Docker')
```

**💡 Explanation:** Returns a **tuple**: `(before, separator, after)`. If the separator isn't found, you get `(whole_string, '', '')`.

---

### 🔀 Lab 22 – `rpartition()`

**Purpose:** Splits into 3 parts at the **last** match.

```python
data = "Python-Docker-Kubernetes"
print(data.rpartition("-"))
```

**📤 Output**
```
('Python-Docker', '-', 'Kubernetes')
```

---

### 🔗 Lab 23 – `join()`

**Purpose:** Joins a list of strings into one string.

```python
names = ["Sanjay", "Rahul", "Amit"]
print("-".join(names))
```

**📤 Output**
```
Sanjay-Rahul-Amit
```

**💡 Explanation:** The syntax is `separator.join(list)`. The string **before** the dot goes **between** the items. `join()` is the opposite of `split()`:

```python
print(" ".join(["Hello", "World"]))   # Hello World
print("".join(["P", "y"]))            # Py
```

> ⚠️ All items must be strings. `"-".join([1, 2])` raises a `TypeError`.

---

## Part E – Alignment & Padding (Labs 24–27)

### ↔️ Lab 24 – `center()`

**Purpose:** Places the string in the center of a given width.

```python
name = "Python"
print(name.center(20, "-"))
```

**📤 Output**
```
-------Python-------
```

**💡 Explanation:** The total width is 20 and "Python" takes 6, so 14 fill characters are added: 7 on each side. The fill character is optional and defaults to a space.

---

### ⬅️ Lab 25 – `ljust()`

**Purpose:** Aligns the string to the **left** and pads on the right.

```python
name = "Python"
print(name.ljust(10, "-"))
```

**📤 Output**
```
Python----
```

---

### ➡️ Lab 26 – `rjust()`

**Purpose:** Aligns the string to the **right** and pads on the left.

```python
name = "Python"
print(name.rjust(10, "-"))
```

**📤 Output**
```
----Python
```

> 💡 These three methods are handy for printing neat tables. If the width is smaller than the string, the string is returned unchanged.

---

### 0️⃣ Lab 27 – `zfill()`

**Purpose:** Adds zeros on the left until the string reaches a given width.

```python
number = "123"
print(number.zfill(6))
```

**📤 Output**
```
000123
```

**💡 Explanation:** Useful for IDs and roll numbers (`007`, `000123`). It keeps a sign at the front: `"-42".zfill(6)` → `-00042`.

---

## Part F – Checking Methods: is…() (Labs 28–39)

> 💡 All `is...()` methods return **`True` or `False`**. Most of them return `False` for an empty string `""`.

### 🔢 Lab 28 – `isalnum()`

**Purpose:** Checks whether **every** character is a letter **or** a digit.

```python
value = "Python123"
print(value.isalnum())
```

**📤 Output**
```
True
```

**💡 Explanation:** "Alnum" means **al**phabet + **num**ber. The string does **not** need both: `"Python"` and `"123"` are both `True`. Any space or symbol makes it `False`, so `"Python 123".isalnum()` → `False`.

---

### 🔤 Lab 29 – `isalpha()`

**Purpose:** Checks whether every character is a **letter**.

```python
value = "Python"
print(value.isalpha())
```

**📤 Output**
```
True
```

**💡 Explanation:** `"Python3".isalpha()` → `False` (it has a digit) and `"Hello World".isalpha()` → `False` (it has a space).

---

### 🔤 Lab 30 – `isascii()`

**Purpose:** Checks whether every character is an **ASCII** character.

```python
value = "Python123"
print(value.isascii())
```

**📤 Output**
```
True
```

**💡 Explanation:** ASCII covers the basic English letters, digits and common symbols (128 characters). Hindi text, emoji and accented letters are not ASCII: `"नमस्ते".isascii()` → `False`.

---

### 🔢 Lab 31 – `isdecimal()`

```python
value = "12345"
print(value.isdecimal())
```

**📤 Output**
```
True
```

### 🔢 Lab 32 – `isdigit()`

```python
value = "12345"
print(value.isdigit())
```

**📤 Output**
```
True
```

### 🔢 Lab 33 – `isnumeric()`

```python
value = "12345"
print(value.isnumeric())
```

**📤 Output**
```
True
```

**💡 Explanation for Labs 31–33:** All three return `True` for normal digits like `"12345"`. They differ only on special Unicode characters:

| Value | `isdecimal()` | `isdigit()` | `isnumeric()` |
|---|---|---|---|
| `"123"` | ✅ True | ✅ True | ✅ True |
| `"²"` (superscript) | ❌ False | ✅ True | ✅ True |
| `"½"` (fraction) | ❌ False | ❌ False | ✅ True |
| `"12.5"` | ❌ False | ❌ False | ❌ False |
| `"-5"` | ❌ False | ❌ False | ❌ False |

```
 isdecimal  ⊂  isdigit  ⊂  isnumeric     (strictest → loosest)
```

> ⚠️ None of them accept a decimal point or a minus sign. Use `isdecimal()` to check whether text can safely go into `int()`.

---

### 🐍 Lab 34 – `isidentifier()`

**Purpose:** Checks whether the string is a valid Python **variable name**.

```python
value = "student_name"
print(value.isidentifier())
```

**📤 Output**
```
True
```

**💡 Explanation:** Valid names use letters, digits and `_`, and can't start with a digit, so `"2name".isidentifier()` → `False`. Note that Python keywords pass this check (`"class".isidentifier()` → `True`) even though you can't use them as variable names.

---

### 🔡 Lab 35 – `islower()`

```python
value = "python"
print(value.islower())
```

**📤 Output**
```
True
```

### 🔠 Lab 36 – `isupper()`

```python
value = "PYTHON"
print(value.isupper())
```

**📤 Output**
```
True
```

**💡 Explanation for Labs 35–36:** These checks only look at **letters**: digits and symbols are ignored, so `"PYTHON123".isupper()` → `True`. The string must contain at least one letter, so `"123".isupper()` → `False`.

---

### 🔤 Lab 37 – `istitle()`

**Purpose:** Checks whether the string is in title case.

```python
value = "Python Programming"
print(value.istitle())
```

**📤 Output**
```
True
```

**💡 Explanation:** Every word must start with an uppercase letter followed by lowercase letters. `"Python programming".istitle()` → `False`.

---

### ⬜ Lab 38 – `isspace()`

**Purpose:** Checks whether the string contains **only whitespace**.

```python
value = "   "
print(value.isspace())
```

**📤 Output**
```
True
```

**💡 Explanation:** Spaces, tabs and newlines all count as whitespace. An empty string `""` returns `False`. This is handy for rejecting blank input.

---

### 🖨️ Lab 39 – `isprintable()`

**Purpose:** Checks whether all characters are printable.

```python
value = "Hello Python"
print(value.isprintable())
```

**📤 Output**
```
True
```

**💡 Explanation:** Characters like `\n` (newline) and `\t` (tab) are **not** printable: `"Hello\n".isprintable()` → `False`.

---

## Part G – Encoding & Formatting (Labs 40–42)

### 💾 Lab 40 – `encode()`

**Purpose:** Converts the string into **bytes**.

```python
name = "Python"
print(name.encode())
```

**📤 Output**
```
b'Python'
```

**💡 Explanation:** The `b` prefix means the result is a **bytes** object (`<class 'bytes'>`). The default encoding is **UTF-8**. Bytes are what get saved to files and sent over networks. Non-English characters become several bytes each: `"नमस्ते".encode()` → `b'\xe0\xa4\xa8...'`. To reverse it, use `.decode()`: `b'Python'.decode()` → `'Python'`.

---

### 🧩 Lab 41 – `format()`

**Purpose:** Inserts values into a string.

```python
name = "Sanjay"
course = "Python"

message = "My name is {} and I teach {}."
print(message.format(name, course))
```

**📤 Output**
```
My name is Sanjay and I teach Python.
```

**💡 Explanation:** Each `{}` is a placeholder, filled in order by the values you pass to `format()`.

> 💡 **The modern way: f-strings (Python 3.6+).** Put `f` before the quotes and write the variable inside `{}`:
> ```python
> print(f"My name is {name} and I teach {course}.")
> ```

---

### 🧩 Lab 42 – `format_map()`

**Purpose:** Inserts values from a **dictionary** into a string.

```python
data = {
    "name": "Sanjay",
    "course": "Python"
}

message = "My name is {name} and I teach {course}."
print(message.format_map(data))
```

**📤 Output**
```
My name is Sanjay and I teach Python.
```

**💡 Explanation:** Each `{key}` placeholder is filled with the matching value from the dictionary. `message.format(**data)` gives the same result.

---

## Part H – Advanced Methods (Labs 43–48)

### 🔄 Lab 43 – `maketrans()`

**Purpose:** Creates a **translation table** (a character-to-character mapping).

```python
table = str.maketrans("abc", "123")
print("abc".translate(table))
```

**📤 Output**
```
123
```

**💡 Explanation:** `str.maketrans("abc", "123")` means a→1, b→2, c→3. Both strings must be the **same length**. It's called on `str` itself, not on a particular string. A third argument lists characters to **delete**: `"hello world".translate(str.maketrans("", "", "lo"))` → `he wrd`.

---

### 🔄 Lab 44 – `translate()`

**Purpose:** Replaces characters using a translation table.

```python
table = str.maketrans("abc", "123")
text = "abcabc"
print(text.translate(table))
```

**📤 Output**
```
123123
```

**💡 Explanation:** `translate()` applies the table to every character. Use it to replace **many single characters** in one go. Use `replace()` for whole words.

---

### ⬅️ Lab 45 – `removeprefix()` *(Python 3.9+)*

**Purpose:** Removes a given prefix from the start of the string.

```python
name = "Mr. Sanjay"
print(name.removeprefix("Mr. "))
```

**📤 Output**
```
Sanjay
```

**💡 Explanation:** If the string doesn't start with that prefix, it's returned unchanged: `"Mr. Sanjay".removeprefix("Dr. ")` → `Mr. Sanjay`.

> ⚠️ **Don't use `lstrip()` for this.** `lstrip("Mr. ")` removes any of the characters `M`, `r`, `.` and space, not the whole word "Mr. ".

---

### ➡️ Lab 46 – `removesuffix()` *(Python 3.9+)*

**Purpose:** Removes a given suffix from the end of the string.

```python
file = "python.txt"
print(file.removesuffix(".txt"))
```

**📤 Output**
```
python
```

---

### ↹ Lab 47 – `expandtabs()`

**Purpose:** Replaces tab characters (`\t`) with spaces.

```python
data = "Python\tDocker"
print(data.expandtabs(4))
```

**📤 Output**
```
Python  Docker
```

**💡 Explanation:** Tab stops are placed every 4 columns (0, 4, 8…). "Python" ends at column 6, so the tab moves to the next stop at column 8, adding **2 spaces**. The default tab size is 8.

---

### 🔎 Lab 48 – `__contains__()` and the `in` operator

**Purpose:** Checks whether a substring is present in the string.

```python
name = "Sanjay"
print("jay" in name)
```

**📤 Output**
```
True
```

**💡 Explanation:** `"jay" in name` calls `name.__contains__("jay")` behind the scenes. Methods with double underscores are called **dunder** (magic) methods. You almost never call them directly, so always use `in` (or `not in`). It's case-sensitive: `"JAY" in name` → `False`.

---

## ⚠️ Common Mistakes & Gotchas

| Code | You might expect | Python gives | Why |
|---|---|---|---|
| `name.upper()` then `print(name)` | `SANJAY` | `Sanjay` | Strings are immutable. Store the result: `name = name.upper()` |
| `name.upper` (no brackets) | `SANJAY` | `<built-in method upper...>` | Methods need `()` |
| `name[0] = "R"` | `Ranjay` | `TypeError` | You can't change a string in place. Use `replace()` or slicing. |
| `"sanjay".index("z")` | `-1` | `ValueError` | Use `find()` if the text might be missing |
| `"Python 123".isalnum()` | `True` | `False` | The space isn't a letter or digit |
| `"12.5".isdigit()` | `True` | `False` | `.` and `-` are not digits |
| `"Mr. Mark".lstrip("Mr. ")` | `Mark` | `ark` | `lstrip` removes a **set of characters**. Use `removeprefix()`. |
| `"-".join([1, 2, 3])` | `1-2-3` | `TypeError` | Convert first: `"-".join(map(str, [1, 2, 3]))` |
| `"Sanjay".startswith("san")` | `True` | `False` | All string methods are case-sensitive |
| `"they're".title()` | `They're` | `They'Re` | `title()` treats `'` as a word break |

---

## 📋 Cheat Sheet

### Case conversion
| Method | Example | Result |
|---|---|---|
| `upper()` | `"hi".upper()` | `HI` |
| `lower()` | `"HI".lower()` | `hi` |
| `capitalize()` | `"hi there".capitalize()` | `Hi there` |
| `title()` | `"hi there".title()` | `Hi There` |
| `swapcase()` | `"Hi".swapcase()` | `hI` |
| `casefold()` | `"HI".casefold()` | `hi` (for comparisons) |

### Searching & counting
| Method | Example | Result |
|---|---|---|
| `count()` | `"banana".count("a")` | `3` |
| `find()` / `rfind()` | `"banana".find("a")` / `.rfind("a")` | `1` / `5` (`-1` if missing) |
| `index()` / `rindex()` | `"banana".index("a")` / `.rindex("a")` | `1` / `5` (error if missing) |
| `startswith()` | `"python".startswith("py")` | `True` |
| `endswith()` | `"file.txt".endswith(".txt")` | `True` |
| `in` | `"py" in "python"` | `True` |

### Modifying & cleaning
| Method | Example | Result |
|---|---|---|
| `replace()` | `"Hi Sam".replace("Sam", "Ram")` | `Hi Ram` |
| `strip()` / `lstrip()` / `rstrip()` | `"  hi  ".strip()` | `hi` |
| `removeprefix()` | `"Mr. Sam".removeprefix("Mr. ")` | `Sam` |
| `removesuffix()` | `"a.txt".removesuffix(".txt")` | `a` |
| `maketrans()` + `translate()` | `"abc".translate(str.maketrans("abc", "123"))` | `123` |
| `expandtabs()` | `"a\tb".expandtabs(4)` | `a   b` |

### Splitting & joining
| Method | Example | Result |
|---|---|---|
| `split()` | `"a b c".split()` | `['a', 'b', 'c']` |
| `rsplit()` | `"a-b-c".rsplit("-", 1)` | `['a-b', 'c']` |
| `splitlines()` | `"a\nb".splitlines()` | `['a', 'b']` |
| `partition()` | `"a-b-c".partition("-")` | `('a', '-', 'b-c')` |
| `rpartition()` | `"a-b-c".rpartition("-")` | `('a-b', '-', 'c')` |
| `join()` | `"-".join(["a", "b"])` | `a-b` |

### Alignment & padding
| Method | Example | Result |
|---|---|---|
| `center()` | `"hi".center(6, "*")` | `**hi**` |
| `ljust()` | `"hi".ljust(5, "*")` | `hi***` |
| `rjust()` | `"hi".rjust(5, "*")` | `***hi` |
| `zfill()` | `"7".zfill(3)` | `007` |

### Checking methods (return True/False)
| Method | True when… |
|---|---|
| `isalnum()` | all characters are letters or digits |
| `isalpha()` | all characters are letters |
| `isascii()` | all characters are ASCII |
| `isdecimal()` | all characters are 0–9 style digits (strictest) |
| `isdigit()` | all characters are digits (also accepts `²`) |
| `isnumeric()` | all characters are numeric (also accepts `½`) |
| `isidentifier()` | the string is a valid variable name |
| `islower()` / `isupper()` | all letters are lowercase / uppercase |
| `istitle()` | every word starts with a capital letter |
| `isspace()` | only whitespace (and not empty) |
| `isprintable()` | no `\n`, `\t` or other control characters |

### Encoding & formatting
| Method | Example | Result |
|---|---|---|
| `encode()` | `"hi".encode()` | `b'hi'` |
| `format()` | `"{} is {}".format("Sky", "blue")` | `Sky is blue` |
| `format_map()` | `"{a}".format_map({"a": 1})` | `1` |
| f-string | `f"{2 + 3}"` | `5` |

---

## 🎯 Practice Tasks

Try each task yourself **before** looking at the answers.

| # | Task |
|---|---|
| 1 | Convert `"python programming"` to uppercase. |
| 2 | Convert `"PYTHON PROGRAMMING"` to lowercase. |
| 3 | Convert `"hello world"` to title case. |
| 4 | How many times does `"a"` appear in `"banana"`? |
| 5 | Find `"Python"` in `"I love Python"`. |
| 6 | Replace `"World"` with `"Python"` in `"Hello World"`. |
| 7 | Remove the extra spaces from `"   Python   "`. |
| 8 | Convert `"Python Docker Kubernetes"` into a list. |
| 9 | Join `["Python", "Docker", "Kubernetes"]` using `"-"`. |
| 10 | Check whether `"Python123"` is alphanumeric. |
| 11 | Check whether `"Python"` is alphabetic. |
| 12 | Make `"12345"` 10 characters long using `zfill()`. |
| 13 | Remove `"Mr. "` from `"Mr. Sanjay"`. |
| 14 | Remove `".txt"` from `"python.txt"`. |
| 15 | Check whether `"PYTHON"` is uppercase. |

---

## ✅ Answers

> All answers are also in `answers.py`. Run `python answers.py` to check them.

<details>
<summary><b>Q1. Convert "python programming" to uppercase</b></summary>

```python
print("python programming".upper())
```
**📤 Output**
```
PYTHON PROGRAMMING
```
</details>

<details>
<summary><b>Q2. Convert "PYTHON PROGRAMMING" to lowercase</b></summary>

```python
print("PYTHON PROGRAMMING".lower())
```
**📤 Output**
```
python programming
```
</details>

<details>
<summary><b>Q3. Convert "hello world" to title case</b></summary>

```python
print("hello world".title())
```
**📤 Output**
```
Hello World
```
Use `title()`, not `capitalize()`. `capitalize()` would give `Hello world`.
</details>

<details>
<summary><b>Q4. How many times does "a" appear in "banana"?</b></summary>

```python
print("banana".count("a"))
```
**📤 Output**
```
3
```
</details>

<details>
<summary><b>Q5. Find "Python" in "I love Python"</b></summary>

```python
text = "I love Python"
print(text.find("Python"))
print("Python" in text)
```
**📤 Output**
```
7
True
```
`find()` gives the **position** where "Python" starts (I=0, space=1, l=2 … P=7). `in` just answers **yes or no**.
</details>

<details>
<summary><b>Q6. Replace "World" with "Python" in "Hello World"</b></summary>

```python
print("Hello World".replace("World", "Python"))
```
**📤 Output**
```
Hello Python
```
</details>

<details>
<summary><b>Q7. Remove the extra spaces from "   Python   "</b></summary>

```python
print("   Python   ".strip())
print(repr("   Python   ".strip()))
```
**📤 Output**
```
Python
'Python'
```
`repr()` shows the quotes, which proves no spaces are left.
</details>

<details>
<summary><b>Q8. Convert "Python Docker Kubernetes" into a list</b></summary>

```python
print("Python Docker Kubernetes".split())
```
**📤 Output**
```
['Python', 'Docker', 'Kubernetes']
```
</details>

<details>
<summary><b>Q9. Join ["Python", "Docker", "Kubernetes"] using "-"</b></summary>

```python
print("-".join(["Python", "Docker", "Kubernetes"]))
```
**📤 Output**
```
Python-Docker-Kubernetes
```
The separator `"-"` comes **before** `.join()`, not inside it.
</details>

<details>
<summary><b>Q10. Check whether "Python123" is alphanumeric</b></summary>

```python
print("Python123".isalnum())
```
**📤 Output**
```
True
```
</details>

<details>
<summary><b>Q11. Check whether "Python" is alphabetic</b></summary>

```python
print("Python".isalpha())
```
**📤 Output**
```
True
```
</details>

<details>
<summary><b>Q12. Make "12345" 10 characters long using zfill()</b></summary>

```python
print("12345".zfill(10))
```
**📤 Output**
```
0000012345
```
The number passed to `zfill()` is the **total length**, not the number of zeros to add. Here 5 zeros are added.
</details>

<details>
<summary><b>Q13. Remove "Mr. " from "Mr. Sanjay"</b></summary>

```python
print("Mr. Sanjay".removeprefix("Mr. "))
```
**📤 Output**
```
Sanjay
```
On Python 3.8 or older, use `"Mr. Sanjay".replace("Mr. ", "", 1)` instead.
</details>

<details>
<summary><b>Q14. Remove ".txt" from "python.txt"</b></summary>

```python
print("python.txt".removesuffix(".txt"))
```
**📤 Output**
```
python
```
</details>

<details>
<summary><b>Q15. Check whether "PYTHON" is uppercase</b></summary>

```python
print("PYTHON".isupper())
```
**📤 Output**
```
True
```
</details>

---

## 🚀 Bonus Challenges

1. Reverse the string `"Python"`.
2. Count the words in `"Python is easy to learn"`.
3. Check whether `"Madam"` is a palindrome (it reads the same backwards), ignoring case.
4. Turn `"  sanjay DAHIYA  "` into `"Sanjay Dahiya"` in one line.
5. Get the file extension from `"report.final.pdf"`.

<details>
<summary>👉 Show bonus answers</summary>

```python
# 1
print("Python"[::-1])                                    # nohtyP

# 2
print(len("Python is easy to learn".split()))            # 5

# 3
word = "Madam"
print(word.casefold() == word.casefold()[::-1])          # True

# 4
print("  sanjay DAHIYA  ".strip().title())               # Sanjay Dahiya

# 5
print("report.final.pdf".rpartition(".")[2])             # pdf
```
</details>

---

<p align="center"><b>🐍 End of String Methods Lab · Happy Coding!</b></p>
