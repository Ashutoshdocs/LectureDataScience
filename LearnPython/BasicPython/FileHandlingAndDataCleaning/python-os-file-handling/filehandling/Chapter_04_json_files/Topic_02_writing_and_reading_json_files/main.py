# Import the module or specific tools needed for this lesson.
import json

# Assign the calculated or created value to settings for later use.
settings = {
    # Perform this operation; the expression or method shown determines the exact action.
    "theme": "dark",
    # Perform this operation; the expression or method shown determines the exact action.
    "language": "hi",
    # Perform this operation; the expression or method shown determines the exact action.
    "greeting": "नमस्ते",
    # Perform this operation; the expression or method shown determines the exact action.
    "recent_files": ["report.csv", "notes.txt"],
    # Perform this operation; the expression or method shown determines the exact action.
    "window": {"width": 1280, "height": 720},
# Perform this operation; the expression or method shown determines the exact action.
}

# Open/use the resource in a context manager so it is closed automatically.
with open("settings.json", "w", encoding="utf-8") as f:
    # Call the relevant Python function/method to perform this file or data operation.
    json.dump(settings, f, indent=2, ensure_ascii=False)

# Open/use the resource in a context manager so it is closed automatically.
with open("settings.json", encoding="utf-8") as f:
    # Display this value so we can inspect the program's result.
    print(f.read())

# Open/use the resource in a context manager so it is closed automatically.
with open("settings.json", encoding="utf-8") as f:
    # Assign the calculated or created value to loaded for later use.
    loaded = json.load(f)

# Display this value so we can inspect the program's result.
print(loaded["window"]["width"])
# Display this value so we can inspect the program's result.
print(loaded.get("font_size", 14))
# Display this value so we can inspect the program's result.
print(loaded == settings)
