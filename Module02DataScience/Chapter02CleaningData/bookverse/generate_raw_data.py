"""
Step 0 - Generate intentionally MESSY raw CSV files into data/raw/.

Real-world exports are never clean, so this script injects the kind of problems
a data scientist has to fix: duplicate rows, inconsistent genre labels,
"4 stars" style ratings, out-of-range values, mixed date formats, orphan IDs,
self-friendships, stray whitespace, missing values ...

Run:  python generate_raw_data.py
"""
import csv
import os
import random
from datetime import datetime, timedelta

random.seed(7)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")
os.makedirs(OUT, exist_ok=True)

GENRE_VARIANTS = {
    "Fantasy": ["Fantasy", "fantasy", " FANTASY ", "Fantasy "],
    "Science Fiction": ["Science Fiction", "sci-fi", "Sci Fi", "SCIFI", "science fiction"],
    "Mystery": ["Mystery", "mystery", "Mystery/Crime", " MYSTERY"],
    "Romance": ["Romance", "romance", "Romantic", "ROMANCE "],
    "Thriller": ["Thriller", "thriller", "Thrillers", "THRILLER"],
    "History": ["History", "history", "Historical", "HISTORY "],
    "Self-Help": ["Self-Help", "self help", "Self Help", "selfhelp"],
    "Biography": ["Biography", "biography", "Bio", "Memoir/Biography"],
}
WORDS = {
    "Fantasy": (["Ember", "Silver", "Hollow", "Dragon", "Moonlit", "Thorned", "Forgotten", "Crystal"],
                ["Crown", "Throne", "Forest", "Prophecy", "Blade", "Kingdom", "Spellbook", "Tower"]),
    "Science Fiction": (["Quantum", "Stellar", "Neon", "Orbital", "Silent", "Final", "Binary", "Red"],
                        ["Horizon", "Colony", "Signal", "Drift", "Protocol", "Nebula", "Machine", "Frontier"]),
    "Mystery": (["Midnight", "Locked", "Vanishing", "Crimson", "Quiet", "Last", "Hidden", "Seventh"],
                ["Key", "Room", "Witness", "Letter", "Alibi", "Garden", "Clue", "Manor"]),
    "Romance": (["Summer", "Paper", "Golden", "Second", "Endless", "Starlit", "Sweet", "Wild"],
                ["Hearts", "Promise", "Kiss", "Letters", "Season", "Vows", "Rose", "Embrace"]),
    "Thriller": (["Dead", "Burning", "Cold", "Dark", "Fatal", "Shadow", "Broken", "Black"],
                 ["Code", "Hour", "Target", "Network", "Line", "Pursuit", "Ledger", "Deal"]),
    "History": (["Ancient", "Lost", "Iron", "Imperial", "Great", "Silk", "Fallen", "Golden"],
                ["Empires", "Roads", "Age", "Dynasty", "Revolution", "Republic", "Voyages", "Kingdoms"]),
    "Self-Help": (["Tiny", "Deep", "Focused", "Calm", "Brave", "Clear", "Daily", "Mindful"],
                  ["Habits", "Work", "Mind", "Living", "Steps", "Choices", "Mornings", "Growth"]),
    "Biography": (["Unbroken", "Restless", "Remarkable", "Fearless", "Humble", "Curious", "Extraordinary", "Patient"],
                  ["Life", "Journey", "Pioneer", "Dreamer", "Voice", "Maverick", "Legacy", "Path"]),
}
FIRST = ["Aarav", "Diya", "Kabir", "Meera", "Rohan", "Ananya", "Vikram", "Isha", "Arjun", "Saanvi",
         "Neha", "Karan", "Priya", "Aditya", "Tara", "Nikhil", "Riya", "Siddharth", "Zara", "Dev",
         "Liam", "Emma", "Noah", "Olivia", "Mateo", "Sofia", "Yuki", "Leila", "Omar", "Chen"]
LAST = ["Kapoor", "Iyer", "Nair", "Rao", "Gupta", "Patel", "Joshi", "Menon", "Reddy", "Das",
        "Fernandes", "Khan", "Bose", "Kulkarni", "Singh", "Turner", "Garcia", "Tanaka", "Haddad", "Lin"]
CITIES = ["Pune", "Mumbai", "Bengaluru", "Delhi", "Hyderabad", "Chennai", "Kolkata", "Jaipur"]
GENRES = list(GENRE_VARIANTS)
END = datetime(2026, 10, 31, 22, 0, 0)


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote data/raw/{name:<18} {len(rows):>5} rows")


# ---------------------------------------------------------------- books
books, used, genre_of = [], set(), {}
bid = 1
for genre in GENRES:
    adjs, nouns = WORDS[genre]
    made = 0
    while made < 15:
        title = f"The {random.choice(adjs)} {random.choice(nouns)}"
        if title in used:
            continue
        used.add(title)
        author = f"{random.choice(FIRST)} {random.choice(LAST)}"
        year, pages = random.randint(1988, 2026), random.randint(140, 720)
        # --- inject mess ---
        g = random.choice(GENRE_VARIANTS[genre])
        t = title
        if random.random() < 0.10: t = f"  {t} "
        if random.random() < 0.06: t = t.lower()
        a = "" if random.random() < 0.05 else author
        y = str(year)
        r = random.random()
        if r < 0.08: y = "unknown"
        elif r < 0.18: y = f"{year}.0"
        p = "" if random.random() < 0.06 else str(pages)
        books.append([bid, t, a, g, y, p])
        genre_of[bid] = genre
        bid += 1; made += 1
