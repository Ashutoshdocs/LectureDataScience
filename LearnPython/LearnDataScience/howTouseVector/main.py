
import csv

# Prepare empty lists
months = []
sales = []

# Read data from CSV file
with open("sales_data.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        months.append(row["Month"])
        sales.append(int(row["Sales"]))


# Calculate annual sales and average sales
annual_sales = sum(sales)
average_sales = annual_sales / len(sales)

# Find highest and lowest sales
highest_sales = max(sales)
lowest_sales = min(sales)

# Find indexes of best and worst months
best_index = sales.index(highest_sales)
worst_index = sales.index(lowest_sales)

# Find corresponding month names
best_month = months[best_index]
worst_month = months[worst_index]

# Prepare result lists
above_average_months = []
projected_sales = []
sales_increase = []

# Process every month
for i in range(len(sales)):

    if sales[i] > average_sales:
        above_average_months.append(months[i])

    # Calculate hypothetical 10% increase
    projected = sales[i] * 1.10
    projected_sales.append(projected)

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
