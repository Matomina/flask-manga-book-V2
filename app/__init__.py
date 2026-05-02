"""
========================================================
MANGABOOK – APPLICATION FACTORY
--------------------------------------------------------
Initialisation principale de l'application Flask.

Architecture :
- Public séparé
- Admin séparé
- Templates isolés par blueprint
- Extensions centralisées
========================================================
"""

from __future__ import annotations

import os
from typing import Any

from flask import Flask

from .config import Config
from .core import (
    register_context_processors,
    register_error_handlers,
    register_template_filters,
)
from .db import init_app as init_db_app


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Créer et configurer l'application Flask."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    register_extensions(app)
    register_context_processors(app)
    register_template_filters(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_extensions(app: Flask) -> None:
    """Initialiser les extensions et services globaux."""
    init_db_app(app)


def register_blueprints(app: Flask) -> None:
    """Enregistrer les blueprints de l'application."""
    from .admin.routes import bp as admin_bp
    from .auth.routes import bp as auth_bp
    from .forum import bp as forum_bp
    from .public.routes import bp as public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(admin_bp)
