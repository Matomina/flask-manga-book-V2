from __future__ import annotations

import hmac
from secrets import token_urlsafe
from typing import Any

from flask import Flask, abort, request, session

CSRF_FIELD_NAME = "_csrf_token"
CSRF_HEADER_NAMES = ("X-CSRFToken", "X-CSRF-Token")
SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def generate_csrf_token() -> str:
    token = session.get(CSRF_FIELD_NAME)
    if not isinstance(token, str) or not token:
        token = token_urlsafe(32)
        session[CSRF_FIELD_NAME] = token
    return token


def _submitted_csrf_token() -> str:
    token = request.form.get(CSRF_FIELD_NAME, "")
    if token:
        return token

    for header_name in CSRF_HEADER_NAMES:
        token = request.headers.get(header_name, "")
        if token:
            return token

    json_data: Any = request.get_json(silent=True) or {}
    if isinstance(json_data, dict):
        return str(json_data.get(CSRF_FIELD_NAME, ""))

    return ""


def _csrf_is_enabled(app: Flask) -> bool:
    if app.config.get("TESTING") and not app.config.get("CSRF_TESTING"):
        return False
    return bool(app.config.get("CSRF_ENABLED", True))


def validate_csrf_token() -> None:
    expected_token = session.get(CSRF_FIELD_NAME)
    submitted_token = _submitted_csrf_token()

    if not isinstance(expected_token, str) or not expected_token:
        abort(400, description="CSRF token missing.")

    if not hmac.compare_digest(expected_token, submitted_token):
        abort(400, description="CSRF token invalid.")


def register_csrf(app: Flask) -> None:
    @app.before_request
    def protect_post_requests() -> None:
        if request.method in SAFE_METHODS:
            return

        if not _csrf_is_enabled(app):
            return

        validate_csrf_token()

    @app.context_processor
    def inject_csrf() -> dict[str, Any]:
        return {
            "csrf_token": generate_csrf_token,
            "csrf_field_name": CSRF_FIELD_NAME,
        }