books += [list(row) for row in random.sample(books, 8)]  # exact duplicates
random.shuffle(books)

# ---------------------------------------------------------------- users
people = [(1, "alice", "Alice Sharma", "Pune", 0), (2, "bob", "Bob Mehta", "Mumbai", 0)]
taken = {"alice", "bob"}
for uid in range(3, 61):
    fn, ln = random.choice(FIRST), random.choice(LAST)
    uname = f"{fn.lower()}{random.randint(10, 99)}"
    while uname in taken:
        uname = f"{fn.lower()}{random.randint(10, 99)}"
    taken.add(uname)
    people.append((uid, uname, f"{fn} {ln}", random.choice(CITIES), 0))
users = []
for uid, uname, full, city, _ in people:
    email = f"{uname}@example.com"
    if random.random() < 0.15: email = email.upper()
    if random.random() < 0.04: email = email.replace("@", "")       # invalid
    if random.random() < 0.12: full = full.replace(" ", "   ")       # extra spaces
    if random.random() < 0.10: uname = f" {uname} "
    if random.random() < 0.08 and uid > 2: city = ""
    users.append([uid, uname, full, city, email])
users += [list(row) for row in random.sample(users[2:], 5)]  # duplicates
users.append(["", "ghost_user", "No Id", "Pune", "ghost@example.com"])  # missing id

# --------------------------------------------- taste profiles & ratings
prefs = {1: ["Fantasy", "Science Fiction"], 2: ["Mystery", "Thriller"]}
for uid in range(3, 61):
    prefs[uid] = random.sample(GENRES, 2)
# a few "bridge" readers so Alice & Bob get interesting cross-recommendations
for uid in (5, 9, 14, 21): prefs[uid] = ["Fantasy", random.choice(["Mystery", "Thriller", "Science Fiction"])]
for uid in (6, 11, 17, 25): prefs[uid] = ["Mystery", random.choice(["Thriller", "Fantasy", "History"])]

books_by_genre = {g: [b for b, gg in genre_of.items() if gg == g] for g in GENRES}
all_ids = list(genre_of)


def fmt_rating(v):
    r = random.random()
    if r < 0.06: return f"{v} stars"
    if r < 0.10: return f"{v}/5"
    if r < 0.13: return ""
    if r < 0.15: return random.choice(["0", "9", "-1"])
    return str(v)


def fmt_time(dt):
    r = random.random()
    if r < 0.10: return dt.strftime("%d/%m/%Y")
    if r < 0.20: return str(int(dt.timestamp()))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


ratings = []
for uid in range(1, 61):
    fav_pool = books_by_genre[prefs[uid][0]] + books_by_genre[prefs[uid][1]]
    n = random.randint(9, 15) if uid <= 2 else random.randint(12, 28)
    chosen = set(random.sample(fav_pool, min(len(fav_pool), int(n * 0.75))))
    while len(chosen) < n:
        chosen.add(random.choice(all_ids))
    for b in chosen:
        fav = genre_of[b] in prefs[uid]
        v = random.choice([5, 5, 4, 4, 3]) if fav else random.choice([1, 2, 2, 3, 4])
        dt = END - timedelta(days=random.randint(0, 365), minutes=random.randint(0, 1440))
        ratings.append([uid, b, fmt_rating(v), fmt_time(dt)])
# re-ratings (same user/book, later time) -> keep latest
for row in random.sample(ratings, 25):
    ratings.append([row[0], row[1], str(random.randint(3, 5)), (END - timedelta(days=random.randint(0, 5))).strftime("%Y-%m-%d %H:%M:%S")])
# orphans
for _ in range(6):
    ratings.append([random.choice([777, 3, 4]), 999, "4", END.strftime("%Y-%m-%d %H:%M:%S")])
random.shuffle(ratings)

# ---------------------------------------------------------------- friends
friends = {(1, 2)}
for uid in range(1, 61):
    for _ in range(random.randint(2, 5)):
        if random.random() < 0.6:  # homophily: similar readers befriend each other
            pool = [u for u in range(1, 61) if set(prefs[u]) & set(prefs[uid]) and u != uid]
        else:
            pool = [u for u in range(1, 61) if u != uid]
        other = random.choice(pool)
        if {uid, other} == {1, 2}: continue
        if uid in (1, 2) and len([p for p in friends if uid in p]) > 4: continue
        friends.add((uid, other))
friends = [list(p) for p in friends]
friends += [[b, a] for a, b in random.sample(friends, 10)]      # reversed duplicates
friends += [[u, u] for u in random.sample(range(1, 61), 5)]     # self loops
friends += [[3, 555]]                                           # orphan

print("Generating messy raw data ...")
write("books_raw.csv", ["book_id", "title", "author", "genre", "year", "pages"], books)
write("users_raw.csv", ["user_id", "username", "full_name", "city", "email"], users)
write("ratings_raw.csv", ["user_id", "book_id", "rating", "timestamp"], ratings)
write("friends_raw.csv", ["user_a", "user_b"], friends)
print("Done. Next: python data_pipeline.py")
