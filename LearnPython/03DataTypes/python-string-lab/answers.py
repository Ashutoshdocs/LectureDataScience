"""
Python String Methods Lab - Answers to the 15 Student Practice Tasks.

Run:  python answers.py      (needs Python 3.9+ for Q13 and Q14)
"""

print("Q1. Convert 'python programming' to uppercase")
print("python programming".upper())

print("\nQ2. Convert 'PYTHON PROGRAMMING' to lowercase")
print("PYTHON PROGRAMMING".lower())

print("\nQ3. Convert 'hello world' to title case")
print("hello world".title())

print("\nQ4. How many times does 'a' appear in 'banana'?")
print("banana".count("a"))

print("\nQ5. Find 'Python' in 'I love Python'")
text = "I love Python"
print(text.find("Python"))
print("Python" in text)

print("\nQ6. Replace 'World' with 'Python' in 'Hello World'")
print("Hello World".replace("World", "Python"))

print("\nQ7. Remove the extra spaces from '   Python   '")
print("   Python   ".strip())
print(repr("   Python   ".strip()))

print("\nQ8. Convert 'Python Docker Kubernetes' into a list")
print("Python Docker Kubernetes".split())

print("\nQ9. Join ['Python', 'Docker', 'Kubernetes'] using '-'")
print("-".join(["Python", "Docker", "Kubernetes"]))

print("\nQ10. Check whether 'Python123' is alphanumeric")
print("Python123".isalnum())

print("\nQ11. Check whether 'Python' is alphabetic")
print("Python".isalpha())

print("\nQ12. Make '12345' 10 characters long using zfill()")
print("12345".zfill(10))

print("\nQ13. Remove 'Mr. ' from 'Mr. Sanjay'")
print("Mr. Sanjay".removeprefix("Mr. "))

print("\nQ14. Remove '.txt' from 'python.txt'")
print("python.txt".removesuffix(".txt"))

print("\nQ15. Check whether 'PYTHON' is uppercase")
print("PYTHON".isupper())
