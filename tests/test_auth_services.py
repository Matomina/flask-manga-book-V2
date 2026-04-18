from __future__ import annotations

from app.auth.services import authenticate_user, get_user_by_email


def test_get_user_by_email_found(app):
    with app.app_context():
        user = get_user_by_email("admin@test.com")

    assert user is not None
    assert user["email"] == "admin@test.com"
    assert user["role"] == "admin"


def test_get_user_by_email_normalizes_email(app):
    with app.app_context():
        user = get_user_by_email("  ADMIN@TEST.COM  ")

    assert user is not None
    assert user["email"] == "admin@test.com"


def test_get_user_by_email_not_found(app):
    with app.app_context():
        user = get_user_by_email("unknown@test.com")

    assert user is None


def test_authenticate_user_success(app):
    with app.app_context():
        user = authenticate_user("admin@test.com", "test")

    assert user is not None
    assert user["email"] == "admin@test.com"


def test_authenticate_user_wrong_password(app):
    with app.app_context():
        user = authenticate_user("admin@test.com", "wrong-password")

    assert user is None


def test_authenticate_user_unknown_email(app):
    with app.app_context():
        user = authenticate_user("unknown@test.com", "test")

    assert user is None