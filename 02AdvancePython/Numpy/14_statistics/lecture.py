"""Lecture 14 — Statistics: aggregates, spread, percentiles, cumsum/diff."""
import numpy as np

print("=== 1. sum, mean, min, max ===")
sales = np.array([120, 340, 90, 410, 275, 180, 305])
days = np.array(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

print("Total  :", sales.sum())
print("Mean   :", sales.mean())
print("Lowest :", sales.min())
print("Highest:", sales.max())
print("Range  :", sales.max() - sales.min(), "=", np.ptp(sales))

print("Best day index :", sales.argmax(), "->", days[sales.argmax()])
print("Worst day index:", sales.argmin(), "->", days[sales.argmin()])
print("Days above mean:", (sales > sales.mean()).sum(), days[sales > sales.mean()])

print(np.sum([10, 20, 30]))         # works on lists too

print("\n=== 2. median, std, percentile ===")
salaries = np.array([25, 28, 30, 32, 35, 38, 40, 250])  # in thousands

print("Mean  :", salaries.mean())
print("Median:", np.median(salaries))
print("Std   :", salaries.std().round(1))
print("25th, 75th percentile:", np.percentile(salaries, [25, 75]))

normal = salaries[salaries < 100]       # drop the outlier
print("Mean without outlier:", normal.mean().round(1))
print("Std  without outlier:", normal.std().round(1))
print("Sample std (ddof=1) :", normal.std(ddof=1).round(2))

more = np.append(salaries, 500)
print("With a 500 salary -> mean", more.mean().round(1), "median", np.median(more))

print("\n=== 3. cumsum, cumprod, diff ===")
daily_steps = np.array([4200, 6100, 5300, 8800, 7600])
print("Running total:", np.cumsum(daily_steps))
print("Change vs day before:", np.diff(daily_steps))
print("Days that improved:", (np.diff(daily_steps) > 0).sum())
print("Biggest jump on day index:", np.diff(daily_steps).argmax() + 1)

savings = np.full(12, 500)               # Rs 500 every month
print("Balance by month:", savings.cumsum())
print("Rs 1000 growing 10%/yr:", (1000 * np.cumprod(np.full(5, 1.1))).round(2))

print("\n=== 4. Correlation ===")
hours = np.array([1, 2, 3, 4, 5, 6])
score = np.array([52, 58, 65, 70, 78, 85])
print("hours vs score correlation:", np.corrcoef(hours, score)[0, 1].round(3))
