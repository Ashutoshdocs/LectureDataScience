"""Lecture 22: Project: payment system (ABC, template method, mixins, polymorphism, dataclasses, exceptions)."""
import itertools
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------- exceptions ----------
class PaymentError(Exception):
    """Base class: catch this to handle any payment problem."""


class InvalidDetails(PaymentError):
    pass


class LimitExceeded(PaymentError):
    pass


class InsufficientBalance(PaymentError):
    pass


class RefundNotAllowed(PaymentError):
    pass


# ---------- data ----------
@dataclass
class CartItem:
    name: str
    price: float
    qty: int = 1

    @property
    def total(self):
        return self.price * self.qty


@dataclass(frozen=True)
class Transaction:
    txn_id: str
    method: str
    amount: float
    fee: float
    status: str = "PAID"

    @property
    def charged(self):
        return round(self.amount + self.fee, 2)

    def __str__(self):
        return f"{self.txn_id} {self.status:<8} {self.method:<22} amount {self.amount:>9,.2f} + fee {self.fee:>6,.2f} = {self.charged:>9,.2f}"


class Cart:
    def __init__(self):
        self._items = []

    def add(self, name, price, qty=1):
        if price <= 0 or qty < 1:
            raise ValueError("price must be > 0 and qty >= 1")
        self._items.append(CartItem(name, price, qty))
        return self

    @property
    def total(self):
        return round(sum(i.total for i in self._items), 2)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)


# ---------- abstraction ----------
class PaymentMethod(ABC):
    NAME = "payment"
    MAX_AMOUNT = float("inf")
    _ids = itertools.count(1)
    log = []                                          # shared transaction log

    def pay(self, amount):                            # TEMPLATE METHOD: fixed steps
        self.validate()
        if amount > self.limit():
            raise LimitExceeded(f"{self.NAME} limit is {self.limit():,.0f}, tried {amount:,.2f}")
        fee = round(self.fee(amount), 2)
        self._process(amount + fee)
        txn = Transaction(f"T{next(self._ids):04d}", self.describe(), amount, fee)
        PaymentMethod.log.append(txn)
        return txn

    def limit(self):
        return self.MAX_AMOUNT

    def describe(self):
        return self.NAME

    @abstractmethod
    def validate(self):
        ...

    @abstractmethod
    def fee(self, amount):
        ...

    @abstractmethod
    def _process(self, total):
        ...


class RefundableMixin:
    def refund(self, txn):
        log = PaymentMethod.log                       # check the CURRENT status, not the caller's copy
        index = next((i for i, t in enumerate(log) if t.txn_id == txn.txn_id), None)
        if index is None:
            raise RefundNotAllowed(f"{txn.txn_id} is not a known transaction")
        current = log[index]
        if current.status != "PAID":
            raise RefundNotAllowed(f"{txn.txn_id} is already {current.status}")
        if current.method != self.describe():
            raise RefundNotAllowed(f"{txn.txn_id} was not paid with {self.describe()}")
        self._reverse(current.charged)
        log[index] = Transaction(current.txn_id, current.method, current.amount, current.fee, status="REFUNDED")
        return log[index]

    def _reverse(self, total):                        # default: nothing to undo locally
        pass


# ---------- concrete methods ----------
class UPI(PaymentMethod):
    NAME = "UPI"
    MAX_AMOUNT = 100_000

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def validate(self):
        if not re.fullmatch(r"[\w.\-]+@[a-z]+", self.upi_id):
            raise InvalidDetails(f"bad UPI id {self.upi_id!r}")

    def fee(self, amount):
        return 0

    def _process(self, total):
        pass                                          # pretend to call the UPI network

    def describe(self):
        return f"UPI {self.upi_id}"


class Card(RefundableMixin, PaymentMethod):
    NAME = "Card"
    MAX_AMOUNT = 200_000

    def __init__(self, number, expiry):
        digits = number.replace(" ", "")
        self._valid_number = digits.isdigit() and len(digits) == 16 and self._luhn(digits)
        self._masked = "**** " + digits[-4:]          # never keep the full number around
        self.expiry = expiry

    @classmethod
    def from_string(cls, text):                       # "4111 1111 1111 1111|12/28"
        number, expiry = text.split("|")
        return cls(number, expiry)

    @staticmethod
    def _luhn(digits):
        total = 0
        for i, d in enumerate(reversed(digits)):
            n = int(d)
            if i % 2:
                n = n * 2 - 9 if n > 4 else n * 2
            total += n
        return total % 10 == 0

    def validate(self):
        if not self._valid_number:
            raise InvalidDetails(f"card {self._masked} failed the number check")
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d\d", self.expiry):
            raise InvalidDetails(f"bad expiry {self.expiry!r}")

    def fee(self, amount):
        return amount * 0.02

    def _process(self, total):
        pass

    def describe(self):
        return f"Card {self._masked}"


