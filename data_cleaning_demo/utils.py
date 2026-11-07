"""
utils.py - small helpers shared by every step.

Each step saves its result to the output/ folder, and the next step loads it.
  * .pkl (pickle) keeps the exact data types (dates, booleans, integers),
    so the next step gets the data exactly as the previous one left it.
  * .csv is saved alongside so you can open it in Excel and see the change.
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "raw_data.csv"
OUT_DIR = BASE_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

# Wider printing so tables don't wrap in the terminal
pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 20)


def banner(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def read_raw() -> pd.DataFrame:
    """Read the raw CSV with every column as text.

    Why text? If pandas guesses the types, a single bad value like 'thirty'
    turns the whole age column into text anyway, and values like ' Rohan'
    or '₹45,000' get handled inconsistently. Reading as text keeps the data
    exactly as it is in the file, and we convert each column ourselves.
    """
    return pd.read_csv(RAW_FILE, dtype=str, keep_default_na=False, na_values=[""])


def save(df: pd.DataFrame, name: str) -> None:
    df.to_pickle(OUT_DIR / f"{name}.pkl")
    df.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"\n>> Saved output/{name}.csv  ({df.shape[0]} rows x {df.shape[1]} columns)")


def load(name: str) -> pd.DataFrame:
    path = OUT_DIR / f"{name}.pkl"
    if not path.exists():
        raise SystemExit(f"{path.name} not found - run the previous step first.")
    return pd.read_pickle(path)
