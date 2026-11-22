# Lecture 22: Project: payment system

Run: `python lecture.py`

A checkout system that accepts several payment methods, each with its own fees, limits and validation, and supports refunds, receipts and a transaction log. This project focuses on **abstraction + polymorphism + mixins + custom exceptions**.

## Class design

```
 PaymentMethod (ABC)                        Checkout ──uses──▶ PaymentMethod   (dependency injection)
   ├── UPI                                     │
   ├── Card        (+ RefundableMixin)         └──has──▶ Cart ──has many──▶ CartItem (dataclass)
   ├── Wallet      (+ RefundableMixin)                    │
   └── CashOnDelivery                                     └──produces──▶ Transaction (frozen dataclass)

 PaymentError ─┬─ InvalidDetails
               ├─ LimitExceeded
               ├─ InsufficientBalance
               └─ RefundNotAllowed
```

| Concept | Where |
|---------|-------|
| **Abstraction** | `PaymentMethod` declares `validate()`, `_process()` and `fee()`; `Checkout` knows only this contract |
| **Template method** | `PaymentMethod.pay()` runs the fixed steps *validate → check limit → fee → process → record* |
| **Polymorphism** | `checkout.pay(method)` works with any method; fees and limits differ per class |
| **Inheritance** | each method overrides only what differs; class attributes `MAX_AMOUNT`, `NAME` |
| **Mixin** | `RefundableMixin.refund()` is added only to methods that support refunds |
| **Encapsulation** | card number stored masked; wallet balance read-only; `_process` internal |
| **Dataclasses** | `CartItem`, and an immutable `Transaction` (frozen) |
| **Magic methods** | `Cart.__len__`, `__iter__`, `__str__` on receipts |
| **Custom exceptions** | callers can catch `PaymentError` broadly, or one specific subclass |
| **Class method** | `Card.from_string("4111 1111 1111 1111|12/28")` alternative constructor |

## Fees and limits

| Method | Fee | Max per payment | Refundable |
|--------|-----|-----------------|------------|
| UPI | 0 | 1,00,000 | no |
| Card | 2% | 2,00,000 | yes |
| Wallet | 1% (min Rs 5) | the wallet balance | yes |
| Cash on delivery | flat Rs 40 | 10,000 | no |

## Adding a new payment method

Write one class: subclass `PaymentMethod`, implement `validate`, `_process` and `fee`, and optionally add `RefundableMixin`. **Nothing else changes.** This is the Open/Closed principle in action.

## Extension exercises

1. Add `NetBanking(PaymentMethod)` with a bank allow-list.
2. Add split payment: pay part by wallet and the rest by UPI.
3. Add a `@retry` decorator (from the Functions course) around `_process` for flaky gateways.
4. Make refunds partial: `refund(txn, amount)`.

**Next →** [Lecture 23: Practice exercises](../23_practice_exercises/)
