"""cafe/orders.py"""

from .menu import PRICES
from . import _counter          # private helper module (underscore = internal)


class Order:
    def __init__(self, customer):
        self.number = _counter.next_number()
        self.customer = customer
        self.items = []

    def add(self, item):
        if item not in PRICES:
            raise ValueError(f"{item!r} is not on the menu")
        self.items.append(item)

    def total(self):
        return sum(PRICES[i] for i in self.items)

    def __repr__(self):
        return f"Order #{self.number} for {self.customer}: {self.items}"
