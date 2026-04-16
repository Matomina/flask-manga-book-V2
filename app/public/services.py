from __future__ import annotations

import sqlite3

from app.db import get_db


def get_all_articles() -> list[sqlite3.Row]:
    """Récupérer tous les articles triés par date de création décroissante."""
    connection = get_db()

    return connection.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()


def get_featured_articles(limit: int = 8) -> list[sqlite3.Row]:
    """Récupérer une sélection d'articles à mettre en avant sur l'accueil."""
    connection = get_db()

    return connection.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def get_article_by_id(article_id: int) -> sqlite3.Row | None:
    """Récupérer un article par son identifiant."""
    connection = get_db()

    return connection.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        WHERE id = ?
        """,
        (article_id,),
    ).fetchone()


def add_favorite(user_id: int, article_id: int) -> None:
    """Ajouter un article aux favoris de l'utilisateur."""
    connection = get_db()

    connection.execute(
        """
        INSERT OR IGNORE INTO favorites (user_id, article_id)
        VALUES (?, ?)
        """,
        (user_id, article_id),
    )
    connection.commit()


def remove_favorite(user_id: int, article_id: int) -> None:
    """Retirer un article des favoris de l'utilisateur."""
    connection = get_db()

    connection.execute(
        """
        DELETE FROM favorites
        WHERE user_id = ? AND article_id = ?
        """,
        (user_id, article_id),
    )
    connection.commit()


def get_user_favorites(user_id: int) -> list[sqlite3.Row]:
    """Récupérer les articles favoris d'un utilisateur."""
    connection = get_db()

    return connection.execute(
        """
        SELECT a.id, a.name, a.genres, a.universe, a.image, a.price, a.stock, a.release_day, f.created_at
        FROM favorites AS f
        JOIN articles AS a ON a.id = f.article_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC, a.id DESC
        """,
        (user_id,),
    ).fetchall()
def add_to_history(user_id: int, article_id: int) -> None:
    """Ajouter un article à l'historique (ou mettre à jour la date)."""
    connection = get_db()

    connection.execute(
        """
        INSERT INTO history (user_id, article_id)
        VALUES (?, ?)
        ON CONFLICT(user_id, article_id)
        DO UPDATE SET viewed_at = CURRENT_TIMESTAMP
        """,
        (user_id, article_id),
    )
    connection.commit()

def get_user_history(user_id: int) -> list[sqlite3.Row]:
    """Récupérer l'historique d'un utilisateur."""
    connection = get_db()

    return connection.execute(
        """
        SELECT a.id, a.name, a.genres, a.universe, a.image, a.price, a.stock, a.release_day, h.viewed_at
        FROM history AS h
        JOIN articles AS a ON a.id = h.article_id
        WHERE h.user_id = ?
        ORDER BY h.viewed_at DESC
        """,
        (user_id,),
    ).fetchall()

def create_contact_message(user_id: int, sujet: str, message: str) -> None:
    """Créer un message de contact."""
    connection = get_db()

    connection.execute(
        """
        INSERT INTO contact (user_id, sujet, message)
        VALUES (?, ?, ?)
        """,
        (user_id, sujet, message),
    )
    connection.commit()

    