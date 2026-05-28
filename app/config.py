from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"


class Config:
    """Configuration globale de l'application Flask."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    DATABASE = os.environ.get("DATABASE", str(INSTANCE_DIR / "manga.sqlite"))
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "app/static/uploads")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB

    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
    TESTING = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"


class ProductionConfig(Config):
    """Configuration stricte pour un déploiement HTTPS en production."""

    DEBUG = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SESSION_COOKIE_SECURE = True


class TestConfig(Config):
    """Configuration utilisée pour les tests."""

    TESTING = True
    DEBUG = False
    DATABASE = str(INSTANCE_DIR / "test.sqlite")
    SECRET_KEY = "test-secret-key"
    WTF_CSRF_ENABLED = False
