"""shop.pricing.discounts"""

DISCOUNT_CODES = {
    "STUDENT10": 0.10,
    "FESTIVE20": 0.20,
}


def apply_discount(amount, code):
    """Apply a discount code; unknown codes give no discount."""
    rate = DISCOUNT_CODES.get(code.upper(), 0)
    return round(amount * (1 - rate), 2)
