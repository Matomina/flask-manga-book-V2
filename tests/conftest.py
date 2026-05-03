from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import get_db, reset_db


@pytest.fixture
def app():
    """Créer une application Flask de test avec une base SQLite temporaire."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DEBUG": False,
            "DATABASE": db_path,
            "SECRET_KEY": "test",
        }
    )

    with app.app_context():
        reset_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Créer un client de test Flask."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Créer un runner CLI de test Flask."""
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    """Retourner la connexion DB active dans le contexte de test."""
    with app.app_context():
        yield get_db()


@pytest.fixture
def auth(client):
    """Helper pour les actions d'authentification."""

    class AuthActions:
        def login(
            self,
            email: str = "admin@test.com",
            password: str = "test",
            follow_redirects: bool = False,
        ):
            return client.post(
                "/auth/login",
                data={
                    "email": email,
                    "password": password,
                },
                follow_redirects=follow_redirects,
            )

        def login_as_admin(self, follow_redirects: bool = False):
            return self.login(
                email="admin@test.com",
                password="test",
                follow_redirects=follow_redirects,
            )

        def login_as_user(self, follow_redirects: bool = False):
            return self.login(
                email="user@test.com",
                password="test",
                follow_redirects=follow_redirects,
            )

        def logout(self, follow_redirects: bool = False):
            return client.post("/auth/logout", follow_redirects=follow_redirects)

    return AuthActions()
