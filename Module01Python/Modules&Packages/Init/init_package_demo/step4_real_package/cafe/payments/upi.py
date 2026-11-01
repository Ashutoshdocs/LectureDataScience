"""cafe/payments/upi.py"""

# Two dots = go UP one level to the parent package 'cafe'.
# Same as:  from cafe import SHOP_NAME
from .. import SHOP_NAME


def pay_upi(order, upi_id):
    return (f"Paid Rs {order.total()} by UPI from {upi_id} "
            f"to {SHOP_NAME} for order #{order.number}")
