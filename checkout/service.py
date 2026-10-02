"""Checkout business logic — deliberately contains one bug (see
tests/test_checkout.py).
"""


def calculate_total(items: list[dict], discount_code: str | None = None) -> float:
    subtotal = sum(item["price"] * item["quantity"] for item in items)

    if discount_code == "SAVE10":
        # BUG (ticket: "checkout total wrong when a discount code is applied"):
        # SAVE10 is supposed to mean "10% off", but this subtracts a flat 10
        # currency units instead, which is only correct by coincidence when
        # the subtotal happens to be exactly 100.
        subtotal = subtotal - 10

    return round(subtotal, 2)
