"""
PROJECT 3: STUDENT RESULT MANAGEMENT

Concepts: *args, loops, built-in sum(), return multiple values.
"""


def calculate_result(name, *marks):
    if not marks:
        return name, 0, 0.0, "No marks supplied"

    total = sum(marks)
    percentage = total / len(marks)

    if percentage >= 90:
        grade = "A"
    elif percentage >= 75:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "Needs improvement"

    return total, percentage, grade


result = calculate_result("Rahul", 85, 90, 78, 88, 95)

total, percentage, grade = result

print("Total:", total)
print("Percentage:", round(percentage, 2))
print("Grade:", grade)
