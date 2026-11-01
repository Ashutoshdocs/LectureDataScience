"""cafe/payments/cash.py"""


def pay_cash(order, given):
    change = given - order.total()
    if change < 0:
        raise ValueError(f"Need Rs {-change} more")
    return f"Paid cash for order #{order.number}. Change: Rs {change}"
