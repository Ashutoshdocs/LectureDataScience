"""
PROJECT 2: EMPLOYEE DETAILS

Concepts:
- A required positional parameter (name)
- *args for any number of skills
- **kwargs for flexible named employee details
"""


def employee(name, *skills, **details):
    print("\\nEMPLOYEE INFORMATION")
    print("Name:", name)

    print("\\nSkills:")
    if skills:
        for skill in skills:
            print("-", skill)
    else:
        print("No skills provided")

    print("\\nAdditional details:")
    if details:
        for key, value in details.items():
            print(f"{key}: {value}")
    else:
        print("No additional details provided")


employee(
    "Rahul",
    "Python",
    "Azure",
    "Docker",
    "Kubernetes",
    age=28,
    city="Pune",
    salary=60000,
    department="DevOps"
)
