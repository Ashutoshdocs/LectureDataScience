"""
PROJECT 01 - EMPLOYEE DATA ANALYSIS SYSTEM
Domain: HR Analytics | Technology: Python + Polars + CSV

Run:  python project1_employee_analysis.py
Creates: employees.csv and employee_report.csv in the current folder.
"""

# LAB 01 - IMPORT POLARS
import polars as pl


def lab(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# LAB 02 - CREATE EMPLOYEE CSV FILE
lab("LAB 02 - CREATE EMPLOYEE CSV FILE")
data = """Employee_ID,Name,Department,Salary,Age,Experience
101,Rahul,IT,50000,25,2
102,Amit,HR,40000,30,5
103,Priya,IT,65000,28,4
104,Neha,Finance,45000,27,3
105,Rohit,IT,75000,32,7
106,Simran,HR,55000,29,6
107,Vikas,Finance,60000,35,10
108,Pooja,IT,80000,31,8
109,Ankit,Sales,35000,24,1
110,Anjali,Sales,50000,28,4
"""

with open("employees.csv", "w") as file:
    file.write(data)

print("employees.csv created")

# LAB 03 - READ EMPLOYEE CSV FILE
lab("LAB 03 - READ EMPLOYEE CSV FILE")
df = pl.read_csv("employees.csv")
print(df)

# LAB 04 - COUNT TOTAL EMPLOYEES
lab("LAB 04 - COUNT TOTAL EMPLOYEES")
print(df.height)

# LAB 05 - FILTER SALARY GREATER THAN 50000
lab("LAB 05 - FILTER SALARY GREATER THAN 50000")
print(df.filter(pl.col("Salary") > 50000))

# LAB 06 - FIND IT DEPARTMENT EMPLOYEES
lab("LAB 06 - FIND IT DEPARTMENT EMPLOYEES")
print(df.filter(pl.col("Department") == "IT"))

# LAB 07 - CALCULATE AVERAGE SALARY
lab("LAB 07 - CALCULATE AVERAGE SALARY")
print(df.select(pl.col("Salary").mean()))
print(df["Salary"].mean())

# LAB 08 - DEPARTMENT-WISE TOTAL SALARY
lab("LAB 08 - DEPARTMENT-WISE TOTAL SALARY")
print(
    df.group_by("Department")
    .agg(pl.col("Salary").sum().alias("Total_Salary"))
    .sort("Department")
)

# LAB 09 - FIND HIGHEST-PAID EMPLOYEE
lab("LAB 09 - FIND HIGHEST-PAID EMPLOYEE")
print(df.sort("Salary", descending=True).head(1))

# LAB 10 - FIND EXPERIENCED EMPLOYEES
lab("LAB 10 - FIND EXPERIENCED EMPLOYEES (Experience > 5)")
print(df.filter(pl.col("Experience") > 5))

# LAB 11 - DEPARTMENT-WISE EMPLOYEE COUNT
lab("LAB 11 - DEPARTMENT-WISE EMPLOYEE COUNT")
print(
    df.group_by("Department")
    .agg(pl.len().alias("Total_Employees"))
    .sort("Department")
)

# LAB 12 - GENERATE FINAL HR REPORT
lab("LAB 12 - GENERATE FINAL HR REPORT")
report = (
    df.group_by("Department")
    .agg(
        pl.col("Salary").mean().alias("Average_Salary"),
        pl.col("Salary").sum().alias("Total_Salary"),
        pl.len().alias("Total_Employees"),
    )
    .sort("Department")
)
print(report)
report.write_csv("employee_report.csv")
print("employee_report.csv created")

print("\nPROJECT 01 COMPLETED SUCCESSFULLY")
