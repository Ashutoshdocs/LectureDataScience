# 🇵🇦 Panama Tech Academy — Reading Files, Step by Step

Learn to **read and write files in Python** by turning messy raw data into clean JSON and answers, one small step at a time.
**Every step reads a file, does one thing, and writes a new output file.**

Pure Python, standard library only.

---

## 📁 Start With These Files

| File | What it is |
|---|---|
| `raw_data.txt` | Messy Instagram profile data (the only data file you need) |
| `step0_reading_files.ipynb` … `step6_answers.ipynb` | One notebook per step |
| `README.md` | This guide |

The `outputs/` folder is **created for you** when you run step 0. Every other file lands there.

---

## 🔁 The Flow

```
raw_data.txt
   │ step 0  read & write basics      ─▶ outputs/step0_report.txt
   │ step 1  strip spaces & tabs      ─▶ outputs/step1_stripped.txt
   │ step 2  remove Follow/Message    ─▶ outputs/step2_no_junk.txt
   │ step 3  POSTS → posts            ─▶ outputs/step3_fixed_words.txt
   │ step 4  group + remove dupes     ─▶ outputs/step4_cleaned.txt
   │ step 5  convert to JSON          ─▶ outputs/step5_clean_data.json
   │ step 6  answer questions         ─▶ outputs/step6_answers.txt
```

Each step reads the **previous step's output**, so run them **in order**.

---

## 🚀 Steps

**Setup (once)**
```bash
pip install notebook
cd panama-tech-academy-steps
jupyter notebook
```
Open each notebook and run all cells (**Kernel → Restart & Run All**).

### Step 0 — Reading & writing files
`open()` and `close()` · `with open(...)` · `read()` · `readline()` · `readlines()` · looping over a file · write mode `"w"` vs append mode `"a"` · creating a folder with `os.makedirs`
**Output:** `step0_report.txt` — 3,277 characters, 250 lines, 35 blank lines

### Step 1 — Remove extra spaces & tabs
`split("\n")` · `strip()` · list comprehension · `"\n".join()`
**Output:** `step1_stripped.txt`

### Step 2 — Remove junk lines
Filter out the `Follow` / `Message` button text that was copied by mistake (6 lines).
**Output:** `step2_no_junk.txt`

### Step 3 — Fix count words
`POSTS` / `Posts` → `posts` using `rsplit(" ", 1)` and `lower()`, without breaking `18.6K`.
**Output:** `step3_fixed_words.txt`

### Step 4 — Group into profiles & remove duplicates
Blank line = new profile · track usernames with a `set` · 27 profiles → **25 unique**
**Output:** `step4_cleaned.txt`

### Step 5 — Organize into JSON
Convert `2,300` / `18.6K` / `1.2M` to numbers · build a dictionary per profile · `json.dump`
**Output:** `step5_clean_data.json`
```json
{
    "username": "pty_dev_daily",
    "posts": 1240,
    "followers": 18600,
    "following": 210,
    "name": "PTY Dev Daily",
    "category": "Media",
    "bio": "💻 Daily dev news from Panama\npanamadevdaily.pa"
}
```

### Step 6 — Answer the questions
`json.load` · `max(..., key=...)` · counting with a dictionary
**Output:** `step6_answers.txt`

| Question | Answer |
|---|---|
| Maximum posts | **panama_tech_jobs** — 2,450 |
| Maximum followers | **luis_fintech_pty** — 1,200,000 |
| Follows the most people | **diego_builds** — 1,320 |
| Categories | **17** (Community is the largest with 5) |

---

## 💡 Practice

1. In step 0, count how many lines contain an emoji 📍.
2. If step 2 did not remove `Follow` / `Message`, what would step 5 store as that profile's name? (Hint: count the lines.)
3. In step 6, also write the top 5 profiles by followers to the answers file.
4. Delete the `outputs/` folder and re-run everything. Do you get the same files?

---

*Sample data prepared for teaching by **Panama Tech Academy**.*
