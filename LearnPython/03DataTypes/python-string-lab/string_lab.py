"""
Python String (str) Methods Lab - all 48 labs in one script.

Run:  python string_lab.py      (needs Python 3.9+ for removeprefix/removesuffix)
"""


def lab(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


# ---------------- PART A: CASE CONVERSION ----------------
lab("01. upper()")
name = "sanjay"
print(name.upper())

lab("02. lower()")
name = "SANJAY"
print(name.lower())

lab("03. capitalize()")
name = "sanjay dahiya"
print(name.capitalize())

lab("04. title()")
name = "sanjay dahiya"
print(name.title())

lab("05. swapcase()")
name = "SaNjAy"
print(name.swapcase())

lab("06. casefold()")
name = "SANJAY"
print(name.casefold())

# ---------------- PART B: SEARCHING & COUNTING ----------------
lab("07. count()")
name = "banana"
print(name.count("a"))

lab("08. find()")
name = "sanjay"
print(name.find("j"))

lab("09. rfind()")
name = "banana"
print(name.rfind("a"))

lab("10. index()")
name = "sanjay"
print(name.index("j"))

lab("11. rindex()")
name = "banana"
print(name.rindex("a"))

lab("12. startswith()")
name = "sanjay"
print(name.startswith("san"))

lab("13. endswith()")
name = "sanjay"
print(name.endswith("jay"))

# ---------------- PART C: MODIFYING & CLEANING ----------------
lab("14. replace()")
name = "Hello Sanjay"
print(name.replace("Sanjay", "Rahul"))

lab("15. strip()")
name = "   Sanjay   "
print(name.strip())

lab("16. lstrip()")
name = "   Sanjay"
print(name.lstrip())

lab("17. rstrip()")
name = "Sanjay   "
print(name.rstrip())

# ---------------- PART D: SPLITTING & JOINING ----------------
lab("18. split()")
name = "Sanjay Dahiya Trainer"
print(name.split())

lab("19. rsplit()")
data = "Python-Docker-Kubernetes"
print(data.rsplit("-", 1))

lab("20. splitlines()")
data = "Python\nDocker\nKubernetes"
print(data.splitlines())

lab("21. partition()")
data = "Python-Docker"
print(data.partition("-"))

lab("22. rpartition()")
data = "Python-Docker-Kubernetes"
print(data.rpartition("-"))

lab("23. join()")
names = ["Sanjay", "Rahul", "Amit"]
print("-".join(names))

# ---------------- PART E: ALIGNMENT & PADDING ----------------
lab("24. center()")
name = "Python"
print(name.center(20, "-"))

lab("25. ljust()")
name = "Python"
print(name.ljust(10, "-"))

lab("26. rjust()")
name = "Python"
print(name.rjust(10, "-"))

lab("27. zfill()")
number = "123"
print(number.zfill(6))

# ---------------- PART F: CHECKING (is...) METHODS ----------------
lab("28. isalnum()")
value = "Python123"
print(value.isalnum())

lab("29. isalpha()")
value = "Python"
print(value.isalpha())

lab("30. isascii()")
value = "Python123"
print(value.isascii())

lab("31. isdecimal()")
value = "12345"
print(value.isdecimal())

lab("32. isdigit()")
value = "12345"
print(value.isdigit())

lab("33. isnumeric()")
value = "12345"
print(value.isnumeric())

lab("34. isidentifier()")
value = "student_name"
print(value.isidentifier())

lab("35. islower()")
value = "python"
print(value.islower())

lab("36. isupper()")
value = "PYTHON"
print(value.isupper())

lab("37. istitle()")
value = "Python Programming"
print(value.istitle())

lab("38. isspace()")
value = "   "
print(value.isspace())

lab("39. isprintable()")
value = "Hello Python"
print(value.isprintable())

# ---------------- PART G: ENCODING & FORMATTING ----------------
lab("40. encode()")
name = "Python"
print(name.encode())

lab("41. format()")
name = "Sanjay"
course = "Python"
message = "My name is {} and I teach {}."
print(message.format(name, course))

lab("42. format_map()")
data = {
    "name": "Sanjay",
    "course": "Python"
}
message = "My name is {name} and I teach {course}."
print(message.format_map(data))

# ---------------- PART H: ADVANCED METHODS ----------------
lab("43. maketrans()")
table = str.maketrans("abc", "123")
print("abc".translate(table))

lab("44. translate()")
table = str.maketrans("abc", "123")
text = "abcabc"
print(text.translate(table))

lab("45. removeprefix()")
name = "Mr. Sanjay"
print(name.removeprefix("Mr. "))

lab("46. removesuffix()")
file = "python.txt"
print(file.removesuffix(".txt"))

lab("47. expandtabs()")
data = "Python\tDocker"
print(data.expandtabs(4))

lab("48. __contains__() / in")
name = "Sanjay"
print("jay" in name)

print("\nAll 48 labs completed successfully.")
