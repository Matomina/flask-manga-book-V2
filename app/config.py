from __future__ import annotations

import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"

DEFAULT_DATABASE = str(INSTANCE_DIR / "manga.sqlite")
DEFAULT_TEST_DATABASE = str(INSTANCE_DIR / "test.sqlite")
DEFAULT_MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB


class Config:
    """Configuration globale de l'application Flask."""

    SECRET_KEY = None
    DATABASE = DEFAULT_DATABASE
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = DEFAULT_MAX_CONTENT_LENGTH


class TestConfig(Config):
    """Configuration utilisée pour les tests."""

    TESTING = True
    DEBUG = False
    SECRET_KEY = "test"
    DATABASE = DEFAULT_TEST_DATABASE
    UPLOAD_FOLDER = "app/static/uploads"


def apply_environment_config(config: dict[str, Any]) -> None:
    """Appliquer les variables d'environnement supportées."""

    if secret_key := os.environ.get("SECRET_KEY"):
        config["SECRET_KEY"] = secret_key

    if database := os.environ.get("DATABASE"):
        config["DATABASE"] = database

    if "FLASK_DEBUG" in os.environ:
        config["DEBUG"] = os.environ["FLASK_DEBUG"] == "1"

    if max_content_length := os.environ.get("MAX_CONTENT_LENGTH"):
        config["MAX_CONTENT_LENGTH"] = int(max_content_length)


def validate_required_config(config: dict[str, Any]) -> None:
    """Valider la configuration minimale requise."""

    if config.get("TESTING") and not config.get("SECRET_KEY"):
        config["SECRET_KEY"] = TestConfig.SECRET_KEY

    if not config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY must be set outside testing. "
            "Copy .env.example to .env and set SECRET_KEY."
        )
