# Open/use the resource in a context manager so it is closed automatically.
with open("emails.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to raw for later use.
    raw = f.read().splitlines()
# Display this value so we can inspect the program's result.
print("raw lines        :", len(raw))

# Assign the calculated or created value to no_blank for later use.
no_blank = [line for line in raw if line.strip()]
# Display this value so we can inspect the program's result.
print("non-blank        :", len(no_blank))

# Assign the calculated or created value to exact for later use.
exact = list(dict.fromkeys(no_blank))
# Display this value so we can inspect the program's result.
print("exact duplicates removed:", len(exact))

# Assign the calculated or created value to seen for later use.
seen = set()
# Assign the calculated or created value to unique for later use.
unique = []
# Loop through each item so the same operation is applied repeatedly.
for line in no_blank:
    # Assign the calculated or created value to key for later use.
    key = line.strip().lower()
    # Check this condition; the indented block runs only when it is true.
    if key not in seen:
        # Perform this operation; the expression or method shown determines the exact action.
        seen.add(key)
        # Perform this operation; the expression or method shown determines the exact action.
        unique.append(key)
# Display this value so we can inspect the program's result.
print("normalised duplicates removed:", len(unique))
# Display this value so we can inspect the program's result.
print(unique)

# Open/use the resource in a context manager so it is closed automatically.
with open("emails_clean.txt", "w", encoding="utf-8") as f:
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("\n".join(unique) + "\n")
