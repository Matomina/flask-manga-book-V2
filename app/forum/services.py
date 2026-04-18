from __future__ import annotations

import sqlite3

from app.db import get_db


TOPIC_COLUMNS = """
t.id,
t.user_id,
t.title,
t.message,
t.created_at,
u.first_name,
u.last_name,
u.role
"""

REPLY_COLUMNS = """
r.id,
r.topic_id,
r.user_id,
r.message,
r.created_at,
u.first_name,
u.last_name,
u.role
"""


def _execute_write(query: str, params: tuple = ()) -> int:
    """Exécuter une requête d'écriture, commit et retourner le lastrowid."""
    db = get_db()
    cursor = db.execute(query, params)
    db.commit()
    return int(cursor.lastrowid)


def _normalize_text(value: str) -> str:
    """Nettoyer une chaîne utilisateur."""
    return value.strip()


def _user_exists(user_id: int) -> bool:
    """Vérifier si un utilisateur existe."""
    db = get_db()
    row = db.execute(
        """
        SELECT 1
        FROM user
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()
    return row is not None


def _topic_exists(topic_id: int) -> bool:
    """Vérifier si un sujet existe."""
    db = get_db()
    row = db.execute(
        """
        SELECT 1
        FROM topics
        WHERE id = ?
        """,
        (topic_id,),
    ).fetchone()
    return row is not None


def get_all_topics() -> list[sqlite3.Row]:
    """Récupérer tous les sujets du forum, du plus récent au plus ancien."""
    db = get_db()
    return db.execute(
        f"""
        SELECT
            {TOPIC_COLUMNS},
            (
                SELECT COUNT(*)
                FROM replies AS r
                WHERE r.topic_id = t.id
            ) AS reply_count
        FROM topics AS t
        JOIN user AS u ON u.id = t.user_id
        ORDER BY t.created_at DESC, t.id DESC
        """
    ).fetchall()


def get_topic_by_id(topic_id: int) -> sqlite3.Row | None:
    """Récupérer un sujet du forum par son identifiant."""
    db = get_db()
    return db.execute(
        f"""
        SELECT
            {TOPIC_COLUMNS},
            (
                SELECT COUNT(*)
                FROM replies AS r
                WHERE r.topic_id = t.id
            ) AS reply_count
        FROM topics AS t
        JOIN user AS u ON u.id = t.user_id
        WHERE t.id = ?
        """,
        (topic_id,),
    ).fetchone()


def get_replies_by_topic_id(topic_id: int) -> list[sqlite3.Row]:
    """Récupérer les réponses d'un sujet dans l'ordre chronologique."""
    db = get_db()
    return db.execute(
        f"""
        SELECT
            {REPLY_COLUMNS}
        FROM replies AS r
        JOIN user AS u ON u.id = r.user_id
        WHERE r.topic_id = ?
        ORDER BY r.created_at ASC, r.id ASC
        """,
        (topic_id,),
    ).fetchall()


def create_topic(user_id: int, title: str, message: str) -> int:
    """Créer un sujet de forum et retourner son identifiant."""
    title = _normalize_text(title)
    message = _normalize_text(message)

    if not title or not message:
        raise ValueError("Le titre et le message sont obligatoires.")

    if not _user_exists(user_id):
        raise ValueError("Utilisateur introuvable.")

    return _execute_write(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (user_id, title, message),
    )


def create_reply(topic_id: int, user_id: int, message: str) -> int:
    """Créer une réponse sur un sujet et retourner son identifiant."""
    message = _normalize_text(message)

    if not message:
        raise ValueError("Le message est obligatoire.")

    if not _topic_exists(topic_id):
        raise ValueError("Sujet introuvable.")

    if not _user_exists(user_id):
        raise ValueError("Utilisateur introuvable.")

    return _execute_write(
        """
        INSERT INTO replies (topic_id, user_id, message)
        VALUES (?, ?, ?)
        """,
        (topic_id, user_id, message),
    )