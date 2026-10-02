from payments import service as payments_service


def test_payment_gateway_timeout():
    """SCRUM ticket: payment fails with unhandled error during gateway
    timeout. A timeout should come back as a clean 'failed' result, not an
    unhandled exception — see payments/service.py.
    """
    result = payments_service.process_payment(100.0, simulate_timeout=True)

    assert result["status"] == "failed"
    assert "timeout" in result["reason"].lower()
