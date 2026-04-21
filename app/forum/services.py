from __future__ import annotations

import sqlite3

from app.db import get_db


TOPIC_COLUMNS = """
t.id,
t.user_id,
t.title,
t.message,
t.created_at,
u.first_name AS author_first_name,
u.last_name AS author_last_name,
u.role AS author_role
"""

REPLY_COLUMNS = """
r.id,
r.topic_id,
r.user_id,
r.message,
r.created_at,
u.first_name AS author_first_name,
u.last_name AS author_last_name,
u.role AS author_role
"""


def _execute_insert(query: str, params: tuple = ()) -> int:
    """Exécuter une insertion, commit et retourner le lastrowid."""
    db = get_db()
    cursor = db.execute(query, params)
    db.commit()
    return int(cursor.lastrowid)


def _execute_write(query: str, params: tuple = ()) -> None:
    """Exécuter une requête d'écriture et commit."""
    db = get_db()
    db.execute(query, params)
    db.commit()


def _normalize_text(value: str | None) -> str:
    """Nettoyer une chaîne utilisateur."""
    return (value or "").strip()


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


def get_all_topics_for_admin() -> list[sqlite3.Row]:
    """Récupérer tous les sujets du forum pour la modération admin."""
    return get_all_topics()


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


def get_reply_by_id(reply_id: int) -> sqlite3.Row | None:
    """Récupérer une réponse par son identifiant."""
    db = get_db()
    return db.execute(
        f"""
        SELECT
            {REPLY_COLUMNS}
        FROM replies AS r
        JOIN user AS u ON u.id = r.user_id
        WHERE r.id = ?
        """,
        (reply_id,),
    ).fetchone()


def create_topic(user_id: int, title: str, message: str) -> int:
    """Créer un sujet de forum et retourner son identifiant."""
    normalized_title = _normalize_text(title)
    normalized_message = _normalize_text(message)

    if not normalized_title or not normalized_message:
        raise ValueError("Le titre et le message sont obligatoires.")

    if not _user_exists(user_id):
        raise ValueError("Utilisateur introuvable.")

    return _execute_insert(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (user_id, normalized_title, normalized_message),
    )


def create_reply(topic_id: int, user_id: int, message: str) -> int:
    """Créer une réponse sur un sujet et retourner son identifiant."""
    normalized_message = _normalize_text(message)

    if not normalized_message:
        raise ValueError("Le message est obligatoire.")

    if not _topic_exists(topic_id):
        raise ValueError("Sujet introuvable.")

    if not _user_exists(user_id):
        raise ValueError("Utilisateur introuvable.")

    return _execute_insert(
        """
        INSERT INTO replies (topic_id, user_id, message)
        VALUES (?, ?, ?)
        """,
        (topic_id, user_id, normalized_message),
    )


def delete_topic_by_id(topic_id: int) -> None:
    """Supprimer un sujet du forum par son identifiant."""
    _execute_write(
        """
        DELETE FROM topics
        WHERE id = ?
        """,
        (topic_id,),
    )


def delete_reply_by_id(reply_id: int) -> None:
    """Supprimer une réponse du forum par son identifiant."""
    _execute_write(
        """
        DELETE FROM replies
        WHERE id = ?
        """,
        (reply_id,),
    )