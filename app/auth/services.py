from __future__ import annotations

import sqlite3

from werkzeug.security import check_password_hash

from app.db import get_db


def get_user_by_email(email: str) -> sqlite3.Row | None:
    """Récupérer un utilisateur par son email."""
    db = get_db()
    normalized_email = email.strip().lower()

    try:
        return db.execute(
            """
            SELECT id, first_name, last_name, email, password, role
            FROM user
            WHERE email = ?
            """,
            (normalized_email,),
        ).fetchone()
    except sqlite3.Error:
        return None


def authenticate_user(email: str, password: str) -> sqlite3.Row | None:
    """Authentifier un utilisateur avec son email et son mot de passe."""
    user = get_user_by_email(email)

    if user is None:
        return None

    if not check_password_hash(user["password"], password):
        return None

    return user