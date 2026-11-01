"""shop.pricing.tax"""

GST_RATE = 0.18


def add_tax(amount, rate=GST_RATE):
    return round(amount * (1 + rate), 2)
