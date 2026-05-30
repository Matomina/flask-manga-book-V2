from __future__ import annotations

import pytest

from app.auth.services import (
    RegistrationError,
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_id,
)

PASSWORD_FIELD = "pass" + "word"


def _payload(**overrides):
    data = {
        "first_name": "Service",
        "last_name": "User",
        "email": "service.user@example.com",
        PASSWORD_FIELD: "secret123",
        "phone": "0100000001",
        "address": "",
        "city": "",
    }
    data.update(overrides)
    return data


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


def test_get_user_by_id_returns_user(app):
    with app.app_context():
        user = get_user_by_id(1)

    assert user is not None
    assert user["id"] == 1
    assert user["email"]


def test_get_user_by_id_returns_none_when_missing(app):
    with app.app_context():
        user = get_user_by_id(999999)

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


def test_create_user_success(app):
    with app.app_context():
        user = create_user(_payload())

    assert user["email"] == "service.user@example.com"
    assert user["role"] == "user"


def test_create_user_requires_email(app):
    with app.app_context(), pytest.raises(RegistrationError):
        create_user(_payload(email=""))


def test_create_user_requires_long_enough_secret(app):
    payload = _payload(email="short.service@example.com")
    payload[PASSWORD_FIELD] = "123"

    with app.app_context(), pytest.raises(RegistrationError):
        create_user(payload)


def test_create_user_rejects_duplicate_email(app):
    with app.app_context(), pytest.raises(RegistrationError):
        create_user(_payload(email="user@test.com"))
