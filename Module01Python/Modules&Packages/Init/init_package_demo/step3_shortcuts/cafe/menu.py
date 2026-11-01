"""cafe/menu.py"""

PRICES = {"tea": 20, "coffee": 40, "samosa": 15}


def show_menu():
    for item, price in PRICES.items():
        print(f"  {item:<8} Rs {price}")
