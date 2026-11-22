# Lecture 04: Reading & writing files

Run: `python lecture.py` (it writes its output files into an `output/` folder next to the script)

## Reading

| Format | Read | Needs |
|--------|------|-------|
| CSV | `pd.read_csv("file.csv")` | n/a |
| Excel | `pd.read_excel("file.xlsx", sheet_name="Sheet1")` | `openpyxl` |
| JSON | `pd.read_json("file.json")` | n/a |
| SQL | `pd.read_sql("SELECT ...", connection)` | a DB driver |
| Clipboard | `pd.read_clipboard()` | copy a table from Excel or a web page first |
| Web page tables | `pd.read_html(url)` | `lxml` |
| Parquet (fast, big data) | `pd.read_parquet("file.parquet")` | `pyarrow` |

## The most useful `read_csv` options

| Option | Use it when… | Example |
|--------|-------------|---------|
| `sep` | the file isn't comma-separated | `sep=";"`, `sep="\t"` |
| `usecols` | you only need some columns | `usecols=["date", "units"]` |
| `index_col` | a column should be the index | `index_col="order_id"` |
| `parse_dates` | a column holds dates | `parse_dates=["date"]` |
| `dtype` | force column types | `dtype={"customer_id": "str"}` |
| `na_values` | extra markers for "missing" | `na_values=["n/a", "-"]` |
| `nrows` | preview a huge file | `nrows=1000` |
| `skiprows`, `header` | junk lines at the top | `skiprows=2` |
| `thousands` | numbers like `12,500` | `thousands=","` |
| `encoding` | weird characters / errors | `encoding="latin-1"` |

## Paths

Relative paths are relative to **the folder you run Python from**, not where the script lives. This course builds paths from the script's own location so they always work:

```python
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / "data"
sales = pd.read_csv(DATA / "sales.csv")
```

> ⚠️ Windows paths: use `r"C:\Users\me\file.csv"` (raw string) or forward slashes. Otherwise `\n` and `\t` inside the path become newline and tab.

## Writing

| Format | Write |
|--------|-------|
| CSV | `df.to_csv("out.csv", index=False)` |
| Excel | `df.to_excel("out.xlsx", sheet_name="Report", index=False)` |
| Several sheets | `with pd.ExcelWriter("out.xlsx") as w: df1.to_excel(w, sheet_name="A"); df2.to_excel(w, sheet_name="B")` |
| JSON | `df.to_json("out.json", orient="records", indent=2)` |
| Markdown table | `df.to_markdown()` (needs `tabulate`) |

> ⚠️ Forgetting `index=False` writes the 0, 1, 2… index as an extra unnamed column. When you read the file back you'll see a mysterious `Unnamed: 0` column.

## Exercises

1. Read only `date`, `product` and `units` from `sales.csv`.
2. Read `sales.csv` with `order_id` as the index. What is `sales.loc[1001]`?
3. Save only Furniture orders to `output/furniture.csv`.
4. Read `students.csv` and save it as an Excel file with two sheets: class 10A and class 10B.

<details><summary>Solutions</summary>

```python
pd.read_csv(DATA / "sales.csv", usecols=["date", "product", "units"])
s = pd.read_csv(DATA / "sales.csv", index_col="order_id"); s.loc[1001]
sales[sales["category"] == "Furniture"].to_csv(OUT / "furniture.csv", index=False)
with pd.ExcelWriter(OUT / "classes.xlsx") as w:
    for c, part in students.groupby("class"):
        part.to_excel(w, sheet_name=c, index=False)
```
</details>

**Next →** [Lecture 05: Exploring data](../05_exploring_data/)
