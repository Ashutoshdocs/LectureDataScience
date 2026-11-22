"""Regenerate the course datasets (already included — run only if you deleted them).

Usage:  python make_data.py
"""
import pathlib
import numpy as np
import pandas as pd

here = pathlib.Path(__file__).parent
rng = np.random.default_rng(2026)

# ---------- sales.csv : 240 orders across 2025 ----------
products = pd.DataFrame({
    "product":  ["Laptop", "Phone", "Tablet", "Headphones", "Charger", "Desk", "Chair", "Lamp"],
    "category": ["Electronics"] * 5 + ["Furniture"] * 3,
    "price":    [55000, 25000, 18000, 3500, 900, 12000, 7500, 1500],
})
n = 240
idx = rng.choice(len(products), size=n, p=[.10, .18, .10, .17, .20, .07, .08, .10])
dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
sales = pd.DataFrame({
    "order_id": np.arange(1001, 1001 + n),
    "date": dates,
    "region": rng.choice(["North", "South", "East", "West"], size=n, p=[.3, .25, .25, .2]),
    "product": products["product"].to_numpy()[idx],
    "category": products["category"].to_numpy()[idx],
    "units": rng.integers(1, 6, n),
    "unit_price": products["price"].to_numpy()[idx],
    "customer_id": rng.integers(1, 41, n),
}).sort_values("date").reset_index(drop=True)
sales["date"] = sales["date"].dt.strftime("%Y-%m-%d")
sales.to_csv(here / "sales.csv", index=False)

# ---------- customers.csv : 40 customers (ids 1-40, plus one with no orders) ----------
first = ["Asha", "Ravi", "Meena", "John", "Zara", "Ali", "Priya", "Karan", "Neha", "Omar",
         "Sara", "Vikram", "Lena", "Arjun", "Fatima", "Rohan", "Isha", "David", "Anita", "Sam"]
cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru", "Pune"]
customers = pd.DataFrame({
    "customer_id": np.arange(1, 42),
    "name": [f"{first[i % 20]} {chr(65 + i // 20)}." for i in range(41)],
    "city": rng.choice(cities, 41),
    "joined": (pd.Timestamp("2022-01-01")
               + pd.to_timedelta(rng.integers(0, 1000, 41), unit="D")).strftime("%Y-%m-%d"),
    "segment": rng.choice(["Retail", "Business"], 41, p=[.7, .3]),
})
customers.to_csv(here / "customers.csv", index=False)

# ---------- students.csv : 12 students, 4 subjects, a few gaps ----------
students = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Zara", "Ali", "Priya", "Karan", "Neha", "Omar", "Sara", "Vikram"],
    "class": ["10A", "10A", "10B", "10B", "10A", "10B", "10A", "10B", "10A", "10B", "10A", "10B"],
    "gender": ["F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M"],
    "maths":   [78, 92, 45, 83, 67, 71, 88, 59, 95, np.nan, 73, 64],
    "science": [85, 88, 52, 64, 73, 80, 91, np.nan, 89, 58, 77, 70],
    "english": [62, 79, 68, 90, 58, 66, 84, 72, 91, 61, np.nan, 75],
    "cs":      [90, 95, 40, 77, 81, 85, 93, 66, 97, 55, 79, 68],
})
students.to_csv(here / "students.csv", index=False)

# ---------- messy_customers.csv : deliberately dirty data for lecture 21 ----------
messy = pd.DataFrame({
    "Customer ID": ["001", "002", "003", "003", "004", "005", "006", "007", "008", "009"],
    " Full Name ": ["  asha rao", "RAVI KUMAR", "Meena Iyer ", "Meena Iyer ", "john d'souza",
                    "Zara Khan", None, "ali  hasan", "Priya Nair", "karan mehta"],
    "Email": ["asha@mail.com", "ravi@MAIL.com", "meena@mail.com", "meena@mail.com", "john@mail",
              "zara@mail.com", "unknown@mail.com", "ali@mail.com", "", "karan@mail.com"],
    "Age": ["34", "29", "41", "41", "-5", "27", "38", "n/a", "31", "250"],
    "City": ["delhi", "Mumbai ", "chennai", "chennai", "Delhi", "MUMBAI", "Pune", "pune", "Bengaluru", "bangalore"],
    "Signup Date": ["2024-01-15", "15/02/2024", "2024-03-01", "2024-03-01", "2024-04-10",
                    "2024-05-22", "2024-06-30", "not known", "2024-08-05", "2024-09-12"],
    "Spend (Rs)": ["12,500", "8,200", "15,000", "15,000", "3,400", "22,100", "", "9,900", "11,000", "7,750"],
})
messy.to_csv(here / "messy_customers.csv", index=False)

print("Wrote:", ", ".join(p.name for p in sorted(here.glob("*.csv"))))
