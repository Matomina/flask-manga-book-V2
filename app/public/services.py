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