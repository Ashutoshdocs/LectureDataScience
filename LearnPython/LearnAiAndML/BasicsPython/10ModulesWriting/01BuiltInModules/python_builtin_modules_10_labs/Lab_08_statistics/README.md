# LAB 8 — Python `statistics` Module

## Purpose
Calculate basic statistics.

## What you will learn
`statistics` calculates common descriptive statistics. Mean is the average, median is the middle value, and mode is the most frequent value.

## Code

```python
import statistics

marks = [78, 85, 90, 85, 92, 70, 85]

print("Marks:", marks)
print("Mean:", statistics.mean(marks))
print("Median:", statistics.median(marks))
print("Mode:", statistics.mode(marks))
print("Population standard deviation:", statistics.pstdev(marks))
print("Population variance:", statistics.pvariance(marks))
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
Change the marks and compare mean, median, and mode. `pstdev()` and `pvariance()` treat the data as the entire population; use `stdev()` and `variance()` for sample statistics.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
