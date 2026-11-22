"""Lecture 00: Prerequisites, and the copy-paste problem that functions solve."""

print("=== The copy-paste problem (no functions) ===")
class_a = [78, 92, 45, 83]
class_b = [67, 71, 88]
class_c = [95, 59, 73, 64, 80]

total = 0
for m in class_a:
    total += m
avg_a = total / len(class_a)
print("Class A average:", round(avg_a, 2))

total = 0
for m in class_b:
    total += m
avg_b = total / len(class_b)
print("Class B average:", round(avg_b, 2))

total = 0
for m in class_c:
    total += m
avg_c = total / len(class_a)          # BUG: copied from block A and not updated!
print("Class C average:", round(avg_c, 2), "<- wrong: the copy still divides by len(class_a)")
print("Same logic written 3 times = 3 places for bugs. Lecture 01 fixes this with one function.")

print("\n=== Skills you'll need ===")
for n in range(1, 6):
    print(f"  {n} squared is {n ** 2}")

for n in [-3, 0, 7]:
    if n < 0:
        label = "negative"
    elif n == 0:
        label = "zero"
    else:
        label = "positive"
    print(f"  {n}: {label}")

print("\n=== Mutable vs immutable ===")
a = [1, 2]
b = a
b.append(3)
print("  list a after appending through b:", a, "(same list)")
x = 5
y = x
y += 1
print("  int x after y += 1:", x, "(ints can't change; y is a new int)")
