"""
Python int Data Type Lab - Answers to the 20 Practical Questions.

Run:  python answers.py
"""

print("Q1. Create an integer variable and print its value")
marks = 85
print(marks)

print("\nQ2. Check the data type of an integer using type()")
year = 2026
print(type(year))

print("\nQ3. Create a positive integer")
students = 45
print(students)
print(students > 0)

print("\nQ4. Create a negative integer")
balance = -750
print(balance)
print(balance < 0)

print("\nQ5. Create an integer with value 0")
score = 0
print(score)
print(type(score))

print("\nQ6. Perform addition of two integers")
a = 25
b = 15
print(a + b)

print("\nQ7. Perform subtraction of two integers")
a = 100
b = 35
print(a - b)

print("\nQ8. Perform multiplication of two integers")
a = 12
b = 8
print(a * b)

print("\nQ9. Perform division of two integers")
a = 20
b = 4
print(a / b)
print(type(a / b))

print("\nQ10. Perform floor division of two integers")
a = 17
b = 5
print(a // b)

print("\nQ11. Find the remainder using %")
a = 17
b = 5
print(a % b)

print("\nQ12. Calculate power using **")
base = 5
exponent = 3
print(base ** exponent)

print("\nQ13. Convert a string into an integer using int()")
text = "250"
number = int(text)
print(number)
print(type(number))
print(number + 50)

print("\nQ14. Convert a float into an integer")
price = 99.99
print(int(price))

print("\nQ15. Find the absolute value using abs()")
loss = -320
print(abs(loss))

print("\nQ16. Calculate power using pow()")
print(pow(3, 4))

print("\nQ17. Compare two integers using comparison operators")
x = 15
y = 25
print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

print("\nQ18. Create and print a very large integer")
big = 123456789012345678901234567890123456789
print(big)
print(type(big))
print(2 ** 100)

print("\nQ19. Round a number using round()")
print(round(7.6))
print(round(7.4))
print(round(3.14159, 2))

print("\nQ20. Program demonstrating different integer operators")
a = 17
b = 5
print("a =", a, " b =", b)
print("Addition       :", a + b)
print("Subtraction    :", a - b)
print("Multiplication :", a * b)
print("Division       :", a / b)
print("Floor Division :", a // b)
print("Remainder      :", a % b)
print("Power          :", a ** b)
print("Equal          :", a == b)
print("Not Equal      :", a != b)
print("Greater        :", a > b)
print("Less           :", a < b)
