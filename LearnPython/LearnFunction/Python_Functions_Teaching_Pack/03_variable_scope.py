"""
MODULE 3: VARIABLE SCOPE

Run each section separately if you want students to predict the output.
"""


# PART A: Local variable
def show_local():
    student_name = "Rahul"  # Local to show_local()
    print("Inside function:", student_name)


show_local()

# Uncommenting the next line causes NameError because student_name is local.
# print(student_name)


# PART B: Reading a global variable
college = "PanamaTechAcademy"


def show_college():
    print("College inside function:", college)


show_college()
print("College outside function:", college)


# PART C: Local variable with the same name as a global variable
x = 100


def local_example():
    x = 50
    print("Local x:", x)


local_example()
print("Global x:", x)


# PART D: Modifying a global variable
balance = 1000


def deposit():
    global balance
    balance = balance + 500
    print("Balance inside deposit():", balance)


deposit()
print("Balance after function call:", balance)


# PART E: Enclosing scope and nonlocal
def outer():
    count = 10

    def inner():
        nonlocal count
        count += 1

    inner()
    print("Enclosing count after inner():", count)


outer()


# PART F: LEGB demonstration
name = "Global"


def outer_name():
    name = "Enclosing"

    def inner_name():
        name = "Local"
        print("LEGB lookup result:", name)

    inner_name()


outer_name()

"""
LEGB lookup order:
L = Local
E = Enclosing function
G = Global/module
B = Built-in
Python searches in this order when resolving a name.
"""
