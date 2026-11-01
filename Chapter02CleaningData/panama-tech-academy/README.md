# 🇵🇦 Coders of Panama — Panama Tech Academy

A beginner-friendly Python data-parsing challenge by **Panama Tech Academy**.
You take messy, copy-pasted Instagram profile data, turn it into clean JSON, and answer real questions about it using plain Python — no pandas, no libraries beyond `json`.

---

## 📖 The Story

You walk into the office of **Rodrigo Castillo**, Panama City's most famous (and most impatient) venture capitalist, and ask him for **2.2 billion USD** to build "the Silicon Valley of Central America."

He laughs at you in front of the whole floor.

Then he asks where you live. *"Casco Viejo,"* you say. After talking to you for a while, he gives you a challenge instead of a cheque:

> Collect the raw Instagram data of all **@panamatechacademy** followers and tell me:
> - Who has the **maximum posts**?
> - Who has the **maximum followers**?
> - Who **follows the maximum** number of people?
> - **How many categories** (Digital creator, Nonprofit organization, Community…) are there, and **how many people** are in each?
>
> You have **24 hours**.

You ask him for the data. He laughs again.

So you hire **Valentina Ríos** (Costa del Este) and **Samuel Chen** (San Miguelito). Since they live far apart — and the Corredor at rush hour is no joke — you all meet at a little café in **Casco Viejo**, and they copy every follower profile into a text file by hand.

---

## 📁 Project Files

| File | What it is |
|---|---|
| `coders-of-panama.ipynb` | The full solution notebook — story, code, and outputs for every task |
| `finaldata.txt` | Raw profile data for all followers (input to the notebook) |
| `initialdata.txt` | The first small sample collected by the team |
| `data.json` | Clean, structured data produced by the notebook |
| `README.md` | This file |

### Raw data format (`finaldata.txt`)
Each profile is a block of lines, separated from the next by a blank line:

```
startuphub_pty            ← username
2,300 posts               ← posts
45K followers             ← followers (may use commas, K or M)
120 following             ← following
Startup Hub Panama        ← display name
Media                     ← category (optional)
🦄 News from the ...      ← bio lines (optional)
startuphub.pty/newsletter
```

### Clean data format (`data.json`)
```json
{
    "username": "startuphub_pty",
    "no_of_posts": 2300,
    "no_of_followers": 45000,
    "type_of_page": "Media",
    "no_of_following": 120,
    "name": "Startup Hub Panama",
    "bio": "🦄 News from the Tech Hub of Central America\n..."
}
```

---

## ✅ Tasks Completed

All tasks are implemented in the notebook, step by step:

1. **Read the raw file** – load `finaldata.txt` with UTF-8 (the bios are full of emojis).
2. **Split into profiles** – split on blank lines and drop empty leftovers → **107 profiles**.
3. **Parse each profile** – convert `6,851`, `22.4K`, `681K`, `1.2M` into real integers; label missing categories as `Unknown`.
4. **Save clean JSON** – write everything to `data.json`.
5. **Who has the maximum posts?**
6. **Who has the maximum followers?**
7. **Who follows the maximum people?**
8. **How many categories are there?**
9. **How many people are in each category?**
10. **Bonus: data quality check** – find usernames that were collected twice.

---

## 📊 Results

| Question | Answer |
|---|---|
| Maximum posts | **startuphub_pty** — 2,300 posts |
| Maximum followers | **_lucianavega** — 681,000 followers |
| Follows the most people | **panama_tech_bro** — 890 following |
| Number of categories | **34** |

### People per category

| Category | Count | | Category | Count |
|---|---|---|---|---|
| Community | 33 | | Software Engineer | 1 |
| Media | 12 | | Cafe Explorer | 1 |
| Blog | 8 | | Founder | 1 |
| Tech | 7 | | Backend Developer | 1 |
| Personal Blog | 5 | | Frontend Dev | 1 |
| Education | 4 | | Full-stack Dev | 1 |
| Lifestyle | 3 | | Artist + Coder | 1 |
| Tech Creator | 2 | | Product Manager | 1 |
| Engineer | 2 | | Recruiter | 1 |
| Food & Drink | 2 | | Cafe Nerd | 1 |
| Developer | 2 | | Coder | 1 |
| Design | 2 | | Comedy | 1 |
| Entrepreneur | 2 | | Data Science | 1 |
| Public Figure | 2 | | Data Scientist | 1 |
| Educator | 2 | | Nonprofit organization | 1 |
| | | | Digital creator | 1 |
| | | | Blogger | 1 |
| | | | Investor | 1 |
| | | | Writer | 1 |

### Data quality note
107 profiles were collected but only **105 usernames are unique** — `sanfran_startup_stories` and `machinelearning_pty` were each copied twice (with different numbers). A good next exercise is deciding which copy to keep.

---

## 🚀 How to Run

```bash
# 1. Install Jupyter (if you don't have it)
pip install notebook

# 2. Open the project folder and start Jupyter
cd panama-tech-academy
jupyter notebook

# 3. Open coders-of-panama.ipynb and run all cells (Kernel → Restart & Run All)
```

Requirements: **Python 3.8+**. Only the standard library is used.

---

## 🧠 What You'll Learn

- Reading text files with the correct encoding
- Splitting and cleaning raw text with `split()` and list comprehensions
- Writing a parsing function and handling edge cases (`K` / `M` suffixes, missing fields)
- Converting data to JSON with `json.dumps`
- Finding maximums with a simple loop
- Counting unique values with a `set` and frequencies with a `dict`
- Spotting duplicate records — a real-world data-cleaning skill

## 💡 Try It Yourself — Extra Challenges

1. Who has the **lowest** follower count?
2. Which profile has the best **followers-to-following ratio**?
3. Remove the duplicate usernames and re-run every answer.
4. List every profile whose bio mentions **Python**.
5. Group profiles by neighbourhood (📍 Casco Viejo, Obarrio, Costa del Este…).

---

> The profiles in this dataset are sample data prepared for teaching purposes.

**Made with ❤️ in Panama City by Panama Tech Academy**
