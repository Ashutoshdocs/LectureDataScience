# Common module with a little extra reusable functionality.

def calculate_area(length, width):
    return length * width

def calculate_perimeter(length, width):
    return 2 * (length + width)

def describe_rectangle(length, width):
    print("Rectangle details")
    print("Length:", length)
    print("Width:", width)
    print("Area:", calculate_area(length, width))
    print("Perimeter:", calculate_perimeter(length, width))
