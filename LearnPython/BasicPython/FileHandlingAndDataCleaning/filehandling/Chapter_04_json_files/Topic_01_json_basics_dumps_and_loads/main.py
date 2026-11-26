# Import the module or specific tools needed for this lesson.
import json

# Assign the calculated or created value to student for later use.
student = {
    # Perform this operation; the expression or method shown determines the exact action.
    "name": "Asha",
    # Perform this operation; the expression or method shown determines the exact action.
    "age": 16,
    # Perform this operation; the expression or method shown determines the exact action.
    "subjects": ["Maths", "Physics"],
    # Perform this operation; the expression or method shown determines the exact action.
    "passed": True,
    # Perform this operation; the expression or method shown determines the exact action.
    "rank": None,
# Perform this operation; the expression or method shown determines the exact action.
}

# Assign the calculated or created value to text for later use.
text = json.dumps(student)
# Display this value so we can inspect the program's result.
print(text)
# Display this value so we can inspect the program's result.
print(type(text).__name__)

# Assign the calculated or created value to back for later use.
back = json.loads(text)
# Display this value so we can inspect the program's result.
print(back["subjects"][0], type(back).__name__)

# Display this value so we can inspect the program's result.
print(json.dumps((1, 2)), json.dumps("नमस्ते"), json.dumps("नमस्ते", ensure_ascii=False))
