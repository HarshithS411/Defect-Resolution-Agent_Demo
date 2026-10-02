"""Cart business logic — deliberately contains one bug (see
tests/test_cart.py).
"""

# Tiny in-memory "database" of carts: {cart_id: {item_id: quantity}}
_carts: dict[str, dict[str, int]] = {}


def add_item(cart_id: str, item_id: str, quantity: int) -> dict:
    cart = _carts.setdefault(cart_id, {})
    cart[item_id] = cart.get(item_id, 0) + quantity
    return cart


def update_quantity(cart_id: str, item_id: str, quantity: int) -> dict:
    cart = _carts.setdefault(cart_id, {})
    # BUG (ticket: "cart allows negative item quantity"): there's no
    # validation here, so a negative quantity is accepted as-is, which can
    # drive a line item (and the checkout total) negative.
    cart[item_id] = quantity
    return cart


def get_cart(cart_id: str) -> dict:
    return _carts.get(cart_id, {})
