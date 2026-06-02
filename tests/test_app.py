from __future__ import annotations

import sqlite3

import pytest

from app import create_app
from app.config import DEFAULT_MAX_CONTENT_LENGTH
from app.core.csrf import CSRF_FIELD_NAME


def test_config(tmp_path):
    db_path = tmp_path / "test.sqlite3"

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(db_path),
        }
    )

    assert app is not None
    assert app.config["TESTING"] is True
    assert app.config["DEBUG"] is False
    assert app.config["SECRET_KEY"] == "test"
    assert app.config["DATABASE"] == str(db_path)
    assert app.config["MAX_CONTENT_LENGTH"] == DEFAULT_MAX_CONTENT_LENGTH


def test_config_uses_environment_values(monkeypatch, tmp_path):
    db_path = tmp_path / "env.sqlite3"

    monkeypatch.setenv("SECRET_KEY", "secure-test-key")
    monkeypatch.setenv("DATABASE", str(db_path))
    monkeypatch.setenv("FLASK_DEBUG", "1")
    monkeypatch.setenv("MAX_CONTENT_LENGTH", "1048576")
    monkeypatch.setenv("AUTO_SEED_DEMO", "1")

    app = create_app()

    assert app.config["SECRET_KEY"] == "secure-test-key"
    assert app.config["DATABASE"] == str(db_path)
    assert app.config["DEBUG"] is True
    assert app.config["MAX_CONTENT_LENGTH"] == 1048576
    assert app.config["AUTO_SEED_DEMO"] is True


def test_auto_seed_demo_bootstraps_empty_database(monkeypatch, tmp_path):
    db_path = tmp_path / "demo.sqlite3"

    monkeypatch.setenv("SECRET_KEY", "secure-test-key")
    monkeypatch.setenv("DATABASE", str(db_path))
    monkeypatch.setenv("AUTO_SEED_DEMO", "1")

    create_app()

    with sqlite3.connect(db_path) as connection:
        article_count = connection.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        migration_count = connection.execute(
            "SELECT COUNT(*) FROM schema_migrations"
        ).fetchone()[0]

    assert article_count > 0
    assert migration_count > 0


def test_config_requires_secret_key_outside_testing(monkeypatch, tmp_path):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE", raising=False)
    monkeypatch.delenv("FLASK_DEBUG", raising=False)
    monkeypatch.delenv("MAX_CONTENT_LENGTH", raising=False)
    monkeypatch.delenv("AUTO_SEED_DEMO", raising=False)

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(
            {
                "DATABASE": str(tmp_path / "app.sqlite3"),
            }
        )


def test_request_token_rejects_missing_token(app):
    app.config["CSRF_TESTING"] = True
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_role"] = "admin"
        session[CSRF_FIELD_NAME] = "known-token"

    response = client.post("/auth/logout")

    assert response.status_code == 400


def test_request_token_accepts_form_token(app):
    app.config["CSRF_TESTING"] = True
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_role"] = "admin"
        session[CSRF_FIELD_NAME] = "known-token"

    response = client.post(
        "/auth/logout",
        data={CSRF_FIELD_NAME: "known-token"},
    )

    assert response.status_code == 302


def test_request_token_accepts_header_token(app):
    app.config["CSRF_TESTING"] = True
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_role"] = "admin"
        session[CSRF_FIELD_NAME] = "known-token"

    response = client.post(
        "/auth/logout",
        headers={"X-CSRF-Token": "known-token"},
    )

    assert response.status_code == 302
