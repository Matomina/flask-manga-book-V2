from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"


class Config:
    """Configuration globale de l'application Flask."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    DATABASE = str(INSTANCE_DIR / "manga.sqlite")

    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
    TESTING = False


class TestConfig(Config):
    """Configuration utilisée pour les tests."""

    TESTING = True
    DEBUG = False
    DATABASE = str(INSTANCE_DIR / "test.sqlite")

    UPLOAD_FOLDER = "app/static/uploads"


MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
