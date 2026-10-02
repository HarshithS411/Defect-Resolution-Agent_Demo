from checkout import service as checkout_service


def test_checkout_with_discount():
    """SCRUM ticket: checkout total wrong when a discount code is applied.
    SAVE10 should mean 10% off, not a flat $10 off — see checkout/service.py.
    """
    items = [{"price": 60.0, "quantity": 2}]  # subtotal = 120.0

    total = checkout_service.calculate_total(items, discount_code="SAVE10")

    assert total == 108.0  # 10% off 120.0
