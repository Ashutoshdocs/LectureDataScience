"""
MODULE 7: **kwargs

**kwargs collects extra keyword arguments into a dictionary.
The name `kwargs` is a convention.
"""


# A. See what **kwargs collects
def show_details(**kwargs):
    print("Collected details:", kwargs)
    print("Type:", type(kwargs))


show_details(name="Rahul", age=25, city="Pune")


# B. Read values from kwargs
def student_details(**kwargs):
    print("Name:", kwargs.get("name", "Not provided"))
    print("Age:", kwargs.get("age", "Not provided"))
    print("City:", kwargs.get("city", "Not provided"))


student_details(name="Rahul", age=25, city="Pune")
student_details(name="Amit")


# C. Loop through all keyword arguments
def print_profile(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)


print_profile(
    name="Priya",
    course="Python",
    city="Patna",
    college="ABC College"
)


# D. Normal parameter combined with **kwargs
def employee(name, **details):
    print("Employee name:", name)
    for key, value in details.items():
        print(key, ":", value)


employee(
    "Rahul",
    age=28,
    department="IT",
    salary=60000,
    city="Pune"
)


# E. Unpacking a dictionary with **
def create_user(name, city):
    print(f"User {name} lives in {city}.")


user_data = {"name": "Riya", "city": "Patna"}
create_user(**user_data)
