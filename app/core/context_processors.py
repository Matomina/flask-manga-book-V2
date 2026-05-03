from __future__ import annotations

from typing import Any

from flask import Flask, session

from app.db import get_db


def register_context_processors(app: Flask) -> None:
    """Enregistrer les context processors globaux."""

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
