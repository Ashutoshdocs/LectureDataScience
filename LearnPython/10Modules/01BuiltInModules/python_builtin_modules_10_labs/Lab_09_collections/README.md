# LAB 9 — Python `collections` Module

## Purpose
Use specialised collection types.

## What you will learn
`Counter` counts items, `defaultdict` supplies a default value for missing keys, and `deque` is a double-ended queue that supports efficient operations at both ends.

## Code

```python
from collections import Counter, defaultdict, deque

# Counter counts repeated values.
fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
counts = Counter(fruits)
print("Fruit counts:", counts)
print("Most common:", counts.most_common(2))

# defaultdict creates a default value for a missing key.
marks = defaultdict(list)
marks["Asha"].append(90)
marks["Asha"].append(95)
marks["Ravi"].append(88)
print("Student marks:", dict(marks))

# deque supports efficient additions/removals at both ends.
tasks = deque(["task1", "task2"])
tasks.append("task3")
tasks.appendleft("urgent task")
print("Task queue:", list(tasks))
print("Next task:", tasks.popleft())
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
Try counting another list of items, grouping names by department with `defaultdict(list)`, or using `appendleft()` and `pop()` with a deque.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
