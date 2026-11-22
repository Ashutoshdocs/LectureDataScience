# Program 2: Calculate the perimeter of a rectangle
# Notice that the rectangle input/validation logic is repeated here.

def calculate_perimeter(length, width):
    return 2 * (length + width)

length = 10
width = 5

perimeter = calculate_perimeter(length, width)
print("Program 2")
print("Length:", length)
print("Width:", width)
print("Perimeter:", perimeter)
