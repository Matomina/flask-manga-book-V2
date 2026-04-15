import os
import tempfile
import pytest

from manga import create_app
from manga.db import init_db, get_db


@pytest.fixture
def app():
    """Application de test avec DB temporaire."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "SECRET_KEY": "test",
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Helper pour login/logout."""
    class AuthActions:
        def login(self, email="admin@test.com", password="test"):
            return client.post("/auth/login", data={
                "email": email,
                "password": password
            })

        def logout(self):
            return client.get("/auth/logout")

    return AuthActions()