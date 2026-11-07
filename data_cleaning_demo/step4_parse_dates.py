"""
STEP 4 - PARSE DATES (join_date)
--------------------------------
The file uses four date formats:
  2023-01-15     -> %Y-%m-%d   (ISO, the best one)
  15/02/2023     -> %d/%m/%Y   (day first, Indian/European style)
  2023.03.20     -> %Y.%m.%d
  March 5 2023   -> %B %d %Y

How: try each known format in turn and keep the first one that works.
This is safer than letting pandas guess.

Things to consider:
  * AMBIGUITY: '03/04/2023' could be 3 April or 4 March. Find out from the
    data owner whether dates are day-first; never assume.
  * List the formats explicitly. If a value matches none of them, it shows
    up as unparsed so you can fix it, instead of being silently misread.
  * Check the result: no dates in the future and none implausibly old.
  * Store dates as datetime64, not text, so you can sort, filter and do
    date arithmetic on them.
"""
import pandas as pd
from utils import banner, load, save

df = load("step3_numbers")

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%Y.%m.%d", "%B %d %Y"]


def parse_date(value):
    if pd.isna(value):
        return pd.NaT
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(value.strip(), format=fmt)
        except ValueError:
            continue
    return pd.NaT  # matched no known format


raw = df["join_date"].copy()
df["join_date"] = pd.to_datetime(raw.apply(parse_date))

banner("Before -> after (one example of each format)")
examples = pd.DataFrame({"raw": raw, "parsed": df["join_date"]}).drop_duplicates("raw")
print(examples.to_string(index=False))

banner("Checks")
unparsed = raw.notna() & df["join_date"].isna()
print("Values that matched no format :", unparsed.sum(), list(raw[unparsed].unique()))
print("Blank in the original file    :", raw.isna().sum())
print("Future dates                  :", (df["join_date"] > pd.Timestamp.today()).sum())
print("Date range                    :", df["join_date"].min().date(), "to", df["join_date"].max().date())
print("Type                          :", df["join_date"].dtype)

save(df, "step4_dates")
