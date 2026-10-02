"""Payments business logic — deliberately contains one bug (see
tests/test_payments.py).
"""


class PaymentGatewayTimeout(Exception):
    """Raised when the (simulated) external payment gateway doesn't respond."""


def _call_payment_gateway(amount: float, simulate_timeout: bool = False) -> dict:
    """Stands in for a real call to an external payment provider."""
    if simulate_timeout:
        raise PaymentGatewayTimeout("Payment gateway timeout: no response received")
    return {"status": "success", "amount": amount}


def process_payment(amount: float, simulate_timeout: bool = False) -> dict:
    # BUG (ticket: "payment fails with unhandled error during gateway
    # timeout"): there's no error handling around the gateway call, so a
    # timeout bubbles up as an unhandled exception (-> 500) instead of a
    # clean, user-facing "payment failed" response.
    result = _call_payment_gateway(amount, simulate_timeout=simulate_timeout)
    return result
