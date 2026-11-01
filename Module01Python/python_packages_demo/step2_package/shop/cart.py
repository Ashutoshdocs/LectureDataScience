"""shop.cart - a module inside the shop package."""

# Relative import from a SUB-PACKAGE of the same package
from .pricing import apply_discount, add_tax


class Cart:
    def __init__(self):
        self.items = []  # list of (name, price, qty)

    def add(self, name, price, qty=1):
        self.items.append((name, price, qty))
        return self  # allows chaining: cart.add(...).add(...)

    def subtotal(self):
        return sum(price * qty for _, price, qty in self.items)

    def total(self, discount_code=None):
        amount = self.subtotal()
        if discount_code:
            amount = apply_discount(amount, discount_code)
        return add_tax(amount)

    def __repr__(self):
        return f"Cart({len(self.items)} items, subtotal={self.subtotal():.2f})"
