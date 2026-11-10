"""
MODULE 4: PARAMETERS AND ARGUMENTS

Parameter: variable written in the function definition.
Argument: actual value supplied in the function call.
"""


# A. Non-parameterized function
def welcome():
    print("Welcome to the Python class!")


welcome()


# B. Parameterized function
def greet(name):  # name is a parameter
    print("Welcome,", name)


greet("Rahul")  # "Rahul" is an argument
greet("Amit")
greet("Priya")


# C. Multiple positional parameters
def add(a, b):
    print("Sum:", a + b)


add(10, 20)
add(100, 200)


# D. Positional arguments: values are assigned by position
def student(name, age):
    print("Name:", name)
    print("Age:", age)


student("Rahul", 25)


# E. Keyword arguments: values are assigned by parameter name
student(age=25, name="Rahul")


# F. Default parameter
def greet_with_default(name="Student"):
    print("Welcome,", name)


greet_with_default()
greet_with_default("Amit")


# G. Mixing positional and keyword arguments
def employee(name, department, city="Pune"):
    print(name, department, city)


employee("Riya", "IT")
employee("Riya", department="Cloud", city="Patna")

# Gotcha: positional arguments must come before keyword arguments in a call.
# employee(name="Riya", "IT")  # SyntaxError
