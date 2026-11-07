"""
Run all 30 NumPy Python Shell labs in one go.

Usage (from your system terminal, inside this folder):
    python run_all_labs.py

Each lab prints its title, the command and the result exactly as the
Python Shell would show it, so learners can compare with their own output.
"""
import numpy as np

LABS = [
    ("LAB 01 - Check NumPy installation", None),
    ("LAB 02 - Check NumPy version", "np.__version__"),
    ("LAB 03 - Create a simple array", "np.array([10, 20, 30, 40])"),
    ("LAB 04 - Create an array of zeros", "np.zeros(5)"),
    ("LAB 05 - Create an array of ones", "np.ones(4)"),
    ("LAB 06 - Create an array filled with a value", "np.full(5, 7)"),
    ("LAB 07 - Create a range of values", "np.arange(1, 11)"),
    ("LAB 08 - Create evenly spaced values", "np.linspace(0, 10, 5)"),
    ("LAB 09 - Create a 1D array", "np.array([1, 2, 3, 4, 5])"),
    ("LAB 10 - Create a 2D array", "np.array([[1, 2, 3], [4, 5, 6]])"),
    ("LAB 11 - Create a 3D array", "np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])"),
    ("LAB 12 - Create an identity matrix", "np.eye(3)"),
    ("LAB 13 - Check number of dimensions", "np.array([[1, 2], [3, 4]]).ndim"),
    ("LAB 14 - Check array shape", "np.array([[1, 2, 3], [4, 5, 6]]).shape"),
    ("LAB 15 - Count array elements", "np.array([[1, 2, 3], [4, 5, 6]]).size"),
    ("LAB 16 - Check data type", "np.array([1, 2, 3]).dtype"),
    ("LAB 17 - Check bytes per element", "np.array([1, 2, 3], dtype=np.int32).itemsize"),
    ("LAB 18 - Access the first element", "np.array([10, 20, 30, 40])[0]"),
    ("LAB 19 - Access the last element", "np.array([10, 20, 30, 40])[-1]"),
    ("LAB 20 - Slice an array", "np.array([10, 20, 30, 40, 50])[1:4]"),
    ("LAB 21 - Add two arrays", "np.array([1, 2, 3]) + np.array([10, 20, 30])"),
    ("LAB 22 - Subtract arrays", "np.array([10, 20, 30]) - np.array([1, 2, 3])"),
    ("LAB 23 - Multiply array elements", "np.array([2, 3, 4]) * np.array([5, 6, 7])"),
    ("LAB 24 - Multiply an array by a number", "np.array([1, 2, 3]) * 10"),
    ("LAB 25 - Find the sum", "np.sum([10, 20, 30, 40])"),
    ("LAB 26 - Find the mean", "np.mean([10, 20, 30, 40])"),
    ("LAB 27 - Find the maximum", "np.max([10, 50, 20, 40])"),
    ("LAB 28 - Find the minimum", "np.min([10, 50, 20, 40])"),
    ("LAB 29 - Sort an array", "np.sort([30, 10, 40, 20])"),
    ("LAB 30 - Reshape an array", "np.arange(1, 7).reshape(2, 3)"),
]

for title, command in LABS:
    print("=" * 60)
    print(title)
    print("-" * 60)
    print(">>> import numpy as np")
    if command:
        print(">>>", command)
        print(repr(eval(command)))
    else:
        print("(no output means NumPy imported successfully)")
    print()

print("All 30 labs completed successfully.")
