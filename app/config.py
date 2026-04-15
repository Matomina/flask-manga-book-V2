from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"


class Config:
    """Configuration globale de l'application Flask."""

    # =====================================================
    # Sécurité
    # =====================================================
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    # =====================================================
    # Base de données
    # =====================================================
    DATABASE = str(INSTANCE_DIR / "manga.sqlite")

    # =====================================================
    # Environnement
    # =====================================================
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"