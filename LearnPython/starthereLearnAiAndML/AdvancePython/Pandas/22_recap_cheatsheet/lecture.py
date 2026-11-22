"""Lecture 22: Recap. A self-test touching every major topic.

Read each question, PREDICT the answer, then run the file and compare.
"""
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 140)

sales = pd.read_csv(DATA / "sales.csv", parse_dates=["date"])
customers = pd.read_csv(DATA / "customers.csv")
students = pd.read_csv(DATA / "students.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]

questions = [
    ("Lecture 05 | How many rows and columns does sales have?",
     lambda: sales.shape),
    ("Lecture 05 | Most common product?",
     lambda: sales["product"].value_counts().idxmax()),
    ("Lecture 06 | Ravi's cs mark, using loc?",
     lambda: students.set_index("name").loc["Ravi", "cs"]),
    ("Lecture 07 | Orders from the North with 5 units?",
     lambda: len(sales[(sales["region"] == "North") & (sales["units"] == 5)])),
    ("Lecture 08 | Share of orders that are 'bulk' (units >= 4)?",
     lambda: round(np.where(sales["units"] >= 4, 1, 0).mean(), 3)),
    ("Lecture 09 | Top 3 students by cs?",
     lambda: students.nlargest(3, "cs")["name"].tolist()),
    ("Lecture 10 | Students with no missing marks?",
     lambda: len(students.dropna())),
    ("Lecture 12 | Products whose name ends in 'er'?",
     lambda: sorted(sales.loc[sales["product"].str.endswith("er"), "product"].unique().tolist())),
    ("Lecture 13 | Revenue by category (Rs lakh)?",
     lambda: (sales.groupby("category")["revenue"].sum() / 1e5).round(1).to_dict()),
    ("Lecture 14 | Orders per region x category?",
     lambda: pd.crosstab(sales["region"], sales["category"])),
    ("Lecture 15 | Revenue by customer segment (Rs lakh)?",
     lambda: (sales.merge(customers, on="customer_id").groupby("segment")["revenue"].sum() / 1e5)
             .round(1).to_dict()),
    ("Lecture 16 | Average mark per subject (long format)?",
     lambda: students.melt(id_vars=["name", "class", "gender"], var_name="subject", value_name="mark")
             .groupby("subject")["mark"].mean().round(1).to_dict()),
    ("Lecture 17 | Best quarter by revenue?",
     lambda: str(sales.set_index("date")["revenue"].resample("QE").sum().idxmax().to_period("Q"))),
    ("Lecture 17 | Orders placed on a Sunday?",
     lambda: (sales["date"].dt.day_name() == "Sunday").sum()),
]

for i, (q, answer) in enumerate(questions, start=1):
    print(f"\nQ{i:02}. {q}")
    print(answer())

print("\nIf every answer matched your prediction, you're ready for real data. Well done!")
