"""MiniShop — a small demo FastAPI app used to test an AI defect-resolution
agent. It contains 5 deliberate bugs (see README.md), each with a failing
pytest test under tests/, and each mapped to a sample Jira ticket.

Run locally:
    uvicorn main:app --reload
Then open http://127.0.0.1:8000/docs for interactive Swagger docs.
"""

from fastapi import FastAPI

from auth.router import router as auth_router
from cart.router import router as cart_router
from checkout.router import router as checkout_router
from payments.router import router as payments_router

app = FastAPI(
    title="MiniShop",
    description="A small demo app used to test an AI defect-resolution agent.",
)

app.include_router(auth_router)
app.include_router(checkout_router)
app.include_router(payments_router)
app.include_router(cart_router)


@app.get("/")
def root():
    return {"service": "MiniShop API", "status": "running"}
