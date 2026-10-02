from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import service

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str


@router.post("/signup")
def signup(req: SignupRequest):
    try:
        return service.signup(req.email, req.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(req: LoginRequest):
    try:
        return service.login(req.email, req.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    # Note: bug #1 raises an unhandled KeyError here (not a ValueError),
    # which FastAPI will turn into a 500 — that's intentional, see service.py.


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest):
    try:
        return service.reset_password(req.email, req.new_password)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
