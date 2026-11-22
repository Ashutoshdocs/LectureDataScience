import re

text = "Contact support at help@example.com or sales@example.org"

# Find all email-like matches in the text.
emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
print("Found email addresses:", emails)

# Search for a pattern.
match = re.search(r"support", text)
print("Found support:", bool(match))

# Replace a word.
updated_text = re.sub(r"support", "customer care", text)
print("Updated text:", updated_text)

# Check whether a string contains only 10 digits.
mobile = "9876543210"
if re.fullmatch(r"\d{10}", mobile):
    print("Mobile number has 10 digits")
else:
    print("Invalid mobile number")
