"""
STEP 5 - VALIDATE EMAILS AND STANDARDISE BOOLEANS
-------------------------------------------------
email     : 'user41@example' has no domain ending (.com etc.) -> invalid.
            Check with a regular expression (regex).
is_active : stored as 1/0, yes/no, Y/N or blank. Map all of these to
            True / False, and leave blank as <NA> (unknown).

Things to consider:
  * An email that passes the regex can still be wrong; the regex only
    checks the format. Keep a flag column so the rows can be followed up.
  * You can't recover a wrong email, so set it to missing. Never invent one.
  * Blank is_active means "unknown", not "False". Treating blanks as False
    would make the active-rate wrong. Use pandas' nullable 'boolean' type.
  * Any value not in the mapping (e.g. 'maybe') becomes <NA>. Print the
    unmapped values so a new spelling isn't lost unnoticed.
"""
import pandas as pd
from utils import banner, load, save

df = load("step4_dates")

EMAIL_PATTERN = r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$"
BOOL_MAP = {
    "1": True, "yes": True, "y": True, "true": True,
    "0": False, "no": False, "n": False, "false": False,
}

# ---------- email ----------
valid = df["email"].str.fullmatch(EMAIL_PATTERN, na=False)
invalid = df["email"].notna() & ~valid

banner("Invalid emails (format is wrong)")
print(df.loc[invalid, ["id", "name", "email"]].to_string(index=False))

df["email_valid"] = valid
df.loc[invalid, "email"] = pd.NA
print(f"\nInvalid -> set to missing: {invalid.sum()}   Blank in file: {(~valid).sum() - invalid.sum()}")

# ---------- is_active ----------
raw = df["is_active"].copy()
normalised = raw.str.strip().str.lower()
df["is_active"] = normalised.map(BOOL_MAP).astype("boolean")

banner("is_active: raw value -> boolean")
print(pd.crosstab(raw.fillna("<blank>"), df["is_active"].astype(str)))

unmapped = normalised.notna() & ~normalised.isin(BOOL_MAP.keys())
print("\nUnrecognised values:", list(raw[unmapped].unique()) or "none")
print("\nCounts:\n", df["is_active"].value_counts(dropna=False).to_string(), sep="")

save(df, "step5_emails_booleans")
