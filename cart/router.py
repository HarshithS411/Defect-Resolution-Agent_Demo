from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import service

router = APIRouter(prefix="/cart", tags=["cart"])


class CartItemRequest(BaseModel):
    cart_id: str
    item_id: str
    quantity: int


@router.post("/add")
def add_item(req: CartItemRequest):
    return service.add_item(req.cart_id, req.item_id, req.quantity)


@router.post("/update")
def update_quantity(req: CartItemRequest):
    try:
        return service.update_quantity(req.cart_id, req.item_id, req.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cart_id}")
def get_cart(cart_id: str):
    return service.get_cart(cart_id)
