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
VALID_ORDER_STATUSES = {
    "pending",
    "paid",
    "shipped",
    "delivered",
    "cancelled",
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


def get_all_contacts(status_filter: str = "all") -> list[sqlite3.Row]:
    """Récupérer les messages de contact avec filtre optionnel."""
    db = get_db()

    where_sql = ""
    params: tuple = ()

    if status_filter == "unread":
        where_sql = "WHERE c.status != 'read'"
    elif status_filter == "read":
        where_sql = "WHERE c.status = 'read'"

    return db.execute(
        f"""
        SELECT c.id, c.sujet, c.message, c.status, c.created_at, u.email
        FROM contact AS c
        LEFT JOIN user AS u ON u.id = c.user_id
        {where_sql}
        ORDER BY c.created_at DESC, c.id DESC
        """,
        params,
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
# USERS ADMIN
# =========================


def get_all_users_admin() -> list[sqlite3.Row]:
    """Récupérer tous les utilisateurs pour l'administration."""
    db = get_db()

    return db.execute(
        """
        SELECT
            id,
            first_name,
            last_name,
            email,
            phone,
            address,
            city,
            role,
            created_at
        FROM user
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()


def get_user_by_id_admin(user_id: int) -> sqlite3.Row | None:
    """Récupérer un utilisateur admin par son identifiant."""
    db = get_db()

    return db.execute(
        """
        SELECT
            id,
            first_name,
            last_name,
            email,
            phone,
            address,
            city,
            role,
            created_at
        FROM user
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()


# =========================
# ORDERS ADMIN
# =========================


def get_all_orders_admin(status_filter: str = "all") -> list[sqlite3.Row]:
    """Récupérer toutes les commandes pour l'administration."""
    db = get_db()

    where_sql = ""
    params: tuple[str, ...] = ()

    if status_filter in {
        "pending",
        "paid",
        "shipped",
        "delivered",
        "cancelled",
    }:
        where_sql = "WHERE o.status = ?"
        params = (status_filter,)

    return db.execute(
        f"""
        SELECT
            o.id,
            o.user_id,
            o.total_amount,
            o.status,
            o.created_at,
            u.first_name,
            u.last_name,
            u.email
        FROM orders AS o
        JOIN user AS u ON u.id = o.user_id
        {where_sql}
        ORDER BY o.created_at DESC, o.id DESC
        """,
        params,
    ).fetchall()


def get_order_by_id_admin(order_id: int) -> sqlite3.Row | None:
    """Récupérer une commande admin par son identifiant."""
    db = get_db()

    return db.execute(
        """
        SELECT
            o.id,
            o.user_id,
            o.total_amount,
            o.status,
            o.created_at,
            u.first_name,
            u.last_name,
            u.email,
            u.phone,
            u.address,
            u.city
        FROM orders AS o
        JOIN user AS u ON u.id = o.user_id
        WHERE o.id = ?
        """,
        (order_id,),
    ).fetchone()


def get_order_items_by_order_id(order_id: int) -> list[sqlite3.Row]:
    """Récupérer les lignes d'articles d'une commande."""
    db = get_db()

    return db.execute(
        """
        SELECT
            oa.id,
            oa.order_id,
            oa.article_id,
            oa.quantity,
            oa.unit_price,
            a.name,
            a.genres,
            a.universe,
            a.image
        FROM orders_articles AS oa
        JOIN articles AS a ON a.id = oa.article_id
        WHERE oa.order_id = ?
        ORDER BY oa.id ASC
        """,
        (order_id,),
    ).fetchall()


def update_order_status_admin(order_id: int, status: str) -> bool:
    """Mettre à jour le statut d'une commande admin."""
    normalized_status = _normalize_str(status)

    if normalized_status not in VALID_ORDER_STATUSES:
        raise ValueError("Statut de commande invalide.")

    db = get_db()

    cursor = db.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (normalized_status, order_id),
    )
    db.commit()

    return cursor.rowcount > 0


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
        SET
            name = ?,
            genres = ?,
            universe = ?,
            image = ?,
            price = ?,
            stock = ?,
            release_day = ?
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
