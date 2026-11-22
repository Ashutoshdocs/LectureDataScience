# LAB 3 — Python `datetime` Module

## Purpose
Work with dates and times.

## What you will learn
`date.today()` returns the current date. `datetime.now()` returns the local date and time. `strftime()` formats a date/time, while `timedelta` represents a duration.

## Code

```python
from datetime import date, datetime, timedelta

today = date.today()
now = datetime.now()

print("Today's date:", today)
print("Current date and time:", now)
print("Formatted date:", now.strftime("%d-%m-%Y %H:%M"))

# Create a specific date.
joining_date = date(2024, 1, 15)
print("Joining year:", joining_date.year)
print("Joining month:", joining_date.month)

# Calculate a date 7 days from today.
next_week = today + timedelta(days=7)
print("Date after 7 days:", next_week)
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
Try adding 30 days or formatting the date as `%Y/%m/%d`. The displayed current time depends on the computer's timezone.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
