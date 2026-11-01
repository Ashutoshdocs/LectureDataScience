# Social Network – Data Cleaning & Recommendations (Demo)

A beginner-friendly demo that shows how social media sites suggest **"People You May Know"** and **"Pages You Might Like"**. It uses plain Python (plus pandas for tables) in an **Anaconda Jupyter Notebook**.

## 📁 Project Files

| File | Description |
|------|-------------|
| `README.md` | This guide |
| `social_data.json` | Randomly generated, intentionally messy social-network data (28 users, 18 pages) |
| `SocialNetwork.ipynb` | Jupyter notebook covering all three tasks |

Running the notebook creates two more files:

| Output | Description |
|--------|-------------|
| `clean_social_data.json` | Cleaned, structured users and pages |
| `recommendations.csv` | Friend and page suggestions for every user |

## 🗂️ Data Format

```json
{
  "users": [
    {"id": 1, "name": "Amit", "friends": [2, 3], "liked_pages": [101, 105]}
  ],
  "pages": [
    {"id": 101, "name": "Python Developers"}
  ]
}
```

## 📚 Tasks in the Notebook

### 1. Cleaning and Structuring the Data
Problems in the raw data, and how the notebook fixes them:

| Problem | Example | Fix |
|---------|---------|-----|
| IDs stored as text | `"11"`, `["1", "8"]` | Convert to integers |
| Messy names | `"  meera  "` | Trim and title-case |
| Missing names | `""` | Drop the user |
| Duplicate users | Two records with ID `4` | Merge their friends and likes |
| Self-friendships | User 3 is friends with 3 | Remove |
| Non-existent friends | Friend ID `99` | Remove |
| One-way friendships | A lists B, but B doesn't list A | Make friendships two-way |
| Duplicate / blank pages | `"  cricket fans "`, `""` | Keep one clean name per ID |
| Likes for missing pages | Page `150` | Remove |
| Inactive users | No friends, no likes | Remove |

The cleaned data is then organised into lookup dictionaries and three tidy tables: **users**, **friendships** and **likes**.

### 2. Finding "People You May Know"
**Logic:** if you share many friends with someone, you probably know them.

1. Look at your friends' friends.
2. Skip yourself and people you're already friends with.
3. Count the mutual friends for each person.
4. Suggest the people with the most mutual friends.

```
People Amit may know:
  Neha  – 4 mutual friend(s)
  Sneha – 3 mutual friend(s)
```

### 3. Finding "Pages You Might Like"
**Logic:** people who like the same pages as you have similar interests.

1. Find users who like at least one of the same pages as you.
2. Score each user by how many pages you both like.
3. Add that score to every page they like that you haven't liked yet.
4. Suggest the highest-scoring pages.

A bonus version also adds points for pages your **friends** like.

## 🚀 How to Run (Anaconda)

1. Install [Anaconda](https://www.anaconda.com/download) if you don't have it.
2. Put all files in the same folder.
3. Open **Anaconda Navigator → Jupyter Notebook**, or run this in Anaconda Prompt:
   ```bash
   cd path/to/your/folder
   jupyter notebook
   ```
4. Open `SocialNetwork.ipynb`.
5. Click **Kernel → Restart & Run All**, or run cells one at a time with `Shift + Enter`.

### Requirements
- Python 3.9+
- pandas (included with Anaconda)
- `json` and `collections` (built into Python)

## 💡 Try It Yourself
- Change `user = 1` to another ID to see their suggestions.
- Change `friend_weight` in `pages_you_might_like_v2` to give friends' likes more or less importance.
- Add new users or pages to `social_data.json` and re-run the notebook.

## 📝 License
Free to use for learning and demos. All data is randomly generated, so no real people are included.
