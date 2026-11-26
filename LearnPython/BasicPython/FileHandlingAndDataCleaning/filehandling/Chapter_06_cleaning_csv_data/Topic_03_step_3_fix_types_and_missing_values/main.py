# Import the module or specific tools needed for this lesson.
from parsers import to_int, to_money, to_date, valid_email

# Display this value so we can inspect the program's result.
print("AGE (valid 0-120)")
# Loop through each item so the same operation is applied repeatedly.
for v in [" 23 ", "N/A", "abc", "-5", ""]:
    # Display this value so we can inspect the program's result.
    print(f"  {v!r:<8} -> {to_int(v, 0, 120)}")

# Display this value so we can inspect the program's result.
print("SPEND")
# Loop through each item so the same operation is applied repeatedly.
for v in ["1,200", "₹640", "  2,050.50 ", "", "850"]:
    # Display this value so we can inspect the program's result.
    print(f"  {v!r:<14} -> {to_money(v)}")

# Display this value so we can inspect the program's result.
print("JOINED")
# Loop through each item so the same operation is applied repeatedly.
for v in ["2024-01-15", "15/02/2024", "2024/03/18", "March 5"]:
    # Display this value so we can inspect the program's result.
    print(f"  {v!r:<12} -> {to_date(v)}")

# Display this value so we can inspect the program's result.
print("EMAIL")
# Loop through each item so the same operation is applied repeatedly.
for v in ["asha@mail.com", "kabir@mail", "zoya@mail.com"]:
    # Display this value so we can inspect the program's result.
    print(f"  {v!r:<15} -> {valid_email(v)}")
