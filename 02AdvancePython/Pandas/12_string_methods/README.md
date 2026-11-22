# Lecture 12: String methods with `.str`

Run: `python lecture.py`

Text columns are messy: extra spaces, MIXED case, typos, several facts squeezed into one field. The `.str` accessor applies Python string methods to **every value at once**, vectorized and safe with missing values.

```python
df["name"].str.upper()        # instead of [n.upper() for n in df["name"]]
```

## Cleaning

| Method | Does |
|--------|------|
| `.str.strip()` / `.lstrip()` / `.rstrip()` | remove surrounding spaces |
| `.str.lower()` / `.upper()` / `.title()` | change case |
| `.str.replace("old", "new")` | replace text (`regex=True` for patterns) |
| `.str.replace(r"\s+", " ", regex=True)` | squash repeated spaces |
| `.str.zfill(3)` | pad with zeros: `"7"` → `"007"` |
| `.str.pad(10, side="right")` | pad with spaces |

## Testing (return True/False, so they work as filters)

| Method | Example |
|--------|---------|
| `.str.contains("x")` | `df[df["email"].str.contains("@")]` |
| `.str.startswith("A")` / `.endswith(".com")` | prefixes / suffixes |
| `.str.isdigit()` / `.isalpha()` | content checks |
| `.str.match(r"^\d{3}$")` | regex match from the start |
| `.str.len()` | length of each string |

Use `case=False` with `contains` for a case-insensitive search, and `na=False` to treat missing values as "no match".

## Splitting & extracting

| Method | Example → result |
|--------|------------------|
| `.str.split(" ")` | `"Asha Rao"` → `["Asha", "Rao"]` |
| `.str.split(" ", expand=True)` | → two **columns** |
| `.str.split("@").str[1]` | the domain of an email |
| `.str[0]`, `.str[:3]` | first character / first 3 characters |
| `.str.extract(r"(\d+)")` | the first number found |
| `.str.get_dummies(sep=",")` | `"a,b"` → indicator columns |
| `.str.cat(sep=", ")` | join all values into one string |

## Regex in 60 seconds

| Pattern | Matches |
|---------|---------|
| `\d` | a digit; `\d+` one or more digits |
| `\s` | whitespace |
| `\w` | letter, digit or underscore |
| `.` | any character |
| `^` / `$` | start / end |
| `[A-Z]` | any capital letter |
| `( )` | a group to **extract** |

```python
pd.Series(["Order #123", "Order #45"]).str.extract(r"#(\d+)")   # 123, 45
```

## Exercises

1. Clean `["  asha rao", "RAVI KUMAR", "meena  iyer "]` into Title Case with single spaces.
2. Split them into `first` and `last` columns.
3. Extract the domain from a list of emails.
4. Find products whose name contains `"a"` (any case).

<details><summary>Solutions</summary>

```python
s.str.strip().str.replace(r"\s+", " ", regex=True).str.title()
clean.str.split(" ", expand=True).set_axis(["first", "last"], axis=1)
emails.str.split("@").str[1]
sales["product"].str.contains("a", case=False)
```
</details>

**Next →** [Lecture 13: GroupBy & aggregation](../13_groupby_aggregation/)
