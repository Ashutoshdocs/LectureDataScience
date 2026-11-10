"""
MODULE 5: RETURN STATEMENT

print() displays a value.
return sends a value back to the caller.
"""


# A. print() does not return the displayed result
def add_and_print(a, b):
    print(a + b)


result = add_and_print(10, 20)
print("Stored result:", result)  # None


# B. return sends the result back
def add_and_return(a, b):
    return a + b


result = add_and_return(10, 20)
print("Returned result:", result)


# C. Reuse a returned value
def calculate_total(price, quantity):
    return price * quantity


total = calculate_total(500, 3)
discount = total * 0.10
final_amount = total - discount

print("Total:", total)
print("Discount:", discount)
print("Final amount:", final_amount)


# D. Return multiple values (Python packs them into a tuple)
def calculate(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    return addition, subtraction, multiplication


add_result, sub_result, mul_result = calculate(20, 10)
print(add_result, sub_result, mul_result)


# E. return exits the function immediately
def check():
    print("Step 1")
    return "Finished"
    print("Step 2 - this line will not execute")


message = check()
print(message)


# F. No explicit return means Python returns None
def say_hello():
    print("Hello!")


answer = say_hello()
print("Return value:", answer)
