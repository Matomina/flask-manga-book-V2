from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.db import get_db

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
VALID_ARTICLE_GENRES = {"manga", "figurine", "textile", "vaisselle", "goodies"}
VALID_RELEASE_DAYS = {
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
    "Sans jour fixe",
}
VALID_ARTICLE_UNIVERSES = {
    "naruto",
    "jujutsu_kaisen",
    "one_piece",
    "demon_slayer",
    "dragon_ball",
}
UPLOAD_FOLDER = "uploads"


# =========================
# HELPERS
# =========================


def _normalize_str(value: Any) -> str:
    """Nettoyer une valeur texte et garantir une chaîne."""
    return str(value or "").strip()


def _normalize_optional_str(value: Any) -> str | None:
    """Nettoyer une valeur texte optionnelle."""
    cleaned = _normalize_str(value)
    return cleaned or None


# =========================
# CONTACTS
# =========================


def get_all_contacts() -> list[sqlite3.Row]:
    """Récupérer tous les messages de contact."""
    db = get_db()

    return db.execute(
        """
        SELECT c.id, c.sujet, c.message, c.status, c.created_at, u.email
        FROM contact AS c
        LEFT JOIN user AS u ON u.id = c.user_id
        ORDER BY c.created_at DESC, c.id DESC
        """
    ).fetchall()


def get_contact_by_id(contact_id: int) -> sqlite3.Row | None:
    """Récupérer un message de contact par son identifiant."""
    db = get_db()

    return db.execute(
        """
        SELECT c.id, c.sujet, c.message, c.status, c.created_at, u.email
        FROM contact AS c
        LEFT JOIN user AS u ON u.id = c.user_id
        WHERE c.id = ?
        """,
        (contact_id,),
    ).fetchone()


def mark_contact_as_read(contact_id: int) -> None:
    """Marquer un message de contact comme lu."""
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
    """Récupérer les statistiques globales du dashboard admin."""
    db = get_db()

    row = db.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM user) AS users,
            (SELECT COUNT(*) FROM articles) AS articles,
            (SELECT COUNT(*) FROM orders) AS orders,
            (SELECT COUNT(*) FROM contact) AS contacts,
            (SELECT COUNT(*) FROM contact WHERE status != 'read') AS unread_contacts,
            (SELECT COUNT(*) FROM topics) AS forum_topics,
            (SELECT COUNT(*) FROM replies) AS forum_replies,
            (
                SELECT COUNT(*)
                FROM articles
                WHERE stock > 0 AND stock <= 5
            ) AS low_stock_articles,
            (
                SELECT COUNT(*)
                FROM articles
                WHERE stock <= 0
            ) AS out_of_stock_articles
        """
    ).fetchone()

    return {
        "users": row["users"],
        "articles": row["articles"],
        "orders": row["orders"],
        "contacts": row["contacts"],
        "unread_contacts": row["unread_contacts"],
        "forum_topics": row["forum_topics"],
        "forum_replies": row["forum_replies"],
        "low_stock_articles": row["low_stock_articles"],
        "out_of_stock_articles": row["out_of_stock_articles"],
    }


# =========================
# ARTICLES ADMIN
# =========================


def get_all_articles_admin() -> list[sqlite3.Row]:
    """Récupérer tous les articles pour l'administration."""
    db = get_db()

    return db.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()


def get_article_by_id_admin(article_id: int) -> sqlite3.Row | None:
    """Récupérer un article admin par son identifiant."""
    db = get_db()

    return db.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        WHERE id = ?
        """,
        (article_id,),
    ).fetchone()


def create_article(data: dict[str, Any]) -> None:
    """Créer un article."""
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


def update_article(article_id: int, data: dict[str, Any]) -> None:
    """Mettre à jour un article existant."""
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
    """Supprimer un article."""
    db = get_db()

    db.execute(
        "DELETE FROM articles WHERE id = ?",
        (article_id,),
    )
    db.commit()


# =========================
# VALIDATION ARTICLES
# =========================


def validate_article_data(
    data: dict[str, Any],
    *,
    require_image: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    """Valider et nettoyer les données d’un article."""
    errors: list[str] = []

    name = _normalize_str(data.get("name"))
    genres = _normalize_str(data.get("genres"))
    universe = _normalize_optional_str(data.get("universe"))
    image = _normalize_optional_str(data.get("image"))
    release_day = _normalize_optional_str(data.get("release_day"))

    try:
        price = float(data.get("price", 0))
        if price < 0:
            errors.append("Le prix doit être positif.")
    except (TypeError, ValueError):
        errors.append("Prix invalide.")
        price = 0.0

    try:
        stock = int(data.get("stock", 0))
        if stock < 0:
            errors.append("Stock invalide.")
    except (TypeError, ValueError):
        errors.append("Stock invalide.")
        stock = 0

    if not name:
        errors.append("Le nom est obligatoire.")

    if genres not in VALID_ARTICLE_GENRES:
        errors.append("Genre invalide.")

    if universe is not None and universe not in VALID_ARTICLE_UNIVERSES:
        errors.append("Univers invalide.")

    if release_day is not None and release_day not in VALID_RELEASE_DAYS:
        errors.append("Jour de sortie invalide.")

    if require_image and not image:
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


# =========================
# UPLOAD IMAGE
# =========================


def allowed_file(filename: str) -> bool:
    """Vérifier si l'extension du fichier est autorisée."""
    if not filename or "." not in filename:
        return False

    extension = Path(filename).suffix.lower().lstrip(".")
    return extension in ALLOWED_EXTENSIONS


def save_image(file: FileStorage | None) -> str | None:
    """Sauvegarder une image et retourner son chemin relatif dans static."""
    if file is None or not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    original_name = secure_filename(file.filename)
    filename = f"{uuid4().hex}_{original_name}"

    upload_dir = Path(current_app.root_path) / "static" / UPLOAD_FOLDER
    upload_dir.mkdir(parents=True, exist_ok=True)

    upload_path = upload_dir / filename
    file.save(upload_path)

    return f"{UPLOAD_FOLDER}/{filename}"
