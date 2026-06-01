from __future__ import annotations

import pytest

from app import create_app
from app.config import DEFAULT_MAX_CONTENT_LENGTH


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

    app = create_app()

    assert app.config["SECRET_KEY"] == "secure-test-key"
    assert app.config["DATABASE"] == str(db_path)
    assert app.config["DEBUG"] is True
    assert app.config["MAX_CONTENT_LENGTH"] == 1048576


def test_config_requires_secret_key_outside_testing(monkeypatch, tmp_path):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE", raising=False)
    monkeypatch.delenv("FLASK_DEBUG", raising=False)
    monkeypatch.delenv("MAX_CONTENT_LENGTH", raising=False)

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(
            {
                "DATABASE": str(tmp_path / "app.sqlite3"),
            }
        )
