# LAB 7 — Python `json` Module

## Purpose
Read and write JSON data.

## What you will learn
`json.dumps()` converts Python data to a JSON string; `json.loads()` parses a JSON string. `json.dump()` and `json.load()` work directly with file objects.

## Code

```python
import json
from pathlib import Path

student = {
    "name": "Asha",
    "course": "Python",
    "completed": True,
    "scores": [85, 90, 92]
}

# Convert a Python dictionary into a JSON string.
json_text = json.dumps(student, indent=4)
print("JSON string:")
print(json_text)

# Convert JSON text back into a Python dictionary.
loaded_student = json.loads(json_text)
print("Student name:", loaded_student["name"])

# Save JSON to a file and read it back.
file_path = Path("student.json")
file_path.write_text(json_text, encoding="utf-8")

data_from_file = json.loads(file_path.read_text(encoding="utf-8"))
print("Scores from file:", data_from_file["scores"])
```

## Run the lab

From this lab's folder:

```bash
python3 lab.py
```

On Windows, you can use:

```powershell
py lab.py
```

## Expected result
The script prints example values demonstrating the module. Some values are intentionally different on each run or machine (for example, random numbers, current date/time, paths, and platform information).

## Try it yourself
Add a new key such as `city` to the dictionary and verify it appears in the JSON file. JSON supports objects, arrays, strings, numbers, booleans, and null.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
