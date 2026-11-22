"""Lecture 12: String methods with the .str namespace."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(140)

people = pl.DataFrame({
    "name": ["  asha rao", "RAVI   KUMAR", "meena iyer ", "John D'Souza", None],
    "email": ["asha@gmail.com", "ravi@YAHOO.com", "meena@gmail.com", "john@work.org", "x@y"],
    "phone": ["98-765-43210", "9123456789", "(91) 99887 76655", "n/a", "8888"],
    "id": ["7", "12", "103", "4", "56"],
})
print(people)

print("\n=== Cleaning ===")
people = people.with_columns(
    name=pl.col("name").str.strip_chars().str.replace_all(r"\s+", " ").str.to_titlecase(),
    email=pl.col("email").str.to_lowercase(),
    id=pl.col("id").str.zfill(4),
)
print(people)

print("\n=== Testing ===")
print(people.select(
    "email",
    gmail=pl.col("email").str.contains("gmail"),
    dot_com=pl.col("email").str.ends_with(".com"),
    has_a=pl.col("name").str.contains("(?i)a"),
    name_len=pl.col("name").str.len_chars(),
))

print("\n=== Splitting ===")
print(people.select(
    "name",
    parts=pl.col("name").str.split(" "),
    first=pl.col("name").str.split(" ").list.first(),
    last=pl.col("name").str.split(" ").list.last(),
    domain=pl.col("email").str.split("@").list.last(),
))
print(people.select(pl.col("name").str.split_exact(" ", 1)
                    .struct.rename_fields(["first", "last"]).struct.unnest()))

print("\n=== Extracting with regex ===")
print(people.select(
    "phone",
    digits=pl.col("phone").str.replace_all(r"\D", ""),
).with_columns(valid=pl.col("digits").str.contains(r"^(91)?\d{10}$")))

orders = pl.DataFrame({"text": ["Order #123 (paid)", "Order #45 (due)", "Refund #9 (paid)"]})
print(orders.with_columns(number=pl.col("text").str.extract(r"#(\d+)", 1).str.to_integer()))
print(orders.select(pl.col("text").str.extract_groups(
    r"(?<kind>\w+) #(?<number>\d+) \((?<status>\w+)\)").struct.unnest()))
print(pl.DataFrame({"s": ["a1b22c333"]}).select(
    all_numbers=pl.col("s").str.extract_all(r"\d+"), digit_count=pl.col("s").str.count_matches(r"\d")))

print("\n=== Joining text ===")
print(people.select(initials=pl.concat_str(
    pl.col("name").str.slice(0, 1), pl.col("name").str.split(" ").list.last().str.slice(0, 1))))

sales = pl.read_csv(DATA / "sales.csv")
print(sales.group_by("category").agg(
    products=pl.col("product").unique().sort().str.join(", ")).sort("category"))

print("\n=== On the course data ===")
print("products with 'a':", sorted(sales.filter(pl.col("product").str.contains("(?i)a"))["product"].unique().to_list()))
