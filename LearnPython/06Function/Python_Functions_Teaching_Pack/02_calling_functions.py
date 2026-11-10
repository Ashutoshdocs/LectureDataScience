"""
MODULE 2: CALLING FUNCTIONS AND EXECUTION FLOW

Trace the output in order.
When Python reaches greet(), it enters the function body.
When the function finishes, execution continues after the call.
"""

print("1. Program started")


def greet():
    print("3. Inside the function")


print("2. Function has been defined")
print("Before function call")

greet()

print("4. Program continues after function call")
print("5. Program ended")
