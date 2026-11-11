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
