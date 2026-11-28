# Import the module or specific tools needed for this lesson.
from pathlib import Path

# Assign the calculated or created value to template for later use.
template = Path("letter.txt").read_text(encoding="utf-8")

# Assign the calculated or created value to students for later use.
students = [
    # Perform this operation; the expression or method shown determines the exact action.
    {"name": "Asha", "course": "Data Science", "score": 91},
    # Perform this operation; the expression or method shown determines the exact action.
    {"name": "Ravi", "course": "Web Development", "score": 78},
# Perform this operation; the expression or method shown determines the exact action.
]

# Call the relevant Python function/method to perform this file or data operation.
Path("letters").mkdir(exist_ok=True)
# Loop through each item so the same operation is applied repeatedly.
for s in students:
    # Assign the calculated or created value to text for later use.
    text = template
    # Loop through each item so the same operation is applied repeatedly.
    for key, value in s.items():
        # Assign the calculated or created value to text for later use.
        text = text.replace("{" + key + "}", str(value))
    # Assign the calculated or created value to out for later use.
    out = Path("letters") / f"letter_{s['name'].lower()}.txt"
    # Perform this operation; the expression or method shown determines the exact action.
    out.write_text(text, encoding="utf-8")
    # Display this value so we can inspect the program's result.
    print("wrote", out)

# Display this value so we can inspect the program's result.
print("---")
# Display this value so we can inspect the program's result.
print(Path("letters/letter_asha.txt").read_text(encoding="utf-8").strip())
