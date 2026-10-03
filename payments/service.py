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
    try:
        result = _call_payment_gateway(amount, simulate_timeout=simulate_timeout)
        return result
    except PaymentGatewayTimeout as e:
        return {"status": "failed", "reason": str(e)}
