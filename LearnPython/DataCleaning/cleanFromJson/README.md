# Social Network – Data Cleaning & Recommendation Project

A beginner-friendly Python project based on the supplied `SocialNetwork.ipynb` notebook and `social_data.json` dataset.

The notebook's work is divided into separate `.py` files so each task can be taught, run, and understood independently.

## Project structure

```text
python_social_network_recommendation_project/
├── README.md
├── requirements.txt
├── social_data.json
├── task1_clean_and_structure.py
├── task2_people_you_may_know.py
├── task3_pages_you_might_like.py
├── task4_combine_recommendations.py
├── run_all.py
└── outputs/
```

## Requirements

- Python 3.9+
- pandas
- `json` and `collections` are included with Python.

Install pandas:

```bash
python -m pip install -r requirements.txt
```

## Task 1 – Clean and structure the data

Run:

```bash
python task1_clean_and_structure.py
```

Input: `social_data.json`

This task:
1. Loads the users and pages from JSON.
2. Reports duplicate IDs, blank names, inactive users, and IDs stored as text.
3. Converts user, friend, and page IDs to integers.
4. Trims and title-cases user names.
5. Drops users with blank names.
6. Merges duplicate user records by combining friends and liked pages.
7. Removes duplicate page records and blank page names.
8. Removes self-friendships and references to missing users.
9. Makes friendships mutual.
10. Removes invalid page likes and inactive users.
11. Creates lookup dictionaries and pandas tables.

Outputs in `outputs/`:
- `clean_social_data.json`
- `users.csv`
- `friendships.csv`
- `likes.csv`
- `popular_pages.csv`

## Task 2 – People You May Know

Run after Task 1:

```bash
python task2_people_you_may_know.py
```

Input: `outputs/clean_social_data.json`

Logic:
1. Visit the friends of the selected user.
2. Visit each friend's friends.
3. Skip the selected user and existing friends.
4. Count how many mutual friends each candidate has.
5. Return the highest-scoring candidates.

The example selected user is `1` (Amit). Change `selected_user = 1` in the script to test another user ID.

Output:
- `outputs/people_you_may_know.csv`

## Task 3 – Pages You Might Like

Run after Task 1:

```bash
python task3_pages_you_might_like.py
```

Input: `outputs/clean_social_data.json`

Main recommendation logic:
1. Find users who like at least one of the same pages.
2. Score each similar user by the number of shared pages.
3. Add that score to pages they like that the selected user has not liked.
4. Recommend the highest-scoring pages.

Bonus logic:
- Add extra points for pages liked by direct friends.
- `friend_weight` controls the extra points. The default is `1`.

The example selected user is `1` (Amit). Change `selected_user = 1` to test another user.

Output:
- `outputs/pages_you_might_like.csv`

## Task 4 – Combine recommendation reports

Run after Task 2 and Task 3:

```bash
python task4_combine_recommendations.py
```

Inputs:
- `outputs/people_you_may_know.csv`
- `outputs/pages_you_might_like.csv`

Output:
- `outputs/recommendations.csv`

This final report has one row per user and both recommendation columns.

## Run the entire project

Instead of running each task manually, use:

```bash
python run_all.py
```

The helper runs tasks in order and stops if a task fails.

## Recommended teaching order

| Order | File | Concept |
|---|---|---|
| 1 | `task1_clean_and_structure.py` | JSON, dictionaries, sets, loops, data cleaning, pandas |
| 2 | `task2_people_you_may_know.py` | Graph relationships, nested loops, sets, Counter |
| 3 | `task3_pages_you_might_like.py` | Set intersection/difference, scoring, recommendations |
| 4 | `task4_combine_recommendations.py` | pandas merge and CSV export |
| 5 | `run_all.py` | Run multiple Python scripts in sequence |

## Important notes

- Keep `social_data.json` in the project root beside the `.py` files.
- Run Task 1 before Tasks 2 and 3 because they use `outputs/clean_social_data.json`.
- Run Tasks 2 and 3 before Task 4 because it combines their CSV files.
- The dataset is randomly generated demo data, as described in the supplied project README.
- This is a simple educational recommendation demo, not a production social-network recommendation system.
