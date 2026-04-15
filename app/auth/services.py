from __future__ import annotations

import sqlite3

from werkzeug.security import check_password_hash

from app.db import get_db


def get_user_by_email(email: str) -> sqlite3.Row | None:
    """Récupérer un utilisateur par son email."""
    connection = get_db()

    return connection.execute(
        """
        SELECT id, first_name, last_name, email, password, role
        FROM user
        WHERE email = ?
        """,
        (email,),
    ).fetchone()


def authenticate_user(email: str, password: str) -> sqlite3.Row | None:
    """Authentifier un utilisateur."""
    user = get_user_by_email(email)

    if user is None:
        return None

    is_valid_password = check_password_hash(user["password"], password)

    if not is_valid_password:
        return None

    return user


def get_user_by_email(email: str) -> sqlite3.Row | None:
    connection = get_db()

    email = email.strip().lower()

    try:
        return connection.execute(
            """
            SELECT id, first_name, last_name, email, password, role
            FROM user
            WHERE email = ?
            """,
            (email,),
        ).fetchone()
    except sqlite3.Error:
        return None