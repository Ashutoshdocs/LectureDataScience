"""Lecture 12: String methods with the .str accessor."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

people = pd.DataFrame({
    "name": ["  asha rao", "RAVI KUMAR", "meena  iyer ", "John D'Souza", None],
    "email": ["asha@gmail.com", "ravi@YAHOO.com", "meena@gmail.com", "john@work.org", "x@y"],
    "phone": ["98-765-43210", "9123456789", "(91) 99887 76655", "n/a", "8888"],
    "id": ["7", "12", "103", "4", "56"],
})
print(people, "\n")

print("=== Cleaning ===")
clean = (people["name"]
         .str.strip()
         .str.replace(r"\s+", " ", regex=True)
         .str.title())
print(clean.tolist())
print("upper:", people["email"].str.lower().str.upper().tolist()[:2])
print("zfill:", people["id"].str.zfill(4).tolist())

print("\n=== Testing ===")
print("gmail users :", people.loc[people["email"].str.contains("gmail"), "email"].tolist())
print("contains 'a' (any case, NaN -> False):\n",
      people["name"].str.contains("a", case=False, na=False).tolist())
print(".com emails :", people["email"].str.lower().str.endswith(".com").tolist())
print("name lengths:", clean.str.len().tolist())

print("\n=== Splitting ===")
parts = clean.str.split(" ", expand=True).set_axis(["first", "last"], axis=1)
print(parts)
print("domains:", people["email"].str.lower().str.split("@").str[1].tolist())
print("initials:", (clean.str[0] + clean.str.split(" ").str[-1].str[0]).tolist())

print("\n=== Extracting with regex ===")
digits = people["phone"].str.replace(r"\D", "", regex=True)     # keep digits only
print("digits only :", digits.tolist())
print("valid 10/12 :", digits.str.match(r"^(91)?\d{10}$").tolist())
orders = pd.Series(["Order #123 (paid)", "Order #45 (due)", "Refund #9 (paid)"])
print(orders.str.extract(r"(?P<kind>\w+) #(?P<number>\d+) \((?P<status>\w+)\)"))

print("\n=== get_dummies and cat ===")
tags = pd.Series(["tea,coffee", "coffee", "juice,tea"])
print(tags.str.get_dummies(sep=","))
print("joined:", clean.dropna().str.cat(sep=" | "))

print("\n=== On the course data ===")
sales = pd.read_csv(DATA / "sales.csv")
print("products with 'a':", sorted(sales.loc[sales["product"].str.contains("a", case=False), "product"].unique()))
print("product codes    :", sales["product"].str.upper().str[:3].unique().tolist())
