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

# This block runs only when common.py is executed directly.
# It does not run when another file imports common.py.
if __name__ == "__main__":
    print("Testing common.py directly")
    describe_rectangle(8, 4)
