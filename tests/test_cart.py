import pytest

from cart import service as cart_service


def test_cart_negative_quantity():
    """SCRUM ticket: cart allows negative item quantity.
    update_quantity should reject a negative quantity instead of silently
    accepting it — see cart/service.py.
    """
    with pytest.raises(ValueError):
        cart_service.update_quantity("cart-1", "item-1", -5)
