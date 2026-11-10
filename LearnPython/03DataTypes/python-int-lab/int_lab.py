"""
Python int Data Type Lab - all 20 labs in one script.

Run:  python int_lab.py
"""

print("01. Creating an integer variable")
age = 25
print(age)

print("\n02. Checking the integer data type - type()")
number = 100
print(type(number))

print("\n03. Positive integer")
number = 500
print(number)

print("\n04. Negative integer")
temperature = -10
print(temperature)

print("\n05. Zero integer")
number = 0
print(number)
print(type(number))

print("\n06. Integer addition")
a = 10
b = 20
result = a + b
print(result)

print("\n07. Integer subtraction")
a = 50
b = 20
result = a - b
print(result)

print("\n08. Integer multiplication")
a = 10
b = 5
result = a * b
print(result)

print("\n09. Integer division - /")
a = 10
b = 2
result = a / b
print(result)

print("\n10. Floor division - //")
a = 10
b = 3
result = a // b
print(result)

print("\n11. Modulus - %")
a = 10
b = 3
result = a % b
print(result)

print("\n12. Power operator - **")
a = 2
b = 3
result = a ** b
print(result)

print("\n13. Integer comparison")
a = 10
b = 20
print(a == b)
print(a < b)
print(a > b)

print("\n14. Converting to integer - int()")
number = int("100")
print(number)
print(type(number))

print("\n15. Converting float to integer")
number = int(10.99)
print(number)

print("\n16. Converting boolean to integer")
print(int(True))
print(int(False))

print("\n17. Large integer")
number = 999999999999999999999999999999
print(number)

print("\n18. Integer absolute value - abs()")
number = -50
print(abs(number))

print("\n19. Integer power - pow()")
result = pow(2, 5)
print(result)

print("\n20. Integer rounding - round()")
number = 10.75
result = round(number)
print(result)
print(type(result))

print("\nAll 20 labs completed successfully.")
