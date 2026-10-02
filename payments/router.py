from fastapi import APIRouter
from pydantic import BaseModel

from . import service

router = APIRouter(prefix="/payments", tags=["payments"])


class PaymentRequest(BaseModel):
    amount: float
    simulate_timeout: bool = False


@router.post("/pay")
def pay(req: PaymentRequest):
    # Note: bug #4 means a timeout here raises an unhandled exception,
    # which FastAPI turns into a 500 — that's intentional, see service.py.
    result = service.process_payment(req.amount, req.simulate_timeout)
    return result
