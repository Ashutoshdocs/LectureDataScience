# Panama Tech Academy – Python File Reading & Data Cleaning

A beginner-friendly project that converts messy Instagram profile text into clean, structured JSON and answers questions about the profiles.

The original seven notebook lessons have been converted into separate, commented Python scripts.

## Project structure

```text
python_file_reading_cleaning_project/
├── README.md
├── raw_data.txt
├── step0_reading_files.py
├── step1_strip_spaces.py
├── step2_remove_junk.py
├── step3_fix_words.py
├── step4_group_and_dedupe.py
├── step5_to_json.py
├── step6_answers.py
├── run_all.py
└── outputs/
```

The `outputs/` folder is created automatically. Each step writes its result there.

## Requirements

- Python 3
- No third-party packages
- Uses only Python standard-library modules: `os`, `pathlib`, and `json`

You do not need pandas, NumPy, or pip packages for this project.

## Run the complete project

Open PowerShell or a terminal in this project folder:

```powershell
python run_all.py
```

The helper runs all seven scripts in the correct order and stops if a step fails.

You can also run each script individually, in order:

```powershell
python step0_reading_files.py
python step1_strip_spaces.py
python step2_remove_junk.py
python step3_fix_words.py
python step4_group_and_dedupe.py
python step5_to_json.py
python step6_answers.py
```

## Step-by-step guide

### Step 0 – Reading and writing files

File concepts:
- `open()` and `close()`
- `with open(...)`
- `read()`, `readline()`, and `readlines()`
- Looping over a file
- Write mode `"w"` and append mode `"a"`
- Creating folders with `os.makedirs()`

Input: `raw_data.txt`

Output: `outputs/step0_report.txt`

### Step 1 – Remove extra spaces and tabs

Concepts:
- `split("\n")`
- `strip()`
- List comprehension
- `"\n".join()`

Input: `raw_data.txt`

Output: `outputs/step1_stripped.txt`

### Step 2 – Remove junk lines

Remove copied Instagram button labels:
- `Follow`
- `Message`

Input: `outputs/step1_stripped.txt`

Output: `outputs/step2_no_junk.txt`

### Step 3 – Fix count words

Standardise count labels such as `POSTS`, `Posts`, `FOLLOWERS` and `Followers` to lowercase.

The number part remains unchanged. For example, `18.6K Followers` becomes `18.6K followers`.

Concepts:
- `rsplit(" ", 1)`
- `lower()`
- Tuple membership

Input: `outputs/step2_no_junk.txt`

Output: `outputs/step3_fixed_words.txt`

### Step 4 – Group profiles and remove duplicates

- A blank line marks the end of a profile.
- The first line in each profile is its username.
- A `set` tracks usernames already seen.
- Duplicate usernames are removed.

The supplied data contains 27 profile blocks and 25 unique usernames.

Input: `outputs/step3_fixed_words.txt`

Output: `outputs/step4_cleaned.txt`

### Step 5 – Convert profiles to JSON

Convert count formats into integers:
- `2,300` → `2300`
- `18.6K` → `18600`
- `1.2M` → `1200000`

Build a dictionary for every profile and write the list of dictionaries using `json.dump()`.

Concepts:
- Functions
- `replace()`
- `endswith()`
- `float()` and `int()`
- `json.dump()`
- `ensure_ascii=False` to preserve emoji and accented characters

Input: `outputs/step4_cleaned.txt`

Output: `outputs/step5_clean_data.json`

Each profile contains:
- `username`
- `posts`
- `followers`
- `following`
- `name`
- `category`
- `bio`

### Step 6 – Answer questions

Load the JSON file with `json.load()` and use `max()` with a `key` function to find:
- Profile with the maximum posts
- Profile with the maximum followers
- Profile following the most people

Use a dictionary to count profiles by category.

Input: `outputs/step5_clean_data.json`

Output: `outputs/step6_answers.txt`

Expected answers for the supplied dataset:
- Maximum posts: `panama_tech_jobs` – 2,450
- Maximum followers: `luis_fintech_pty` – 1,200,000
- Follows the most: `diego_builds` – 1,320
- Categories: 17

## Output files

| Step | Output |
|---|---|
| 0 | `outputs/step0_report.txt` |
| 1 | `outputs/step1_stripped.txt` |
| 2 | `outputs/step2_no_junk.txt` |
| 3 | `outputs/step3_fixed_words.txt` |
| 4 | `outputs/step4_cleaned.txt` |
| 5 | `outputs/step5_clean_data.json` |
| 6 | `outputs/step6_answers.txt` |

## Important

- Keep `raw_data.txt` in the same folder as the Python scripts.
- Run the scripts in order because each step after Step 1 reads the previous step's output.
- Step 1 reads the original `raw_data.txt`; Step 0 is a separate file-reading and file-writing demonstration.
- All file paths are built relative to the script location, so you can run the scripts from another current working directory.
- Re-running the scripts overwrites the generated output files with fresh results.

## Practice tasks

1. In Step 0, count how many lines contain the location-pin emoji `📍`.
2. Predict what Step 5 would store as a profile name if Step 2 did not remove the `Follow` and `Message` lines.
3. In Step 6, add code to write the top five profiles by followers.
4. Delete the `outputs/` folder and run `python run_all.py` again. Confirm that the scripts recreate the folder and output files.
