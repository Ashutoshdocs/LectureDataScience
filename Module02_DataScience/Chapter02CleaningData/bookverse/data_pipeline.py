"""
Step 1 - Data science pipeline: CLEAN -> STRUCTURE -> LOAD into SQL.

Reads the messy CSVs in data/raw/, cleans them with pandas, writes a
cleaning report (data/cleaning_report.json, shown in the app's
"Data Insights" tab) and loads the clean tables into MySQL / SQLite.

Run:  python data_pipeline.py
"""
import json
import os
import re
from datetime import datetime

import numpy as np
import pandas as pd
from werkzeug.security import generate_password_hash

from db import BASE_DIR, DEMO_USERS, books, engine, friendships, metadata, ratings, users

RAW = os.path.join(BASE_DIR, "data", "raw")
REPORT_PATH = os.path.join(BASE_DIR, "data", "cleaning_report.json")

GENRE_MAP = {
    "fantasy": "Fantasy",
    "sciencefiction": "Science Fiction", "scifi": "Science Fiction",
    "mystery": "Mystery", "mysterycrime": "Mystery",
    "romance": "Romance", "romantic": "Romance",
    "thriller": "Thriller", "thrillers": "Thriller",
    "history": "History", "historical": "History",
    "selfhelp": "Self-Help",
    "biography": "Biography", "bio": "Biography", "memoirbiography": "Biography",
}
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")


class Report:
    """Collects what every cleaning step did, for transparency."""

    def __init__(self, table, df):
        self.table, self.rows_in, self.steps = table, len(df), []

    def add(self, step, affected):
        self.steps.append({"step": step, "affected": int(affected)})
        print(f"    - {step:<55} {int(affected):>5}")

    def done(self, df):
        return {"table": self.table, "rows_in": self.rows_in, "rows_out": len(df), "steps": self.steps}


def read_raw(name):
    return pd.read_csv(os.path.join(RAW, name), dtype=str, keep_default_na=False)


def strip_all(df, rep):
    before = df.copy()
    df = df.apply(lambda s: s.str.strip())
    rep.add("Trimmed leading/trailing whitespace (cells)", (before != df).sum().sum())
    return df


# ------------------------------------------------------------------ books
def clean_books():
    df = read_raw("books_raw.csv")
    rep = Report("books", df)
    df = strip_all(df, rep)

    n = len(df); df = df.drop_duplicates(); rep.add("Removed exact duplicate rows", n - len(df))
    n = len(df); df = df.drop_duplicates("book_id"); rep.add("Removed duplicate book_id", n - len(df))

    key = df["genre"].str.lower().str.replace(r"[^a-z]", "", regex=True)
    canon = key.map(GENRE_MAP)
    rep.add("Standardised genre labels (e.g. 'sci-fi' -> 'Science Fiction')", (canon != df["genre"]).sum())
    df["genre"] = canon
    n = len(df); df = df[df["genre"].notna()]; rep.add("Dropped rows with unknown genre", n - len(df))

    low = df["title"].str.islower()
    df.loc[low, "title"] = df.loc[low, "title"].str.title().str.replace(r"\bThe\b", "The", regex=True)
    rep.add("Fixed lowercase titles -> Title Case", low.sum())

    miss = df["author"] == ""
    df.loc[miss, "author"] = "Unknown Author"
    rep.add("Filled missing authors with 'Unknown Author'", miss.sum())

    year = pd.to_numeric(df["year"], errors="coerce")
    rep.add("Converted year to integer ('2015.0' -> 2015)", df["year"].str.contains(r"\.", regex=True).sum())
    rep.add("Invalid years set to NULL ('unknown')", year.isna().sum())
    df["year"] = year.round().astype("Int64")

    pages = pd.to_numeric(df["pages"], errors="coerce")
    rep.add("Imputed missing page counts with genre median", pages.isna().sum())
    df["pages"] = pages.fillna(pages.groupby(df["genre"]).transform("median")).round().astype("Int64")

    df["book_id"] = df["book_id"].astype(int)
    return df.sort_values("book_id"), rep.done(df)


# ------------------------------------------------------------------ users
def clean_users():
    df = read_raw("users_raw.csv")
    rep = Report("users", df)
    df = strip_all(df, rep)

    n = len(df); df = df[df["user_id"] != ""]; rep.add("Dropped rows with missing user_id", n - len(df))
    n = len(df); df = df.drop_duplicates("user_id"); rep.add("Removed duplicate users", n - len(df))

    collapsed = df["full_name"].str.replace(r"\s+", " ", regex=True)
    rep.add("Collapsed repeated spaces in names", (collapsed != df["full_name"]).sum())
    df["full_name"] = collapsed
    df["username"] = df["username"].str.lower()
    dup = df["username"].duplicated(keep="first")
    df.loc[dup, "username"] = df.loc[dup, "username"] + "_" + df.loc[dup, "user_id"]
    rep.add("Made duplicate usernames unique", dup.sum())

    lower = df["email"].str.lower()
    rep.add("Lower-cased emails", (lower != df["email"]).sum())
    valid = lower.str.match(EMAIL_RE)
    rep.add("Invalid emails set to NULL", (~valid).sum())
    df["email"] = lower.where(valid, None)

    miss = df["city"] == ""
    df.loc[miss, "city"] = "Unknown"
    rep.add("Filled missing city with 'Unknown'", miss.sum())

    df["user_id"] = df["user_id"].astype(int)
    return df.sort_values("user_id"), rep.done(df)


