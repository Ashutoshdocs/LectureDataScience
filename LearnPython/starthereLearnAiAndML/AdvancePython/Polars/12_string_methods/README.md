# Lecture 12: String methods: the `.str` namespace

Run: `python lecture.py`

Text methods live under `pl.col("x").str.…`. They're vectorized, multi-threaded, and `null`-safe: a null input gives a null output, never a crash.

## Cleaning

| Method | Does |
|--------|------|
| `.str.strip_chars()` | trim spaces (also `strip_chars_start` / `_end`) |
| `.str.to_lowercase()` / `.to_uppercase()` / `.to_titlecase()` | case |
| `.str.replace("a", "b")` | first match (regex by default) |
| `.str.replace_all(r"\s+", " ")` | every match |
| `.str.replace_all(".", "", literal=True)` | treat the pattern as plain text, not regex |
| `.str.zfill(4)` | `"7"` → `"0007"` |
| `.str.pad_start(10, "*")` / `.pad_end(...)` | padding |

## Testing (return Boolean → use in `filter`)

| Method | Example |
|--------|---------|
| `.str.contains("gmail")` | substring / regex; `literal=True` for plain text |
| `.str.contains("(?i)gmail")` | case-insensitive (regex flag) |
| `.str.starts_with("A")` / `.ends_with(".com")` | prefix / suffix |
| `.str.len_chars()` | length in characters (`len_bytes` for bytes) |

## Splitting & extracting

| Method | Result |
|--------|--------|
| `.str.split(" ")` | a `List` column: `["Asha", "Rao"]` |
| `.str.split(" ").list.get(0)` | first item |
| `.str.split(" ").list.last()` | last item |
| `.str.split_exact(" ", 1).struct.unnest()` | fixed number of parts → **separate columns** |
| `.str.slice(0, 3)` / `.str.head(3)` / `.str.tail(3)` | substrings |
| `.str.extract(r"#(\d+)", 1)` | one regex group |
| `.str.extract_groups(r"(?<kind>\w+) #(?<num>\d+)")` | named groups → a `Struct` |
| `.str.extract_all(r"\d+")` | every match → a list |
| `.str.count_matches(r"\d")` | how many matches |
| `pl.concat_str([...], separator=" ")` | join columns |
| `.str.join(", ")` (in `agg`) | join many rows into one string |

## Converting

`.str.to_date(fmt)`, `.str.to_datetime(fmt)`, `.str.to_integer()`, and `.cast(pl.Float64, strict=False)` (Lecture 11).

## Exercises

1. Clean `["  asha rao", "RAVI   KUMAR", "meena iyer "]` to Title Case with single spaces.
2. Split into `first` and `last` columns.
3. Extract each email's domain.
4. Products containing `"a"` in any case.

<details><summary>Solutions</summary>

```python
pl.col("name").str.strip_chars().str.replace_all(r"\s+", " ").str.to_titlecase()
pl.col("name").str.split_exact(" ", 1).struct.rename_fields(["first", "last"]).struct.unnest()
pl.col("email").str.split("@").list.last()
sales.filter(pl.col("product").str.contains("(?i)a"))
```
</details>

**Next →** [Lecture 13: Group by & aggregation](../13_group_by_aggregation/)
