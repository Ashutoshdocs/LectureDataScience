# 🇵🇦 Panama Tech Academy — Raw Data to Clean JSON (Demo)

A hands-on Python demo: start with **messy, copy-pasted Instagram profile data**, clean it, organize it into **JSON**, and answer questions with it.
Pure Python, standard library only.

---

## 📁 Files

| File | Purpose |
|---|---|
| `raw_data.txt` | The messy starting data (25 profiles, copied by hand) |
| `01_cleaning.ipynb` | Cleans the raw text → creates `cleaned_data.txt` |
| `02_clean_json.ipynb` | Organizes the clean text → creates `clean_data.json` |
| `03_answer_questions.ipynb` | Loads the JSON and answers the questions |
| `cleaned_data.txt` | Output of notebook 01 |
| `clean_data.json` | Output of notebook 02 |

```
raw_data.txt ──01──▶ cleaned_data.txt ──02──▶ clean_data.json ──03──▶ answers
```

---

## 🧹 What's messy in `raw_data.txt`

- Extra spaces and tabs at the start/end of lines
- Random gaps: 1, 2, 3 blank lines, or lines containing only a space
- Inconsistent words: `posts`, `Posts`, `POSTS`, `FOLLOWERS`
- Instagram buttons copied by mistake: `Follow`, `Message`
- Numbers in different formats: `2,300`, `18.6K`, `1.2M`
- Duplicate profiles (copied twice)
- A profile with no category or bio

---

## 🚀 Steps to Generate Each Task

**Setup (once)**
```bash
pip install notebook
cd panama-tech-academy-demo
jupyter notebook
```

**Step 1 — Clean the data** → open `01_cleaning.ipynb` and run all cells
1. Read `raw_data.txt`
2. Strip spaces/tabs from every line
3. Remove `Follow` / `Message` lines
4. Lowercase count words (`POSTS` → `posts`), keeping `18.6K` as is
5. Group lines into profiles using blank lines
6. Remove duplicate usernames
7. Save `cleaned_data.txt` with exactly one blank line between profiles

✅ Result: 27 blocks → **25 unique profiles**

**Step 2 — Create clean JSON** → open `02_clean_json.ipynb` and run all cells
1. Read `cleaned_data.txt` and split into profiles
2. Convert `2,300` / `18.6K` / `1.2M` into integers
3. Turn each profile into a dictionary (missing category → `Unknown`)
4. Save `clean_data.json`

✅ Result: a list of 25 objects like this:
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

**Step 3 — Answer the questions** → open `03_answer_questions.ipynb` and run all cells

| Question | Answer |
|---|---|
| Who has the maximum posts? | **panama_tech_jobs** — 2,450 |
| Who has the maximum followers? | **luis_fintech_pty** — 1,200,000 |
| Who follows the maximum people? | **diego_builds** — 1,320 |
| How many categories? | **17** (Community is the largest with 5) |

> ⚠️ Run the notebooks **in order** (01 → 02 → 03). Each one uses the file made by the one before it.

---

## 💡 Practice Tasks for Students

1. Who has the **fewest** followers?
2. Find every profile whose bio mentions **Python**.
3. Calculate the **average** followers per category.
4. List the top 5 profiles by followers.
5. Add a new messy profile to `raw_data.txt` and re-run all three notebooks.

---

*Sample data prepared for teaching by **Panama Tech Academy**.*