# ---------------------------------------------------------------- ratings
def parse_ts(v):
    v = str(v).strip()
    if v.isdigit():
        return datetime.fromtimestamp(int(v))
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return pd.NaT


def clean_ratings(valid_users, valid_books):
    df = read_raw("ratings_raw.csv")
    rep = Report("ratings", df)
    df = strip_all(df, rep)

    numeric = df["rating"].str.fullmatch(r"-?\d+(\.\d+)?")
    rep.add("Parsed text ratings ('4 stars', '5/5' -> number)", ((~numeric) & (df["rating"] != "")).sum())
    df["rating"] = pd.to_numeric(df["rating"].str.extract(r"(-?\d+(?:\.\d+)?)")[0], errors="coerce")

    n = len(df); df = df[df["rating"].notna()]; rep.add("Dropped empty ratings", n - len(df))
    n = len(df); df = df[df["rating"].between(1, 5)]; rep.add("Dropped out-of-range ratings (not 1-5)", n - len(df))

    std = df["timestamp"].str.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    rep.add("Unified mixed timestamp formats (epoch, dd/mm/yyyy)", (~std).sum())
    df["rated_at"] = df["timestamp"].map(parse_ts)
    n = len(df); df = df[df["rated_at"].notna()]; rep.add("Dropped unparseable timestamps", n - len(df))

    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
    df["book_id"] = pd.to_numeric(df["book_id"], errors="coerce")
    n = len(df)
    df = df[df["user_id"].isin(valid_users) & df["book_id"].isin(valid_books)]
    rep.add("Dropped orphan ratings (unknown user/book)", n - len(df))

    n = len(df)
    df = df.sort_values("rated_at").drop_duplicates(["user_id", "book_id"], keep="last")
    rep.add("De-duplicated re-ratings (kept the latest)", n - len(df))

    df = df.astype({"user_id": int, "book_id": int})
    return df[["user_id", "book_id", "rating", "rated_at"]], rep.done(df)


# ---------------------------------------------------------------- friends
def clean_friends(valid_users):
    df = read_raw("friends_raw.csv").apply(lambda s: pd.to_numeric(s.str.strip(), errors="coerce"))
    rep = Report("friendships", df)
    n = len(df); df = df.dropna().astype(int); rep.add("Dropped malformed rows", n - len(df))
    n = len(df); df = df[df["user_a"] != df["user_b"]]; rep.add("Removed self-friendships", n - len(df))
    a, b = np.minimum(df["user_a"], df["user_b"]), np.maximum(df["user_a"], df["user_b"])
    df = pd.DataFrame({"user_a": a, "user_b": b})
    n = len(df); df = df.drop_duplicates(); rep.add("Removed reversed/duplicate pairs (A-B = B-A)", n - len(df))
    n = len(df)
    df = df[df["user_a"].isin(valid_users) & df["user_b"].isin(valid_users)]
    rep.add("Dropped orphan friendships", n - len(df))
    return df, rep.done(df)


# ------------------------------------------------------------------- load
def to_records(df):
    """pandas/numpy types -> plain Python types (PyMySQL can't send numpy ints)."""
    out = []
    for rec in df.to_dict("records"):
        clean = {}
        for k, v in rec.items():
            if v is None or (not isinstance(v, str) and pd.isna(v)):
                v = None
            elif isinstance(v, np.integer):
                v = int(v)
            elif isinstance(v, np.floating):
                v = float(v)
            elif isinstance(v, pd.Timestamp):
                v = v.to_pydatetime()
            clean[k] = v
        out.append(clean)
    return out


def insert_chunks(conn, table, records, size=500):
    for i in range(0, len(records), size):
        conn.execute(table.insert(), records[i:i + size])


def main():
    print("== BookVerse data pipeline ==")
    print("  Cleaning books ...");    b, rb = clean_books()
    print("  Cleaning users ...");    u, ru = clean_users()
    print("  Cleaning ratings ...");  r, rr = clean_ratings(set(u["user_id"]), set(b["book_id"]))
    print("  Cleaning friendships ..."); f, rf = clean_friends(set(u["user_id"]))

    u["password_hash"] = u["username"].map(
        lambda name: generate_password_hash(DEMO_USERS[name]) if name in DEMO_USERS else None)

    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tables": [rb, ru, rr, rf],
        "summary": {
            "books": len(b), "users": len(u), "ratings": len(r), "friendships": len(f),
            "genres": sorted(b["genre"].unique().tolist()),
            "avg_rating": round(float(r["rating"].mean()), 2),
            "sparsity_pct": round(100 * (1 - len(r) / (len(u) * len(b))), 1),
        },
    }
    with open(REPORT_PATH, "w") as fh:
        json.dump(report, fh, indent=2)

    print(f"  Loading into database: {engine.url.render_as_string(hide_password=True)}")
    metadata.drop_all(engine)
    metadata.create_all(engine)
    with engine.begin() as conn:
        insert_chunks(conn, users, to_records(u[["user_id", "username", "full_name", "city", "email", "password_hash"]]))
        insert_chunks(conn, books, to_records(b[["book_id", "title", "author", "genre", "year", "pages"]]))
        insert_chunks(conn, ratings, to_records(r))
        insert_chunks(conn, friendships, to_records(f))
    s = report["summary"]
    print(f"  Loaded {s['users']} users, {s['books']} books, {s['ratings']} ratings, {s['friendships']} friendships")
    print(f"  Matrix sparsity: {s['sparsity_pct']}%  |  report -> data/cleaning_report.json")
    print("Done. Start the app: python app.py")


if __name__ == "__main__":
    main()
