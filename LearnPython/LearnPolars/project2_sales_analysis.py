"""
PROJECT 02 - E-COMMERCE SALES ANALYSIS
Domain: Business / Sales Analytics | Technology: Python + Polars + CSV

Run:  python project2_sales_analysis.py
Creates: sales.csv and sales_report.csv in the current folder.
"""

# LAB 01 - IMPORT POLARS
import polars as pl


def lab(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# LAB 02 - CREATE SALES CSV FILE
lab("LAB 02 - CREATE SALES CSV FILE")
data = """Order_ID,Product,Category,City,Quantity,Price
1001,Laptop,Electronics,Delhi,2,50000
1002,Mobile,Electronics,Mumbai,3,20000
1003,Keyboard,Accessories,Delhi,5,1000
1004,Mouse,Accessories,Noida,10,500
1005,Laptop,Electronics,Noida,1,50000
1006,Mobile,Electronics,Delhi,2,20000
1007,Monitor,Electronics,Mumbai,2,15000
1008,Keyboard,Accessories,Noida,4,1000
1009,Mouse,Accessories,Delhi,6,500
1010,Monitor,Electronics,Noida,3,15000
"""

with open("sales.csv", "w") as file:
    file.write(data)

print("sales.csv created")

# LAB 03 - READ SALES CSV FILE
lab("LAB 03 - READ SALES CSV FILE")
df = pl.read_csv("sales.csv")
print(df)

# LAB 04 - CALCULATE REVENUE FOR EACH ORDER
lab("LAB 04 - CALCULATE REVENUE FOR EACH ORDER")
df = df.with_columns(
    (pl.col("Quantity") * pl.col("Price")).alias("Revenue")
)
print(df)

# LAB 05 - CALCULATE TOTAL REVENUE
lab("LAB 05 - CALCULATE TOTAL REVENUE")
print(df.select(pl.col("Revenue").sum()))

# LAB 06 - FIND PRODUCT-WISE REVENUE
lab("LAB 06 - FIND PRODUCT-WISE REVENUE")
print(
    df.group_by("Product")
    .agg(pl.col("Revenue").sum().alias("Total_Revenue"))
    .sort("Total_Revenue", descending=True)
)

# LAB 07 - CALCULATE CITY-WISE REVENUE
lab("LAB 07 - CALCULATE CITY-WISE REVENUE")
print(
    df.group_by("City")
    .agg(pl.col("Revenue").sum().alias("Total_Revenue"))
    .sort("Total_Revenue", descending=True)
)

# LAB 08 - CALCULATE CATEGORY-WISE REVENUE
lab("LAB 08 - CALCULATE CATEGORY-WISE REVENUE")
print(
    df.group_by("Category")
    .agg(pl.col("Revenue").sum().alias("Total_Revenue"))
    .sort("Total_Revenue", descending=True)
)

# LAB 09 - FIND ORDERS WITH REVENUE ABOVE 40000
lab("LAB 09 - FIND ORDERS WITH REVENUE ABOVE 40000")
print(df.filter(pl.col("Revenue") > 40000))

# LAB 10 - CALCULATE TOTAL QUANTITY SOLD
lab("LAB 10 - CALCULATE TOTAL QUANTITY SOLD")
print(df.select(pl.col("Quantity").sum()))

# LAB 11 - CALCULATE AVERAGE ORDER REVENUE
lab("LAB 11 - CALCULATE AVERAGE ORDER REVENUE")
print(df.select(pl.col("Revenue").mean()))

# LAB 12 - GENERATE FINAL SALES REPORT
lab("LAB 12 - GENERATE FINAL SALES REPORT")
sales_report = (
    df.group_by("Product")
    .agg(
        pl.col("Quantity").sum().alias("Total_Quantity"),
        pl.col("Revenue").sum().alias("Total_Revenue"),
    )
    .sort("Total_Revenue", descending=True)
)
print(sales_report)
sales_report.write_csv("sales_report.csv")
print("sales_report.csv created")

print("\nPROJECT 02 COMPLETED SUCCESSFULLY")
