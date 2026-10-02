from fastapi import APIRouter
from pydantic import BaseModel

from . import service

router = APIRouter(prefix="/checkout", tags=["checkout"])


class CartItem(BaseModel):
    price: float
    quantity: int


class CheckoutRequest(BaseModel):
    items: list[CartItem]
    discount_code: str | None = None


@router.post("/total")
def get_total(req: CheckoutRequest):
    items = [item.dict() for item in req.items]
    total = service.calculate_total(items, req.discount_code)
    return {"total": total}
