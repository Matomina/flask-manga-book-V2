from __future__ import annotations

import sqlite3

from app.db import get_db

ARTICLE_COLUMNS = """
a.id,
a.name,
a.genres,
a.universe,
a.image,
a.price,
a.stock,
a.release_day,
a.created_at
"""

ARTICLE_SELECT = f"""
SELECT {ARTICLE_COLUMNS}
FROM articles AS a
"""


def _execute_write(query: str, params: tuple = ()) -> None:
    """Exécuter une requête d'écriture et valider la transaction."""
    db = get_db()
    db.execute(query, params)
    db.commit()


def _normalize_text(value: str | None) -> str:
    """Nettoyer une chaîne utilisateur."""
    return (value or "").strip()


def _article_exists(article_id: int) -> bool:
    """Vérifier si un article existe."""
    db = get_db()
    row = db.execute(
        """
        SELECT 1
        FROM articles
        WHERE id = ?
        """,
        (article_id,),
    ).fetchone()
    return row is not None


def get_all_articles() -> list[sqlite3.Row]:
    """Récupérer tous les articles triés par date de création décroissante."""
    db = get_db()
    return db.execute(
        f"""
        {ARTICLE_SELECT}
        ORDER BY a.created_at DESC, a.id DESC
        """
    ).fetchall()


def get_featured_articles(limit: int = 8) -> list[sqlite3.Row]:
    """Récupérer une sélection d'articles à mettre en avant sur l'accueil."""
    db = get_db()
    return db.execute(
        f"""
        {ARTICLE_SELECT}
        ORDER BY a.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def get_article_by_id(article_id: int) -> sqlite3.Row | None:
    """Récupérer un article par son identifiant avec son détail public éventuel."""
    db = get_db()
    return db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.genres,
            a.universe,
            a.image,
            a.price,
            a.stock,
            a.release_day,
            a.created_at,
            dap.description
        FROM articles AS a
        LEFT JOIN detail_articles_public AS dap
            ON dap.article_id = a.id
        WHERE a.id = ?
        """,
        (article_id,),
    ).fetchone()


def add_favorite(user_id: int, article_id: int) -> None:
    """Ajouter un article aux favoris de l'utilisateur."""
    if not _article_exists(article_id):
        raise ValueError("Article introuvable.")

    _execute_write(
        """
        INSERT OR IGNORE INTO favorites (user_id, article_id)
        VALUES (?, ?)
        """,
        (user_id, article_id),
    )


def remove_favorite(user_id: int, article_id: int) -> None:
    """Retirer un article des favoris de l'utilisateur."""
    _execute_write(
        """
        DELETE FROM favorites
        WHERE user_id = ? AND article_id = ?
        """,
        (user_id, article_id),
    )


def get_user_favorites(user_id: int) -> list[sqlite3.Row]:
    """Récupérer les articles favoris d'un utilisateur."""
    db = get_db()
    return db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.genres,
            a.universe,
            a.image,
            a.price,
            a.stock,
            a.release_day,
            a.created_at,
            f.created_at AS favorited_at
        FROM favorites AS f
        JOIN articles AS a ON a.id = f.article_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC, a.id DESC
        """,
        (user_id,),
    ).fetchall()


def add_to_history(user_id: int, article_id: int) -> None:
    """Ajouter un article à l'historique ou mettre à jour sa date de consultation."""
    if not _article_exists(article_id):
        raise ValueError("Article introuvable.")

    _execute_write(
        """
        INSERT INTO history (user_id, article_id)
        VALUES (?, ?)
        ON CONFLICT(user_id, article_id)
        DO UPDATE SET viewed_at = CURRENT_TIMESTAMP
        """,
        (user_id, article_id),
    )


def get_user_history(user_id: int) -> list[sqlite3.Row]:
    """Récupérer l'historique d'un utilisateur."""
    db = get_db()
    return db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.genres,
            a.universe,
            a.image,
            a.price,
            a.stock,
            a.release_day,
            a.created_at,
            h.viewed_at
        FROM history AS h
        JOIN articles AS a ON a.id = h.article_id
        WHERE h.user_id = ?
        ORDER BY h.viewed_at DESC, a.id DESC
        """,
        (user_id,),
    ).fetchall()


def create_contact_message(
    user_id: int, sujet: str | None, message: str | None
) -> None:
    """Créer un message de contact."""
    normalized_sujet = _normalize_text(sujet)
    normalized_message = _normalize_text(message)

    if not normalized_sujet or not normalized_message:
        raise ValueError("Le sujet et le message sont obligatoires.")

    _execute_write(
        """
        INSERT INTO contact (user_id, sujet, message)
        VALUES (?, ?, ?)
        """,
        (user_id, normalized_sujet, normalized_message),
    )
