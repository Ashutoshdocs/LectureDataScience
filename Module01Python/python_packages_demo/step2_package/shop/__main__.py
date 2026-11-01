"""Runs when you execute the package itself:   python -m shop"""

from shop import Cart

cart = Cart().add("Notebook", 50, 3).add("Pen", 10, 5)
print(cart)
print("Total with GST:", cart.total())
