from auth import service as auth_service


def test_login_after_reset():
    """SCRUM ticket: login fails with 500 error after password reset.
    Currently fails with KeyError: 'password_hash' — see auth/service.py.
    """
    auth_service.signup("alice@example.com", "oldpass123")
    auth_service.reset_password("alice@example.com", "newpass456")

    result = auth_service.login("alice@example.com", "newpass456")

    assert result["email"] == "alice@example.com"
    assert "token" in result


def test_token_expiry_duration():
    """SCRUM ticket: users get logged out a few minutes after login.
    Currently fails because the token lifetime is ~59x too short —
    see auth/service.py.
    """
    auth_service.signup("bob@example.com", "pass123")
    auth_service.login("bob@example.com", "pass123")

    user = auth_service._users["bob@example.com"]
    lifetime_seconds = user["token_expires_at"] - user["token_issued_at"]

    expected_seconds = auth_service.TOKEN_LIFETIME_MINUTES * 60
    assert lifetime_seconds >= expected_seconds - 2
