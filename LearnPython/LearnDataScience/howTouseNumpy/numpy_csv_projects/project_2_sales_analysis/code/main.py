import csv
from pathlib import Path
import numpy as np

# Locate the CSV file in this project's data folder.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sales.csv"

products = []
sales_rows = []

# Read product names and monthly unit sales from CSV.
with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    month_names = reader.fieldnames[1:]

    for row in reader:
        products.append(row["Product"])
        sales_rows.append([int(row[month]) for month in month_names])

products = np.array(products)
months = np.array(month_names)
sales = np.array(sales_rows)

print("Products:")
print(products)
print("\nMonths:")
print(months)
print("\nSales data (units):")
print(sales)

# Total sales for each product and each month.
product_totals = np.sum(sales, axis=1)
monthly_totals = np.sum(sales, axis=0)

print("\nProduct totals:")
for product, total in zip(products, product_totals):
    print(product, ":", total)

print("\nMonthly totals:")
for month, total in zip(months, monthly_totals):
    print(month, ":", total)

# Best-selling product and best/lowest-performing months.
best_product_index = np.argmax(product_totals)
best_month_index = np.argmax(monthly_totals)
lowest_month_index = np.argmin(monthly_totals)

print("\nBest-selling product:", products[best_product_index])
print("Units sold:", product_totals[best_product_index])
print("Best month:", months[best_month_index], monthly_totals[best_month_index])
print("Lowest month:", months[lowest_month_index], monthly_totals[lowest_month_index])

# Average monthly sales for each product.
product_averages = np.mean(sales, axis=1)
print("\nAverage monthly sales per product:")
for product, average in zip(products, product_averages):
    print(product, ":", round(average, 2))

# Find product-month combinations with more than 150 units sold.
high_sales_mask = sales > 150
print("\nValues above 150 units:")
print(sales[high_sales_mask])

row_indices, column_indices = np.where(sales > 150)
for row, column in zip(row_indices, column_indices):
    print(products[row], months[column], sales[row, column])

# Month-over-month unit change and percentage change.
monthly_change = np.diff(sales, axis=1)
print("\nMonth-over-month unit change:")
print(monthly_change)

previous_month = sales[:, :-1]
current_month = sales[:, 1:]

percentage_change = np.divide(
    (current_month - previous_month) * 100,
    previous_month,
    out=np.full(current_month.shape, np.nan, dtype=float),
    where=previous_month != 0
)
print("\nPercentage change:")
print(np.round(percentage_change, 2))

# Product contribution to all units sold.
grand_total = np.sum(sales)
product_contribution = (product_totals / grand_total) * 100

print("\nProduct contribution:")
for product, contribution in zip(products, product_contribution):
    print(product, ":", round(contribution, 2), "%")

# Monthly target analysis.
monthly_target = 500
target_met = monthly_totals >= monthly_target

print("\nMonthly target analysis:")
for month, total, achieved in zip(months, monthly_totals, target_met):
    print(month, "Sales:", total, "Target:", "Met" if achieved else "Not Met")

print("\n========== MONTHLY SALES REPORT ==========")
print("Grand total units sold:", grand_total)
print("Monthly target:", monthly_target)
print("Months meeting target:", np.count_nonzero(target_met))
