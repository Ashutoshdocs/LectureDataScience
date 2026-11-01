"""cafe/orders.py — uses menu.py from the SAME package."""

# Relative import: the dot means "from this same package".
# Same as:  from cafe.menu import PRICES
from .menu import PRICES


class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add(self, item):
        if item not in PRICES:
            raise ValueError(f"{item!r} is not on the menu")
        self.items.append(item)

    def total(self):
        return sum(PRICES[i] for i in self.items)
