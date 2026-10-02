"""Auth business logic — deliberately contains two bugs for the defect-agent
project to find and fix (see the tests in tests/test_auth.py).
"""

import hashlib
import time

# Tiny in-memory "database" of users, keyed by email.
_users: dict[str, dict] = {}

TOKEN_LIFETIME_MINUTES = 30


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def signup(email: str, password: str) -> dict:
    if email in _users:
        raise ValueError("User already exists")
    _users[email] = {
        "email": email,
        "password_hash": _hash_password(password),
        "token_issued_at": None,
        "token_expires_at": None,
    }
    return {"email": email}


def issue_token(email: str) -> str:
    user = _users[email]
    now = time.time()
    # BUG (ticket: "users get logged out a few minutes after login"):
    # TOKEN_LIFETIME_MINUTES is a count of MINUTES, but it's added to `now`
    # (seconds since epoch) without converting to seconds first. The token
    # ends up expiring in 30 *seconds* instead of 30 *minutes*.
    expires_at = now + TOKEN_LIFETIME_MINUTES
    user["token_issued_at"] = now
    user["token_expires_at"] = expires_at
    return f"token-{email}-{int(expires_at)}"


def is_token_valid(email: str) -> bool:
    user = _users.get(email)
    if not user or user.get("token_expires_at") is None:
        return False
    return time.time() < user["token_expires_at"]


def login(email: str, password: str) -> dict:
    user = _users.get(email)
    if not user:
        raise ValueError("Invalid credentials")
    if user["password_hash"] != _hash_password(password):
        raise ValueError("Invalid credentials")
    token = issue_token(email)
    return {"email": email, "token": token}


def reset_password(email: str, new_password: str) -> dict:
    user = _users.get(email)
    if not user:
        raise ValueError("User not found")
    # BUG (ticket: "login fails with 500 error after password reset"):
    # this deletes the key that login() depends on, instead of updating it
    # in place. The next login() call does user["password_hash"] on a user
    # dict that no longer has that key -> unhandled KeyError -> 500.
    del user["password_hash"]
    user["password_hash_updated"] = _hash_password(new_password)
    return {"email": email, "status": "password reset"}
