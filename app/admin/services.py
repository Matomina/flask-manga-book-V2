from __future__ import annotations

import sqlite3

from app.db import get_db


# =========================
# CONTACTS
# =========================

def get_all_contacts() -> list[sqlite3.Row]:
    """Récupérer tous les messages de contact."""
    db = get_db()

    return db.execute(
        """
        SELECT c.id, c.sujet, c.message, c.status, c.created_at,
               u.email
        FROM contact c
        LEFT JOIN user u ON u.id = c.user_id
        ORDER BY c.created_at DESC
        """
    ).fetchall()


def get_contact_by_id(contact_id: int) -> sqlite3.Row | None:
    """Récupérer un message de contact par ID."""
    db = get_db()

    return db.execute(
        """
        SELECT c.id, c.sujet, c.message, c.status, c.created_at,
               u.email
        FROM contact c
        LEFT JOIN user u ON u.id = c.user_id
        WHERE c.id = ?
        """,
        (contact_id,),
    ).fetchone()


def mark_contact_as_read(contact_id: int) -> None:
    """Marquer un message comme lu."""
    db = get_db()

    db.execute(
        """
        UPDATE contact
        SET status = 'read'
        WHERE id = ?
        """,
        (contact_id,),
    )
    db.commit()


# =========================
# DASHBOARD
# =========================

def get_dashboard_stats() -> dict[str, int]:
    """Récupérer les stats globales pour le dashboard admin."""
    db = get_db()

    users = db.execute("SELECT COUNT(*) AS count FROM user").fetchone()["count"]
    articles = db.execute("SELECT COUNT(*) AS count FROM articles").fetchone()["count"]
    orders = db.execute("SELECT COUNT(*) AS count FROM orders").fetchone()["count"]
    contacts = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]

    return {
        "users": users,
        "articles": articles,
        "orders": orders,
        "contacts": contacts,
    }


# =========================
# ARTICLES ADMIN
# =========================

def get_all_articles_admin() -> list[sqlite3.Row]:
    db = get_db()

    return db.execute(
        """
        SELECT id, name, genres, universe, price, stock, created_at
        FROM articles
        ORDER BY created_at DESC
        """
    ).fetchall()


def get_article_by_id_admin(article_id: int) -> sqlite3.Row | None:
    db = get_db()

    return db.execute(
        """
        SELECT *
        FROM articles
        WHERE id = ?
        """,
        (article_id,),
    ).fetchone()


def create_article(data: dict) -> None:
    db = get_db()

    db.execute(
        """
        INSERT INTO articles (name, genres, universe, image, price, stock, release_day)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["genres"],
            data["universe"],
            data["image"],
            data["price"],
            data["stock"],
            data["release_day"],
        ),
    )
    db.commit()


def update_article(article_id: int, data: dict) -> None:
    db = get_db()

    db.execute(
        """
        UPDATE articles
        SET name = ?, genres = ?, universe = ?, image = ?, price = ?, stock = ?, release_day = ?
        WHERE id = ?
        """,
        (
            data["name"],
            data["genres"],
            data["universe"],
            data["image"],
            data["price"],
            data["stock"],
            data["release_day"],
            article_id,
        ),
    )
    db.commit()


def delete_article(article_id: int) -> None:
    db = get_db()

    db.execute(
        "DELETE FROM articles WHERE id = ?",
        (article_id,),
    )
    db.commit()


# =========================
# VALIDATION (PRO)
# =========================

def validate_article_data(data: dict) -> tuple[dict, list[str]]:
    """Valider et nettoyer les données d’un article."""
    errors = []

    name = data.get("name", "").strip()
    genres = data.get("genres", "").strip()
    universe = data.get("universe", "").strip() or None
    image = data.get("image", "").strip()
    release_day = data.get("release_day", "").strip() or None

    # prix
    try:
        price = float(data.get("price", 0))
        if price < 0:
            errors.append("Le prix doit être positif.")
    except ValueError:
        errors.append("Prix invalide.")
        price = 0

    # stock
    try:
        stock = int(data.get("stock", 0))
        if stock < 0:
            errors.append("Stock invalide.")
    except ValueError:
        errors.append("Stock invalide.")
        stock = 0

    if not name:
        errors.append("Le nom est obligatoire.")

    if genres not in ["manga", "figurine", "textile", "vaisselle", "goodies"]:
        errors.append("Genre invalide.")

    if not image:
        errors.append("Image obligatoire.")

    clean_data = {
        "name": name,
        "genres": genres,
        "universe": universe,
        "image": image,
        "price": price,
        "stock": stock,
        "release_day": release_day,
    }

    return clean_data, errors