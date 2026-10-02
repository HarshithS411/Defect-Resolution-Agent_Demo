# MiniShop — sample app for the defect-resolution agent

A tiny FastAPI app with 5 deliberate bugs, one per module, each with a
pytest test that currently **fails** against the buggy code and will
**pass** once the bug is fixed correctly. This is the codebase your defect
agent will read, patch, and validate against.

```
minishop/
├── main.py                 # FastAPI app, mounts all 4 routers
├── auth/        service.py # bugs #1 and #2
├── checkout/    service.py # bug #3
├── payments/    service.py # bug #4
├── cart/        service.py # bug #5
└── tests/                  # one test file per module; 5 tests total
```

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Run the app:
```bash
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs for interactive Swagger docs.

Run the tests (confirm all 5 currently fail — that's expected, the bugs are
still in place):
```bash
pytest tests/ -v
```

## Pushing to your own GitHub repo

```bash
git init
git add .
git commit -m "Initial commit: MiniShop with 5 seeded bugs"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## The 5 Jira tickets to create

Create these as Bug-type issues in your Jira project, using the same
template style as before. Each maps 1:1 to a bug above.

---

**Ticket 1 — Login fails with 500 error after password reset**

```
🔴 Problem
Users are locked out of the application immediately after resetting their
password because the login attempt fails with a 500 Internal Server Error.

🔄 Steps to Reproduce
1. Sign up a user via POST /auth/signup
2. Reset the password via POST /auth/reset-password
3. Attempt to log in using the newly created password via POST /auth/login

📉 Expected Result
The user is successfully authenticated and receives a token.

🚨 Actual Result
The system returns a 500 Internal Server Error.
```

---

**Ticket 2 — Users get logged out a few minutes after login**

```
🔴 Problem
Users report being logged out randomly just a couple of minutes after
signing in, well before any reasonable session length.

🔄 Steps to Reproduce
1. Log in via POST /auth/login
2. Note the token issued
3. Wait ~1 minute and try to use the token

📉 Expected Result
The session should remain valid for 30 minutes.

🚨 Actual Result
The session becomes invalid after only a few seconds.
```

---

**Ticket 3 — Checkout total wrong when a discount code is applied**

```
🔴 Problem
When the SAVE10 discount code is applied at checkout, the total doesn't
reflect a correct 10% discount for carts of varying sizes.

🔄 Steps to Reproduce
1. Add items to checkout totalling more than $100
2. Apply discount code SAVE10 via POST /checkout/total
3. Compare the returned total to a manual 10% calculation

📉 Expected Result
Total should be exactly 10% off the subtotal.

🚨 Actual Result
Total is only ever $10 less than the subtotal, regardless of cart size.
```

---

**Ticket 4 — Payment fails with unhandled error during gateway timeout**

```
🔴 Problem
When the payment gateway times out, the API crashes with an unhandled
error instead of returning a clean failure response.

🔄 Steps to Reproduce
1. Call POST /payments/pay with simulate_timeout: true

📉 Expected Result
API should return a clean JSON response like
{"status": "failed", "reason": "..."}

🚨 Actual Result
The request results in a 500 Internal Server Error.
```

---

**Ticket 5 — Cart allows negative item quantity**

```
🔴 Problem
The cart API accepts negative quantities, which can drive a line item
(and the checkout total) negative.

🔄 Steps to Reproduce
1. Call POST /cart/update with quantity: -5

📉 Expected Result
The API should reject negative quantities with a clear error.

🚨 Actual Result
The negative quantity is accepted without any validation error.
```

---

## Mapping (for the agent's knowledge base / your own reference)

| Ticket | Component | File | Test |
|---|---|---|---|
| 1 | Auth Service | `auth/service.py` → `reset_password()` | `test_login_after_reset` |
| 2 | Auth Service | `auth/service.py` → `issue_token()` | `test_token_expiry_duration` |
| 3 | Checkout | `checkout/service.py` → `calculate_total()` | `test_checkout_with_discount` |
| 4 | Payments | `payments/service.py` → `process_payment()` | `test_payment_gateway_timeout` |
| 5 | Cart | `cart/service.py` → `update_quantity()` | `test_cart_negative_quantity` |
