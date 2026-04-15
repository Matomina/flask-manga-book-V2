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
from datetime import datetime
from typing import Any

from flask import Flask, session

from .config import Config
from .db import get_db, init_app as init_db_app


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


def register_context_processors(app: Flask) -> None:
    """Enregistrer les injections globales pour les templates."""

    @app.context_processor
    def inject_user() -> dict[str, Any]:
        user = None
        favorites_ids: list[int] = []

        user_id = session.get("user_id")
        if user_id is not None:
            connection = get_db()

            user = connection.execute(
                "SELECT id, first_name, role FROM user WHERE id = ?",
                (user_id,),
            ).fetchone()

            favorites = connection.execute(
                """
                SELECT article_id
                FROM favorites
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchall()

            favorites_ids = [favorite["article_id"] for favorite in favorites]

        return {
            "current_user": user,
            "favorites_ids": favorites_ids,
        }


def register_template_filters(app: Flask) -> None:
    """Enregistrer les filtres Jinja personnalisés."""

    months_fr = {
        1: "janvier",
        2: "février",
        3: "mars",
        4: "avril",
        5: "mai",
        6: "juin",
        7: "juillet",
        8: "août",
        9: "septembre",
        10: "octobre",
        11: "novembre",
        12: "décembre",
    }

    @app.template_filter("format_datetime_fr")
    def format_datetime_fr(value: str | None) -> str:
        """Formater une date SQL en français."""
        if not value:
            return ""

        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value

        month = months_fr[dt.month]
        return f"{dt.day:02d} {month} {dt.year} à {dt.hour:02d}h{dt.minute:02d}"


def register_blueprints(app: Flask) -> None:
    """Enregistrer les blueprints de l'application."""

    from .admin.admin import bp as admin_bp
    from .admin.articles import bp as admin_articles_bp
    from .admin.auth import bp as auth_bp
    from .admin.contacts import bp as contacts_bp
    from .admin.forum import bp as admin_forum_bp
    from .admin.orders import bp as orders_bp
    from .admin.users import bp as users_bp
    from .public.articles import bp as public_articles_bp
    from .public.routes import bp as public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(public_articles_bp)

    app.register_blueprint(admin_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_articles_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(admin_forum_bp)


def register_error_handlers(app: Flask) -> None:
    """Enregistrer les gestionnaires d'erreurs globaux."""

    @app.errorhandler(404)
    def page_not_found(error: Exception) -> tuple[str, int]:
        return "Page non trouvée", 404