class Wallet(RefundableMixin, PaymentMethod):
    NAME = "Wallet"

    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def limit(self):                                  # overridden: limit is the balance
        return self._balance

    def validate(self):
        if self._balance <= 0:
            raise InsufficientBalance(f"{self.owner}'s wallet is empty")

    def fee(self, amount):
        return max(5, amount * 0.01)

    def _process(self, total):
        if total > self._balance:
            raise InsufficientBalance(f"wallet has {self._balance:,.2f}, needs {total:,.2f} incl. fee")
        self._balance = round(self._balance - total, 2)

    def _reverse(self, total):
        self._balance = round(self._balance + total, 2)

    def describe(self):
        return f"Wallet ({self.owner})"


class CashOnDelivery(PaymentMethod):
    NAME = "Cash on delivery"
    MAX_AMOUNT = 10_000

    def validate(self):
        pass

    def fee(self, amount):
        return 40

    def _process(self, total):
        pass


# ---------- checkout depends only on the abstraction ----------
class Checkout:
    def __init__(self, cart):
        self.cart = cart

    def pay(self, method: PaymentMethod):
        if not isinstance(method, PaymentMethod):
            raise TypeError("method must be a PaymentMethod")
        if not len(self.cart):
            raise PaymentError("cart is empty")
        return method.pay(self.cart.total)


def try_pay(checkout, method):
    try:
        txn = checkout.pay(method)
        print(f"  ✔ {txn}")
        return txn
    except PaymentError as e:
        print(f"  ✘ {method.describe():<22} {type(e).__name__}: {e}")


def main():
    cart = Cart().add("Headphones", 2499).add("Phone case", 399, 2).add("Cable", 199)
    checkout = Checkout(cart)
    print(f"=== Cart: {len(cart)} lines, total Rs {cart.total:,.2f} ===")
    for item in cart:
        print(f"    {item.name:<12} {item.qty} x {item.price:>7,.2f} = {item.total:>8,.2f}")

    print("\n=== Same checkout, different payment methods (polymorphism) ===")
    asha_wallet = Wallet("Asha", 5000)
    card = Card.from_string("4111 1111 1111 1111|12/28")
    txns = [try_pay(checkout, m) for m in [
        UPI("asha@okbank"),
        card,
        asha_wallet,
        CashOnDelivery(),
        UPI("not a upi id"),
        Card("1234 5678 9012 3456", "12/28"),
        Card("4111 1111 1111 1111", "13/28"),
        Wallet("Ravi", 1000),
        Wallet("Dev", 0),
    ]]
    print(f"  Asha's wallet balance now: {asha_wallet.balance:,.2f}")

    print("\n=== Limits ===")
    big = Checkout(Cart().add("Laptop", 150_000))
    big_results = [try_pay(big, m) for m in (UPI("asha@okbank"), card, CashOnDelivery())]
    laptop_txn = big_results[1]

    print("\n=== Refunds (only where RefundableMixin was mixed in) ===")
    card_txn, wallet_txn, upi_txn = txns[1], txns[2], txns[0]
    print("  ", card.refund(card_txn))
    print("  ", asha_wallet.refund(wallet_txn), f"-> wallet back to {asha_wallet.balance:,.2f}")
    for label, method, txn in [("refund the same receipt twice", card, card_txn),
                               ("refund a card payment to the wallet", asha_wallet, laptop_txn)]:
        try:
            method.refund(txn)
        except RefundNotAllowed as e:
            print(f"   {label} -> RefundNotAllowed: {e}")
    print("   UPI has refund()?", hasattr(UPI("a@b"), "refund"), "| Card has refund()?", hasattr(card, "refund"))

    print("\n=== Transaction log ===")
    for t in PaymentMethod.log:
        print("  ", t)
    try:
        upi_txn.status = "HACKED"
    except Exception as e:
        print("   transactions are immutable ->", type(e).__name__)
    print("   Card MRO:", " -> ".join(c.__name__ for c in Card.__mro__))
    try:
        checkout.pay("cash")
    except TypeError as e:
        print("   checkout.pay('cash') -> TypeError:", e)


if __name__ == "__main__":
    main()
