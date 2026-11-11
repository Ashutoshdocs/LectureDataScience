# LAB 10 — Python `re` Module

## Purpose
Search and validate text with regular expressions.

## What you will learn
`re` provides regular-expression operations. `findall()` returns matches, `search()` finds the first match, `sub()` replaces matches, and `fullmatch()` checks whether the entire string matches a pattern.

## Code

```python
import re

text = "Contact support at help@example.com or sales@example.org"

# Find all email-like matches in the text.
emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
print("Found email addresses:", emails)

# Search for a pattern.
match = re.search(r"support", text)
print("Found support:", bool(match))

# Replace a word.
updated_text = re.sub(r"support", "customer care", text)
print("Updated text:", updated_text)

# Check whether a string contains only 10 digits.
mobile = "9876543210"
if re.fullmatch(r"\d{10}", mobile):
    print("Mobile number has 10 digits")
else:
    print("Invalid mobile number")
```

## Run the lab

From this lab's folder:

```bash
python3 lab.py
```

On Windows, you can use:

```powershell
py lab.py
```

## Expected result
The script prints example values demonstrating the module. Some values are intentionally different on each run or machine (for example, random numbers, current date/time, paths, and platform information).

## Try it yourself
Try validating a 6-digit PIN using `re.fullmatch(r"\d{6}", pin)`. Regular expressions are pattern checks, not proof that an email address or phone number is real.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
