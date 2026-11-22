"""Lecture 21: Project: cleaning a messy customer file, step by step."""
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 20)

raw = pd.read_csv(DATA / "messy_customers.csv", dtype={"Customer ID": str})
print("=== RAW ===")
print(raw)
print("\nraw columns:", raw.columns.tolist())
print(raw.dtypes)

df = raw.copy()                                     # never touch the raw data

print("\n=== 1. Column names ===")
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(r"[()]", "", regex=True)
              .str.replace(r"\s+", "_", regex=True))
df = df.rename(columns={"spend_rs": "spend"})
print(df.columns.tolist())

print("\n=== 2. Duplicates ===")
print("duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)
print("rows now:", len(df))

print("\n=== 3. Names: whitespace and case ===")
df["full_name"] = (df["full_name"].str.strip()
                   .str.replace(r"\s+", " ", regex=True)
                   .str.title())
print(df["full_name"].tolist())

print("\n=== 4. Email: lowercase, empty -> missing, validate ===")
df["email"] = df["email"].str.strip().str.lower().replace("", np.nan)
df["email_valid"] = df["email"].str.match(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", na=False)
print(df[["email", "email_valid"]])

print("\n=== 5. Age: text -> number, impossible -> missing ===")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
bad_age = ~df["age"].between(0, 120) & df["age"].notna()
print("impossible ages:", df.loc[bad_age, "age"].tolist())
df["age"] = df["age"].mask(bad_age).astype("Int64")
print(df["age"].tolist())

print("\n=== 6. City: whitespace, case, synonyms ===")
print("before:", raw["City"].unique().tolist())
df["city"] = (df["city"].str.strip().str.title()
              .replace({"Bangalore": "Bengaluru", "Bombay": "Mumbai"}))
print("after :", df["city"].unique().tolist())

print("\n=== 7. Dates in two formats ===")
s = df["signup_date"]
trap = pd.to_datetime(s, format="mixed", dayfirst=True, errors="coerce")
iso = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
dmy = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
df["signup_date"] = iso.fillna(dmy)
print(pd.DataFrame({"raw": s, "mixed+dayfirst (WRONG)": trap, "safe": df["signup_date"]}))

print("\n=== 8. Spend: '12,500' -> 12500 ===")
df["spend"] = pd.to_numeric(df["spend"].str.replace(",", ""), errors="coerce")
print(df["spend"].tolist())

print("\n=== CLEAN ===")
print(df)
print(df.dtypes)

print("\n=== Report ===")
print(f"rows: {len(raw)} -> {len(df)}")
print("missing values after cleaning:\n", df.isna().sum()[lambda x: x > 0])
review = df[~df["email_valid"] | df["age"].isna() | df["signup_date"].isna()
            | df["full_name"].isna() | df["spend"].isna()]
print(f"{len(review)} rows need human review:", review["customer_id"].tolist())

df.to_csv(OUT / "customers_clean.csv", index=False)
review.to_csv(OUT / "needs_review.csv", index=False)
print("saved output/customers_clean.csv and output/needs_review.csv")


# ---- The same steps as one reusable function ----
def clean(path):
    d = pd.read_csv(path, dtype={"Customer ID": str})
    d.columns = (d.columns.str.strip().str.lower().str.replace(r"[()]", "", regex=True)
                 .str.replace(r"\s+", "_", regex=True))
    d = d.rename(columns={"spend_rs": "spend"}).drop_duplicates().reset_index(drop=True)
    age = pd.to_numeric(d["age"], errors="coerce")
    return d.assign(
        full_name=d["full_name"].str.strip().str.replace(r"\s+", " ", regex=True).str.title(),
        email=d["email"].str.strip().str.lower().replace("", np.nan),
        age=age.where(age.between(0, 120)).astype("Int64"),
        city=d["city"].str.strip().str.title().replace({"Bangalore": "Bengaluru"}),
        signup_date=pd.to_datetime(d["signup_date"], format="%Y-%m-%d", errors="coerce")
                     .fillna(pd.to_datetime(d["signup_date"], format="%d/%m/%Y", errors="coerce")),
        spend=pd.to_numeric(d["spend"].str.replace(",", ""), errors="coerce"),
    )


print("\nclean() gives the same result?",
      clean(DATA / "messy_customers.csv").equals(df.drop(columns="email_valid")))
