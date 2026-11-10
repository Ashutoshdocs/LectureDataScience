"""
Polars Industry Projects - Answers to the Practice Exercises.

Run the two project scripts first (they create employees.csv and sales.csv):
    python project1_employee_analysis.py
    python project2_sales_analysis.py
Then run:
    python answers.py
"""
import polars as pl


def q(title):
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)


emp = pl.read_csv("employees.csv")
sales = pl.read_csv("sales.csv").with_columns(
    (pl.col("Quantity") * pl.col("Price")).alias("Revenue")
)

print("=" * 60)
print("PROJECT 01 - EMPLOYEE EXERCISES")
print("=" * 60)

q("E1. Show all employees of the HR department")
print(emp.filter(pl.col("Department") == "HR"))

q("E2. Show only the Name and Salary columns")
print(emp.select("Name", "Salary"))

q("E3. Find the youngest employee")
print(emp.sort("Age").head(1))

q("E4. Find employees with salary between 45000 and 60000 (inclusive)")
print(emp.filter(pl.col("Salary").is_between(45000, 60000)))

q("E5. Find IT employees earning more than 60000")
print(emp.filter((pl.col("Department") == "IT") & (pl.col("Salary") > 60000)))

q("E6. Add a Bonus column equal to 10% of Salary")
print(emp.with_columns((pl.col("Salary") * 0.10).alias("Bonus")))

q("E7. Find the maximum experience in each department")
print(
    emp.group_by("Department")
    .agg(pl.col("Experience").max().alias("Max_Experience"))
    .sort("Department")
)

print("\n" + "=" * 60)
print("PROJECT 02 - SALES EXERCISES")
print("=" * 60)

q("S1. Show all orders from Delhi")
print(sales.filter(pl.col("City") == "Delhi"))

q("S2. Count the number of orders in each city")
print(
    sales.group_by("City")
    .agg(pl.len().alias("Total_Orders"))
    .sort("City")
)

q("S3. Find the best-selling product by quantity")
print(
    sales.group_by("Product")
    .agg(pl.col("Quantity").sum().alias("Total_Quantity"))
    .sort("Total_Quantity", descending=True)
    .head(1)
)

q("S4. Find Electronics orders with Quantity of 2 or more")
print(
    sales.filter(
        (pl.col("Category") == "Electronics") & (pl.col("Quantity") >= 2)
    )
)

q("S5. Add a GST column (18% of Revenue) and a Final_Amount column")
print(
    sales.with_columns(
        (pl.col("Revenue") * 0.18).alias("GST")
    ).with_columns(
        (pl.col("Revenue") + pl.col("GST")).alias("Final_Amount")
    ).select("Order_ID", "Product", "Revenue", "GST", "Final_Amount")
)

q("S6. Find the minimum, maximum and average Revenue")
print(
    sales.select(
        pl.col("Revenue").min().alias("Min_Revenue"),
        pl.col("Revenue").max().alias("Max_Revenue"),
        pl.col("Revenue").mean().alias("Avg_Revenue"),
    )
)

q("S7. City-wise report (orders, quantity, revenue) saved to city_report.csv")
city_report = (
    sales.group_by("City")
    .agg(
        pl.len().alias("Total_Orders"),
        pl.col("Quantity").sum().alias("Total_Quantity"),
        pl.col("Revenue").sum().alias("Total_Revenue"),
    )
    .sort("Total_Revenue", descending=True)
)
print(city_report)
city_report.write_csv("city_report.csv")
print("city_report.csv created")
